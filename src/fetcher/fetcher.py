from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from urllib.parse import urlparse

import httpx

from src.fetcher.content_extractor import extract_content
from src.fetcher.substack_fetcher import SubstackAuth, fetch_substack
from src.fetcher.types import FetchResult
from src.fetcher.url_utils import SKIP_DOMAINS, is_medium_url, is_substack_url

logger = logging.getLogger(__name__)


def _build_substack_auth(cookies: dict[str, str] | None) -> SubstackAuth | None:
    if not cookies:
        return None
    raw = cookies.get("substack.com", "")
    sid = lli = ""
    for pair in raw.split(";"):
        pair = pair.strip()
        if pair.startswith("substack.sid="):
            sid = pair[len("substack.sid=") :]
        elif pair.startswith("substack.lli="):
            lli = pair[len("substack.lli=") :]
    if sid:
        return SubstackAuth(sid=sid, lli=lli)
    return None


async def fetch_urls(
    urls: list[str],
    cookies: dict[str, str] | None = None,
    concurrency: int = 10,
    max_retries: int = 3,
    timeout: int = 30,
) -> list[FetchResult]:
    semaphore = asyncio.Semaphore(concurrency)
    substack_auth = _build_substack_auth(cookies)

    async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:

        async def fetch_one(url: str) -> FetchResult:
            async with semaphore:
                domain = urlparse(url).netloc
                now = datetime.now()

                if any(d in domain for d in SKIP_DOMAINS):
                    return FetchResult(
                        url=url,
                        status="unavailable",
                        title=None,
                        content=None,
                        domain=domain,
                        fetch_date=now,
                    )

                if is_substack_url(url):
                    return await fetch_substack(url, auth=substack_auth, timeout=timeout)

                if is_medium_url(url):
                    return FetchResult(
                        url=url,
                        status="failed",
                        title=None,
                        content=None,
                        domain=domain,
                        fetch_date=now,
                        error="403 Client Error: requires browser fetch for Medium",
                    )

                headers: dict[str, str] = {}
                if cookies:
                    if domain in cookies:
                        headers["Cookie"] = cookies[domain]
                    else:
                        parts = domain.split(".")
                        for i in range(1, len(parts)):
                            parent = ".".join(parts[i:])
                            if parent in cookies:
                                headers["Cookie"] = cookies[parent]
                                break

                for attempt in range(max_retries):
                    try:
                        resp = await client.get(url, headers=headers)
                        if resp.status_code in (404, 410):
                            return FetchResult(
                                url=url,
                                status="dead",
                                title=None,
                                content=None,
                                domain=domain,
                                fetch_date=now,
                            )
                        resp.raise_for_status()

                        extracted = extract_content(resp.text, url)
                        return FetchResult(
                            url=url,
                            status="ok",
                            title=None,
                            content=extracted or resp.text,
                            domain=domain,
                            fetch_date=now,
                        )
                    except httpx.HTTPError as e:
                        if attempt < max_retries - 1:
                            await asyncio.sleep(2**attempt)
                        else:
                            logger.warning("fetch failed url=%s error=%s", url, e)
                            return FetchResult(
                                url=url,
                                status="failed",
                                title=None,
                                content=None,
                                domain=domain,
                                fetch_date=now,
                                error=str(e),
                            )
                return FetchResult(
                    url=url,
                    status="failed",
                    title=None,
                    content=None,
                    domain=domain,
                    fetch_date=now,
                    error="max retries exceeded",
                )

        async def safe_fetch(url: str) -> FetchResult:
            try:
                urlparse(url)
            except Exception:
                return FetchResult(
                    url=url,
                    status="failed",
                    title=None,
                    content=None,
                    domain="",
                    fetch_date=datetime.now(),
                    error="invalid URL",
                )
            return await fetch_one(url)

        tasks = [safe_fetch(url) for url in urls]
        return list(await asyncio.gather(*tasks))

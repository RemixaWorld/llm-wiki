from __future__ import annotations

import logging
from pathlib import Path

from src.fetcher.browser_fetcher import fetch_with_browser
from src.fetcher.cache import is_cached_ok, read_cache, write_cache
from src.fetcher.content_filter import check_quality
from src.fetcher.dedup import DedupIndex
from src.fetcher.fetcher import fetch_urls
from src.fetcher.medium_fetcher import extract_medium_content
from src.fetcher.types import FetchResult
from src.fetcher.url_collector import UrlSource, collect_urls
from src.fetcher.url_utils import is_medium_url

logger = logging.getLogger(__name__)


async def run_fetch(
    urls: list[str],
    web_dir: Path,
    *,
    urls_file: str | None = None,
    retry_failed: bool = False,
    use_browser: bool = False,
    concurrency: int = 10,
    cookies: dict[str, str] | None = None,
) -> list[FetchResult]:
    """Fetch URLs and cache results to data/web/. Returns all results."""
    src = UrlSource(
        urls=urls,
        urls_file=urls_file,
        retry_dir=web_dir if retry_failed else None,
    )
    collected, _ = collect_urls(src)

    if not collected:
        logger.info("no URLs to fetch")
        return []

    # Filter out already-cached ok URLs
    to_fetch = [u for u in collected if not is_cached_ok(u, web_dir)]
    logger.info(
        "urls total=%d cached=%d to_fetch=%d",
        len(collected),
        len(collected) - len(to_fetch),
        len(to_fetch),
    )

    if not to_fetch:
        return [r for u in collected if (r := read_cache(u, web_dir)) is not None]

    # Fetch via httpx
    results = await fetch_urls(to_fetch, cookies=cookies, concurrency=concurrency)

    # Quality filter + dedup
    dedup = DedupIndex(web_dir)
    for i, r in enumerate(results):
        if r.status != "ok" or not r.content:
            continue
        quality = check_quality(r.content)
        if not quality.passed:
            status = (
                quality.reason if quality.reason in ("error_page", "low_quality") else "low_quality"
            )
            results[i] = r.model_copy(update={"status": status})
            continue
        dup = dedup.check(r.domain, r.content)
        if dup:
            results[i] = r.model_copy(
                update={"status": "duplicate", "error": f"duplicate of {dup}"}
            )

    # Write all results to cache
    for r in results:
        write_cache(r, web_dir)

    # Browser retry
    browser_needed = [
        r for r in results if r.status == "failed" and (is_medium_url(r.url) or use_browser)
    ]
    if browser_needed:
        try:
            from playwright.async_api import async_playwright

            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                for r in browser_needed:
                    br = await fetch_with_browser(r.url, browser)
                    if br.status == "ok" and br.html:
                        content = extract_medium_content(br.html) if is_medium_url(r.url) else None
                        if content is None:
                            from src.fetcher.content_extractor import extract_content

                            content = extract_content(br.html, r.url)
                        quality = check_quality(content)
                        final_status = "ok" if quality.passed else "low_quality"
                        updated = r.model_copy(update={"status": final_status, "content": content})
                        write_cache(updated, web_dir)
                await browser.close()
        except ImportError:
            logger.warning(
                "playwright not installed, skipping browser fetch. "
                "Install with: uv pip install playwright && playwright install chromium"
            )

    # Return all results (including previously cached)
    final: list[FetchResult] = []
    for u in collected:
        cached = read_cache(u, web_dir)
        if cached:
            final.append(cached)
    return final


async def fetch_single(url: str, web_dir: Path, *, use_browser: bool = False) -> FetchResult:
    """Fetch a single URL. Returns cached result if available, otherwise fetches."""
    cached = read_cache(url, web_dir)
    if cached and cached.status == "ok":
        return cached
    results = await run_fetch([url], web_dir, use_browser=use_browser)
    if results:
        return results[0]
    import datetime

    return FetchResult(
        url=url,
        status="failed",
        domain="",
        fetch_date=datetime.datetime.now(),
        error="no result",
    )

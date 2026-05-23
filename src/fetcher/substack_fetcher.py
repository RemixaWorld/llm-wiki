from __future__ import annotations

import json
import logging
import re
from datetime import datetime

import httpx
from bs4 import BeautifulSoup
from html2text import HTML2Text
from pydantic import BaseModel

from src.config import get_settings
from src.fetcher.types import FetchResult

logger = logging.getLogger(__name__)


class SubstackAuth(BaseModel):
    sid: str
    lli: str

    def cookie_header(self) -> str:
        return f"substack.sid={self.sid}; substack.lli={self.lli}"


def _slug_from_url(url: str) -> tuple[str, str]:
    parts = url.split("/p/")
    if len(parts) != 2:
        return "", ""
    slug = parts[1].rstrip("/")
    pub = parts[0].split("//")[1].split(".substack.com")[0]
    return pub, slug


def _build_html2text() -> HTML2Text:
    h = HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0
    h.protect_links = True
    h.unicode_snob = True
    h.images_to_alt = False
    return h


def _extract_body_html(body_html: str) -> str:
    soup = BeautifulSoup(body_html, "html.parser")

    for tag in soup.find_all("div", class_=re.compile(r"subscription-widget|image-link-expand")):
        tag.decompose()
    for tag in soup.find_all("p", class_=re.compile(r"button-wrapper")):
        tag.decompose()
    for tag in soup.find_all("button"):
        tag.decompose()

    for latex in soup.find_all(class_="latex-rendered"):
        attrs_str = latex.get("data-attrs", "")
        try:
            attrs = json.loads(attrs_str)
            expr = attrs.get("persistentExpression", "")
            if expr:
                latex.replace_with(f"\n$$\n{expr}\n$$\n")
        except (json.JSONDecodeError, AttributeError):
            pass

    for figure in soup.find_all("figure"):
        img = figure.find("img")
        caption = figure.find("figcaption")
        caption_text = caption.get_text().strip() if caption else "image"
        if img:
            src = img.get("src", "")
            if src:
                figure.replace_with(f"\n\n![{caption_text}]({src})\n\n")

    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src and "substackcdn.com" in src:
            img.replace_with(f"\n\n![image]({src})\n\n")

    h = _build_html2text()
    md = h.handle(str(soup))

    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()


async def fetch_substack(
    url: str,
    auth: SubstackAuth | None = None,
    timeout: int = 30,
) -> FetchResult:
    from urllib.parse import urlparse

    domain = urlparse(url).netloc
    now = datetime.now()
    pub, slug = _slug_from_url(url)

    if not pub or not slug:
        return FetchResult(
            url=url,
            status="failed",
            title=None,
            content=None,
            domain=domain,
            fetch_date=now,
            error="could not parse substack URL",
        )

    api_url = f"https://{pub}.substack.com/api/v1/posts/{slug}"
    headers: dict[str, str] = {}
    if auth:
        headers["Cookie"] = auth.cookie_header()

    try:
        settings = get_settings()
        proxy = settings.http_proxy or None
        async with httpx.AsyncClient(
            timeout=timeout, follow_redirects=True, proxy=proxy
        ) as client:
            resp = await client.get(api_url, headers=headers)

        if resp.status_code == 404:
            return FetchResult(
                url=url,
                status="dead",
                title=None,
                content=None,
                domain=domain,
                fetch_date=now,
            )
        resp.raise_for_status()

        data = resp.json()
        body_html = data.get("body_html", "")
        title = data.get("title")
        audience = data.get("audience", "")

        if not body_html:
            return FetchResult(
                url=url,
                status="failed",
                title=title,
                content=None,
                domain=domain,
                fetch_date=now,
                error="empty body_html from API",
            )

        reaction = data.get("reaction")
        if audience == "only_paid" and reaction is None:
            if auth is None:
                logger.warning(
                    "substack paywall no cookie url=%s hint=%s",
                    url,
                    "Update cookies.json: add 'substack.sid' and 'substack.lli' to substack.com entry",
                )
                return FetchResult(
                    url=url,
                    status="paywalled",
                    title=title,
                    content=None,
                    domain=domain,
                    fetch_date=now,
                    error="paywalled: requires substack.sid/substack.lli in cookies.json",
                )
            else:
                logger.warning(
                    "substack paywall cookie expired url=%s hint=%s",
                    url,
                    "substack.sid cookie may have expired, recapture from browser",
                )
                return FetchResult(
                    url=url,
                    status="paywalled",
                    title=title,
                    content=None,
                    domain=domain,
                    fetch_date=now,
                    error="paywalled: substack.sid cookie expired or invalid",
                )

        markdown = _extract_body_html(body_html)

        return FetchResult(
            url=url,
            status="ok",
            title=title,
            content=markdown,
            domain=domain,
            fetch_date=now,
        )

    except httpx.HTTPError as e:
        logger.warning("substack fetch failed url=%s error=%s", url, e)
        return FetchResult(
            url=url,
            status="failed",
            title=None,
            content=None,
            domain=domain,
            fetch_date=now,
            error=str(e),
        )

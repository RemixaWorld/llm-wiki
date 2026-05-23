from __future__ import annotations

import logging
from datetime import datetime
from urllib.parse import urlparse

from pydantic import BaseModel

logger = logging.getLogger(__name__)

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
)


class BrowserFetchResult(BaseModel):
    url: str
    status: str  # ok | failed
    html: str | None = None
    domain: str
    fetch_date: datetime
    error: str | None = None


async def fetch_with_browser(
    url: str,
    browser: object,
    cookies: list[dict] | None = None,
    timeout: int = 30,
    auth_url: str | None = None,
    proxy: str | None = None,
) -> BrowserFetchResult:
    domain = urlparse(url).netloc
    now = datetime.now()
    context = None

    try:
        context_opts: dict = {
            "user_agent": DEFAULT_USER_AGENT,
            "bypass_csp": True,
        }
        if proxy:
            context_opts["proxy"] = {"server": proxy}
        context = await browser.new_context(**context_opts)

        if cookies:
            await context.add_cookies(cookies)

        page = await context.new_page()

        if auth_url and cookies:
            await page.goto(auth_url, wait_until="domcontentloaded", timeout=timeout * 1000)
            await page.wait_for_timeout(2000)

        await page.goto(url, wait_until="domcontentloaded", timeout=timeout * 1000)
        await page.wait_for_timeout(3000)
        html = await page.content()

        return BrowserFetchResult(
            url=url,
            status="ok",
            html=html,
            domain=domain,
            fetch_date=now,
        )
    except Exception as e:
        logger.warning("browser fetch failed url=%s error=%s", url, e)
        return BrowserFetchResult(
            url=url,
            status="failed",
            html=None,
            domain=domain,
            fetch_date=now,
            error=str(e),
        )
    finally:
        if context:
            await context.close()


def parse_cookie_string(cookie_str: str, domain: str) -> list[dict]:
    cookies = []
    for pair in cookie_str.split(";"):
        pair = pair.strip()
        if "=" in pair:
            name, value = pair.split("=", 1)
            cookies.append(
                {
                    "name": name.strip(),
                    "value": value.strip(),
                    "domain": domain,
                    "path": "/",
                }
            )
    return cookies

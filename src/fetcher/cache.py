from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

import yaml

from src.fetcher.types import FetchResult
from src.fetcher.url_utils import get_domain_dir, url_to_filename

logger = logging.getLogger(__name__)


def cache_path_for_url(url: str, web_dir: Path) -> Path:
    domain_dir = get_domain_dir(url)
    filename = url_to_filename(url)
    return web_dir / domain_dir / filename


def read_cache(url: str, web_dir: Path) -> FetchResult | None:
    path = cache_path_for_url(url, web_dir)
    if not path.exists():
        return None
    try:
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            return None
        end = text.find("---", 3)
        if end == -1:
            return None
        meta = yaml.safe_load(text[3:end])
        body = text[end + 3 :].strip()
        return FetchResult(
            url=meta.get("url", url),
            status=meta.get("status", "unknown"),
            title=meta.get("title"),
            content=body or None,
            domain=meta.get("domain", ""),
            fetch_date=meta.get("fetch_date", datetime.now()),
            error=meta.get("error"),
        )
    except Exception:
        logger.warning("corrupt cache file path=%s", path)
        return None


def write_cache(result: FetchResult, web_dir: Path) -> Path:
    path = cache_path_for_url(result.url, web_dir)
    path.parent.mkdir(parents=True, exist_ok=True)

    meta: dict = {
        "url": result.url,
        "status": result.status,
        "domain": result.domain,
        "fetch_date": result.fetch_date.isoformat(),
    }
    if result.title:
        meta["title"] = result.title
    if result.error:
        meta["error"] = result.error

    frontmatter = yaml.dump(meta, default_flow_style=False).strip()
    body = result.content or ""
    content = f"---\n{frontmatter}\n---\n\n{body}\n"

    path.write_text(content, encoding="utf-8")
    return path


def is_cached_ok(url: str, web_dir: Path) -> bool:
    result = read_cache(url, web_dir)
    return result is not None and result.status == "ok"

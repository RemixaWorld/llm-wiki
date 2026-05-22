from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel


class UrlSource(BaseModel):
    urls: list[str] = []
    urls_file: str | None = None
    retry_dir: Path | None = None


def _urls_from_file(path: str) -> list[str]:
    urls: list[str] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped:
            urls.append(stripped)
    return urls


def _urls_from_retry(retry_dir: Path) -> list[str]:
    urls: list[str] = []
    for wf in retry_dir.rglob("*.md"):
        text = wf.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        end = text.find("---", 3)
        if end == -1:
            continue
        meta = yaml.safe_load(text[3:end])
        status = meta.get("status", "")
        if status != "ok" and meta.get("url"):
            urls.append(meta["url"])
    return urls


def collect_urls(source: UrlSource) -> tuple[list[str], dict[str, str]]:
    all_urls: list[str] = []
    seen: set[str] = set()

    # 1. Direct URLs
    for u in source.urls:
        if u not in seen:
            seen.add(u)
            all_urls.append(u)

    # 2. URL file
    if source.urls_file:
        for u in _urls_from_file(source.urls_file):
            if u not in seen:
                seen.add(u)
                all_urls.append(u)

    # 3. Retry failed
    if source.retry_dir and source.retry_dir.exists():
        for u in _urls_from_retry(source.retry_dir):
            if u not in seen:
                seen.add(u)
                all_urls.append(u)

    return all_urls, {}

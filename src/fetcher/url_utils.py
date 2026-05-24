from __future__ import annotations

import hashlib
from urllib.parse import urlparse

SKIP_DOMAINS = (
    "twitter.com",
    "x.com",
    "reddit.com",
    "www.reddit.com",
    "old.reddit.com",
)


def url_to_filename(url: str) -> str:
    url_hash = hashlib.sha256(url.encode()).hexdigest()[:8]
    return f"{url_hash}.md"


def get_domain_dir(url: str) -> str:
    return urlparse(url).netloc

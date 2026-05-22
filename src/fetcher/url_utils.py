from __future__ import annotations

import hashlib
from urllib.parse import urlparse


MEDIUM_DOMAINS = {
    "medium.com",
    "levelup.gitconnected.com",
    "ai.gopubby.com",
    "pub.towardsai.net",
    "generativeai.pub",
    "blog.devgenius.io",
    "python.plainenglish.io",
    "ai.plainenglish.io",
    "blog.gopenai.com",
    "blog.stackademic.com",
}

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
    domain = urlparse(url).netloc
    if domain in MEDIUM_DOMAINS:
        return "medium"
    return domain


def is_medium_url(url: str) -> bool:
    domain = urlparse(url).netloc
    return domain in MEDIUM_DOMAINS


def is_substack_url(url: str) -> bool:
    return ".substack.com/p/" in url

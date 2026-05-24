from __future__ import annotations

from src.fetcher.url_utils import (
    get_domain_dir,
    url_to_filename,
)


def test_url_to_filename_deterministic():
    assert url_to_filename("https://example.com/a") == url_to_filename("https://example.com/a")


def test_url_to_filename_different_urls():
    assert url_to_filename("https://a.com") != url_to_filename("https://b.com")


def test_url_to_filename_format():
    name = url_to_filename("https://example.com")
    assert name.endswith(".md")
    assert len(name) == 11  # 8 hex chars + ".md"


def test_get_domain_dir_regular():
    assert get_domain_dir("https://www.pinecone.io/learn/chunking") == "www.pinecone.io"

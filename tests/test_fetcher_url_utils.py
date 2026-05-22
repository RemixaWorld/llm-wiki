from __future__ import annotations

from src.fetcher.url_utils import (
    get_domain_dir,
    is_medium_url,
    is_substack_url,
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


def test_get_domain_dir_medium():
    assert get_domain_dir("https://medium.com/test") == "medium"
    assert get_domain_dir("https://levelup.gitconnected.com/test") == "medium"


def test_is_medium_url():
    assert is_medium_url("https://medium.com/something")
    assert not is_medium_url("https://example.com")


def test_is_substack_url():
    assert is_substack_url("https://kaitchup.substack.com/p/grpo-train")
    assert not is_substack_url("https://substack.com")

from __future__ import annotations

from src.fetcher.medium_fetcher import extract_medium_content
from src.fetcher.substack_fetcher import SubstackAuth, _slug_from_url
from src.fetcher.url_utils import is_medium_url, is_substack_url


class TestMediumExtractor:
    def test_extract_from_html(self):
        html = (
            "<html><body><article><h1>Test Title</h1>"
            "<p>This is a test paragraph with enough content to pass quality checks.</p>"
            "</article></body></html>"
        )
        result = extract_medium_content(html)
        assert result is not None
        assert "Test Title" in result

    def test_extract_empty_html(self):
        assert extract_medium_content("") is None
        assert extract_medium_content(None) is None


class TestSubstackHelpers:
    def test_slug_from_url(self):
        pub, slug = _slug_from_url("https://kaitchup.substack.com/p/grpo-train-llms")
        assert pub == "kaitchup"
        assert slug == "grpo-train-llms"

    def test_slug_from_bad_url(self):
        pub, slug = _slug_from_url("https://example.com/no-slug")
        assert pub == ""
        assert slug == ""

    def test_substack_auth_cookie_header(self):
        auth = SubstackAuth(sid="abc", lli="xyz")
        assert "substack.sid=abc" in auth.cookie_header()
        assert "substack.lli=xyz" in auth.cookie_header()

    def test_is_medium_url(self):
        assert is_medium_url("https://medium.com/something")
        assert is_medium_url("https://blog.devgenius.io/test")
        assert not is_medium_url("https://example.com")

    def test_is_substack_url(self):
        assert is_substack_url("https://pub.substack.com/p/article")
        assert not is_substack_url("https://substack.com")

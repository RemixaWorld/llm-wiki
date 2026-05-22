from __future__ import annotations

from src.fetcher.browser_fetcher import parse_cookie_string


def test_parse_cookie_string():
    cookies = parse_cookie_string("sid=abc123; token=xyz", "example.com")
    assert len(cookies) == 2
    assert cookies[0]["name"] == "sid"
    assert cookies[0]["value"] == "abc123"
    assert cookies[0]["domain"] == "example.com"


def test_parse_cookie_string_empty():
    assert parse_cookie_string("", "example.com") == []


def test_parse_cookie_string_single():
    cookies = parse_cookie_string("key=val", "example.com")
    assert len(cookies) == 1
    assert cookies[0]["name"] == "key"

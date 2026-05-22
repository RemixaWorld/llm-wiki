from __future__ import annotations

from datetime import datetime
from pathlib import Path

from src.fetcher.cache import is_cached_ok, read_cache, write_cache
from src.fetcher.types import FetchResult


class TestCache:
    def test_write_and_read(self, tmp_path: Path):
        web = tmp_path / "web"
        now = datetime.now()
        result = FetchResult(
            url="https://example.com/article",
            status="ok",
            title="Test Article",
            content="Hello world content",
            domain="example.com",
            fetch_date=now,
        )
        path = write_cache(result, web)
        assert path.exists()
        assert "example.com" in str(path)

        cached = read_cache("https://example.com/article", web)
        assert cached is not None
        assert cached.status == "ok"
        assert cached.title == "Test Article"
        assert "Hello world" in (cached.content or "")

    def test_read_missing(self, tmp_path: Path):
        assert read_cache("https://missing.com", tmp_path / "web") is None

    def test_is_cached_ok(self, tmp_path: Path):
        web = tmp_path / "web"
        now = datetime.now()
        ok_result = FetchResult(
            url="https://ok.com",
            status="ok",
            content="x" * 300,
            domain="ok.com",
            fetch_date=now,
        )
        write_cache(ok_result, web)
        assert is_cached_ok("https://ok.com", web) is True
        assert is_cached_ok("https://missing.com", web) is False

    def test_write_failed_still_caches(self, tmp_path: Path):
        web = tmp_path / "web"
        now = datetime.now()
        result = FetchResult(
            url="https://fail.com",
            status="failed",
            domain="fail.com",
            fetch_date=now,
            error="timeout",
        )
        path = write_cache(result, web)
        assert path.exists()
        cached = read_cache("https://fail.com", web)
        assert cached is not None
        assert cached.status == "failed"

    def test_is_cached_ok_false_for_failed(self, tmp_path: Path):
        web = tmp_path / "web"
        now = datetime.now()
        result = FetchResult(
            url="https://fail.com",
            status="failed",
            domain="fail.com",
            fetch_date=now,
        )
        write_cache(result, web)
        assert is_cached_ok("https://fail.com", web) is False

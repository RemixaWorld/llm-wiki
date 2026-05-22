from __future__ import annotations

from pathlib import Path

from src.fetcher.url_collector import UrlSource, collect_urls


class TestCollectUrls:
    def test_direct_urls(self):
        src = UrlSource(urls=["https://a.com", "https://b.com"])
        urls, _ = collect_urls(src)
        assert urls == ["https://a.com", "https://b.com"]

    def test_dedup_preserves_order(self):
        src = UrlSource(urls=["https://a.com", "https://b.com", "https://a.com"])
        urls, _ = collect_urls(src)
        assert urls == ["https://a.com", "https://b.com"]

    def test_from_file(self, tmp_path: Path):
        f = tmp_path / "urls.txt"
        f.write_text("https://c.com\nhttps://d.com\n")
        src = UrlSource(urls_file=str(f))
        urls, _ = collect_urls(src)
        assert urls == ["https://c.com", "https://d.com"]

    def test_from_file_skips_blank_lines(self, tmp_path: Path):
        f = tmp_path / "urls.txt"
        f.write_text("https://c.com\n\n  \nhttps://d.com\n")
        src = UrlSource(urls_file=str(f))
        urls, _ = collect_urls(src)
        assert urls == ["https://c.com", "https://d.com"]

    def test_retry_failed(self, tmp_path: Path):
        web = tmp_path / "web" / "example.com"
        web.mkdir(parents=True)
        (web / "abc12345.md").write_text("---\nstatus: failed\nurl: https://example.com/fail\n---\n")
        (web / "def67890.md").write_text("---\nstatus: ok\nurl: https://example.com/ok\n---\n")
        src = UrlSource(retry_dir=tmp_path / "web")
        urls, _ = collect_urls(src)
        assert urls == ["https://example.com/fail"]

    def test_mixed_sources_dedup(self, tmp_path: Path):
        f = tmp_path / "urls.txt"
        f.write_text("https://a.com\n")
        src = UrlSource(urls=["https://a.com", "https://b.com"], urls_file=str(f))
        urls, _ = collect_urls(src)
        assert urls == ["https://a.com", "https://b.com"]

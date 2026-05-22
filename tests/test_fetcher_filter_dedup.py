from __future__ import annotations

from pathlib import Path

import pytest

from src.fetcher.content_filter import check_quality
from src.fetcher.dedup import DedupIndex, jaccard_similarity, minhash


class TestCheckQuality:
    def test_none_text(self):
        assert check_quality(None).passed is False

    def test_empty_text(self):
        assert check_quality("").passed is False

    def test_short_text(self):
        assert check_quality("short").passed is False

    def test_error_page_403(self):
        assert check_quality("403 Forbidden").passed is False

    def test_error_page_404(self):
        assert check_quality("404 Not Found").passed is False

    def test_valid_content(self):
        text = "x" * 300
        assert check_quality(text).passed is True

    def test_error_page_not_flagged_in_long_content(self):
        text = "cloudflare " * 100
        assert check_quality(text).passed is True


class TestMinhash:
    def test_empty_text(self):
        assert minhash("") == set()

    def test_deterministic(self):
        assert minhash("hello world") == minhash("hello world")

    def test_similar_texts_have_high_jaccard(self):
        a = minhash("The quick brown fox jumps over the lazy dog")
        b = minhash("The quick brown fox jumps over the lazy cat")
        assert jaccard_similarity(a, b) > 0.5


class TestDedupIndex:
    def test_empty_dir(self, tmp_path: Path):
        idx = DedupIndex(tmp_path / "web")
        assert idx.check("example.com", "some content") is None

    def test_detect_duplicate(self, tmp_path: Path):
        web = tmp_path / "web" / "example.com"
        web.mkdir(parents=True)
        (web / "abc12345.md").write_text("---\nstatus: ok\n---\nHello world this is some content for testing")
        idx = DedupIndex(tmp_path / "web")
        result = idx.check("example.com", "Hello world this is some content for testing")
        assert result is not None

    def test_no_duplicate(self, tmp_path: Path):
        web = tmp_path / "web" / "example.com"
        web.mkdir(parents=True)
        (web / "abc12345.md").write_text("---\nstatus: ok\n---\nCompletely different topic about quantum physics")
        idx = DedupIndex(tmp_path / "web")
        assert idx.check("example.com", "Cooking recipes with Italian pasta and tomatoes") is None

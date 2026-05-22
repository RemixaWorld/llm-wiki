from __future__ import annotations

from datetime import datetime

from src.fetcher.types import FetchResult, QualityResult


def test_fetch_result_creation():
    now = datetime.now()
    r = FetchResult(url="https://example.com", status="ok", content="hello", domain="example.com", fetch_date=now)
    assert r.url == "https://example.com"
    assert r.status == "ok"
    assert r.error is None


def test_quality_result_defaults():
    q = QualityResult(passed=True)
    assert q.reason is None

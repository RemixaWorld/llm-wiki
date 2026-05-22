from __future__ import annotations

from datetime import datetime
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from src.fetcher import fetch_single, run_fetch
from src.fetcher.types import FetchResult


class TestRunFetch:
    @pytest.mark.asyncio
    async def test_skip_cached_ok(self, tmp_path: Path):
        web = tmp_path / "web"
        now = datetime.now()
        from src.fetcher.cache import write_cache
        cached = FetchResult(url="https://cached.com", status="ok", content="x" * 300, domain="cached.com", fetch_date=now)
        write_cache(cached, web)

        results = await run_fetch(["https://cached.com"], web)
        assert len(results) == 1
        assert results[0].status == "ok"

    @pytest.mark.asyncio
    async def test_fetch_uncached(self, tmp_path: Path):
        web = tmp_path / "web"
        mock_result = FetchResult(url="https://new.com", status="ok", content="x" * 300, domain="new.com", fetch_date=datetime.now())
        with patch("src.fetcher.fetch_urls", new_callable=AsyncMock, return_value=[mock_result]):
            results = await run_fetch(["https://new.com"], web)
        assert len(results) == 1
        assert results[0].status == "ok"


class TestFetchSingle:
    @pytest.mark.asyncio
    async def test_returns_cached(self, tmp_path: Path):
        web = tmp_path / "web"
        now = datetime.now()
        from src.fetcher.cache import write_cache
        cached = FetchResult(url="https://cached.com", status="ok", content="x" * 300, domain="cached.com", fetch_date=now)
        write_cache(cached, web)

        result = await fetch_single("https://cached.com", web)
        assert result.status == "ok"

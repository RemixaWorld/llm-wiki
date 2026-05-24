from __future__ import annotations

from unittest.mock import AsyncMock, patch

import httpx
import pytest

from src.fetcher.types import FetchResult


@pytest.fixture
def mock_httpx_client():
    with patch("src.fetcher.fetcher.httpx.AsyncClient") as mock_cls:
        client = AsyncMock()
        mock_cls.return_value.__aenter__ = AsyncMock(return_value=client)
        mock_cls.return_value.__aexit__ = AsyncMock(return_value=False)
        yield client


class TestFetchUrls:
    @pytest.mark.asyncio
    async def test_skip_twitter(self, mock_httpx_client):
        from src.fetcher.fetcher import fetch_urls

        results = await fetch_urls(["https://twitter.com/user/status/123"])
        assert results[0].status == "unavailable"

    @pytest.mark.asyncio
    async def test_skip_reddit(self, mock_httpx_client):
        from src.fetcher.fetcher import fetch_urls

        results = await fetch_urls(["https://reddit.com/r/test"])
        assert results[0].status == "unavailable"

    @pytest.mark.asyncio
    async def test_dead_url_404(self, mock_httpx_client):
        from src.fetcher.fetcher import fetch_urls

        resp = httpx.Response(404, request=httpx.Request("GET", "https://example.com"))
        mock_httpx_client.get = AsyncMock(return_value=resp)
        results = await fetch_urls(["https://example.com/gone"])
        assert results[0].status == "dead"

    @pytest.mark.asyncio
    async def test_successful_fetch(self, mock_httpx_client):
        from src.fetcher.fetcher import fetch_urls

        resp = httpx.Response(
            200,
            text="<html><body><p>Content here</p></body></html>",
            request=httpx.Request("GET", "https://example.com"),
        )
        mock_httpx_client.get = AsyncMock(return_value=resp)
        with patch("src.fetcher.fetcher.extract_content", return_value="Content here"):
            results = await fetch_urls(["https://example.com/article"])
        assert results[0].status == "ok"
        assert results[0].domain == "example.com"

    @pytest.mark.asyncio
    async def test_retry_on_network_error(self, mock_httpx_client):
        from src.fetcher.fetcher import fetch_urls

        mock_httpx_client.get = AsyncMock(side_effect=httpx.ConnectError("timeout"))
        with patch("src.fetcher.fetcher.asyncio.sleep", new_callable=AsyncMock):
            results = await fetch_urls(["https://example.com/fail"], max_retries=2)
        assert results[0].status == "failed"

from __future__ import annotations

from datetime import datetime
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from src.fetcher.fetcher import _build_substack_auth
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
    async def test_medium_marked_failed(self, mock_httpx_client):
        from src.fetcher.fetcher import fetch_urls

        results = await fetch_urls(["https://medium.com/test-article"])
        assert results[0].status == "failed"
        assert "browser" in results[0].error.lower()

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

    @pytest.mark.asyncio
    async def test_substack_routing(self, mock_httpx_client):
        from src.fetcher.fetcher import fetch_urls

        with patch("src.fetcher.fetcher.fetch_substack", new_callable=AsyncMock) as mock_sub:
            mock_sub.return_value = FetchResult(
                url="https://pub.substack.com/p/test",
                status="ok",
                content="hello",
                domain="pub.substack.com",
                fetch_date=datetime.now(),
            )
            results = await fetch_urls(["https://pub.substack.com/p/test"])
        assert results[0].status == "ok"
        mock_sub.assert_called_once()


class TestBuildSubstackAuth:
    def test_no_cookies(self):
        assert _build_substack_auth(None) is None

    def test_no_substack_cookie(self):
        assert _build_substack_auth({"example.com": "foo=bar"}) is None

    def test_valid_auth(self):
        auth = _build_substack_auth({"substack.com": "substack.sid=abc; substack.lli=xyz"})
        assert auth is not None
        assert auth.sid == "abc"
        assert auth.lli == "xyz"

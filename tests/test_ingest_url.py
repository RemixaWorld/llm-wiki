from __future__ import annotations

from datetime import datetime
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from src.fetcher.types import FetchResult


class TestExtractTextNode:
    @pytest.mark.asyncio
    async def test_url_auto_fetch(self):
        mock_result = FetchResult(
            url="https://example.com/test",
            status="ok",
            title="Test Page",
            content="Hello world content",
            domain="example.com",
            fetch_date=datetime.now(),
        )
        with patch("src.fetcher.fetch_single", new_callable=AsyncMock, return_value=mock_result):
            from src.ingest import extract_text_node
            state = await extract_text_node({"source_path": "https://example.com/test"})
        assert state["extracted_text"] == "Hello world content"
        assert state["source_title"] == "Test Page"

    @pytest.mark.asyncio
    async def test_url_fetch_failed(self):
        mock_result = FetchResult(
            url="https://fail.com",
            status="failed",
            domain="fail.com",
            fetch_date=datetime.now(),
            error="timeout",
        )
        with patch("src.fetcher.fetch_single", new_callable=AsyncMock, return_value=mock_result):
            from src.ingest import extract_text_node
            state = await extract_text_node({"source_path": "https://fail.com"})
        assert "errors" in state
        assert "failed" in state["errors"][0]

    @pytest.mark.asyncio
    async def test_file_path_unchanged(self, tmp_path: Path):
        f = tmp_path / "test.txt"
        f.write_text("file content here")
        from src.ingest import extract_text_node
        state = await extract_text_node({"source_path": str(f)})
        assert state["extracted_text"] == "file content here"

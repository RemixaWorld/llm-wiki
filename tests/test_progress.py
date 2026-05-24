"""Tests for ingest progress callback integration."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.ingest import (
    chunk_source_node,
    extract_text_node,
    process_batches_node,
    run_ingest,
)
from src.models import Confidence, GeneratedPage, IngestResult, PageType


@pytest.fixture()
def sample_source(tmp_path: Path) -> Path:
    f = tmp_path / "sample.txt"
    f.write_text("Some text about transformers and attention.", encoding="utf-8")
    return f


@pytest.fixture()
def mock_ingest_result() -> IngestResult:
    return IngestResult(
        source_summary=GeneratedPage(
            title="Summary",
            page_type=PageType.SOURCE_SUMMARY,
            tags=["test"],
            confidence=Confidence.HIGH,
            body="Summary body.",
        ),
        concept_pages=[],
        entity_pages=[],
    )


class TestCallbackOnStage:
    @pytest.mark.asyncio
    async def test_extract_text_calls_on_stage(self, sample_source: Path) -> None:
        cb = MagicMock()
        state = {"source_path": str(sample_source), "progress_callback": cb}
        await extract_text_node(state)
        cb.on_stage.assert_called_once_with("extract")

    @pytest.mark.asyncio
    async def test_chunk_source_calls_on_stage(self) -> None:
        cb = MagicMock()
        state = {
            "extracted_text": "Some text.",
            "source_path": "test.txt",
            "progress_callback": cb,
        }
        await chunk_source_node(state)
        cb.on_stage.assert_called_once_with("chunk")

    @pytest.mark.asyncio
    async def test_process_batches_calls_on_stage(
        self, tmp_path: Path, mock_ingest_result: IngestResult, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        import src.config

        src.config._settings = None

        cb = MagicMock()
        state = {
            "chunks": ["Source text."],
            "source_path": "test.txt",
            "source_title": "Test",
            "fresh": True,
            "progress_callback": cb,
        }
        with patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = mock_ingest_result
            await process_batches_node(state)

        cb.on_stage.assert_any_call("process")
        src.config._settings = None


class TestCallbackOnBatchProgress:
    @pytest.mark.asyncio
    async def test_batch_progress_called_per_batch(
        self, tmp_path: Path, mock_ingest_result: IngestResult, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        monkeypatch.setenv("WIKI_BATCH_SIZE", "1")
        import src.config

        src.config._settings = None

        cb = MagicMock()
        state = {
            "chunks": ["chunk0", "chunk1", "chunk2"],
            "source_path": "test.txt",
            "source_title": "Test",
            "fresh": True,
            "progress_callback": cb,
        }
        with patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = mock_ingest_result
            await process_batches_node(state)

        assert cb.on_batch_progress.call_count == 3
        cb.on_batch_progress.assert_any_call(1, 3)
        cb.on_batch_progress.assert_any_call(2, 3)
        cb.on_batch_progress.assert_any_call(3, 3)
        src.config._settings = None


class TestCallbackOnSummary:
    @pytest.mark.asyncio
    async def test_run_ingest_calls_on_summary(
        self,
        sample_source: Path,
        mock_ingest_result: IngestResult,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        import src.config

        src.config._settings = None

        cb = MagicMock()
        with patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = mock_ingest_result
            result = await run_ingest(str(sample_source), progress_callback=cb)

        cb.on_summary.assert_called_once()
        call_args = cb.on_summary.call_args
        assert call_args[0][0] is result["stats"]  # IngestStats
        assert isinstance(call_args[0][1], float)  # duration_s
        assert isinstance(call_args[0][2], list)  # errors
        src.config._settings = None


class TestCallbackBackwardCompat:
    @pytest.mark.asyncio
    async def test_nodes_work_without_callback(
        self,
        sample_source: Path,
        mock_ingest_result: IngestResult,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        import src.config

        src.config._settings = None

        with patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = mock_ingest_result
            result = await run_ingest(str(sample_source))

        assert len(result.get("written_paths", [])) == 1
        assert result.get("errors", []) == []
        src.config._settings = None

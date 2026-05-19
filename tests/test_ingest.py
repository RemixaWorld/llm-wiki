"""Tests for LangGraph ingest pipeline with mocked LLM."""

from __future__ import annotations

from datetime import date, datetime, timezone
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from src.ingest import (
    _write_checkpoint,
    build_ingest_graph,
    chunk_source_node,
    extract_text_node,
    process_batches_node,
    run_ingest,
)
from src.models import (
    Checkpoint,
    Confidence,
    GeneratedPage,
    IngestResult,
    PageType,
    WikiFrontmatter,
)
from src.wiki import read_page, write_page

# ── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture()
def sample_source(tmp_path: Path) -> Path:
    """Create a sample text source file."""
    f = tmp_path / "sample.txt"
    f.write_text(
        "Transformers use self-attention to process sequences in parallel.\n\n"
        "BERT is a bidirectional encoder model pre-trained on large corpora.\n\n"
        "The attention mechanism computes weighted sums over value vectors.",
        encoding="utf-8",
    )
    return f


@pytest.fixture()
def mock_ingest_result() -> IngestResult:
    """Create a mock LLM ingest result."""
    return IngestResult(
        source_summary=GeneratedPage(
            title="Sample Source Summary",
            page_type=PageType.SOURCE_SUMMARY,
            tags=["deep-learning"],
            confidence=Confidence.HIGH,
            body="# Sample Source Summary\n\nOverview of the source.",
            related_titles=["Transformer Architecture"],
        ),
        concept_pages=[
            GeneratedPage(
                title="Transformer Architecture",
                page_type=PageType.CONCEPT,
                tags=["deep-learning", "attention"],
                confidence=Confidence.HIGH,
                body="# Transformer Architecture\n\nSelf-attention for sequences.",
                related_titles=["BERT"],
            ),
        ],
        entity_pages=[
            GeneratedPage(
                title="BERT",
                page_type=PageType.ENTITY,
                tags=["nlp", "pre-training"],
                confidence=Confidence.HIGH,
                body="# BERT\n\nBidirectional encoder.",
                related_titles=[],
            ),
        ],
    )


# ── Node tests ───────────────────────────────────────────────────────────────


class TestExtractTextNode:
    @pytest.mark.asyncio
    async def test_extracts_text(self, sample_source: Path) -> None:
        state = {"source_path": str(sample_source)}
        result = await extract_text_node(state)
        assert "extracted_text" in result
        assert "self-attention" in result["extracted_text"]

    @pytest.mark.asyncio
    async def test_returns_error_on_missing_file(self) -> None:
        state = {"source_path": "/nonexistent/file.txt"}
        result = await extract_text_node(state)
        assert "errors" in result
        assert len(result["errors"]) > 0


class TestChunkSourceNode:
    @pytest.mark.asyncio
    async def test_chunks_text(self) -> None:
        state = {"extracted_text": "Short text.", "source_path": "test.txt"}
        result = await chunk_source_node(state)
        assert "chunks" in result
        assert len(result["chunks"]) >= 1

    @pytest.mark.asyncio
    async def test_empty_text_returns_error(self) -> None:
        state = {"extracted_text": "", "source_path": "test.txt"}
        result = await chunk_source_node(state)
        assert "errors" in result


class TestProcessBatchesNode:
    @pytest.mark.asyncio
    async def test_single_batch(
        self, tmp_path: Path, mock_ingest_result: IngestResult, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        import src.config

        src.config._settings = None

        state = {
            "chunks": ["Some source text about transformers and BERT."],
            "source_path": "test.txt",
            "source_title": "Test Source",
            "fresh": True,
        }

        with patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = mock_ingest_result
            result = await process_batches_node(state)

        assert "written_paths" in result
        assert len(result["written_paths"]) == 3
        # Checkpoint should be deleted after completion
        assert not list(checkpoint_dir.glob("*.json"))

        src.config._settings = None

    @pytest.mark.asyncio
    async def test_empty_chunks_returns_error(self) -> None:
        state = {"chunks": [], "source_path": "test.txt"}
        result = await process_batches_node(state)
        assert "errors" in result

    @pytest.mark.asyncio
    async def test_resumes_from_checkpoint(
        self, tmp_path: Path, mock_ingest_result: IngestResult, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        monkeypatch.setenv("WIKI_BATCH_SIZE", "2")
        import src.config

        src.config._settings = None

        # Pre-create checkpoint with batch 0 completed
        cp = Checkpoint(
            source="test.txt",
            source_title="Test Source",
            total_chunks=4,
            batch_size=2,
            completed_batches=[0],
            generated_titles=["Existing Page"],
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        _write_checkpoint(cp)

        chunks = ["chunk0", "chunk1", "chunk2", "chunk3"]
        state = {
            "chunks": chunks,
            "source_path": "test.txt",
            "source_title": "Test Source",
        }

        call_count = 0

        async def mock_llm_fn(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            return mock_ingest_result

        with patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.side_effect = mock_llm_fn
            result = await process_batches_node(state)

        # Only batch 1 should have been called (batch 0 skipped)
        assert call_count == 1
        assert "written_paths" in result
        assert len(result["written_paths"]) == 3
        # Checkpoint should be deleted (all batches complete)
        assert not list(checkpoint_dir.glob("*.json"))

        src.config._settings = None

    @pytest.mark.asyncio
    async def test_batch_failure_preserves_checkpoint(
        self, tmp_path: Path, mock_ingest_result: IngestResult, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        monkeypatch.setenv("WIKI_BATCH_SIZE", "2")
        import src.config

        src.config._settings = None

        chunks = ["chunk0", "chunk1", "chunk2", "chunk3"]
        state = {
            "chunks": chunks,
            "source_path": "test.txt",
            "source_title": "Test Source",
            "fresh": True,
        }

        call_count = 0

        async def mock_llm_fn(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return mock_ingest_result
            raise RuntimeError("LLM quota exhausted")

        with patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.side_effect = mock_llm_fn
            result = await process_batches_node(state)

        # Batch 0 succeeded, batch 1 failed
        assert call_count == 2
        assert "errors" in result
        assert len(result["errors"]) == 1
        # Batch 0's pages should be written
        assert len(result["written_paths"]) == 3
        # Checkpoint should still exist with only batch 0 completed
        checkpoints = list(checkpoint_dir.glob("*.json"))
        assert len(checkpoints) == 1

        src.config._settings = None


# ── Integration test ─────────────────────────────────────────────────────────


class TestRunIngest:
    @pytest.mark.asyncio
    async def test_full_pipeline(
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

        assert result.get("errors", []) == []
        assert len(result.get("written_paths", [])) == 3

        # Verify pages on disk
        md_files = list(wiki_dir.glob("*.md"))
        assert len(md_files) == 3

        src.config._settings = None

    @pytest.mark.asyncio
    async def test_pipeline_with_missing_source(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import src.config

        src.config._settings = None

        result = await run_ingest("/nonexistent/file.txt")
        assert len(result.get("errors", [])) > 0

        src.config._settings = None


class TestBuildIngestGraph:
    def test_graph_compiles(self) -> None:
        graph = build_ingest_graph()
        app = graph.compile()
        assert app is not None


class TestProcessBatchesMerge:
    @pytest.mark.asyncio
    async def test_merges_when_page_already_exists(
        self, tmp_path: Path, mock_ingest_result: IngestResult, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        import src.config

        src.config._settings = None

        # Pre-create existing page with same title as mock's entity page ("BERT")
        existing_fm = WikiFrontmatter(
            title="BERT",
            page_type=PageType.ENTITY,
            sources=["old/source.pdf"],
            tags=["nlp"],
            created=date(2026, 1, 1),
            updated=date(2026, 1, 1),
            confidence=Confidence.HIGH,
        )
        write_page(existing_fm, "# BERT\n\nOld content about BERT.", wiki_dir)

        state = {
            "chunks": ["Source text about BERT and transformers."],
            "source_path": "new-source.txt",
            "source_title": "New Source",
            "fresh": True,
        }

        from src.models import EditOp, PatchedPage

        mock_patched = PatchedPage(
            edits=[
                EditOp(
                    old_string="# BERT\n\nOld content about BERT.",
                    new_string="# BERT\n\nMerged content combining old and new.",
                ),
            ],
            tags_to_add=["pre-training"],
            confidence=Confidence.HIGH,
        )

        with patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm, \
             patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_merge_llm:
            mock_llm.return_value = mock_ingest_result
            mock_merge_llm.return_value = mock_patched
            result = await process_batches_node(state)

        assert "errors" not in result or len(result.get("errors", [])) == 0
        # Verify BERT page was merged (not just overwritten)
        bert_page = read_page("bert.md", wiki_dir)
        assert "old" in bert_page.frontmatter.sources or "new-source.txt" in bert_page.frontmatter.sources
        assert bert_page.frontmatter.created == date(2026, 1, 1)  # preserved

        src.config._settings = None


class TestBuildBatchMessages:
    def test_includes_wiki_titles_in_prompt(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        import src.config
        src.config._settings = None

        # Create an existing page on disk
        from src.wiki import write_page

        fm = WikiFrontmatter(
            title="Existing Topic",
            page_type=PageType.CONCEPT,
            sources=["old.pdf"],
            created=date(2026, 1, 1),
            updated=date(2026, 1, 1),
        )
        write_page(fm, "Content.", wiki_dir)

        from src.ingest import _build_batch_messages

        messages = _build_batch_messages(
            chunks=["chunk text"],
            batch_start=0,
            batch_size=5,
            source_title="Test Source",
            existing_titles=[],
            wiki_titles=["Existing Topic"],
        )

        user_msg = messages[1]["content"]
        assert "Existing Topic" in user_msg

        src.config._settings = None

    def test_dedupes_combined_titles(self) -> None:
        from src.ingest import _build_batch_messages

        messages = _build_batch_messages(
            chunks=["chunk text"],
            batch_start=0,
            batch_size=5,
            source_title="Test Source",
            existing_titles=["BERT", "GPT"],
            wiki_titles=["BERT", "Transformer"],
        )

        user_msg = messages[1]["content"]
        # BERT should appear only once in the combined list
        assert user_msg.count("BERT") == 1
        assert "GPT" in user_msg
        assert "Transformer" in user_msg


class TestCrossSourceMerge:
    @pytest.mark.asyncio
    async def test_second_source_merges_with_existing_page(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Simulate ingesting source B after source A already created a page."""
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        import src.config

        src.config._settings = None

        # Source A already ingested — "BERT" page exists on disk
        existing_fm = WikiFrontmatter(
            title="BERT",
            page_type=PageType.ENTITY,
            sources=["source-a.pdf"],
            tags=["nlp"],
            created=date(2026, 4, 1),
            updated=date(2026, 4, 1),
            confidence=Confidence.HIGH,
            related=["transformer-architecture.md"],
        )
        write_page(existing_fm, "# BERT\n\nBidirectional encoder from source A.", wiki_dir)

        # Source B generates a page that also has "BERT"
        source_b_result = IngestResult(
            source_summary=GeneratedPage(
                title="Source B Summary",
                page_type=PageType.SOURCE_SUMMARY,
                tags=["nlp"],
                confidence=Confidence.HIGH,
                body="# Source B\n\nOverview.",
                related_titles=[],
            ),
            concept_pages=[],
            entity_pages=[
                GeneratedPage(
                    title="BERT",
                    page_type=PageType.ENTITY,
                    tags=["nlp", "pre-training"],
                    confidence=Confidence.HIGH,
                    body="# BERT\n\nNew details about pre-training from source B.",
                    related_titles=["Source B Summary"],
                ),
            ],
        )

        from src.models import EditOp, PatchedPage

        mock_patched = PatchedPage(
            edits=[
                EditOp(
                    old_string="# BERT\n\nBidirectional encoder from source A.",
                    new_string="# BERT\n\nBidirectional encoder from source A. New details about pre-training from source B.",
                ),
            ],
            tags_to_add=["pre-training"],
            confidence=Confidence.HIGH,
        )

        state = {
            "chunks": ["Content about BERT pre-training."],
            "source_path": "source-b.pdf",
            "source_title": "Source B",
            "fresh": True,
        }

        with patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm, \
             patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_merge_llm:
            mock_llm.return_value = source_b_result
            mock_merge_llm.return_value = mock_patched
            result = await process_batches_node(state)

        assert "errors" not in result or len(result.get("errors", [])) == 0

        # Verify merged BERT page
        bert_page = read_page("bert.md", wiki_dir)
        assert "source-a.pdf" in bert_page.frontmatter.sources
        assert "source-b.pdf" in bert_page.frontmatter.sources
        assert bert_page.frontmatter.created == date(2026, 4, 1)
        assert bert_page.frontmatter.updated == date.today()
        assert "pre-training" in bert_page.frontmatter.tags

        # Source B Summary should be written normally (no merge)
        assert "source-b-summary.md" in result.get("written_paths", [])

        src.config._settings = None

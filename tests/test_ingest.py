"""Tests for LangGraph ingest pipeline with mocked LLM."""

from __future__ import annotations

from datetime import UTC, date, datetime
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
    BriefOutput,
    Checkpoint,
    Confidence,
    GeneratedPage,
    IngestResult,
    MergeDecision,
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
            created_at=datetime.now(UTC).isoformat(),
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
            brief="Bidirectional encoder model for NLP.",
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

        with (
            patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm,
            patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_merge_llm,
        ):
            mock_llm.return_value = mock_ingest_result
            # brief_merge_check → MergeDecision, then merge_page → PatchedPage, BriefOutput
            mock_merge_llm.side_effect = [
                MergeDecision(action="MERGE", reason="new pre-training info"),
                mock_patched,
                BriefOutput(brief="BERT: merged brief."),
            ]
            result = await process_batches_node(state)

        assert "errors" not in result or len(result.get("errors", [])) == 0
        # Verify BERT page was merged (not just overwritten)
        bert_page = read_page("bert.md", wiki_dir)
        assert (
            "old" in bert_page.frontmatter.sources
            or "new-source.txt" in bert_page.frontmatter.sources
        )
        assert bert_page.frontmatter.created == date(2026, 1, 1)  # preserved

        src.config._settings = None


class TestBuildBatchMessages:
    def test_includes_existing_briefs_in_prompt(self) -> None:
        from src.ingest import _build_batch_messages

        messages = _build_batch_messages(
            chunks=["chunk text"],
            batch_start=0,
            batch_size=5,
            source_title="Test Source",
            existing_briefs={"Flash Attention": "IO-aware exact attention algorithm."},
        )

        user_msg = messages[1]["content"]
        assert "Flash Attention" in user_msg
        assert "IO-aware exact attention" in user_msg

    def test_no_existing_briefs_no_title_list(self) -> None:
        from src.ingest import _build_batch_messages

        messages = _build_batch_messages(
            chunks=["chunk text"],
            batch_start=0,
            batch_size=5,
            source_title="Test Source",
            existing_briefs={},
        )

        user_msg = messages[1]["content"]
        assert "Previously generated" not in user_msg


class TestBuildBatchMessagesV2:
    def test_short_text_mode_instruction(self) -> None:
        from src.ingest import _build_batch_messages

        messages = _build_batch_messages(
            chunks=["Very short text about transformers."],
            batch_start=0,
            batch_size=5,
            source_title="Test",
            existing_briefs={},
            is_short=True,
        )
        user_msg = messages[1]["content"]
        assert "only generate the source_summary" in user_msg.lower() or "only" in user_msg.lower()

    def test_normal_text_no_short_instruction(self) -> None:
        from src.ingest import _build_batch_messages

        long_text = " ".join(["word"] * 2000)
        messages = _build_batch_messages(
            chunks=[long_text],
            batch_start=0,
            batch_size=5,
            source_title="Test",
            existing_briefs={},
            is_short=False,
        )
        user_msg = messages[1]["content"]
        assert "only generate" not in user_msg.lower()

    def test_titles_and_briefs_in_prompt(self) -> None:
        from src.ingest import _build_batch_messages

        messages = _build_batch_messages(
            chunks=["chunk text"],
            batch_start=0,
            batch_size=5,
            source_title="Test",
            existing_briefs={
                "Flash Attention": "IO-aware exact attention algorithm.",
                "Self-Attention": "Mechanism for computing weighted sums.",
            },
            is_short=False,
        )
        user_msg = messages[1]["content"]
        assert "Flash Attention" in user_msg
        assert "IO-aware exact attention" in user_msg
        assert "Self-Attention" in user_msg

    def test_system_prompt_is_static(self) -> None:
        """System prompt should not contain dynamic content (for caching)."""
        from src.ingest import _build_batch_messages

        messages = _build_batch_messages(
            chunks=["chunk1"],
            batch_start=0,
            batch_size=5,
            source_title="Source A",
            existing_briefs={"Title": "Brief"},
            is_short=False,
        )
        system_msg = messages[0]["content"]
        assert "Title" not in system_msg
        assert "Brief" not in system_msg
        assert "Source A" not in system_msg


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
            brief="Bidirectional encoder model for NLP tasks.",
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

        with (
            patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm,
            patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_merge_llm,
        ):
            mock_llm.return_value = source_b_result
            # brief_merge_check → MergeDecision, then merge_page → PatchedPage, BriefOutput
            mock_merge_llm.side_effect = [
                MergeDecision(action="MERGE", reason="new pre-training details from source B"),
                mock_patched,
                BriefOutput(brief="BERT: bidirectional encoder with pre-training."),
            ]
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


class TestEmptyTitleFilter:
    """1a: After intra-batch dedup, filter out pages with empty titles."""

    @pytest.mark.asyncio
    async def test_empty_title_pages_are_skipped(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        import src.config

        src.config._settings = None

        # LLM returns a page with an empty title
        ingest_result = IngestResult(
            source_summary=GeneratedPage(
                title="Valid Page",
                page_type=PageType.SOURCE_SUMMARY,
                tags=["test"],
                confidence=Confidence.HIGH,
                body="# Valid Page\n\nContent.",
                related_titles=[],
            ),
            concept_pages=[
                GeneratedPage(
                    title="",
                    page_type=PageType.CONCEPT,
                    tags=["test"],
                    confidence=Confidence.HIGH,
                    body="# Empty Title\n\nShould be filtered.",
                    related_titles=[],
                ),
            ],
            entity_pages=[],
        )

        state = {
            "chunks": ["Some text"],
            "source_path": "test.txt",
            "source_title": "Test",
            "fresh": True,
        }

        with patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = ingest_result
            result = await process_batches_node(state)

        # Only the valid page should be written, empty title filtered
        assert "errors" not in result or len(result.get("errors", [])) == 0
        written = result.get("written_paths", [])
        assert len(written) == 1
        assert "valid-page.md" in written[0]

        src.config._settings = None

    @pytest.mark.asyncio
    async def test_whitespace_only_title_pages_are_skipped(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        import src.config

        src.config._settings = None

        ingest_result = IngestResult(
            source_summary=GeneratedPage(
                title="  ",
                page_type=PageType.SOURCE_SUMMARY,
                tags=["test"],
                confidence=Confidence.HIGH,
                body="# Whitespace Title\n\nShould be filtered.",
                related_titles=[],
            ),
            concept_pages=[],
            entity_pages=[],
        )

        state = {
            "chunks": ["Some text"],
            "source_path": "test.txt",
            "source_title": "Test",
            "fresh": True,
        }

        with patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = ingest_result
            result = await process_batches_node(state)

        written = result.get("written_paths", [])
        assert len(written) == 0

        src.config._settings = None


class TestBatchBriefAdds:
    """1b: BriefIndex.add calls should be deferred until after the per-page loop."""

    @pytest.mark.asyncio
    async def test_brief_adds_happen_after_all_page_writes(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Verify that brief_idx.add() is called AFTER all pages in the batch are written.

        We track the order of write_page and add() calls. With batching,
        all writes should happen before any add() calls.
        """
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        import src.config

        src.config._settings = None

        ingest_result = IngestResult(
            source_summary=GeneratedPage(
                title="Page One",
                page_type=PageType.SOURCE_SUMMARY,
                tags=["test"],
                confidence=Confidence.HIGH,
                body="# Page One\n\nContent one.",
                related_titles=[],
                brief="Summary of page one about testing.",
            ),
            concept_pages=[
                GeneratedPage(
                    title="Page Two",
                    page_type=PageType.CONCEPT,
                    tags=["test"],
                    confidence=Confidence.HIGH,
                    body="# Page Two\n\nContent two.",
                    related_titles=[],
                    brief="Summary of page two about testing.",
                ),
            ],
            entity_pages=[],
        )

        state = {
            "chunks": ["Some text"],
            "source_path": "test.txt",
            "source_title": "Test",
            "fresh": True,
        }

        call_log: list[str] = []

        with (
            patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm,
            patch("src.ingest.write_page") as mock_write,
            patch("src.ingest.BriefIndex") as mock_brief_idx_cls,
        ):
            from src.search import BriefIndex as RealBriefIndex

            mock_llm.return_value = ingest_result

            # Track write_page calls
            original_write = write_page

            def tracked_write(fm, body, wiki_dir_arg):
                call_log.append(f"write:{fm.title}")
                return original_write(fm, body, wiki_dir_arg)

            mock_write.side_effect = tracked_write

            # Track BriefIndex.add calls
            real_idx = RealBriefIndex()
            original_add = real_idx.add

            def tracked_add(path: str, brief: str) -> None:
                call_log.append(f"add:{path}")
                original_add(path, brief)

            real_idx.add = tracked_add  # type: ignore[method-assign]
            mock_brief_idx_cls.return_value = real_idx

            result = await process_batches_node(state)

        written = result.get("written_paths", [])
        assert len(written) == 2

        # With batched adds, all writes should come before all adds
        write_indices = [i for i, c in enumerate(call_log) if c.startswith("write:")]
        add_indices = [i for i, c in enumerate(call_log) if c.startswith("add:")]

        # Every write index should be less than every add index
        if write_indices and add_indices:
            assert max(write_indices) < min(add_indices), (
                f"Writes must all come before adds. Call order: {call_log}"
            )

        src.config._settings = None


class TestEmptyBriefShortcut:
    """1c: Skip brief_merge_check when existing page has empty brief."""

    @pytest.mark.asyncio
    async def test_skips_brief_check_when_existing_has_no_brief(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """When exact collision and existing page has empty brief, go straight to merge."""
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        import src.config

        src.config._settings = None

        # Pre-create existing page with EMPTY brief
        existing_fm = WikiFrontmatter(
            title="BERT",
            page_type=PageType.ENTITY,
            sources=["old/source.pdf"],
            tags=["nlp"],
            created=date(2026, 1, 1),
            updated=date(2026, 1, 1),
            confidence=Confidence.HIGH,
            brief="",  # Empty brief
        )
        write_page(existing_fm, "# BERT\n\nOld content about BERT.", wiki_dir)

        ingest_result = IngestResult(
            source_summary=GeneratedPage(
                title="Source Summary",
                page_type=PageType.SOURCE_SUMMARY,
                tags=["nlp"],
                confidence=Confidence.HIGH,
                body="# Source\n\nOverview.",
                related_titles=[],
            ),
            concept_pages=[],
            entity_pages=[
                GeneratedPage(
                    title="BERT",  # Exact collision
                    page_type=PageType.ENTITY,
                    tags=["nlp", "pre-training"],
                    confidence=Confidence.HIGH,
                    body="# BERT\n\nNew details.",
                    related_titles=[],
                ),
            ],
        )

        from src.models import EditOp, PatchedPage

        mock_patched = PatchedPage(
            edits=[
                EditOp(
                    old_string="# BERT\n\nOld content about BERT.",
                    new_string="# BERT\n\nOld content about BERT. New details.",
                ),
            ],
            tags_to_add=["pre-training"],
            confidence=Confidence.HIGH,
        )

        state = {
            "chunks": ["Content about BERT pre-training."],
            "source_path": "new-source.txt",
            "source_title": "New Source",
            "fresh": True,
        }

        with (
            patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm,
            patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_merge_llm,
        ):
            mock_llm.return_value = ingest_result

            # Should NOT call brief_merge_check at all (no MergeDecision call)
            # Only merge_page calls: PatchedPage + BriefOutput
            mock_merge_llm.side_effect = [
                mock_patched,
                BriefOutput(brief="BERT: merged brief."),
            ]
            result = await process_batches_node(state)

        # Should have merged without calling brief_merge_check
        assert "errors" not in result or len(result.get("errors", [])) == 0
        bert_page = read_page("bert.md", wiki_dir)
        assert bert_page.frontmatter.created == date(2026, 1, 1)

        # Verify brief_merge_check was NOT called (only 2 merge LLM calls: patch + brief)
        assert mock_merge_llm.call_count == 2

        src.config._settings = None


class TestBriefAnalysis:
    @pytest.mark.asyncio
    async def test_build_batch_messages_with_briefs(self) -> None:
        """_build_batch_messages uses existing_briefs dict with titles and briefs."""
        from src.ingest import _build_batch_messages

        messages = _build_batch_messages(
            chunks=["chunk1", "chunk2"],
            batch_start=0,
            batch_size=2,
            source_title="Test Paper",
            existing_briefs={
                "Flash Attention": "IO-aware exact attention algorithm.",
                "Self-Attention": "Mechanism for computing weighted sums.",
            },
        )
        assert "Flash Attention" in messages[1]["content"]
        assert "Self-Attention" in messages[1]["content"]

    @pytest.mark.asyncio
    async def test_build_batch_messages_empty_existing_briefs(self) -> None:
        """No existing briefs → no previously generated pages list injected."""
        from src.ingest import _build_batch_messages

        messages = _build_batch_messages(
            chunks=["chunk1"],
            batch_start=0,
            batch_size=1,
            source_title="Test",
            existing_briefs={},
        )
        assert "Previously generated" not in messages[1]["content"]

    def test_check_fuzzy_collision_returns_page(self, tmp_path: Path) -> None:
        """Fuzzy collision via BM25 returns matched WikiPage."""
        from src.ingest import _check_fuzzy_collision
        from src.search import BriefIndex

        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()

        # Need 3+ pages so BM25 IDF is non-zero (N=2 makes IDF=0 for all terms)
        fm1 = WikiFrontmatter(
            title="Flash Attention",
            page_type=PageType.CONCEPT,
            brief="IO-aware exact attention algorithm using tiling for memory optimization.",
            sources=["test.pdf"],
            tags=["attention"],
            created=date(2026, 5, 20),
            updated=date(2026, 5, 20),
            confidence=Confidence.HIGH,
        )
        write_page(fm1, "Body.", wiki_dir)
        fm2 = WikiFrontmatter(
            title="Reinforcement Learning",
            page_type=PageType.CONCEPT,
            brief="Agent learns optimal policy through environment interaction and rewards.",
            sources=["test.pdf"],
            tags=["rl"],
            created=date(2026, 5, 20),
            updated=date(2026, 5, 20),
            confidence=Confidence.HIGH,
        )
        write_page(fm2, "Body.", wiki_dir)
        fm3 = WikiFrontmatter(
            title="Gradient Descent",
            page_type=PageType.CONCEPT,
            brief="Optimization algorithm for minimizing loss in neural networks.",
            sources=["test.pdf"],
            tags=["optimization"],
            created=date(2026, 5, 20),
            updated=date(2026, 5, 20),
            confidence=Confidence.HIGH,
        )
        write_page(fm3, "Body.", wiki_dir)

        from src.wiki import read_all_pages

        pages = read_all_pages(wiki_dir)
        idx = BriefIndex()
        idx.build(pages)

        result = _check_fuzzy_collision(
            brief_idx=idx,
            new_brief="Attention optimization using memory tiling techniques.",
            wiki_dir=wiki_dir,
        )
        assert result is not None
        assert result.frontmatter.title == "Flash Attention"

    def test_check_fuzzy_collision_no_match(self, tmp_path: Path) -> None:
        """No fuzzy match → returns None."""
        from src.ingest import _check_fuzzy_collision
        from src.search import BriefIndex

        idx = BriefIndex()
        result = _check_fuzzy_collision(
            brief_idx=idx,
            new_brief="Something completely different.",
            wiki_dir=tmp_path,
        )
        assert result is None

"""Tests for page merge logic."""

from __future__ import annotations

from datetime import date

import pytest

from src.merge import _merge_frontmatter, merge_page
from src.models import (
    BriefOutput,
    Confidence,
    GeneratedPage,
    MergeDecision,
    MergedPage,
    PageType,
    TopicMatchDecision,
    WikiFrontmatter,
    WikiPage,
)


class TestMergeFrontmatter:
    def test_merges_sources(self) -> None:
        existing_fm = WikiFrontmatter(
            title="BERT",
            page_type=PageType.ENTITY,
            sources=["papers/bert.pdf"],
            tags=["nlp"],
            created=date(2026, 1, 1),
            updated=date(2026, 1, 1),
            confidence=Confidence.HIGH,
        )
        new_page = GeneratedPage(
            title="BERT",
            page_type=PageType.ENTITY,
            tags=["nlp", "pre-training"],
            confidence=Confidence.MEDIUM,
            body="# BERT\n\nUpdated content.",
            related_titles=["Transformer Architecture"],
        )

        fm, body = _merge_frontmatter(
            existing_fm=existing_fm,
            new_page=new_page,
            merged_body="Merged body.",
            merged_tags=["nlp", "pre-training", "deep-learning"],
            merged_confidence=Confidence.HIGH,
            source_path="articles/bert-guide.md",
        )

        assert "papers/bert.pdf" in fm.sources
        assert "articles/bert-guide.md" in fm.sources
        assert len(fm.sources) == 2
        assert body == "Merged body."

    def test_does_not_duplicate_sources(self) -> None:
        existing_fm = WikiFrontmatter(
            title="BERT",
            page_type=PageType.ENTITY,
            sources=["papers/bert.pdf"],
            tags=["nlp"],
            created=date(2026, 1, 1),
            updated=date(2026, 1, 1),
        )
        new_page = GeneratedPage(
            title="BERT",
            page_type=PageType.ENTITY,
            tags=["nlp"],
            confidence=Confidence.HIGH,
            body="content",
        )

        fm, _ = _merge_frontmatter(
            existing_fm=existing_fm,
            new_page=new_page,
            merged_body="body",
            merged_tags=["nlp"],
            merged_confidence=Confidence.HIGH,
            source_path="papers/bert.pdf",
        )

        assert fm.sources == ["papers/bert.pdf"]

    def test_merges_tags_deduped(self) -> None:
        existing_fm = WikiFrontmatter(
            title="Test",
            page_type=PageType.CONCEPT,
            sources=[],
            tags=["nlp", "deep-learning"],
            created=date(2026, 1, 1),
            updated=date(2026, 1, 1),
        )
        new_page = GeneratedPage(
            title="Test",
            page_type=PageType.CONCEPT,
            tags=["nlp", "transformers"],
            confidence=Confidence.HIGH,
            body="content",
        )

        fm, _ = _merge_frontmatter(
            existing_fm=existing_fm,
            new_page=new_page,
            merged_body="body",
            merged_tags=["nlp", "transformers", "attention"],
            merged_confidence=Confidence.HIGH,
            source_path="new.pdf",
        )

        assert "nlp" in fm.tags
        assert "deep-learning" in fm.tags
        assert "transformers" in fm.tags
        assert "attention" in fm.tags
        assert len(fm.tags) == len(set(fm.tags))

    def test_preserves_created_date(self) -> None:
        existing_fm = WikiFrontmatter(
            title="Test",
            page_type=PageType.CONCEPT,
            created=date(2026, 1, 1),
            updated=date(2026, 1, 1),
        )
        new_page = GeneratedPage(
            title="Test",
            page_type=PageType.CONCEPT,
            tags=[],
            confidence=Confidence.MEDIUM,
            body="content",
        )

        fm, _ = _merge_frontmatter(
            existing_fm=existing_fm,
            new_page=new_page,
            merged_body="body",
            merged_tags=[],
            merged_confidence=Confidence.MEDIUM,
            source_path="new.pdf",
        )

        assert fm.created == date(2026, 1, 1)
        assert fm.updated == date.today()

    def test_merges_related(self) -> None:
        existing_fm = WikiFrontmatter(
            title="Test",
            page_type=PageType.CONCEPT,
            sources=[],
            tags=[],
            created=date(2026, 1, 1),
            updated=date(2026, 1, 1),
            related=["bert.md", "gpt.md"],
        )
        new_page = GeneratedPage(
            title="Test",
            page_type=PageType.CONCEPT,
            tags=[],
            confidence=Confidence.MEDIUM,
            body="content",
            related_titles=["BERT", "Attention Mechanism"],
        )

        fm, _ = _merge_frontmatter(
            existing_fm=existing_fm,
            new_page=new_page,
            merged_body="body",
            merged_tags=[],
            merged_confidence=Confidence.MEDIUM,
            source_path="new.pdf",
        )

        assert "bert.md" in fm.related
        assert "gpt.md" in fm.related
        assert "attention-mechanism.md" in fm.related

    def test_takes_higher_confidence(self) -> None:
        existing_fm = WikiFrontmatter(
            title="Test",
            page_type=PageType.CONCEPT,
            sources=[],
            tags=[],
            created=date(2026, 1, 1),
            updated=date(2026, 1, 1),
            confidence=Confidence.LOW,
        )
        new_page = GeneratedPage(
            title="Test",
            page_type=PageType.CONCEPT,
            tags=[],
            confidence=Confidence.HIGH,
            body="content",
        )

        fm, _ = _merge_frontmatter(
            existing_fm=existing_fm,
            new_page=new_page,
            merged_body="body",
            merged_tags=[],
            merged_confidence=Confidence.HIGH,
            source_path="new.pdf",
        )

        assert fm.confidence == Confidence.HIGH

    def test_keeps_existing_title_and_page_type(self) -> None:
        existing_fm = WikiFrontmatter(
            title="Original Title",
            page_type=PageType.ENTITY,
            sources=[],
            tags=[],
            created=date(2026, 1, 1),
            updated=date(2026, 1, 1),
        )
        new_page = GeneratedPage(
            title="Different Title",
            page_type=PageType.CONCEPT,
            tags=[],
            confidence=Confidence.MEDIUM,
            body="content",
        )

        fm, _ = _merge_frontmatter(
            existing_fm=existing_fm,
            new_page=new_page,
            merged_body="body",
            merged_tags=[],
            merged_confidence=Confidence.MEDIUM,
            source_path="new.pdf",
        )

        assert fm.title == "Original Title"
        assert fm.page_type == PageType.ENTITY


class TestMergePagePatchSuccess:
    @pytest.mark.asyncio
    async def test_patch_succeeds_on_first_attempt(self) -> None:
        from unittest.mock import AsyncMock, patch

        from src.models import EditOp, PatchedPage

        existing_page = WikiPage(
            path="bert.md",
            frontmatter=WikiFrontmatter(
                title="BERT",
                page_type=PageType.ENTITY,
                sources=["papers/bert.pdf"],
                tags=["nlp"],
                created=date(2026, 1, 1),
                updated=date(2026, 1, 1),
                confidence=Confidence.HIGH,
            ),
            body="# BERT\n\nBidirectional encoder.",
        )
        new_page = GeneratedPage(
            title="BERT",
            page_type=PageType.ENTITY,
            tags=["nlp", "pre-training"],
            confidence=Confidence.HIGH,
            body="# BERT\n\nBidirectional encoder with masked language modeling.",
            related_titles=["Transformer Architecture"],
        )

        mock_patched = PatchedPage(
            edits=[
                EditOp(
                    old_string="Bidirectional encoder.",
                    new_string="Bidirectional encoder with masked language modeling.",
                ),
            ],
            tags_to_add=["pre-training"],
            confidence=Confidence.HIGH,
        )

        with patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.side_effect = [
                mock_patched,
                BriefOutput(brief="BERT with masked language modeling."),
            ]
            fm, body = await merge_page(existing_page, new_page, "articles/bert-guide.md")

        assert "masked language modeling" in body
        assert "pre-training" in fm.tags
        assert mock_llm.call_count == 2  # 1 patch + 1 brief regen

    @pytest.mark.asyncio
    async def test_patch_retries_on_failure_then_succeeds(self) -> None:
        from unittest.mock import AsyncMock, patch

        from src.models import EditOp, PatchedPage

        existing_page = WikiPage(
            path="bert.md",
            frontmatter=WikiFrontmatter(
                title="BERT",
                page_type=PageType.ENTITY,
                sources=["papers/bert.pdf"],
                tags=["nlp"],
                created=date(2026, 1, 1),
                updated=date(2026, 1, 1),
            ),
            body="# BERT\n\nBidirectional encoder.",
        )
        new_page = GeneratedPage(
            title="BERT",
            page_type=PageType.ENTITY,
            tags=["nlp"],
            confidence=Confidence.MEDIUM,
            body="# BERT\n\nUpdated content.",
        )

        bad_patch = PatchedPage(
            edits=[EditOp(old_string="NOT IN BODY", new_string="x")],
            tags_to_add=[],
            confidence=Confidence.MEDIUM,
        )
        good_patch = PatchedPage(
            edits=[EditOp(old_string="Bidirectional encoder.", new_string="Updated content.")],
            tags_to_add=[],
            confidence=Confidence.MEDIUM,
        )

        with patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.side_effect = [
                bad_patch,
                good_patch,
                BriefOutput(brief="Updated BERT content."),
            ]
            fm, body = await merge_page(existing_page, new_page, "new.pdf")

        assert body == "# BERT\n\nUpdated content."
        assert mock_llm.call_count == 3  # 2 patch attempts + 1 brief regen

    @pytest.mark.asyncio
    async def test_falls_back_to_rewrite_after_3_patch_failures(self) -> None:
        from unittest.mock import AsyncMock, patch

        from src.models import EditOp, PatchedPage

        existing_page = WikiPage(
            path="bert.md",
            frontmatter=WikiFrontmatter(
                title="BERT",
                page_type=PageType.ENTITY,
                sources=["papers/bert.pdf"],
                tags=["nlp"],
                created=date(2026, 1, 1),
                updated=date(2026, 1, 1),
            ),
            body="# BERT\n\nBidirectional encoder.",
        )
        new_page = GeneratedPage(
            title="BERT",
            page_type=PageType.ENTITY,
            tags=["nlp"],
            confidence=Confidence.MEDIUM,
            body="# BERT\n\nUpdated content.",
        )

        bad_patch = PatchedPage(
            edits=[EditOp(old_string="NOT IN BODY", new_string="x")],
            tags_to_add=[],
            confidence=Confidence.MEDIUM,
        )
        mock_merged = MergedPage(
            body="# BERT\n\nBidirectional encoder. Updated content.",
            tags=["nlp"],
            confidence=Confidence.MEDIUM,
        )

        with patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.side_effect = [
                bad_patch,
                bad_patch,
                bad_patch,
                mock_merged,
                BriefOutput(brief="BERT: bidirectional encoder with updates."),
            ]
            fm, body = await merge_page(existing_page, new_page, "new.pdf")

        assert "Updated content" in body
        assert mock_llm.call_count == 5  # 3 patch + 1 rewrite + 1 brief regen


class TestBriefAnalysis:
    @pytest.mark.asyncio
    async def test_scenario_a_merge(self) -> None:
        """Scenario A: brief + body -> LLM says MERGE."""
        from unittest.mock import AsyncMock, patch

        from src.merge import brief_merge_check

        result = MergeDecision(action="MERGE", reason="New FA2 details.")
        with patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = result
            decision = await brief_merge_check(
                existing_brief="IO-aware exact attention via tiling.",
                existing_title="Flash Attention",
                new_body="Flash Attention 2 reduces non-matmul FLOPs further.",
            )

        assert decision.action == "MERGE"
        assert mock_llm.call_count == 1

    @pytest.mark.asyncio
    async def test_scenario_a_skip(self) -> None:
        """Scenario A: brief + body -> LLM says SKIP."""
        from unittest.mock import AsyncMock, patch

        from src.merge import brief_merge_check

        result = MergeDecision(action="SKIP", reason="Already covered.")
        with patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = result
            decision = await brief_merge_check(
                existing_brief="IO-aware exact attention via tiling.",
                existing_title="Flash Attention",
                new_body="Flash Attention uses tiling to reduce memory access.",
            )

        assert decision.action == "SKIP"
        assert mock_llm.call_count == 1

    @pytest.mark.asyncio
    async def test_scenario_b_same_topic(self) -> None:
        """Scenario B: brief vs brief -> LLM says same topic."""
        from unittest.mock import AsyncMock, patch

        from src.merge import topic_match_check

        result = TopicMatchDecision(same_topic=True, reason="Both about Flash Attention.")
        with patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = result
            decision = await topic_match_check(
                existing_title="Flash Attention",
                existing_brief="IO-aware exact attention via tiling.",
                new_title="Flash Attention Algorithm",
                new_brief="Attention optimization using memory tiling.",
            )

        assert decision.same_topic is True
        assert mock_llm.call_count == 1

    @pytest.mark.asyncio
    async def test_scenario_b_different_topic(self) -> None:
        """Scenario B: brief vs brief -> LLM says different topics."""
        from unittest.mock import AsyncMock, patch

        from src.merge import topic_match_check

        result = TopicMatchDecision(same_topic=False, reason="Different topics.")
        with patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = result
            decision = await topic_match_check(
                existing_title="Flash Attention",
                existing_brief="IO-aware exact attention via tiling.",
                new_title="Attention Span",
                new_brief="Psychological concept about focus duration.",
            )

        assert decision.same_topic is False

    @pytest.mark.asyncio
    async def test_regenerate_brief(self) -> None:
        """Post-merge brief regeneration."""
        from unittest.mock import AsyncMock, patch

        from src.merge import regenerate_brief

        mock_output = BriefOutput(brief="Updated brief about FA1 and FA2.")
        with patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = mock_output
            brief = await regenerate_brief(
                title="Flash Attention",
                merged_body="Updated body about Flash Attention 2.",
            )

        assert brief == "Updated brief about FA1 and FA2."
        assert mock_llm.call_count == 1


class TestBatchCollisionCheck:
    @pytest.mark.asyncio
    async def test_batch_decision_mixed(self) -> None:
        """Multiple collision pairs decided in one call."""
        from unittest.mock import AsyncMock, patch

        from src.merge import batch_collision_check
        from src.models import BatchCollisionDecision, CollisionDecision, CollisionPair

        pairs = [
            CollisionPair(
                new_title="Flash Attention v2",
                existing_title="Flash Attention",
                existing_brief="IO-aware attention.",
                collision_type="exact",
            ),
            CollisionPair(
                new_title="Tiling Strategy",
                existing_title="GPU Tiling",
                existing_brief="Tiling for GPU memory.",
                collision_type="fuzzy",
                new_brief="Tiling strategies for attention.",
            ),
        ]

        expected = BatchCollisionDecision(
            decisions=[
                CollisionDecision(new_title="Flash Attention v2", action="MERGE", reason="same topic"),
                CollisionDecision(new_title="Tiling Strategy", action="SKIP", reason="different focus"),
            ]
        )

        with patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = expected
            result = await batch_collision_check(pairs)

        assert len(result.decisions) == 2
        assert result.decisions[0].action == "MERGE"
        assert result.decisions[1].action == "SKIP"
        assert mock_llm.call_count == 1  # single call

    @pytest.mark.asyncio
    async def test_empty_pairs_returns_empty(self) -> None:
        """No pairs → no LLM call."""
        from src.merge import batch_collision_check

        result = await batch_collision_check([])
        assert result.decisions == []


class TestMergePageWithBrief:
    @pytest.mark.asyncio
    async def test_merge_page_regenerates_brief(self) -> None:
        """merge_page should regenerate brief after successful patch merge."""
        from unittest.mock import AsyncMock, patch

        from src.models import EditOp, PatchedPage

        existing_page = WikiPage(
            path="flash-attention.md",
            frontmatter=WikiFrontmatter(
                title="Flash Attention",
                page_type=PageType.CONCEPT,
                brief="IO-aware exact attention via tiling.",
                sources=["papers/fa.pdf"],
                tags=["attention"],
                created=date(2026, 1, 1),
                updated=date(2026, 1, 1),
                confidence=Confidence.HIGH,
            ),
            body="# Flash Attention\n\nIO-aware exact attention.",
        )
        new_page = GeneratedPage(
            title="Flash Attention",
            page_type=PageType.CONCEPT,
            tags=["attention", "optimization"],
            confidence=Confidence.HIGH,
            body="# Flash Attention\n\nIO-aware exact attention with FA2 improvements.",
            brief="Updated brief about FA1 and FA2.",
        )

        mock_patch = PatchedPage(
            edits=[
                EditOp(
                    old_string="IO-aware exact attention.",
                    new_string="IO-aware exact attention with FA2 improvements.",
                ),
            ],
            tags_to_add=["optimization"],
            confidence=Confidence.HIGH,
        )
        mock_brief = BriefOutput(
            brief="FA1 and FA2: IO-aware exact attention with tiling optimizations."
        )

        with patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.side_effect = [mock_patch, mock_brief]
            fm, body = await merge_page(existing_page, new_page, "papers/fa2.pdf")

        assert "FA2" in body
        assert fm.brief == "FA1 and FA2: IO-aware exact attention with tiling optimizations."
        assert mock_llm.call_count == 2  # 1 patch + 1 brief regen

    @pytest.mark.asyncio
    async def test_merge_page_regen_brief_on_rewrite_fallback(self) -> None:
        """Brief regenerated even when falling back to rewrite."""
        from unittest.mock import AsyncMock, patch

        from src.models import EditOp, PatchedPage

        existing_page = WikiPage(
            path="bert.md",
            frontmatter=WikiFrontmatter(
                title="BERT",
                page_type=PageType.ENTITY,
                brief="Bidirectional encoder.",
                sources=["papers/bert.pdf"],
                tags=["nlp"],
                created=date(2026, 1, 1),
                updated=date(2026, 1, 1),
            ),
            body="# BERT\n\nBidirectional encoder.",
        )
        new_page = GeneratedPage(
            title="BERT",
            page_type=PageType.ENTITY,
            tags=["nlp"],
            confidence=Confidence.MEDIUM,
            body="# BERT\n\nUpdated content.",
            brief="Updated BERT description.",
        )

        bad_patch = PatchedPage(
            edits=[EditOp(old_string="NOT IN BODY", new_string="x")],
            tags_to_add=[],
            confidence=Confidence.MEDIUM,
        )
        mock_merged = MergedPage(
            body="# BERT\n\nBidirectional encoder. Updated content.",
            tags=["nlp"],
            confidence=Confidence.MEDIUM,
        )
        mock_brief = BriefOutput(brief="BERT: bidirectional encoder with updated details.")

        with patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.side_effect = [bad_patch, bad_patch, bad_patch, mock_merged, mock_brief]
            fm, body = await merge_page(existing_page, new_page, "new.pdf")

        assert fm.brief == "BERT: bidirectional encoder with updated details."
        assert mock_llm.call_count == 5  # 3 patch + 1 rewrite + 1 brief regen

"""Tests for page merge logic."""

from __future__ import annotations

from datetime import date

import pytest

from src.merge import _merge_frontmatter, merge_page
from src.models import (
    Confidence,
    GeneratedPage,
    MergedPage,
    PageType,
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
            mock_llm.return_value = mock_patched
            fm, body = await merge_page(existing_page, new_page, "articles/bert-guide.md")

        assert "masked language modeling" in body
        assert "pre-training" in fm.tags
        assert mock_llm.call_count == 1

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
            mock_llm.side_effect = [bad_patch, good_patch]
            fm, body = await merge_page(existing_page, new_page, "new.pdf")

        assert body == "# BERT\n\nUpdated content."
        assert mock_llm.call_count == 2

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
            mock_llm.side_effect = [bad_patch, bad_patch, bad_patch, mock_merged]
            fm, body = await merge_page(existing_page, new_page, "new.pdf")

        assert "Updated content" in body
        assert mock_llm.call_count == 4  # 3 patch + 1 rewrite

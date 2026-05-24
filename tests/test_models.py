"""Tests for Pydantic models."""

from __future__ import annotations

from datetime import date

import pytest

from src.models import (
    Checkpoint,
    Confidence,
    ExtractedSource,
    GeneratedPage,
    IngestResult,
    LintIssue,
    MergeDecision,
    PageType,
    QueryAnswer,
    TopicMatchDecision,
    WikiFrontmatter,
)


class TestPageType:
    def test_values(self):
        assert PageType.CONCEPT == "concept"
        assert PageType.ENTITY == "entity"
        assert PageType.SOURCE_SUMMARY == "source_summary"
        assert PageType.SYNTHESIS == "synthesis"

    def test_all_types_defined(self):
        assert len(PageType) == 4


class TestWikiFrontmatter:
    def test_create_with_alias(self):
        """PageType field uses 'type' alias for YAML compatibility."""
        fm = WikiFrontmatter(title="Test", type="concept")
        assert fm.page_type == PageType.CONCEPT

    def test_create_with_field_name(self):
        fm = WikiFrontmatter(title="Test", page_type=PageType.ENTITY)
        assert fm.page_type == PageType.ENTITY

    def test_defaults(self):
        fm = WikiFrontmatter(title="Test", type="concept")
        assert fm.sources == []
        assert fm.tags == []
        assert fm.confidence == Confidence.MEDIUM
        assert fm.created == date.today()

    def test_invalid_page_type(self):
        with pytest.raises(ValueError):
            WikiFrontmatter(title="Test", type="invalid")


class TestWikiPage:
    def test_create(self, sample_page):
        assert sample_page.path == "test-page.md"
        assert sample_page.frontmatter.title == "Test Page"
        assert "content" in sample_page.body


class TestGeneratedPage:
    def test_create(self, sample_generated_page):
        assert sample_generated_page.title == "Attention Mechanism"
        assert sample_generated_page.page_type == PageType.CONCEPT
        assert len(sample_generated_page.tags) == 2

    def test_defaults(self):
        gp = GeneratedPage(
            title="Min",
            page_type=PageType.CONCEPT,
            tags=["t"],
            body="content",
        )
        assert gp.confidence == Confidence.MEDIUM
        assert gp.related_titles == []


class TestIngestResult:
    def test_create(self, sample_generated_page):
        result = IngestResult(
            source_summary=sample_generated_page,
            concept_pages=[sample_generated_page],
        )
        assert result.source_summary.title == "Attention Mechanism"
        assert len(result.concept_pages) == 1
        assert result.entity_pages == []


class TestQueryAnswer:
    def test_no_persist(self):
        qa = QueryAnswer(
            answer="Attention is...",
            citations=["Transformer Architecture"],
        )
        assert not qa.should_persist
        assert qa.synthesis_page is None
        assert qa.follow_up_queries == []

    def test_with_persist(self, sample_generated_page):
        qa = QueryAnswer(
            answer="Cross-attention combines...",
            citations=["Transformer Architecture", "BERT"],
            should_persist=True,
            synthesis_page=sample_generated_page,
        )
        assert qa.should_persist
        assert qa.synthesis_page is not None


class TestLintIssue:
    def test_create(self):
        issue = LintIssue(
            page="orphan.md",
            issue_type="orphan",
            severity="warning",
            message="No inbound links",
        )
        assert issue.suggestion == ""

    def test_with_suggestion(self):
        issue = LintIssue(
            page="stale.md",
            issue_type="stale",
            severity="info",
            message="Source modified after page update",
            suggestion="Re-ingest the source",
        )
        assert issue.suggestion == "Re-ingest the source"


class TestExtractedSource:
    def test_create(self):
        es = ExtractedSource(
            content="Hello world",
            source_type="text",
            title="test.txt",
        )
        assert es.metadata == {}


class TestEditOp:
    def test_create_edit_op(self) -> None:
        from src.models import EditOp

        op = EditOp(old_string="hello", new_string="world")
        assert op.old_string == "hello"
        assert op.new_string == "world"
        assert op.replace_all is False

    def test_create_edit_op_replace_all(self) -> None:
        from src.models import EditOp

        op = EditOp(old_string="foo", new_string="bar", replace_all=True)
        assert op.replace_all is True


class TestPatchedPage:
    def test_create_patched_page(self) -> None:
        from src.models import Confidence, EditOp, PatchedPage

        page = PatchedPage(
            edits=[
                EditOp(old_string="old text", new_string="new text"),
                EditOp(old_string="another", new_string="replacement"),
            ],
            tags_to_add=["transformers"],
            confidence=Confidence.HIGH,
        )
        assert len(page.edits) == 2
        assert page.tags_to_add == ["transformers"]
        assert page.confidence == Confidence.HIGH

    def test_patched_page_defaults(self) -> None:
        from src.models import Confidence, PatchedPage

        page = PatchedPage(edits=[])
        assert page.tags_to_add == []
        assert page.confidence == Confidence.MEDIUM


class TestBriefField:
    def test_wiki_frontmatter_has_brief(self) -> None:
        fm = WikiFrontmatter(
            title="Test",
            page_type=PageType.CONCEPT,
            brief="A short summary of the page content.",
        )
        assert fm.brief == "A short summary of the page content."

    def test_wiki_frontmatter_brief_defaults_empty(self) -> None:
        fm = WikiFrontmatter(title="Test", page_type=PageType.CONCEPT)
        assert fm.brief == ""

    def test_generated_page_has_brief(self) -> None:
        page = GeneratedPage(
            title="Test",
            page_type=PageType.CONCEPT,
            tags=["test"],
            confidence=Confidence.HIGH,
            body="Content.",
            brief="Short description.",
        )
        assert page.brief == "Short description."

    def test_checkpoint_has_generated_briefs(self) -> None:
        cp = Checkpoint(
            source="test.pdf",
            source_title="Test",
            total_chunks=5,
            created_at="2026-05-20T00:00:00+00:00",
            generated_briefs={"Flash Attention": "IO-aware exact attention via tiling."},
        )
        assert cp.generated_briefs["Flash Attention"] == "IO-aware exact attention via tiling."

    def test_checkpoint_generated_briefs_defaults_empty(self) -> None:
        cp = Checkpoint(
            source="test.pdf",
            source_title="Test",
            total_chunks=5,
            created_at="2026-05-20T00:00:00+00:00",
        )
        assert cp.generated_briefs == {}

    def test_merge_decision_model(self) -> None:
        d = MergeDecision(action="MERGE", reason="New info about FA2.")
        assert d.action == "MERGE"

    def test_topic_match_decision_model(self) -> None:
        d = TopicMatchDecision(same_topic=True, reason="Both about Flash Attention.")
        assert d.same_topic is True


class TestBatchCollisionModels:
    def test_collision_pair_exact(self) -> None:
        from src.models import CollisionPair

        pair = CollisionPair(
            new_title="Flash Attention v2",
            existing_title="Flash Attention",
            existing_brief="IO-aware attention algorithm.",
            collision_type="exact",
        )
        assert pair.collision_type == "exact"
        assert pair.new_brief == ""

    def test_collision_pair_fuzzy(self) -> None:
        from src.models import CollisionPair

        pair = CollisionPair(
            new_title="Attention Optimization",
            existing_title="Flash Attention",
            existing_brief="IO-aware attention algorithm.",
            collision_type="fuzzy",
            new_brief="Techniques for faster attention computation.",
        )
        assert pair.new_brief != ""

    def test_batch_collision_decision(self) -> None:
        from src.models import BatchCollisionDecision, CollisionDecision

        decision = BatchCollisionDecision(
            decisions=[
                CollisionDecision(new_title="A", action="MERGE", reason="same topic"),
                CollisionDecision(new_title="B", action="SKIP", reason="different focus"),
            ]
        )
        assert len(decision.decisions) == 2
        assert decision.decisions[0].action == "MERGE"
        assert decision.decisions[1].action == "SKIP"


class TestIngestStats:
    def test_create_with_defaults(self) -> None:
        from src.models import IngestStats

        stats = IngestStats()
        assert stats.duration_s == 0.0
        assert stats.new == 0
        assert stats.merge == 0
        assert stats.skip == 0
        assert stats.skip_fuzzy_new == 0
        assert stats.page_types == {}

    def test_create_with_values(self) -> None:
        from src.models import IngestStats

        stats = IngestStats(
            duration_s=12.34,
            new=5,
            merge=2,
            skip=1,
            skip_fuzzy_new=0,
            page_types={"concept": 4, "entity": 2, "source_summary": 1},
        )
        assert stats.duration_s == 12.34
        assert stats.new == 5
        assert stats.merge == 2
        assert stats.skip == 1
        assert stats.page_types == {"concept": 4, "entity": 2, "source_summary": 1}

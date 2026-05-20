"""Pydantic schemas for wiki pages, LLM responses, and lint issues."""

from __future__ import annotations

from datetime import date
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field

# ── Enums ────────────────────────────────────────────────────────────────────


class PageType(StrEnum):
    CONCEPT = "concept"
    ENTITY = "entity"
    SOURCE_SUMMARY = "source_summary"
    SYNTHESIS = "synthesis"


class Confidence(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


# ── Wiki page models ────────────────────────────────────────────────────────


class WikiFrontmatter(BaseModel):
    """YAML frontmatter parsed from a wiki page."""

    title: str
    page_type: PageType = Field(alias="type")
    sources: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    created: date = Field(default_factory=date.today)
    updated: date = Field(default_factory=date.today)
    confidence: Confidence = Confidence.MEDIUM
    related: list[str] = Field(default_factory=list, description="[[WikiLink]] targets")
    brief: str = Field(default="", description="Short summary of what this page covers")

    model_config = {"populate_by_name": True}


class WikiPage(BaseModel):
    """A complete wiki page: frontmatter + body content."""

    path: str = Field(description="Relative path within wiki/ dir")
    frontmatter: WikiFrontmatter
    body: str = Field(description="Markdown body after frontmatter")
    raw: str = Field(default="", description="Original raw markdown")


# ── LLM structured output models ────────────────────────────────────────────


class GeneratedPage(BaseModel):
    """LLM output: one wiki page to create."""

    title: str = Field(description="Page title")
    page_type: PageType = Field(description="concept, entity, source_summary, or synthesis")
    tags: list[str] = Field(description="3-7 relevant tags")
    confidence: Confidence = Field(
        default=Confidence.MEDIUM, description="high/medium/low based on source quality"
    )
    body: str = Field(description="Full markdown body content")
    related_titles: list[str] = Field(
        default_factory=list,
        description="Titles of other wiki pages this should link to",
    )
    brief: str = Field(default="", description="Short summary of what this page covers")


class MergedPage(BaseModel):
    """LLM output: merged content from existing + new page about the same topic."""

    body: str = Field(
        description="Merged markdown body preserving all unique information from both versions"
    )
    tags: list[str] = Field(description="Combined tag list from both versions")
    confidence: Confidence = Field(default=Confidence.MEDIUM)


class EditOp(BaseModel):
    """Single edit operation: exact string replacement."""

    old_string: str = Field(description="Exact text from existing body to replace, must be unique")
    new_string: str = Field(description="Replacement text. Empty string = deletion")
    replace_all: bool = Field(default=False, description="True to replace all occurrences")


class PatchedPage(BaseModel):
    """LLM output: a batch of edit operations + metadata delta."""

    edits: list[EditOp] = Field(description="Edit operations to apply in order")
    tags_to_add: list[str] = Field(default_factory=list, description="Tags to add (incremental)")
    confidence: Confidence = Confidence.MEDIUM


class MergeDecision(BaseModel):
    """Scenario A: should we merge new content into existing page?"""

    action: Literal["MERGE", "SKIP"]
    reason: str


class TopicMatchDecision(BaseModel):
    """Scenario B: do two briefs describe the same topic?"""

    same_topic: bool
    reason: str


class BriefOutput(BaseModel):
    """Lightweight model for brief regeneration only."""

    brief: str


class IngestResult(BaseModel):
    """LLM output: all pages to create from a single source."""

    source_summary: GeneratedPage = Field(description="Summary page for the source itself")
    concept_pages: list[GeneratedPage] = Field(
        description="Key concepts extracted from the source (3-10 pages)"
    )
    entity_pages: list[GeneratedPage] = Field(
        default_factory=list,
        description="Named entities worth their own page (people, orgs, tools)",
    )


class QueryAnswer(BaseModel):
    """LLM output: answer to a wiki query."""

    answer: str = Field(description="Direct answer to the question")
    citations: list[str] = Field(description="Wiki page titles used as sources")
    confidence: Confidence = Field(
        default=Confidence.MEDIUM, description="Confidence in the answer"
    )
    follow_up_queries: list[str] = Field(
        default_factory=list, description="Suggested follow-up questions"
    )
    should_persist: bool = Field(
        default=False,
        description="True if this answer reveals a new synthesis worth saving",
    )
    synthesis_page: GeneratedPage | None = Field(
        default=None, description="If should_persist, the page to create"
    )


# ── Lint models ──────────────────────────────────────────────────────────────


class LintIssue(BaseModel):
    """One issue found during wiki lint."""

    page: str = Field(description="Wiki page path")
    issue_type: str = Field(
        description="orphan | contradiction | stale | broken_ref | missing_field"
    )
    severity: str = Field(description="error | warning | info")
    message: str
    suggestion: str = Field(default="")


# ── Checkpoint models ────────────────────────────────────────────────────────


class Checkpoint(BaseModel):
    """Tracks ingest progress for resume after interruption."""

    source: str
    source_title: str
    total_chunks: int
    batch_size: int = 5
    completed_batches: list[int] = Field(default_factory=list)
    generated_titles: list[str] = Field(default_factory=list)
    created_at: str  # ISO datetime for staleness check
    generated_briefs: dict[str, str] = Field(default_factory=dict)


# ── Extraction models ───────────────────────────────────────────────────────


class ExtractedSource(BaseModel):
    """Result of extracting text from a source file or URL."""

    content: str
    source_type: str = Field(description="pdf | url | text | markdown")
    title: str
    metadata: dict[str, str] = Field(default_factory=dict)

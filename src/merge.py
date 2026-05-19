"""Page merge: combine existing wiki pages with new content via LLM."""

from __future__ import annotations

import logging
from datetime import date

from src.config import get_allowed_tags, get_merge_prompt
from src.llm import complete_structured
from src.models import (
    Confidence,
    GeneratedPage,
    MergedPage,
    WikiFrontmatter,
    WikiPage,
)
from src.wiki import title_to_path

logger = logging.getLogger(__name__)

_CONFIDENCE_ORDER = {Confidence.HIGH: 3, Confidence.MEDIUM: 2, Confidence.LOW: 1}


def _merge_frontmatter(
    existing_fm: WikiFrontmatter,
    new_page: GeneratedPage,
    merged_body: str,
    merged_tags: list[str],
    merged_confidence: Confidence,
    source_path: str,
) -> tuple[WikiFrontmatter, str]:
    """Merge frontmatter fields from existing page and new generated page.

    Pure logic -- no LLM call. Returns (merged_frontmatter, merged_body).
    """
    # Sources: append new source if not already present
    sources = list(existing_fm.sources)
    if source_path not in sources:
        sources.append(source_path)

    # Tags: union of existing + LLM-merged tags, deduplicated, order-preserving
    seen: set[str] = set()
    tags: list[str] = []
    for t in existing_fm.tags + merged_tags:
        if t not in seen:
            seen.add(t)
            tags.append(t)

    # Related: union of existing paths + new title-to-path conversions
    existing_related = set(existing_fm.related)
    new_related = {title_to_path(t) for t in new_page.related_titles}
    related = sorted(existing_related | new_related)

    # Confidence: take the higher of existing vs merged
    confidence = (
        merged_confidence
        if _CONFIDENCE_ORDER.get(merged_confidence, 0)
        >= _CONFIDENCE_ORDER.get(existing_fm.confidence, 0)
        else existing_fm.confidence
    )

    fm = WikiFrontmatter(
        title=existing_fm.title,
        page_type=existing_fm.page_type,
        sources=sources,
        tags=tags,
        created=existing_fm.created,
        updated=date.today(),
        confidence=confidence,
        related=related,
    )

    return fm, merged_body


async def merge_page(
    existing: WikiPage,
    new_page: GeneratedPage,
    source_path: str,
) -> tuple[WikiFrontmatter, str]:
    """Merge existing page with new generated page via LLM.

    Sends both page bodies to the LLM with a merge prompt.
    Returns (merged_frontmatter, merged_body) ready for write_page().
    """
    system_prompt = get_merge_prompt()

    allowed_tags = get_allowed_tags()
    if allowed_tags:
        system_prompt += "\n\nPreferred tags (use these when applicable): " + ", ".join(
            allowed_tags
        )

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": (
                f"Merge these two wiki pages about the same topic.\n\n"
                f"=== EXISTING PAGE ===\n"
                f"Title: {existing.frontmatter.title}\n\n"
                f"{existing.body}\n\n"
                f"=== NEW CONTENT (from source: {source_path}) ===\n"
                f"Title: {new_page.title}\n\n"
                f"{new_page.body}\n\n"
                f"Produce a single merged page that preserves all unique "
                f"information from both versions."
            ),
        },
    ]

    result = await complete_structured(
        messages=messages,
        response_model=MergedPage,
        temperature=0.2,
    )

    logger.info("merged page title=%s", existing.frontmatter.title)

    return _merge_frontmatter(
        existing_fm=existing.frontmatter,
        new_page=new_page,
        merged_body=result.body,
        merged_tags=result.tags,
        merged_confidence=result.confidence,
        source_path=source_path,
    )

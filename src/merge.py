"""Page merge: combine existing wiki pages with new content via LLM."""

from __future__ import annotations

import logging
from datetime import date

from src.config import get_allowed_tags, get_edit_prompt, get_merge_prompt
from src.llm import complete_structured
from src.models import (
    BriefOutput,
    Confidence,
    GeneratedPage,
    MergeDecision,
    MergedPage,
    PatchedPage,
    TopicMatchDecision,
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
    brief: str = "",
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
        brief=brief or existing_fm.brief,
    )

    return fm, merged_body


async def brief_merge_check(
    existing_brief: str,
    existing_title: str,
    new_body: str,
) -> MergeDecision:
    """Scenario A: decide whether to merge new content into existing page.

    Uses existing page's brief + new page's body to determine if the new
    content adds significant information.
    """
    messages = [
        {
            "role": "user",
            "content": (
                f'Existing page "{existing_title}" covers: {existing_brief}\n\n'
                f"New content generated about this topic:\n{new_body}\n\n"
                "Does the new content add significant information not covered "
                'by the existing page?\nAnswer MERGE or SKIP. When uncertain, choose MERGE.'
            ),
        },
    ]
    return await complete_structured(
        messages=messages,
        response_model=MergeDecision,
        temperature=0.1,
    )


async def topic_match_check(
    existing_title: str,
    existing_brief: str,
    new_title: str,
    new_brief: str,
) -> TopicMatchDecision:
    """Scenario B: check if two briefs describe the same topic."""
    messages = [
        {
            "role": "user",
            "content": (
                f'Existing page "{existing_title}" covers: {existing_brief}\n'
                f'New page "{new_title}" covers: {new_brief}\n\n'
                "Are these about the same topic?\nAnswer SAME or DIFFERENT."
            ),
        },
    ]
    return await complete_structured(
        messages=messages,
        response_model=TopicMatchDecision,
        temperature=0.1,
    )


async def regenerate_brief(title: str, merged_body: str) -> str:
    """Regenerate brief after merge. Returns the new brief string."""
    result = await complete_structured(
        messages=[
            {
                "role": "user",
                "content": (
                    f'Write a brief summary (1-3 sentences) for this wiki page:\n\n'
                    f"Title: {title}\n\n{merged_body}"
                ),
            },
        ],
        response_model=BriefOutput,
        temperature=0.1,
    )
    return result.brief


def _build_patch_messages(
    existing: WikiPage,
    new_page: GeneratedPage,
    source_path: str,
    last_error: str | None = None,
) -> list[dict[str, str]]:
    """Build LLM messages for patch-mode merge."""
    system_prompt = get_edit_prompt()
    allowed_tags = get_allowed_tags()
    if allowed_tags:
        system_prompt += "\n\nPreferred tags (use these when applicable): " + ", ".join(
            allowed_tags
        )

    user_content = (
        f"Compare the existing wiki page with new content and generate edit operations to merge them.\n\n"
        f"=== EXISTING PAGE ===\n"
        f"Title: {existing.frontmatter.title}\n\n"
        f"{existing.body}\n\n"
        f"=== NEW CONTENT (from source: {source_path}) ===\n"
        f"Title: {new_page.title}\n\n"
        f"{new_page.body}\n\n"
        f"Generate minimal edit operations to add new information to the existing page."
    )

    if last_error:
        user_content += (
            f"\n\nPrevious edit attempt failed with error: {last_error}\n"
            f"Check that old_string exactly matches text in the existing page "
            f"(including spaces, newlines, indentation) and correct it."
        )

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]


def _build_rewrite_messages(
    existing: WikiPage,
    new_page: GeneratedPage,
    source_path: str,
) -> list[dict[str, str]]:
    """Build LLM messages for rewrite-mode merge (fallback)."""
    system_prompt = get_merge_prompt()
    allowed_tags = get_allowed_tags()
    if allowed_tags:
        system_prompt += "\n\nPreferred tags (use these when applicable): " + ", ".join(
            allowed_tags
        )

    return [
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


async def merge_page(
    existing: WikiPage,
    new_page: GeneratedPage,
    source_path: str,
) -> tuple[WikiFrontmatter, str]:
    """Merge existing page with new generated page via edit/patch or full rewrite.

    Tries patch-first (up to 3 attempts with error context on retry).
    Falls back to full rewrite via MergedPage if all patch attempts fail.
    """
    from src.patch import PatchError, apply_edits

    max_patch_attempts = 3
    last_error: str | None = None

    for attempt in range(max_patch_attempts):
        messages = _build_patch_messages(existing, new_page, source_path, last_error)
        result = await complete_structured(
            messages=messages,
            response_model=PatchedPage,
            temperature=0.2,
        )

        try:
            body = apply_edits(existing.body, result.edits)
            logger.info(
                "patched page title=%s attempt=%d edits=%d",
                existing.frontmatter.title,
                attempt + 1,
                len(result.edits),
            )
            merged_tags = list(existing.frontmatter.tags) + result.tags_to_add
            merged_confidence = result.confidence
            fm, merged_body = _merge_frontmatter(
                existing_fm=existing.frontmatter,
                new_page=new_page,
                merged_body=body,
                merged_tags=merged_tags,
                merged_confidence=merged_confidence,
                source_path=source_path,
            )
            fm.brief = await regenerate_brief(existing.frontmatter.title, merged_body)
            return fm, merged_body
        except PatchError as e:
            last_error = str(e)
            logger.warning(
                "patch attempt %d failed for title=%s: %s",
                attempt + 1,
                existing.frontmatter.title,
                e,
            )

    # Fallback: full rewrite
    logger.info("falling back to rewrite for title=%s", existing.frontmatter.title)
    messages = _build_rewrite_messages(existing, new_page, source_path)
    result = await complete_structured(
        messages=messages,
        response_model=MergedPage,
        temperature=0.2,
    )

    logger.info("rewrote page title=%s", existing.frontmatter.title)
    fm, merged_body = _merge_frontmatter(
        existing_fm=existing.frontmatter,
        new_page=new_page,
        merged_body=result.body,
        merged_tags=result.tags,
        merged_confidence=result.confidence,
        source_path=source_path,
    )
    fm.brief = await regenerate_brief(existing.frontmatter.title, merged_body)
    return fm, merged_body

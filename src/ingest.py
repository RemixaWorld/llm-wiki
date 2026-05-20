"""LangGraph ingest pipeline: extract → chunk → process batches → update links."""

from __future__ import annotations

import asyncio
import json
import logging
from datetime import UTC, date, datetime
from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, StateGraph

from src.config import Settings, get_settings
from src.extract import chunk_text, count_tokens, extract_source
from src.llm import complete_structured
from src.merge import batch_collision_check, merge_page
from src.models import (
    Checkpoint,
    CollisionPair,
    GeneratedPage,
    IngestResult,
    WikiFrontmatter,
    WikiPage,
)
from src.search import BriefIndex
from src.wiki import (
    extract_wikilinks,
    get_page_by_title,
    get_page_lock,
    read_all_pages,
    read_page,
    title_to_path,
    write_page,
)

logger = logging.getLogger(__name__)


# ── Checkpoint helpers ────────────────────────────────────────────────────────


def _source_to_slug(source_path: str) -> str:
    return source_path.replace("/", "-").replace("\\", "-")


def _checkpoint_path(source_path: str) -> Path:
    settings = get_settings()
    return settings.checkpoint_dir / f"{_source_to_slug(source_path)}.json"


def _read_checkpoint(source_path: str) -> Checkpoint | None:
    path = _checkpoint_path(source_path)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return Checkpoint.model_validate(data)
    except Exception:
        logger.warning("corrupt checkpoint path=%s, ignoring", path)
        return None


def _write_checkpoint(cp: Checkpoint) -> None:
    path = _checkpoint_path(cp.source)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(cp.model_dump_json(indent=2), encoding="utf-8")


def _delete_checkpoint(source_path: str) -> None:
    path = _checkpoint_path(source_path)
    if path.exists():
        path.unlink()


def _source_modified(source_path: str, cp: Checkpoint) -> bool:
    src = Path(source_path)
    if not src.exists():
        return False
    source_mtime = datetime.fromtimestamp(src.stat().st_mtime, tz=UTC)
    created = datetime.fromisoformat(cp.created_at)
    return source_mtime > created


# ── State ────────────────────────────────────────────────────────────────────


class IngestState(TypedDict, total=False):
    source_path: str
    extracted_text: str
    source_title: str
    chunks: list[str]
    fresh: bool  # skip checkpoint, start from scratch
    written_paths: list[str]
    updated_pages: list[str]
    errors: list[str]


# ── Batch helpers ────────────────────────────────────────────────────────────


def _build_batch_messages(
    chunks: list[str],
    batch_start: int,
    batch_size: int,
    source_title: str,
    existing_briefs: dict[str, str],
    is_short: bool = False,
) -> list[dict[str, str]]:
    """Build LLM messages for a single batch of chunks.

    Message layout optimized for prompt caching:
    [system]  <- static (identical across all batches)
    [user]    <- dynamic content ordered by stability
    """
    from src.config import get_allowed_tags, get_ingest_mode, get_ingest_prompt

    batch = chunks[batch_start : batch_start + batch_size]
    combined = "\n\n---\n\n".join(batch)

    # System prompt: fully static for caching
    system_prompt = get_ingest_prompt()

    # User content: ordered by stability (stable prefix -> variable suffix)
    user_parts: list[str] = []

    # 1. Preferred tags (semi-static)
    allowed_tags = get_allowed_tags()
    if allowed_tags:
        user_parts.append("Preferred tags (use when applicable): " + ", ".join(allowed_tags))

    # 2. Ingest mode or short text (mutually exclusive)
    if is_short:
        user_parts.append(
            "This is a short source text. Only generate the source_summary. "
            "Mention concepts and entities using [[WikiLink]] syntax within the body "
            "--- do not create separate concept_pages or entity_pages."
        )
    else:
        ingest_mode = get_ingest_mode()
        if ingest_mode == "focused":
            user_parts.append(
                "IMPORTANT: Generate only 1-3 concept_pages and 1-3 entity_pages. "
                "Focus on the most important concepts and entities:\n"
                "- Core topic/thesis of the source (not tangential mentions)\n"
                "- Entities/concepts with standalone knowledge value "
                "(worth their own page, not just an example)\n"
                "- Knowledge not already covered by previously generated pages listed below. "
                "Quality over quantity."
            )

    # 3. Previously generated pages from this source (titles + briefs)
    if existing_briefs:
        pages_list = "\n".join(
            f'  - "{title}": {brief}' for title, brief in existing_briefs.items()
        )
        user_parts.append(
            f"Previously generated pages from this source:\n{pages_list}\n"
            "Link to them using [[Title]] syntax. Avoid duplicating their content."
        )

    # 5. Source text (most variable — always last)
    user_parts.append(
        f"Source: {source_title}\n\nCreate wiki pages from this source text:\n\n{combined}"
    )

    user_content = "\n\n".join(user_parts)

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]


def _write_new_page(
    gen_page: GeneratedPage,
    source_path: str,
    today: date,
    settings: Settings,
) -> str:
    """Write a new page to disk and return its path."""
    fm = WikiFrontmatter(
        title=gen_page.title,
        page_type=gen_page.page_type,
        sources=[source_path],
        tags=gen_page.tags,
        created=today,
        updated=today,
        confidence=gen_page.confidence,
        related=[title_to_path(t) for t in gen_page.related_titles],
        brief=gen_page.brief,
    )
    return write_page(fm, gen_page.body, settings.wiki_dir)


def _check_fuzzy_collision(
    brief_idx: BriefIndex,
    new_brief: str,
    wiki_dir: Path,
) -> WikiPage | None:
    """Check BM25 brief index for similar pages. Returns matched WikiPage or None."""
    if not new_brief:
        return None

    results = brief_idx.search(new_brief, top_k=1)
    if not results:
        return None

    path, score = results[0]
    if score < 1.0:
        return None

    try:
        return read_page(path, wiki_dir)
    except Exception:
        return None


# ── Node functions ───────────────────────────────────────────────────────────


async def extract_text_node(state: IngestState) -> IngestState:
    """Extract text from the source file or URL."""
    try:
        result = extract_source(state["source_path"])
        return {
            "extracted_text": result.content,
            "source_title": result.title,
        }
    except Exception as exc:
        logger.error("extraction failed path=%s", state["source_path"], exc_info=True)
        return {"errors": [f"extraction failed: {exc}"]}


async def chunk_source_node(state: IngestState) -> IngestState:
    """Chunk the extracted text into LLM-sized pieces."""
    text = state.get("extracted_text", "")
    if not text:
        return {"errors": state.get("errors", []) + ["no text to chunk"]}

    settings = get_settings()
    chunks = chunk_text(text, max_tokens=settings.max_chunk_tokens)
    logger.info("chunked source chunks=%d", len(chunks))
    return {"chunks": chunks}


async def process_batches_node(state: IngestState) -> IngestState:
    """Process chunks in batches with checkpoint-based resume and brief analysis."""
    chunks = state.get("chunks", [])
    if not chunks:
        return {"errors": state.get("errors", []) + ["no chunks to process"]}

    settings = get_settings()
    source_path = state["source_path"]
    source_title = state.get("source_title", source_path)
    batch_size = settings.batch_size
    total_batches = (len(chunks) + batch_size - 1) // batch_size
    fresh = state.get("fresh", False)

    # Build brief index from existing wiki pages
    brief_idx = BriefIndex()
    if settings.wiki_dir.exists():
        brief_idx.build(read_all_pages(settings.wiki_dir))

    # Load or create checkpoint
    cp = None if fresh else _read_checkpoint(source_path)
    if cp is not None and cp.total_chunks != len(chunks):
        logger.info(
            "chunk count changed old=%d new=%d, starting fresh",
            cp.total_chunks,
            len(chunks),
        )
        cp = None
    if cp is None or _source_modified(source_path, cp):
        if cp is not None:
            logger.info("source modified since checkpoint, starting fresh")
        cp = Checkpoint(
            source=source_path,
            source_title=source_title,
            total_chunks=len(chunks),
            batch_size=batch_size,
            created_at=datetime.now(UTC).isoformat(),
        )
        _write_checkpoint(cp)

    all_written: list[str] = []
    errors = list(state.get("errors", []))

    for batch_idx in range(total_batches):
        if batch_idx in cp.completed_batches:
            logger.info("skipping completed batch=%d", batch_idx)
            continue

        messages = _build_batch_messages(
            chunks=chunks,
            batch_start=batch_idx * batch_size,
            batch_size=batch_size,
            source_title=source_title,
            existing_briefs=cp.generated_briefs,
            is_short=count_tokens(
                "\n\n---\n\n".join(chunks[batch_idx * batch_size : (batch_idx + 1) * batch_size])
            )
            < 500,
        )

        try:
            result = await complete_structured(
                messages=messages,
                response_model=IngestResult,
                temperature=settings.ingest_temperature,
            )

            all_pages = [result.source_summary, *result.concept_pages, *result.entity_pages]

            # Intra-batch dedup: keep first occurrence per title
            seen_titles: set[str] = set()
            deduped: list[GeneratedPage] = []
            for p in all_pages:
                if p.title not in seen_titles:
                    seen_titles.add(p.title)
                    deduped.append(p)
            if len(deduped) < len(all_pages):
                logger.info(
                    "intra-batch dedup removed=%d duplicates",
                    len(all_pages) - len(deduped),
                )
            # 1a: filter empty titles after intra-batch dedup
            all_pages = [p for p in deduped if p.title.strip()]

            today = date.today()
            batch_titles: list[str] = []
            batch_briefs: dict[str, str] = {}
            # collect brief_idx.add() calls and batch them after the loop
            batch_brief_adds: list[tuple[str, str]] = []

            # Phase 1: Collect collision pairs and new pages
            collision_pairs: list[CollisionPair] = []
            collision_existing: dict[str, WikiPage] = {}  # new_title -> existing page
            collision_gen_pages: dict[str, GeneratedPage] = {}  # new_title -> gen page
            new_pages: list[GeneratedPage] = []

            for gen_page in all_pages:
                # Exact collision
                existing_page = get_page_by_title(gen_page.title, settings.wiki_dir)

                if existing_page is not None:
                    collision_pairs.append(
                        CollisionPair(
                            new_title=gen_page.title,
                            existing_title=existing_page.frontmatter.title,
                            existing_brief=existing_page.frontmatter.brief,
                            collision_type="exact",
                            new_brief=gen_page.brief,
                        )
                    )
                    collision_existing[gen_page.title] = existing_page
                    collision_gen_pages[gen_page.title] = gen_page

                else:
                    # Fuzzy collision
                    fuzzy_match = _check_fuzzy_collision(
                        brief_idx,
                        gen_page.brief,
                        settings.wiki_dir,
                    )
                    if fuzzy_match is not None:
                        collision_pairs.append(
                            CollisionPair(
                                new_title=gen_page.title,
                                existing_title=fuzzy_match.frontmatter.title,
                                existing_brief=fuzzy_match.frontmatter.brief,
                                collision_type="fuzzy",
                                new_brief=gen_page.brief,
                            )
                        )
                        collision_existing[gen_page.title] = fuzzy_match
                        collision_gen_pages[gen_page.title] = gen_page
                    else:
                        # No collision → new page
                        new_pages.append(gen_page)

            # Phase 2: Write new pages immediately
            for gen_page in new_pages:
                path = _write_new_page(gen_page, source_path, today, settings)
                all_written.append(path)
                batch_titles.append(gen_page.title)
                batch_briefs[gen_page.title] = gen_page.brief
                batch_brief_adds.append((path, gen_page.brief))

            # Phase 3: Batch collision decisions (1 LLM call)
            if collision_pairs:
                pair_types = {p.new_title: p.collision_type for p in collision_pairs}
                batch_decision = await batch_collision_check(collision_pairs)

                # Collect MERGE and SKIP tasks
                merge_tasks: list[tuple[CollisionDecision, GeneratedPage, WikiPage]] = []
                skip_fuzzy: list[tuple[CollisionDecision, GeneratedPage]] = []

                for decision in batch_decision.decisions:
                    gen_page = collision_gen_pages.get(decision.new_title)
                    existing_page = collision_existing.get(decision.new_title)
                    if gen_page is None or existing_page is None:
                        continue

                    collision_type = pair_types.get(decision.new_title, "exact")

                    if decision.action == "MERGE":
                        merge_tasks.append((decision, gen_page, existing_page))
                    elif collision_type == "fuzzy":
                        skip_fuzzy.append((decision, gen_page))
                    else:
                        logger.info(
                            "batch skip title=%s reason=%s",
                            gen_page.title,
                            decision.reason,
                        )

                # Execute merges in parallel with per-page locks
                if merge_tasks:

                    async def _merge_with_lock(
                        task: tuple[CollisionDecision, GeneratedPage, WikiPage],
                    ) -> tuple[WikiFrontmatter, str]:
                        _, gp, ex = task
                        page_path = title_to_path(ex.frontmatter.title)
                        async with get_page_lock(page_path):
                            return await merge_page(ex, gp, source_path)

                    merge_results = await asyncio.gather(
                        *[_merge_with_lock(t) for t in merge_tasks],
                        return_exceptions=True,
                    )

                    for task, result in zip(merge_tasks, merge_results):
                        decision, gen_page, _ = task
                        if isinstance(result, Exception):
                            errors.append(f"merge failed: {decision.new_title}: {result}")
                            continue
                        merged_fm, merged_body = result
                        path = write_page(merged_fm, merged_body, settings.wiki_dir)
                        batch_brief_adds.append((path, merged_fm.brief))
                        all_written.append(path)
                        batch_titles.append(gen_page.title)
                        batch_briefs[gen_page.title] = gen_page.brief

                # Handle fuzzy SKIPs (write as new pages)
                for _, gen_page in skip_fuzzy:
                    path = _write_new_page(gen_page, source_path, today, settings)
                    batch_brief_adds.append((path, gen_page.brief))
                    all_written.append(path)
                    batch_titles.append(gen_page.title)
                    batch_briefs[gen_page.title] = gen_page.brief

            # Phase 4: Add to BriefIndex after batch
            for add_path, add_brief in batch_brief_adds:
                brief_idx.add(add_path, add_brief)

            # Update checkpoint
            cp.completed_batches.append(batch_idx)
            cp.generated_titles.extend(batch_titles)
            cp.generated_briefs.update(batch_briefs)
            _write_checkpoint(cp)

            logger.info(
                "batch complete batch=%d/%d pages=%d",
                batch_idx + 1,
                total_batches,
                len(batch_titles),
            )

        except Exception as exc:
            logger.error("batch failed batch=%d/%d", batch_idx + 1, total_batches, exc_info=True)
            errors.append(f"batch {batch_idx} failed: {exc}")
            break

    # Delete checkpoint if fully complete
    if len(cp.completed_batches) == total_batches:
        _delete_checkpoint(source_path)

    result_state: IngestState = {"written_paths": all_written}
    if errors:
        result_state["errors"] = errors
    return result_state


async def update_links_node(state: IngestState) -> IngestState:
    """Scan written pages for [[wikilinks]] and update related fields."""
    settings = get_settings()
    written = state.get("written_paths", [])
    updated: list[str] = []

    for path in written:
        try:
            page = read_page(path, settings.wiki_dir)
            links = extract_wikilinks(page.body)

            for link_title in links:
                linked_page = get_page_by_title(link_title, settings.wiki_dir)
                if linked_page:
                    # Check if reverse link exists
                    reverse_path = title_to_path(page.frontmatter.title)
                    if reverse_path not in linked_page.frontmatter.related:
                        linked_page.frontmatter.related.append(reverse_path)
                        write_page(
                            linked_page.frontmatter,
                            linked_page.body,
                            settings.wiki_dir,
                        )
                        updated.append(linked_page.path)
        except Exception:
            logger.warning("failed to update links for path=%s", path, exc_info=True)

    logger.info("updated links pages=%d", len(updated))
    return {"updated_pages": updated}


# ── Graph ────────────────────────────────────────────────────────────────────


def _after_extract(state: IngestState) -> str:
    return END if state.get("errors") else "chunk_source"


def _after_chunk(state: IngestState) -> str:
    return END if state.get("errors") else "process_batches"


def _after_batches(state: IngestState) -> str:
    return END if state.get("errors") else "update_links"


def build_ingest_graph() -> StateGraph:
    """Build the LangGraph ingest pipeline."""
    graph = StateGraph(IngestState)

    graph.add_node("extract_text", extract_text_node)
    graph.add_node("chunk_source", chunk_source_node)
    graph.add_node("process_batches", process_batches_node)
    graph.add_node("update_links", update_links_node)

    graph.set_entry_point("extract_text")
    graph.add_conditional_edges("extract_text", _after_extract)
    graph.add_conditional_edges("chunk_source", _after_chunk)
    graph.add_conditional_edges("process_batches", _after_batches)
    graph.add_edge("update_links", END)

    return graph


async def run_ingest(source_path: str, *, fresh: bool = False) -> IngestState:
    """Run the full ingest pipeline on a source."""
    graph = build_ingest_graph()
    app = graph.compile()

    initial_state: IngestState = {
        "source_path": source_path,
        "fresh": fresh,
        "errors": [],
    }

    result = await app.ainvoke(initial_state)
    return result

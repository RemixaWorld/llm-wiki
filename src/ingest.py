"""LangGraph ingest pipeline: extract → chunk → process batches → update links."""

from __future__ import annotations

import json
import logging
from datetime import UTC, date, datetime, timezone
from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, StateGraph

from src.config import get_settings
from src.extract import chunk_text, extract_source
from src.llm import complete_structured
from src.models import (
    Checkpoint,
    IngestResult,
    WikiFrontmatter,
)
from src.wiki import (
    extract_wikilinks,
    get_page_by_title,
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
    existing_titles: list[str],
) -> list[dict[str, str]]:
    """Build LLM messages for a single batch of chunks.

    Includes existing page titles so the LLM can create cross-batch wikilinks.
    """
    from src.config import get_allowed_tags, get_ingest_prompt

    batch = chunks[batch_start : batch_start + batch_size]
    combined = "\n\n---\n\n".join(batch)

    system_prompt = get_ingest_prompt()
    allowed_tags = get_allowed_tags()
    if allowed_tags:
        system_prompt += "\n\nPreferred tags (use these when applicable): " + ", ".join(
            allowed_tags
        )

    user_content = (
        f"Source: {source_title}\n\n"
        f"Create wiki pages from this source text:\n\n{combined}"
    )
    if existing_titles:
        user_content += (
            f"\n\nThe following wiki pages already exist: {', '.join(existing_titles)}"
            "\nLink to them using [[Title]] syntax where relevant."
        )

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]


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
    """Process chunks in batches with checkpoint-based resume."""
    chunks = state.get("chunks", [])
    if not chunks:
        return {"errors": state.get("errors", []) + ["no chunks to process"]}

    settings = get_settings()
    source_path = state["source_path"]
    source_title = state.get("source_title", source_path)
    batch_size = settings.batch_size
    total_batches = (len(chunks) + batch_size - 1) // batch_size
    fresh = state.get("fresh", False)

    # Load or create checkpoint
    cp = None if fresh else _read_checkpoint(source_path)
    if cp is not None and cp.total_chunks != len(chunks):
        logger.info(
            "chunk count changed old=%d new=%d, starting fresh",
            cp.total_chunks, len(chunks),
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
            created_at=datetime.now(timezone.utc).isoformat(),
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
            existing_titles=cp.generated_titles,
        )

        try:
            result = await complete_structured(
                messages=messages,
                response_model=IngestResult,
                temperature=settings.ingest_temperature,
            )

            all_pages = [result.source_summary, *result.concept_pages, *result.entity_pages]

            # Write pages
            today = date.today()
            batch_titles: list[str] = []
            for gen_page in all_pages:
                fm = WikiFrontmatter(
                    title=gen_page.title,
                    page_type=gen_page.page_type,
                    sources=[source_path],
                    tags=gen_page.tags,
                    created=today,
                    updated=today,
                    confidence=gen_page.confidence,
                    related=[title_to_path(t) for t in gen_page.related_titles],
                )
                path = write_page(fm, gen_page.body, settings.wiki_dir)
                all_written.append(path)
                batch_titles.append(gen_page.title)

            # Update checkpoint (only after pages written — batch atomicity)
            cp.completed_batches.append(batch_idx)
            cp.generated_titles.extend(batch_titles)
            _write_checkpoint(cp)

            logger.info(
                "batch complete batch=%d/%d pages=%d",
                batch_idx + 1, total_batches, len(batch_titles),
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

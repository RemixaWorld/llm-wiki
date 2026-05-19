"""LangGraph ingest pipeline: extract → chunk → generate pages → write → update links."""

from __future__ import annotations

import json
import logging
from datetime import date, datetime
from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, StateGraph

from src.config import get_settings
from src.extract import chunk_text, extract_source
from src.llm import complete_structured
from src.models import (
    Checkpoint,
    GeneratedPage,
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
    source_mtime = datetime.fromtimestamp(src.stat().st_mtime, tz=datetime.UTC)
    created = datetime.fromisoformat(cp.created_at)
    return source_mtime > created


# ── State ────────────────────────────────────────────────────────────────────


class IngestState(TypedDict, total=False):
    source_path: str
    extracted_text: str
    source_title: str
    chunks: list[str]
    generated_pages: list[GeneratedPage]
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


async def generate_pages_node(state: IngestState) -> IngestState:
    """Call LLM to generate wiki pages from chunked source text."""
    from src.config import get_allowed_tags, get_ingest_prompt

    chunks = state.get("chunks", [])
    if not chunks:
        return {"errors": state.get("errors", []) + ["no chunks to process"]}

    settings = get_settings()
    source_path = state["source_path"]
    source_title = state.get("source_title", source_path)

    # Combine chunks for context (truncate if needed)
    combined = "\n\n---\n\n".join(chunks[:5])

    # Load prompt from schema.yaml; append tag vocabulary if available
    system_prompt = get_ingest_prompt()
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
                f"Source: {source_title}\n\nCreate wiki pages from this source text:\n\n{combined}"
            ),
        },
    ]

    try:
        result = await complete_structured(
            messages=messages,
            response_model=IngestResult,
            temperature=settings.ingest_temperature,
        )

        all_pages = [result.source_summary, *result.concept_pages, *result.entity_pages]

        # Set source reference on all pages
        for page in all_pages:
            if not page.related_titles:
                page.related_titles = []

        logger.info(
            "generated pages total=%d concepts=%d entities=%d",
            len(all_pages),
            len(result.concept_pages),
            len(result.entity_pages),
        )
        return {"generated_pages": all_pages}
    except Exception as exc:
        logger.error("page generation failed", exc_info=True)
        return {"errors": state.get("errors", []) + [f"generation failed: {exc}"]}


async def write_pages_node(state: IngestState) -> IngestState:
    """Write generated pages to disk as markdown."""
    pages = state.get("generated_pages", [])
    if not pages:
        return {"errors": state.get("errors", []) + ["no pages to write"]}

    settings = get_settings()
    source_path = state["source_path"]
    written: list[str] = []
    today = date.today()

    for gen_page in pages:
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
        written.append(path)

    logger.info("wrote pages count=%d", len(written))
    return {"written_paths": written}


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


def _should_continue(state: IngestState) -> str:
    """Check if pipeline should continue or stop on errors."""
    errors = state.get("errors", [])
    if errors:
        return END
    return "chunk_source"


def _should_generate(state: IngestState) -> str:
    errors = state.get("errors", [])
    if errors:
        return END
    return "generate_pages"


def _should_write(state: IngestState) -> str:
    errors = state.get("errors", [])
    if errors:
        return END
    return "write_pages"


def build_ingest_graph() -> StateGraph:
    """Build the LangGraph ingest pipeline."""
    graph = StateGraph(IngestState)

    graph.add_node("extract_text", extract_text_node)
    graph.add_node("chunk_source", chunk_source_node)
    graph.add_node("generate_pages", generate_pages_node)
    graph.add_node("write_pages", write_pages_node)
    graph.add_node("update_links", update_links_node)

    graph.set_entry_point("extract_text")
    graph.add_conditional_edges("extract_text", _should_continue)
    graph.add_conditional_edges("chunk_source", _should_generate)
    graph.add_conditional_edges("generate_pages", _should_write)
    graph.add_edge("write_pages", "update_links")
    graph.add_edge("update_links", END)

    return graph


async def run_ingest(source_path: str) -> IngestState:
    """Run the full ingest pipeline on a source."""
    graph = build_ingest_graph()
    app = graph.compile()

    initial_state: IngestState = {
        "source_path": source_path,
        "errors": [],
    }

    result = await app.ainvoke(initial_state)
    return result

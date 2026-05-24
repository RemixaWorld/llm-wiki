## Checkpoint-based Ingest Resume — Implementation Plan

**Goal:** Add batch-based checkpointing to the ingest pipeline so it can resume after interruption and process all chunks (not just the first 5).

**Architecture:** Replace the `generate_pages_node` + `write_pages_node` pair with a single `process_batches_node` that internally loops over batches of 5 chunks, checkpointing after each batch. Each batch = one LLM call + page writes + checkpoint update.

**Tech Stack:** Pydantic (Checkpoint model), stdlib `json` (checkpoint persistence), existing LangGraph pipeline.

---

### Task 1: Checkpoint Model + Config

**Files:**
- Modify: `src/models.py` (add `Checkpoint`)
- Modify: `src/config.py` (add `checkpoint_dir`, `batch_size`)

**Model definition:**

```python
# src/models.py — add after LintIssue

class Checkpoint(BaseModel):
    """Tracks ingest progress for resume after interruption."""
    source: str
    source_title: str
    total_chunks: int
    batch_size: int = 5
    completed_batches: list[int] = Field(default_factory=list)
    generated_titles: list[str] = Field(default_factory=list)
    created_at: str  # ISO datetime for staleness check
```

**Config additions:**

```python
# src/config.py — in Settings class
checkpoint_dir: Path = Path(".wiki-checkpoints")
batch_size: int = 5
```

---

### Task 2: Checkpoint File Helpers

**Files:**
- Modify: `src/ingest.py` (add helpers)
- Test: `tests/test_checkpoint.py` (new)

**Helpers to add in `src/ingest.py`:**

```python
import json
from datetime import datetime, timezone
from pathlib import Path

from src.models import Checkpoint


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
    source_mtime = datetime.fromtimestamp(src.stat().st_mtime, tz=timezone.utc)
    created = datetime.fromisoformat(cp.created_at)
    return source_mtime > created
```

**Tests to write first:**

- `test_source_to_slug` — verify path separator replacement
- `test_write_and_read_checkpoint` — round-trip through JSON file
- `test_delete_checkpoint` — file removed
- `test_read_corrupt_checkpoint_returns_none` — bad JSON handled gracefully
- `test_source_modified_true` — source newer than checkpoint
- `test_source_modified_false` — source older than checkpoint

---

### Task 3: Batch Prompt Builder

**Files:**
- Modify: `src/ingest.py` (add `_build_batch_messages`)
- Test: `tests/test_checkpoint.py` (extend)

```python
def _build_batch_messages(
    chunks: list[str],
    batch_start: int,
    batch_size: int,
    source_title: str,
    existing_titles: list[str],
) -> list[dict[str, str]]:
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
```

**Tests:**

- `test_build_batch_messages_no_existing_titles` — no "already exist" line
- `test_build_batch_messages_with_existing_titles` — "already exist" line present, includes titles
- `test_build_batch_messages_slicing` — with 12 chunks, batch_start=5, batch_size=5, gets chunks[5:10]

---

### Task 4: process_batches_node

**Files:**
- Modify: `src/ingest.py` (replace `generate_pages_node` + `write_pages_node`)
- Modify: `src/ingest.py` — update `IngestState` (remove `generated_pages`, add `fresh`)

**Updated state:**

```python
class IngestState(TypedDict, total=False):
    source_path: str
    extracted_text: str
    source_title: str
    chunks: list[str]
    fresh: bool  # NEW: skip checkpoint, start from scratch
    written_paths: list[str]
    updated_pages: list[str]
    errors: list[str]
```

`generated_pages` removed — pages are now generated and written atomically within each batch.

**New node:**

```python
async def process_batches_node(state: IngestState) -> IngestState:
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
    if cp is None or (cp is not None and _source_modified(source_path, cp)):
        if cp is not None and _source_modified(source_path, cp):
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
```

**Key invariants:**
- Checkpoint updated **only after** pages are written to disk (batch atomicity)
- `write_page` is idempotent — if process crashes between write and checkpoint update, re-running re-writes the same pages (harmless)
- `update_links` remains unchanged — it runs after all batches, is idempotent

**Tests:**

- `test_process_batches_single_batch` — 3 chunks (fits in 1 batch), all pages written, checkpoint deleted
- `test_process_batches_multi_batch` — 12 chunks, 3 batches, all pages written, checkpoint deleted
- `test_process_batches_resume` — create checkpoint with batch 0 completed, verify batch 0 skipped, batches 1+ processed
- `test_process_batches_llm_failure` — LLM fails on batch 1, checkpoint has only batch 0, written_paths has batch 0's pages

---

### Task 5: Update Graph Wiring

**Files:**
- Modify: `src/ingest.py` (graph builder, `run_ingest`)

Remove `generate_pages_node`, `write_pages_node`, `_should_generate`, `_should_write`. Add `process_batches_node`.

```python
def _after_extract(state: IngestState) -> str:
    return END if state.get("errors") else "chunk_source"


def _after_chunk(state: IngestState) -> str:
    return END if state.get("errors") else "process_batches"


def _after_batches(state: IngestState) -> str:
    return END if state.get("errors") else "update_links"


def build_ingest_graph() -> StateGraph:
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
    graph = build_ingest_graph()
    app = graph.compile()

    initial_state: IngestState = {
        "source_path": source_path,
        "fresh": fresh,
        "errors": [],
    }

    result = await app.ainvoke(initial_state)
    return result
```

---

### Task 6: CLI --fresh Flag

**Files:**
- Modify: `src/cli.py` (add `--fresh` to `ingest` and `ingest-all`)

```python
@main.command()
@click.argument("source")
@click.option("--url", is_flag=True, help="Treat SOURCE as a URL instead of file path.")
@click.option("--fresh", is_flag=True, help="Ignore checkpoint, start from scratch.")
def ingest(source: str, url: bool, fresh: bool) -> None:
    from src.ingest import run_ingest

    result = asyncio.run(run_ingest(source, fresh=fresh))
    # ... rest unchanged
```

---

### Task 7: Fix Existing Tests

**Files:**
- Modify: `tests/test_ingest.py`

Existing tests reference `generate_pages_node`, `write_pages_node`, and `run_ingest(source)` without `fresh`. Changes:

1. Remove `TestGeneratePagesNode` and `TestWritePagesNode` classes
2. Replace with `TestProcessBatchesNode` testing the new node
3. Update `run_ingest` calls — add `fresh=True` for tests that don't need checkpoint behavior
4. Remove old imports (`generate_pages_node`, `write_pages_node`), add new ones (`process_batches_node`)
5. Update `TestBuildIngestGraph` — verify new node names in graph

---

### Summary of Changed Files

| File                       | Action                                                                                                      |
| -------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `src/models.py`            | Add `Checkpoint` model                                                                                      |
| `src/config.py`            | Add `checkpoint_dir`, `batch_size` settings                                                                 |
| `src/ingest.py`            | Remove `generate_pages_node` + `write_pages_node`, add helpers + `process_batches_node`, update state/graph |
| `src/cli.py`               | Add `--fresh` flag to `ingest` command                                                                      |
| `tests/test_checkpoint.py` | New file — helpers + batch prompt tests                                                                     |
| `tests/test_ingest.py`     | Update for new node structure                                                                               |
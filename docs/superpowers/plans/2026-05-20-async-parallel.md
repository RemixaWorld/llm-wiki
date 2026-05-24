# Async Parallel LLM Calls — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add two-layer parallelism (intra-batch merge + inter-file ingest) with global LLM concurrency control.

**Architecture:** Global Semaphore in LLM layer caps concurrent API calls. Batch merge loop uses `asyncio.gather` for parallel merges. `ingest-all` dispatches multiple sources concurrently. Per-page Lock serializes merges on the same wiki page to prevent write conflicts.

**Tech Stack:** asyncio (Semaphore, Lock, gather), existing litellm/instructor stack.

---

### Task 1: Add `max_concurrent_llm` config field

**Files:**
- Modify: `src/config.py:37` (after `batch_size` field)
- Modify: `.env.example:19` (append)

- [ ] **Step 1: Add the config field**

In `src/config.py`, after the `batch_size` field (line 41), add:

```python
    # Concurrency
    max_concurrent_llm: int = Field(default=3, gt=0)
```

- [ ] **Step 2: Update `.env.example`**

Append after line 22:

```
# Concurrency
# WIKI_MAX_CONCURRENT_LLM=3
```

- [ ] **Step 3: Run existing tests**

Run: `uv run pytest tests/test_config.py -v`
Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add src/config.py .env.example
git commit -m "feat: add max_concurrent_llm config field"
```

---

### Task 2: Add global LLM semaphore

**Files:**
- Modify: `src/llm.py:1-115` (add semaphore, wrap API call)
- Test: `tests/test_llm.py` (add concurrency test)

- [ ] **Step 1: Write the failing test**

In `tests/test_llm.py`, add a new test class:

```python
class TestLLMSemaphore:
    @pytest.mark.asyncio
    async def test_semaphore_limits_concurrency(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Global semaphore caps concurrent LLM API calls."""
        monkeypatch.setenv("WIKI_MINIMAX_API_KEY", "")
        monkeypatch.setenv("WIKI_GROQ_API_KEY", "")
        monkeypatch.setenv("WIKI_GEMINI_API_KEY", "")
        monkeypatch.setenv("WIKI_MAX_CONCURRENT_LLM", "2")

        import src.config
        import src.llm

        src.config._settings = None
        src.llm._semaphore = None

        import asyncio

        peak = 0
        current = 0

        async def mock_create(**kwargs: object) -> SimpleOutput:
            nonlocal peak, current
            current += 1
            peak = max(peak, current)
            await asyncio.sleep(0.05)
            current -= 1
            return SimpleOutput(answer="ok", confidence=0.9)

        mock_client = AsyncMock()
        mock_client.chat.completions.create = mock_create

        with patch("src.llm.instructor.from_litellm", return_value=mock_client):
            results = await asyncio.gather(
                *[
                    complete_structured(
                        messages=[{"role": "user", "content": f"test {i}"}],
                        response_model=SimpleOutput,
                    )
                    for i in range(5)
                ],
            )

        assert len(results) == 5
        assert peak <= 2  # never exceeded max_concurrent_llm

        src.config._settings = None
        src.llm._semaphore = None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_llm.py::TestLLMSemaphore -v`
Expected: FAIL — `_semaphore` does not exist yet

- [ ] **Step 3: Implement the semaphore**

In `src/llm.py`, add the import and semaphore after the module-level declarations (after line 16):

```python
import asyncio
```

Add after line 19 (`litellm.suppress_debug_info = True`):

```python
_semaphore: asyncio.Semaphore | None = None


def get_llm_semaphore() -> asyncio.Semaphore:
    """Return cached semaphore capped at max_concurrent_llm."""
    global _semaphore
    if _semaphore is None:
        _semaphore = asyncio.Semaphore(get_settings().max_concurrent_llm)
    return _semaphore
```

Wrap the API call in `complete_structured` with the semaphore. Change lines 95-103 from:

```python
            result = await client.chat.completions.create(
                model=model,
                messages=messages,
                response_model=response_model,
                temperature=temperature,
                **kwargs,
            )
            logger.info("llm complete provider=%s model=%s", name, model)
            return result
```

to:

```python
            sem = get_llm_semaphore()
            async with sem:
                result = await client.chat.completions.create(
                    model=model,
                    messages=messages,
                    response_model=response_model,
                    temperature=temperature,
                    **kwargs,
                )
            logger.info("llm complete provider=%s model=%s", name, model)
            return result
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_llm.py -v`
Expected: ALL PASS

- [ ] **Step 5: Commit**

```bash
git add src/llm.py tests/test_llm.py
git commit -m "feat: add global LLM semaphore to cap concurrent API calls"
```

---

### Task 3: Add per-page lock registry to wiki.py

**Files:**
- Modify: `src/wiki.py:23` (after WIKILINK_RE)
- Test: `tests/test_wiki.py` (add lock test)

- [ ] **Step 1: Write the failing test**

In `tests/test_wiki.py`, add the import for `get_page_lock` and a new test class. Update the import block (line 11) to include `get_page_lock`:

```python
from src.wiki import (
    delete_page,
    extract_wikilinks,
    get_page_by_title,
    get_page_lock,
    list_pages,
    parse_frontmatter,
    read_all_pages,
    read_page,
    render_page,
    slugify,
    title_to_path,
    write_page,
)
```

Add test class at end of file:

```python
class TestPageLock:
    @pytest.mark.asyncio
    async def test_same_path_returns_same_lock(self) -> None:
        lock1 = get_page_lock("bert.md")
        lock2 = get_page_lock("bert.md")
        assert lock1 is lock2

    @pytest.mark.asyncio
    async def test_different_paths_return_different_locks(self) -> None:
        lock1 = get_page_lock("bert.md")
        lock2 = get_page_lock("gpt.md")
        assert lock1 is not lock2

    @pytest.mark.asyncio
    async def test_lock_serializes_access(self) -> None:
        import asyncio

        lock = get_page_lock("test-serialize.md")
        order: list[str] = []

        async def task(name: str):
            async with lock:
                order.append(f"{name}-start")
                await asyncio.sleep(0.05)
                order.append(f"{name}-end")

        await asyncio.gather(task("a"), task("b"))
        # a must finish before b starts (or vice versa)
        a_start = order.index("a-start")
        a_end = order.index("a-end")
        b_start = order.index("b-start")
        b_end = order.index("b-end")
        assert a_end < b_start or b_end < a_start
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_wiki.py::TestPageLock -v`
Expected: FAIL — `get_page_lock` not found

- [ ] **Step 3: Implement the lock registry**

In `src/wiki.py`, add the import at top (after line 6 `from pathlib import Path`):

```python
import asyncio
```

Add after line 23 (`WIKILINK_RE = ...`):

```python
# ── Per-page write locks ─────────────────────────────────────────────────────

_page_locks: dict[str, asyncio.Lock] = {}


def get_page_lock(page_path: str) -> asyncio.Lock:
    """Return an asyncio.Lock for a specific wiki page path."""
    if page_path not in _page_locks:
        _page_locks[page_path] = asyncio.Lock()
    return _page_locks[page_path]
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_wiki.py::TestPageLock -v`
Expected: ALL PASS

- [ ] **Step 5: Commit**

```bash
git add src/wiki.py tests/test_wiki.py
git commit -m "feat: add per-page asyncio.Lock registry for write conflict protection"
```

---

### Task 4: Parallelize batch merge loop with per-page locks

**Files:**
- Modify: `src/ingest.py:1-34` (add imports), `src/ingest.py:388-424` (rewrite Phase 3)
- Test: `tests/test_ingest.py` (add parallel merge test)

- [ ] **Step 1: Write the failing test**

In `tests/test_ingest.py`, add a new test class at the end of the file:

```python
class TestParallelMerge:
    @pytest.mark.asyncio
    async def test_multiple_merges_run_concurrently(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Two MERGE decisions execute in parallel via asyncio.gather."""
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        import src.config

        src.config._settings = None

        # Pre-create two existing pages
        from src.wiki import write_page

        for title, body in [("Flash Attention", "# Flash Attention\n\nBody FA."), ("BERT", "# BERT\n\nBody BERT.")]:
            write_page(
                WikiFrontmatter(
                    title=title,
                    page_type=PageType.CONCEPT,
                    sources=["old.pdf"],
                    tags=[],
                    created=date(2026, 1, 1),
                    updated=date(2026, 1, 1),
                    confidence=Confidence.HIGH,
                    brief=f"Existing {title} page.",
                ),
                body,
                wiki_dir,
            )

        # LLM generates both pages (exact collision)
        ingest_result = IngestResult(
            source_summary=GeneratedPage(
                title="Summary",
                page_type=PageType.SOURCE_SUMMARY,
                tags=[],
                confidence=Confidence.HIGH,
                body="Summary.",
                brief="Source summary.",
            ),
            concept_pages=[
                GeneratedPage(
                    title="Flash Attention",
                    page_type=PageType.CONCEPT,
                    tags=["attention"],
                    confidence=Confidence.HIGH,
                    body="# Flash Attention\n\nNew FA details.",
                    brief="Updated FA.",
                ),
            ],
            entity_pages=[
                GeneratedPage(
                    title="BERT",
                    page_type=PageType.ENTITY,
                    tags=["nlp"],
                    confidence=Confidence.HIGH,
                    body="# BERT\n\nNew BERT details.",
                    brief="Updated BERT.",
                ),
            ],
        )

        from src.models import EditOp, PatchedPage

        mock_batch_decision = BatchCollisionDecision(
            decisions=[
                CollisionDecision(new_title="Flash Attention", action="MERGE", reason="same"),
                CollisionDecision(new_title="BERT", action="MERGE", reason="same"),
            ]
        )
        mock_patched_fa = PatchedPage(
            edits=[EditOp(old_string="# Flash Attention\n\nBody FA.", new_string="# Flash Attention\n\nNew FA details.")],
            tags_to_add=[],
            confidence=Confidence.HIGH,
        )
        mock_patched_bert = PatchedPage(
            edits=[EditOp(old_string="# BERT\n\nBody BERT.", new_string="# BERT\n\nNew BERT details.")],
            tags_to_add=[],
            confidence=Confidence.HIGH,
        )

        import asyncio

        merge_call_times: list[tuple[str, float]] = []

        async def tracked_merge_llm(*args, **kwargs):
            import time
            model = kwargs.get("response_model", None)
            name = model.__name__ if model else "unknown"
            merge_call_times.append((name, time.monotonic()))

            if not hasattr(tracked_merge_llm, "call_idx"):
                tracked_merge_llm.call_idx = 0
            idx = tracked_merge_llm.call_idx
            tracked_merge_llm.call_idx += 1

            results = [mock_batch_decision, mock_patched_fa, mock_patched_bert,
                       BriefOutput(brief="FA brief."), BriefOutput(brief="BERT brief.")]
            if idx < len(results):
                return results[idx]
            return BriefOutput(brief="fallback")

        state = {
            "chunks": ["Text about FA and BERT."],
            "source_path": "test.txt",
            "source_title": "Test",
            "fresh": True,
        }

        with (
            patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm,
            patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_merge_llm,
        ):
            mock_llm.return_value = ingest_result
            mock_merge_llm.side_effect = tracked_merge_llm
            result = await process_batches_node(state)

        assert "errors" not in result or len(result.get("errors", [])) == 0
        assert len(result["written_paths"]) == 3  # summary + 2 merges

        src.config._settings = None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_ingest.py::TestParallelMerge::test_multiple_merges_run_concurrently -v`
Expected: May pass with current sequential code — this is a structural test verifying gather works. The real concurrency verification is in Task 2's semaphore test.

- [ ] **Step 3: Rewrite Phase 3 merge loop in ingest.py**

First, add `asyncio` and `get_page_lock` imports. In `src/ingest.py`, add at line 1 area, update the imports:

```python
import asyncio
```

Add `get_page_lock` to the import from `src.wiki` (line 26-33):

```python
from src.wiki import (
    extract_wikilinks,
    get_page_by_title,
    get_page_lock,
    read_all_pages,
    read_page,
    title_to_path,
    write_page,
)
```

Now replace Phase 3 (lines 388-424). Replace the entire block from `# Phase 3: Batch collision decisions` through the `else: # SKIP on exact` block with:

```python
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
```

- [ ] **Step 4: Run all ingest tests**

Run: `uv run pytest tests/test_ingest.py -v`
Expected: ALL PASS (including existing merge/collision tests)

- [ ] **Step 5: Commit**

```bash
git add src/ingest.py tests/test_ingest.py
git commit -m "feat: parallelize batch merge loop with asyncio.gather and per-page locks"
```

---

### Task 5: Concurrent ingest-all

**Files:**
- Modify: `src/cli.py:55-96` (rewrite `ingest_all`)

- [ ] **Step 1: Rewrite `ingest_all` to run concurrently**

Replace the entire `ingest_all` function (lines 58-96) in `src/cli.py` with:

```python
@main.command(name="ingest-all")
@click.option("--glob", "pattern", default="*", help="Glob pattern to match source files.")
@click.option("--fresh", is_flag=True, help="Ignore checkpoint, start from scratch.")
def ingest_all(pattern: str, fresh: bool) -> None:
    """Ingest all matching files from the sources directory."""

    import asyncio

    from src.config import get_settings
    from src.ingest import run_ingest

    settings = get_settings()
    sources = sorted(settings.sources_dir.glob(pattern))
    sources = [s for s in sources if s.is_file()]

    if not sources:
        click.secho(f"No files matching '{pattern}' in {settings.sources_dir}/", fg="yellow")
        return

    click.echo(f"Found {len(sources)} source(s) to ingest (concurrency={settings.max_concurrent_llm}).")

    async def _ingest_all_concurrent() -> list:
        semaphore = asyncio.Semaphore(settings.max_concurrent_llm)

        async def _ingest_one(src_path: Path):
            async with semaphore:
                click.echo(f"\nIngesting: {src_path.name}")
                return await run_ingest(str(src_path), fresh=fresh)

        return await asyncio.gather(
            *[_ingest_one(s) for s in sources],
            return_exceptions=True,
        )

    results = asyncio.run(_ingest_all_concurrent())

    total_pages = 0
    total_errors = 0

    for src_path, result in zip(sources, results):
        if isinstance(result, Exception):
            click.secho(f"  {src_path.name}: FAILED - {result}", fg="red")
            total_errors += 1
        else:
            written = result.get("written_paths", [])
            errors = result.get("errors", [])

            if errors:
                click.secho(f"  {src_path.name}: {len(errors)} error(s)", fg="red")
                for err in errors:
                    click.echo(f"    - {err}")
                total_errors += len(errors)

            if written:
                click.secho(f"  {src_path.name}: {len(written)} pages created", fg="green")
            total_pages += len(written)

    click.echo()
    click.secho(
        f"Done: {total_pages} pages created, {total_errors} errors",
        fg="green" if not total_errors else "yellow",
    )
```

- [ ] **Step 2: Run all tests**

Run: `uv run pytest -v`
Expected: ALL PASS

- [ ] **Step 3: Commit**

```bash
git add src/cli.py
git commit -m "feat: concurrent ingest-all with asyncio.gather and file-level semaphore"
```

---

### Self-Review

**1. Spec coverage:**
- Component 1 (Global LLM Semaphore) → Task 1 + Task 2
- Component 2 (Intra-Batch Merge Parallelism) → Task 4
- Component 3 (Per-Page Write Conflict Protection) → Task 3 + Task 4
- Component 4 (Inter-File Ingest Concurrency) → Task 5
- `.env.example` update → Task 1

**2. Placeholder scan:** No TBD/TODO. All code blocks are complete.

**3. Type consistency:**
- `get_page_lock(page_path: str) -> asyncio.Lock` — defined in wiki.py, called in ingest.py as `get_page_lock(page_path)` where `page_path = title_to_path(...)` returns `str`. Consistent.
- `get_llm_semaphore() -> asyncio.Semaphore` — defined in llm.py, used internally. Consistent.
- `merge_page(existing, new_page, source_path) -> tuple[WikiFrontmatter, str]` — unchanged, called via `_merge_with_lock`. Consistent.
- `max_concurrent_llm` — `int` in config, used by both semaphore sites. Consistent.
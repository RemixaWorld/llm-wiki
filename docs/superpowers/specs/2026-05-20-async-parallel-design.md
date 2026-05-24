# Async Parallel LLM Calls — Design Spec

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add two-layer parallelism (intra-batch merge + inter-file ingest) with global LLM concurrency control.

**Architecture:** Global Semaphore in LLM layer caps concurrent API calls. Batch merge loop uses `asyncio.gather` for parallel merges. `ingest-all` dispatches multiple sources concurrently. Per-page Lock serializes merges on the same wiki page to prevent write conflicts.

**Tech Stack:** asyncio (Semaphore, Lock, gather), existing litellm/instructor stack.

---

## Background

Current state: zero parallelism in the entire project. All `await` calls are sequential. Two bottlenecks identified:

1. **Intra-batch**: N collision merges run sequentially (2-5 LLM calls each, 10-50s each)
2. **Inter-file**: `ingest-all` processes sources one by one

---

## Component 1: Global LLM Semaphore

### config.py

Add field:

```python
max_concurrent_llm: int = 3  # max simultaneous LLM API calls
```

### llm.py

Add module-level semaphore:

```python
_semaphore: asyncio.Semaphore | None = None

def get_llm_semaphore() -> asyncio.Semaphore:
    global _semaphore
    if _semaphore is None:
        _semaphore = asyncio.Semaphore(get_settings().max_concurrent_llm)
    return _semaphore
```

Wrap the actual API call inside `complete_structured`:

```python
sem = get_llm_semaphore()
async with sem:
    response = await client.chat.completions.create(...)
```

This ensures total concurrent LLM calls never exceed `max_concurrent_llm`, regardless of which layer initiated them.

---

## Component 2: Intra-Batch Merge Parallelism

### ingest.py — Phase 3 merge loop

**Before:** sequential `for decision in decisions: await merge_page(...)`

**After:** collect MERGE decisions, gather concurrently:

```python
# Collect merge tasks
merge_tasks: list[tuple[CollisionDecision, GeneratedPage, WikiPage]] = []
for decision in batch_decision.decisions:
    if decision.action == "MERGE":
        merge_tasks.append((decision, gen_page, existing_page))

# Execute merges in parallel (LLM semaphore caps actual concurrency)
if merge_tasks:
    merge_results = await asyncio.gather(
        *[merge_page(ex, gp, source_path) for _, gp, ex in merge_tasks],
        return_exceptions=True,
    )

    # Process results — serialize writes
    for task, result in zip(merge_tasks, merge_results):
        decision, gen_page, existing_page = task
        if isinstance(result, Exception):
            errors.append(f"merge failed: {decision.new_title}: {result}")
            continue
        merged_fm, merged_body = result
        path = write_page(merged_fm, merged_body, settings.wiki_dir)
        batch_brief_adds.append((path, merged_fm.brief))
        all_written.append(path)
        batch_titles.append(gen_page.title)
        batch_briefs[gen_page.title] = gen_page.brief
```

`return_exceptions=True` prevents one failed merge from canceling others.

SKIP decisions (exact and fuzzy) remain unchanged — they don't involve LLM calls.

---

## Component 3: Per-Page Write Conflict Protection

### wiki.py

Add page-level lock registry:

```python
_page_locks: dict[str, asyncio.Lock] = {}

def get_page_lock(page_path: str) -> asyncio.Lock:
    if page_path not in _page_locks:
        _page_locks[page_path] = asyncio.Lock()
    return _page_locks
```

### ingest.py — merge invocation

Wrap `merge_page + write_page` with per-page lock:

```python
# For each MERGE decision:
page_path = title_to_path(existing_page.frontmatter.title)
async with get_page_lock(page_path):
    merged_fm, merged_body = await merge_page(existing_page, gen_page, source_path)
    path = write_page(merged_fm, merged_body, settings.wiki_dir)
```

**Behavior:**
- Different pages: locks don't contend, merges run fully parallel
- Same page: second merge waits for first to complete, then operates on the latest version
- Zero extra LLM calls — the second merge naturally reads the updated page after the first releases the lock

**Lock scope:** Only around merge+write, not around new-page writes (no conflict possible — new pages have unique paths).

---

## Component 4: Inter-File Ingest Concurrency

### cli.py — ingest_all

**Before:** `for src_path in sources: asyncio.run(run_ingest(...))`

**After:** single event loop with `asyncio.gather`:

```python
async def _ingest_all_concurrent(sources, fresh, max_concurrent_files):
    semaphore = asyncio.Semaphore(max_concurrent_files)

    async def _ingest_one(src_path):
        async with semaphore:
            return await run_ingest(str(src_path), fresh=fresh)

    results = await asyncio.gather(
        *[_ingest_one(s) for s in sources],
        return_exceptions=True,
    )
    return results

# In ingest_all:
results = asyncio.run(_ingest_all_concurrent(sources, fresh, settings.max_concurrent_llm))

total_pages = 0
total_errors = 0
for src_path, result in zip(sources, results):
    if isinstance(result, Exception):
        click.secho(f"  {src_path.name}: FAILED - {result}", fg="red")
        total_errors += 1
    else:
        written = result.get("written_paths", [])
        errors = result.get("errors", [])
        ...
```

**Concurrency limit:** Reuses `max_concurrent_llm` setting for file-level semaphore. This is conservative (3 files × 3 max concurrent LLM = at most 9 queued API calls, but global LLM semaphore caps actual concurrent calls at 3).

**Isolation:** Each `run_ingest` has its own BriefIndex and checkpoint — no shared mutable state between files except wiki_dir (protected by per-page locks from Component 3).

---

## Files Changed

| File | Change |
|------|--------|
| `src/config.py` | Add `max_concurrent_llm: int = 3` |
| `src/llm.py` | Add `get_llm_semaphore()`, wrap API call with semaphore |
| `src/wiki.py` | Add `get_page_lock()`, page-level lock registry |
| `src/ingest.py` | Parallel merge loop with `asyncio.gather`, per-page lock around merge+write |
| `src/cli.py` | Concurrent `ingest_all` with `asyncio.gather` + file semaphore |
| `tests/test_llm.py` | Test semaphore wraps API call |
| `tests/test_ingest.py` | Test parallel merge dispatch |
| `tests/test_wiki.py` | Test page lock behavior |
| `tests/test_cli.py` | Test concurrent ingest-all (if existing tests) |

---

## Not Changed

- `src/merge.py` — `merge_page` itself unchanged, parallelism handled by caller
- `src/query.py` — single LLM call, no parallelism opportunity
- Batch-level loop in `ingest.py` — intentionally sequential (brief accumulation dependency)
- `.env.example` — add `WIKI_MAX_CONCURRENT_LLM=3` with sensible default

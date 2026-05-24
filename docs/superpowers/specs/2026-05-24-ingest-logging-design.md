# Ingest Enhanced Logging Design

**Date:** 2026-05-24
**Scope:** Per-source timing, page operation decision statistics, page_type distribution

## Problem

The ingest pipeline has no timing instrumentation and no systematic logging of page operation decisions. The only operation-level log is for exact-collision SKIP. Users cannot see how long each source takes or understand the new/merge/skip breakdown.

## Design

### IngestStats model (`src/models.py`)

New Pydantic model to carry statistics through the pipeline:

```python
class IngestStats(BaseModel):
    duration_s: float = 0.0
    new: int = 0
    merge: int = 0
    skip: int = 0
    skip_fuzzy_new: int = 0
    page_types: dict[str, int] = {}
```

Four operation categories, matching existing code paths in `process_batches_node`:

| Category | Code Path | Meaning |
|----------|-----------|---------|
| `new` | No collision (line 413-414) | Page written as-is |
| `merge` | Exact or fuzzy collision + LLM MERGE (line 441-442) | Existing page updated |
| `skip` | Exact collision + LLM SKIP (line 445-450) | New page discarded |
| `skip_fuzzy_new` | Fuzzy collision + LLM SKIP, but still written (line 480-486) | LLM says "different concept", page kept |

`page_types` counts by `GeneratedPage.page_type` across all operations (e.g. `{"concept": 5, "entity": 2, "source_summary": 1}`).

### IngestState change (`src/ingest.py`)

Add one optional field:

```python
class IngestState(TypedDict, total=False):
    # ... existing fields ...
    stats: IngestStats
```

### Statistics collection in process_batches_node

At function start, create a local counter:

```python
from collections import Counter, defaultdict
op_counts: dict[str, Counter] = defaultdict(Counter)  # op -> page_type counts
```

At each decision point, increment:

- **new** (line ~414): `op_counts["new"][gen_page.page_type] += 1`
- **merge** (line ~441): `op_counts["merge"][gen_page.page_type] += 1`
- **skip exact** (line ~445): `op_counts["skip"][gen_page.page_type] += 1`
- **skip fuzzy → new** (line ~481): `op_counts["skip_fuzzy_new"][gen_page.page_type] += 1`

At function end, build `IngestStats` (without duration) and set it on the returned state:

```python
page_types: dict[str, int] = {}
for op_counter in op_counts.values():
    for pt, count in op_counter.items():
        page_types[pt] = page_types.get(pt, 0) + count

stats = IngestStats(
    new=sum(op_counts.get("new", Counter()).values()),
    merge=sum(op_counts.get("merge", Counter()).values()),
    skip=sum(op_counts.get("skip", Counter()).values()),
    skip_fuzzy_new=sum(op_counts.get("skip_fuzzy_new", Counter()).values()),
    page_types=page_types,
)
result_state["stats"] = stats
```

### Timing in run_ingest

Wrap the graph invocation with `time.perf_counter()`:

```python
import time

async def run_ingest(source_path: str, *, fresh: bool = False) -> IngestState:
    t0 = time.perf_counter()
    result = await app.ainvoke(initial_state)
    elapsed = time.perf_counter() - t0

    stats = result.get("stats") or IngestStats()
    stats.duration_s = round(elapsed, 2)

    logger.info(
        "ingest complete source=%s duration=%.2fs new=%d merge=%d skip=%d skip_fuzzy_new=%d page_types=%s",
        source_path, stats.duration_s,
        stats.new, stats.merge, stats.skip, stats.skip_fuzzy_new,
        stats.page_types,
    )
    result["stats"] = stats
    return result
```

Example output:
```
INFO  ingest complete source=paper.pdf duration=12.34s new=5 merge=2 skip=1 skip_fuzzy_new=0 page_types={'concept': 4, 'entity': 2, 'source_summary': 1}
```

### ingest-all summary log (`src/cli.py`)

After `asyncio.gather` completes, aggregate stats from all sources:

```python
total_duration = 0.0
total_new = total_merge = total_skip = total_skip_fuzzy_new = 0
total_page_types: dict[str, int] = {}
num_sources = 0

for result in results:
    stats = result.get("stats")
    if stats is None:
        continue
    num_sources += 1
    total_duration += stats.duration_s
    total_new += stats.new
    total_merge += stats.merge
    total_skip += stats.skip
    total_skip_fuzzy_new += stats.skip_fuzzy_new
    for pt, count in stats.page_types.items():
        total_page_types[pt] = total_page_types.get(pt, 0) + count

avg_duration = round(total_duration / num_sources, 2) if num_sources > 0 else 0

logger.info(
    "ingest-all complete sources=%d duration=%.2fs avg=%.2fs/source "
    "new=%d merge=%d skip=%d skip_fuzzy_new=%d page_types=%s",
    num_sources, total_duration, avg_duration,
    total_new, total_merge, total_skip, total_skip_fuzzy_new,
    total_page_types,
)
```

Example output:
```
INFO  ingest-all complete sources=5 duration=67.89s avg=13.58s/source new=18 merge=6 skip=3 skip_fuzzy_new=1 page_types={'concept': 14, 'entity': 8, 'source_summary': 5}
```

## Files Changed

| File | Change |
|------|--------|
| `src/models.py` | Add `IngestStats` model |
| `src/ingest.py` | Add `stats` to `IngestState`, collect counters in `process_batches_node`, add timing + summary log in `run_ingest` |
| `src/cli.py` | Add aggregate summary log in `ingest_all` |

## What This Does NOT Do

- No CLI table output (logging only)
- No structured data export or dashboard integration
- No per-batch or per-page logging (single summary line per source)
- No changes to checkpoint or merge logic

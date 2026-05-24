# Ingest Progress Display

## Problem

During `wiki ingest` and `wiki ingest-all`, there is no real-time progress feedback. The user sees nothing until the pipeline completes. For large files with many batches, this can mean minutes of silence while LLM calls run.

## Solution

Add a callback-based progress reporting layer to the ingest pipeline, with a rich-based CLI frontend that displays progress bars and a summary statistics table.

## Architecture

### Callback Protocol

A `ProgressCallback` protocol decouples ingest logic from UI:

```python
from typing import Protocol

class ProgressCallback(Protocol):
    def on_stage(self, stage: str) -> None:
        """Called when entering a new pipeline stage (extract/chunk/process/update_links)."""
        ...

    def on_batch_progress(self, current: int, total: int) -> None:
        """Called after each batch completes during process_batches."""
        ...

    def on_file_progress(self, filename: str, current: int, total: int) -> None:
        """Called before processing each file (for ingest-all)."""
        ...

    def on_summary(self, stats: IngestStats, duration_s: float, errors: list[str]) -> None:
        """Called with final statistics after ingest completes."""
        ...
```

- All methods are optional for callers (protocol pattern)
- `None` callback means no progress output — preserves current behavior
- Lives in `src/progress.py`

### Ingest Integration

**`IngestState` change:**

```python
class IngestState(TypedDict, total=False):
    # ... existing fields ...
    progress_callback: ProgressCallback | None
```

**`run_ingest` signature:**

```python
async def run_ingest(
    source_path: str,
    *,
    fresh: bool = False,
    progress_callback: ProgressCallback | None = None,
) -> IngestState:
```

**Node modifications:**

- `extract_text_node`: calls `on_stage("extract")`
- `chunk_source_node`: calls `on_stage("chunk")`
- `process_batches_node`: calls `on_stage("process")` and `on_batch_progress(batch_idx + 1, total_batches)` after each batch
- `update_links_node`: calls `on_stage("update_links")`
- `run_ingest`: calls `on_summary(stats, elapsed, errors)` before returning

Each node retrieves callback from state, guards against `None`.

### Rich CLI Frontend

**Single file `ingest`:**

- `rich.progress.Progress` with one task tracking pipeline stages
- During `process_batches` stage, the progress description updates to show `batch X/Y`
- On completion, prints a short summary line (pages created, duration, errors)

**`ingest-all`:**

- Outer progress bar: file-level (`file 3/12: attention.pdf`)
- Inner updates: batch progress shown in the file task description (`file 3/12: attention.pdf [batch 2/5]`)
- On completion, renders a `rich.table.Table` summary:

```
┌──────────────────────────┬─────────┬───────┬────────┬───────┬────────┬─────────┐
│ File                     │ Pages   │ New   │ Merge  │ Skip  │ Time   │ Status  │
├──────────────────────────┼─────────┼───────┼────────┼───────┼────────┼─────────┤
│ attention-is-all-you.pdf │ 8       │ 6     │ 2      │ 0     │ 12.3s  │ OK      │
│ bert.pdf                 │ 5       │ 5     │ 0      │ 0     │ 8.1s   │ OK      │
│ broken.pdf               │ 0       │ 0     │ 0      │ 0     │ 2.0s   │ ERROR   │
├──────────────────────────┼─────────┼───────┼────────┼───────┼────────┼─────────┤
│ Total                    │ 13      │ 11    │ 2      │ 0     │ 22.4s  │         │
└──────────────────────────┴─────────┴───────┴────────┴───────┴────────┴─────────┘
```

### File Changes

| File | Change |
|------|--------|
| `src/progress.py` | New file: `ProgressCallback` protocol + `RichProgress` implementation |
| `src/ingest.py` | Add `progress_callback` to state, node functions call callback |
| `src/cli.py` | Create `RichProgress`, wire into `run_ingest` calls, render summary table |
| `pyproject.toml` | Add `rich` dependency |
| `tests/test_progress.py` | New file: mock callback assertions |

### Dependency

- Add `rich>=13.0` to `pyproject.toml` dependencies
- `rich` is a pure-Python library (~2MB), widely used in CLI tools

## Testing

- **Ingest core tests**: pass `progress_callback=None` (default) — no change to existing tests
- **Callback tests**: use `unittest.mock.MagicMock` as callback, assert `on_batch_progress` called correct number of times with correct arguments
- **CLI tests**: excluded from coverage per project rules

## Scope

- No changes to query, lint, stats, or fetch commands
- No changes to LangGraph graph structure
- No changes to checkpoint logic
- Progress is informational only — does not affect pipeline behavior

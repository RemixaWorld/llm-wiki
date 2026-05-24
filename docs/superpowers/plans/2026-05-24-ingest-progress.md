# Ingest Progress Display Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add real-time progress display to the ingest pipeline using a callback protocol and rich CLI frontend.

**Architecture:** A `ProgressCallback` protocol decouples ingest logic from UI. Ingest nodes call optional callback methods at stage transitions and batch completions. The CLI layer provides a `RichIngestProgress` implementation using `rich.progress.Progress` for single-file ingest and `rich.table.Table` for ingest-all summary. No progress callback is passed to `run_ingest` during ingest-all (concurrent files would conflict), so the CLI tracks file-level progress directly.

**Tech Stack:** rich>=13.0, existing LangGraph pipeline, Click CLI

---

## File Structure

| File | Responsibility |
|------|---------------|
| `src/progress.py` (new) | `ProgressCallback` protocol + `RichIngestProgress` class + `build_ingest_summary_table` |
| `src/ingest.py` (modify) | Add `progress_callback` to `IngestState`, node functions call callback, `run_ingest` accepts optional callback |
| `src/cli.py` (modify) | Wire `RichIngestProgress` into `ingest` and `ingest-all` commands |
| `pyproject.toml` (modify) | Add `rich` dependency |
| `tests/test_progress.py` (new) | Mock callback assertions for ingest node integration |

---

### Task 1: Add rich dependency

**Files:**
- Modify: `pyproject.toml:15-31`

- [ ] **Step 1: Add rich to dependencies**

In `pyproject.toml`, add `rich` to the end of the `dependencies` list:

```toml
    "tiktoken>=0.9.0,<1.0",
    "rich>=13.0,<14.0",
```

- [ ] **Step 2: Install**

Run: `uv sync`
Expected: `rich` installed successfully

- [ ] **Step 3: Commit**

```bash
git add pyproject.toml uv.lock
git commit -m "chore: add rich dependency for progress display"
```

---

### Task 2: Create ProgressCallback protocol and failing tests

**Files:**
- Create: `src/progress.py`
- Create: `tests/test_progress.py`

- [ ] **Step 1: Create src/progress.py with the protocol**

```python
"""Progress callback protocol for ingest pipeline."""

from __future__ import annotations

from typing import Protocol

from src.models import IngestStats


class ProgressCallback(Protocol):
    """Protocol for ingest progress reporting."""

    def on_stage(self, stage: str) -> None:
        """Called when entering a new pipeline stage."""
        ...

    def on_batch_progress(self, current: int, total: int) -> None:
        """Called after each batch completes."""
        ...

    def on_file_progress(self, filename: str, current: int, total: int) -> None:
        """Called before processing each file (for ingest-all)."""
        ...

    def on_summary(self, stats: IngestStats, duration_s: float, errors: list[str]) -> None:
        """Called with final statistics after ingest completes."""
        ...
```

- [ ] **Step 2: Create tests/test_progress.py with failing tests**

```python
"""Tests for ingest progress callback integration."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.ingest import (
    chunk_source_node,
    extract_text_node,
    process_batches_node,
    run_ingest,
)
from src.models import Confidence, GeneratedPage, IngestResult, PageType


@pytest.fixture()
def sample_source(tmp_path: Path) -> Path:
    f = tmp_path / "sample.txt"
    f.write_text("Some text about transformers and attention.", encoding="utf-8")
    return f


@pytest.fixture()
def mock_ingest_result() -> IngestResult:
    return IngestResult(
        source_summary=GeneratedPage(
            title="Summary",
            page_type=PageType.SOURCE_SUMMARY,
            tags=["test"],
            confidence=Confidence.HIGH,
            body="Summary body.",
        ),
        concept_pages=[],
        entity_pages=[],
    )


class TestCallbackOnStage:
    @pytest.mark.asyncio
    async def test_extract_text_calls_on_stage(self, sample_source: Path) -> None:
        cb = MagicMock()
        state = {"source_path": str(sample_source), "progress_callback": cb}
        await extract_text_node(state)
        cb.on_stage.assert_called_once_with("extract")

    @pytest.mark.asyncio
    async def test_chunk_source_calls_on_stage(self) -> None:
        cb = MagicMock()
        state = {
            "extracted_text": "Some text.",
            "source_path": "test.txt",
            "progress_callback": cb,
        }
        await chunk_source_node(state)
        cb.on_stage.assert_called_once_with("chunk")

    @pytest.mark.asyncio
    async def test_process_batches_calls_on_stage(
        self, tmp_path: Path, mock_ingest_result: IngestResult, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        import src.config

        src.config._settings = None

        cb = MagicMock()
        state = {
            "chunks": ["Source text."],
            "source_path": "test.txt",
            "source_title": "Test",
            "fresh": True,
            "progress_callback": cb,
        }
        with patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = mock_ingest_result
            await process_batches_node(state)

        cb.on_stage.assert_any_call("process")
        src.config._settings = None


class TestCallbackOnBatchProgress:
    @pytest.mark.asyncio
    async def test_batch_progress_called_per_batch(
        self, tmp_path: Path, mock_ingest_result: IngestResult, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        monkeypatch.setenv("WIKI_BATCH_SIZE", "1")
        import src.config

        src.config._settings = None

        cb = MagicMock()
        state = {
            "chunks": ["chunk0", "chunk1", "chunk2"],
            "source_path": "test.txt",
            "source_title": "Test",
            "fresh": True,
            "progress_callback": cb,
        }
        with patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = mock_ingest_result
            await process_batches_node(state)

        assert cb.on_batch_progress.call_count == 3
        cb.on_batch_progress.assert_any_call(1, 3)
        cb.on_batch_progress.assert_any_call(2, 3)
        cb.on_batch_progress.assert_any_call(3, 3)
        src.config._settings = None


class TestCallbackOnSummary:
    @pytest.mark.asyncio
    async def test_run_ingest_calls_on_summary(
        self,
        sample_source: Path,
        mock_ingest_result: IngestResult,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        import src.config

        src.config._settings = None

        cb = MagicMock()
        with patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = mock_ingest_result
            result = await run_ingest(str(sample_source), progress_callback=cb)

        cb.on_summary.assert_called_once()
        call_args = cb.on_summary.call_args
        assert call_args[0][0] is result["stats"]  # IngestStats
        assert isinstance(call_args[0][1], float)  # duration_s
        assert isinstance(call_args[0][2], list)  # errors
        src.config._settings = None


class TestCallbackBackwardCompat:
    @pytest.mark.asyncio
    async def test_nodes_work_without_callback(
        self,
        sample_source: Path,
        mock_ingest_result: IngestResult,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        import src.config

        src.config._settings = None

        with patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = mock_ingest_result
            result = await run_ingest(str(sample_source))

        assert len(result.get("written_paths", [])) == 1
        assert result.get("errors", []) == []
        src.config._settings = None
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `uv run pytest tests/test_progress.py -v`
Expected: FAIL — `on_stage`, `on_batch_progress`, `on_summary` not called by ingest nodes

- [ ] **Step 4: Commit protocol and tests**

```bash
git add src/progress.py tests/test_progress.py
git commit -m "test: add ProgressCallback protocol and failing integration tests"
```

---

### Task 3: Integrate callback into ingest.py

**Files:**
- Modify: `src/ingest.py:102-112` (IngestState)
- Modify: `src/ingest.py:237-263` (extract_text_node)
- Modify: `src/ingest.py:266-275` (chunk_source_node)
- Modify: `src/ingest.py:278-539` (process_batches_node)
- Modify: `src/ingest.py:542-570` (update_links_node)
- Modify: `src/ingest.py:606-635` (run_ingest)

- [ ] **Step 1: Add import and IngestState field**

At the top of `src/ingest.py`, add to the imports:

```python
from src.progress import ProgressCallback
```

Add `progress_callback` to `IngestState`:

```python
class IngestState(TypedDict, total=False):
    source_path: str
    extracted_text: str
    source_title: str
    chunks: list[str]
    fresh: bool
    written_paths: list[str]
    updated_pages: list[str]
    errors: list[str]
    stats: IngestStats
    progress_callback: ProgressCallback | None
```

- [ ] **Step 2: Add callback to extract_text_node**

At the start of `extract_text_node`, after the docstring line, add:

```python
async def extract_text_node(state: IngestState) -> IngestState:
    """Extract text from the source file or URL."""
    cb = state.get("progress_callback")
    if cb is not None:
        cb.on_stage("extract")
    try:
```

- [ ] **Step 3: Add callback to chunk_source_node**

At the start of `chunk_source_node`, after the docstring line, add:

```python
async def chunk_source_node(state: IngestState) -> IngestState:
    """Chunk the extracted text into LLM-sized pieces."""
    cb = state.get("progress_callback")
    if cb is not None:
        cb.on_stage("chunk")
    text = state.get("extracted_text", "")
```

- [ ] **Step 4: Add callback to process_batches_node**

At the start of `process_batches_node`, after the docstring line, add:

```python
async def process_batches_node(state: IngestState) -> IngestState:
    """Process chunks in batches with checkpoint-based resume and brief analysis."""
    cb = state.get("progress_callback")
    if cb is not None:
        cb.on_stage("process")
    chunks = state.get("chunks", [])
```

After the successful batch completion log (the line `logger.info("batch complete batch=%d/%d pages=%d", ...)`) and before the closing of the `try` block, add:

```python
            logger.info(
                "batch complete batch=%d/%d pages=%d",
                batch_idx + 1,
                total_batches,
                len(batch_titles),
            )
            if cb is not None:
                cb.on_batch_progress(batch_idx + 1, total_batches)
```

- [ ] **Step 5: Add callback to update_links_node**

At the start of `update_links_node`, after the docstring line, add:

```python
async def update_links_node(state: IngestState) -> IngestState:
    """Scan written pages for [[wikilinks]] and update related fields."""
    cb = state.get("progress_callback")
    if cb is not None:
        cb.on_stage("update_links")
    settings = get_settings()
```

- [ ] **Step 6: Update run_ingest signature and add on_summary call**

Replace the `run_ingest` function:

```python
async def run_ingest(
    source_path: str,
    *,
    fresh: bool = False,
    progress_callback: ProgressCallback | None = None,
) -> IngestState:
    """Run the full ingest pipeline on a source."""
    graph = build_ingest_graph()
    app = graph.compile()

    initial_state: IngestState = {
        "source_path": source_path,
        "fresh": fresh,
        "errors": [],
        "progress_callback": progress_callback,
    }

    t0 = time.perf_counter()
    result = await app.ainvoke(initial_state)
    elapsed = time.perf_counter() - t0

    stats = result.get("stats") or IngestStats()
    stats.duration_s = round(elapsed, 2)

    logger.info(
        "ingest complete source=%s duration=%.2fs new=%d merge=%d skip=%d skip_fuzzy_new=%d page_types=%s",
        source_path,
        stats.duration_s,
        stats.new,
        stats.merge,
        stats.skip,
        stats.skip_fuzzy_new,
        stats.page_types,
    )
    result["stats"] = stats

    if progress_callback is not None:
        progress_callback.on_summary(stats, elapsed, result.get("errors", []))

    return result
```

- [ ] **Step 7: Run callback tests**

Run: `uv run pytest tests/test_progress.py -v`
Expected: ALL PASS

- [ ] **Step 8: Run full test suite to verify no regressions**

Run: `make test`
Expected: ALL PASS — existing tests unaffected (callback defaults to `None`)

- [ ] **Step 9: Commit**

```bash
git add src/ingest.py
git commit -m "feat(ingest): integrate progress callback into pipeline nodes"
```

---

### Task 4: Implement RichIngestProgress and summary table

**Files:**
- Modify: `src/progress.py`

- [ ] **Step 1: Add RichIngestProgress class and build_ingest_summary_table**

Replace `src/progress.py` entirely:

```python
"""Progress callback protocol and rich-based progress display for ingest pipeline."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table

if TYPE_CHECKING:
    from src.models import IngestStats


class ProgressCallback(Protocol):
    """Protocol for ingest progress reporting."""

    def on_stage(self, stage: str) -> None:
        """Called when entering a new pipeline stage."""
        ...

    def on_batch_progress(self, current: int, total: int) -> None:
        """Called after each batch completes."""
        ...

    def on_file_progress(self, filename: str, current: int, total: int) -> None:
        """Called before processing each file (for ingest-all)."""
        ...

    def on_summary(self, stats: IngestStats, duration_s: float, errors: list[str]) -> None:
        """Called with final statistics after ingest completes."""
        ...


_STAGE_LABELS: dict[str, str] = {
    "extract": "Extracting text",
    "chunk": "Chunking",
    "process": "Processing batches",
    "update_links": "Updating links",
}


class RichIngestProgress:
    """Rich-based progress display for the ingest pipeline.

    Args:
        show_stages: If True (single-file mode), show stage names and batch progress.
            If False (ingest-all mode), show only file-level progress.
    """

    def __init__(self, *, show_stages: bool = True) -> None:
        self._show_stages = show_stages
        self._progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=Console(stderr=True),
        )
        self._stage_task_id: int | None = None
        self._batch_task_id: int | None = None

    def __enter__(self) -> RichIngestProgress:
        self._progress.start()
        return self

    def __exit__(self, *args: object) -> None:
        self._progress.stop()

    def on_stage(self, stage: str) -> None:
        if not self._show_stages:
            return
        desc = _STAGE_LABELS.get(stage, stage)
        if self._stage_task_id is None:
            self._stage_task_id = self._progress.add_task(desc, total=None)
        else:
            self._progress.update(self._stage_task_id, description=desc, total=None)
        if stage != "process" and self._batch_task_id is not None:
            self._progress.remove_task(self._batch_task_id)
            self._batch_task_id = None

    def on_batch_progress(self, current: int, total: int) -> None:
        if not self._show_stages:
            return
        if self._batch_task_id is None:
            self._batch_task_id = self._progress.add_task(
                f"  batch {current}/{total}", total=total
            )
        else:
            self._progress.update(self._batch_task_id, completed=current)

    def on_file_progress(self, filename: str, current: int, total: int) -> None:
        if self._stage_task_id is None:
            self._stage_task_id = self._progress.add_task("Files", total=total)
        self._progress.update(
            self._stage_task_id,
            completed=current,
            description=f"[{current}/{total}] {filename}",
        )

    def on_summary(self, stats: IngestStats, duration_s: float, errors: list[str]) -> None:
        pass


def build_ingest_summary_table(
    filenames: list[str],
    results: list[object],
    durations: list[float],
) -> Table:
    """Build a rich Table summarizing ingest-all results.

    Args:
        filenames: Source file names.
        results: List of IngestState dicts or Exceptions (from asyncio.gather return_exceptions).
        durations: Per-file durations in seconds.
    """
    from src.models import IngestStats

    table = Table(title="Ingest Summary")
    table.add_column("File", style="cyan")
    table.add_column("Pages", justify="right")
    table.add_column("New", justify="right", style="green")
    table.add_column("Merge", justify="right", style="yellow")
    table.add_column("Skip", justify="right")
    table.add_column("Time", justify="right")
    table.add_column("Status", justify="right")

    total_pages = 0
    total_new = 0
    total_merge = 0
    total_skip = 0
    total_duration = 0.0

    for filename, result, duration in zip(filenames, results, durations, strict=True):
        if isinstance(result, Exception):
            table.add_row(
                filename, "0", "0", "0", "0", f"{duration:.1f}s", "[red]ERROR[/red]"
            )
            total_duration += duration
            continue

        r = result  # type: ignore[union-attr]
        stats: IngestStats | None = r.get("stats")  # type: ignore[union-attr]
        errors: list[str] = r.get("errors", [])  # type: ignore[union-attr]
        written: list[str] = r.get("written_paths", [])  # type: ignore[union-attr]
        pages = len(written)
        new = stats.new if stats else 0
        merge = stats.merge if stats else 0
        skip = (stats.skip if stats else 0) + (stats.skip_fuzzy_new if stats else 0)
        status = "[red]ERROR[/red]" if errors else "[green]OK[/green]"

        table.add_row(
            filename,
            str(pages),
            str(new),
            str(merge),
            str(skip),
            f"{duration:.1f}s",
            status,
        )
        total_pages += pages
        total_new += new
        total_merge += merge
        total_skip += skip
        total_duration += duration

    table.add_section()
    table.add_row(
        "[bold]Total[/bold]",
        f"[bold]{total_pages}[/bold]",
        f"[bold]{total_new}[/bold]",
        f"[bold]{total_merge}[/bold]",
        f"[bold]{total_skip}[/bold]",
        f"[bold]{total_duration:.1f}s[/bold]",
        "",
    )

    return table
```

- [ ] **Step 2: Run existing tests to verify no regressions**

Run: `uv run pytest tests/test_progress.py tests/test_ingest.py -v`
Expected: ALL PASS — protocol import still works, existing tests unaffected

- [ ] **Step 3: Commit**

```bash
git add src/progress.py
git commit -m "feat(progress): add RichIngestProgress and summary table builder"
```

---

### Task 5: Wire RichIngestProgress into CLI

**Files:**
- Modify: `src/cli.py:33-51` (ingest command)
- Modify: `src/cli.py:107-200` (ingest-all command)

- [ ] **Step 1: Replace single ingest command**

Replace the `ingest` command function in `cli.py` (lines 32-51):

```python
@main.command()
@click.argument("source")
@click.option("--fresh", is_flag=True, help="Ignore checkpoint, start from scratch.")
def ingest(source: str, fresh: bool) -> None:
    """Ingest a source file or URL into the wiki."""
    from src.ingest import run_ingest
    from src.progress import RichIngestProgress

    with RichIngestProgress() as progress:
        result = asyncio.run(run_ingest(source, fresh=fresh, progress_callback=progress))

    errors = result.get("errors", [])
    written = result.get("written_paths", [])
    stats = result.get("stats")

    if errors:
        click.secho(f"Errors: {len(errors)}", fg="red")
        for err in errors:
            click.echo(f"  - {err}")
        raise SystemExit(1)

    pages_count = len(written)
    duration = f"{stats.duration_s:.1f}s" if stats else "?"
    ops = []
    if stats:
        if stats.new:
            ops.append(f"new={stats.new}")
        if stats.merge:
            ops.append(f"merge={stats.merge}")
    ops_str = f" ({', '.join(ops)})" if ops else ""
    click.secho(f"Created {pages_count} pages in {duration}{ops_str}", fg="green")
```

- [ ] **Step 2: Replace ingest-all command**

Replace the `ingest_all` command function in `cli.py` (lines 107-200):

```python
@main.command(name="ingest-all")
@click.option("--glob", "pattern", default="*", help="Glob pattern to match source files.")
@click.option("--fresh", is_flag=True, help="Ignore checkpoint, start from scratch.")
def ingest_all(pattern: str, fresh: bool) -> None:
    """Ingest all matching files from the sources directory."""
    from pathlib import Path

    from rich.console import Console

    from src.ingest import run_ingest
    from src.progress import RichIngestProgress, build_ingest_summary_table

    settings = get_settings()
    sources = sorted(settings.sources_dir.glob(pattern))
    sources = [s for s in sources if s.is_file()]

    if not sources:
        click.secho(f"No files matching '{pattern}' in {settings.sources_dir}/", fg="yellow")
        return

    total = len(sources)
    completed_count = 0

    async def _ingest_all_concurrent() -> list:
        nonlocal completed_count
        semaphore = asyncio.Semaphore(settings.max_concurrent_llm)

        async def _ingest_one(src_path: Path):
            nonlocal completed_count
            async with semaphore:
                result = await run_ingest(str(src_path), fresh=fresh)
            completed_count += 1
            progress.on_file_progress(src_path.name, completed_count, total)
            return result

        return await asyncio.gather(
            *[_ingest_one(s) for s in sources],
            return_exceptions=True,
        )

    with RichIngestProgress(show_stages=False) as progress:
        results = asyncio.run(_ingest_all_concurrent())

    # Build and print summary table
    durations = []
    total_pages = 0
    total_errors = 0
    for result in results:
        if isinstance(result, Exception):
            durations.append(0.0)
            total_errors += 1
        else:
            stats = result.get("stats")
            durations.append(stats.duration_s if stats else 0.0)
            total_pages += len(result.get("written_paths", []))
            total_errors += len(result.get("errors", []))

    console = Console(stderr=True)
    table = build_ingest_summary_table([s.name for s in sources], results, durations)
    console.print(table)

    if total_errors:
        raise SystemExit(1)
```

- [ ] **Step 3: Run full test suite**

Run: `make test`
Expected: ALL PASS — CLI is excluded from coverage, ingest tests unaffected

- [ ] **Step 4: Run linter**

Run: `make lint`
Expected: No errors

- [ ] **Step 5: Commit**

```bash
git add src/cli.py
git commit -m "feat(cli): wire RichIngestProgress into ingest and ingest-all commands"
```

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

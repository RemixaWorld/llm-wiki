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

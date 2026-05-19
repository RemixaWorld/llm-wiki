"""Tests for checkpoint helpers and batch message builder."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import patch

import pytest

from src.ingest import (
    _build_batch_messages,
    _checkpoint_path,
    _delete_checkpoint,
    _read_checkpoint,
    _source_modified,
    _source_to_slug,
    _write_checkpoint,
)
from src.models import Checkpoint


class TestSourceToSlug:
    def test_forward_slashes(self):
        assert _source_to_slug("data/web/arxiv.org/00f556a3.md") == "data-web-arxiv.org-00f556a3.md"

    def test_backslashes(self):
        assert _source_to_slug("data\\web\\file.txt") == "data-web-file.txt"

    def test_no_separators(self):
        assert _source_to_slug("file.txt") == "file.txt"


class TestCheckpointRoundTrip:
    def test_write_and_read_checkpoint(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(tmp_path / "checkpoints"))
        import src.config
        src.config._settings = None

        cp = Checkpoint(
            source="data/test.txt",
            source_title="Test",
            total_chunks=10,
            batch_size=5,
            created_at=datetime.now(UTC).isoformat(),
        )
        _write_checkpoint(cp)

        loaded = _read_checkpoint("data/test.txt")
        assert loaded is not None
        assert loaded.source == "data/test.txt"
        assert loaded.total_chunks == 10

        src.config._settings = None

    def test_delete_checkpoint(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(tmp_path / "checkpoints"))
        import src.config
        src.config._settings = None

        cp = Checkpoint(
            source="data/test.txt",
            source_title="Test",
            total_chunks=10,
            created_at=datetime.now(UTC).isoformat(),
        )
        _write_checkpoint(cp)
        assert _read_checkpoint("data/test.txt") is not None

        _delete_checkpoint("data/test.txt")
        assert _read_checkpoint("data/test.txt") is None

        src.config._settings = None

    def test_read_corrupt_checkpoint_returns_none(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(tmp_path / "checkpoints"))
        import src.config
        src.config._settings = None

        cp_path = _checkpoint_path("data/test.txt")
        cp_path.parent.mkdir(parents=True, exist_ok=True)
        cp_path.write_text("{bad json", encoding="utf-8")

        assert _read_checkpoint("data/test.txt") is None

        src.config._settings = None

    def test_read_nonexistent_returns_none(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(tmp_path / "checkpoints"))
        import src.config
        src.config._settings = None

        assert _read_checkpoint("nonexistent.txt") is None

        src.config._settings = None


class TestSourceModified:
    def test_source_newer_than_checkpoint(self, tmp_path: Path):
        src = tmp_path / "source.txt"
        src.write_text("content", encoding="utf-8")

        old_time = (datetime.now(UTC) - timedelta(hours=1)).isoformat()
        cp = Checkpoint(
            source=str(src),
            source_title="Test",
            total_chunks=5,
            created_at=old_time,
        )
        assert _source_modified(str(src), cp) is True

    def test_source_older_than_checkpoint(self, tmp_path: Path):
        src = tmp_path / "source.txt"
        src.write_text("content", encoding="utf-8")

        # Set source mtime to 1 hour ago
        import os
        old_mtime = (datetime.now(UTC) - timedelta(hours=2)).timestamp()
        os.utime(src, (old_mtime, old_mtime))

        future_time = (datetime.now(UTC) + timedelta(hours=1)).isoformat()
        cp = Checkpoint(
            source=str(src),
            source_title="Test",
            total_chunks=5,
            created_at=future_time,
        )
        assert _source_modified(str(src), cp) is False

    def test_nonexistent_source_returns_false(self):
        cp = Checkpoint(
            source="/nonexistent/file.txt",
            source_title="Test",
            total_chunks=5,
            created_at=datetime.now(UTC).isoformat(),
        )
        assert _source_modified("/nonexistent/file.txt", cp) is False


class TestBuildBatchMessages:
    """Tests for _build_batch_messages helper."""

    def test_no_existing_titles(self):
        chunks = ["chunk1", "chunk2"]
        with patch("src.config.load_schema", return_value={}):
            messages = _build_batch_messages(chunks, 0, 5, "Test Source", [])
        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"
        assert "Test Source" in messages[1]["content"]
        assert "chunk1" in messages[1]["content"]
        assert "already exist" not in messages[1]["content"]

    def test_with_existing_titles(self):
        chunks = ["chunk1"]
        with patch("src.config.load_schema", return_value={}):
            messages = _build_batch_messages(chunks, 0, 5, "Test Source", ["BERT", "Transformer"])
        assert "already exist" in messages[1]["content"]
        assert "BERT" in messages[1]["content"]
        assert "Transformer" in messages[1]["content"]

    def test_slicing(self):
        chunks = [f"chunk{i}" for i in range(12)]
        with patch("src.config.load_schema", return_value={}):
            messages = _build_batch_messages(chunks, 5, 5, "Test Source", [])
        assert "chunk5" in messages[1]["content"]
        assert "chunk9" in messages[1]["content"]
        assert "chunk10" not in messages[1]["content"]

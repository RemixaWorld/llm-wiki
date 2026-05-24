from __future__ import annotations

from click.testing import CliRunner

from src.cli import main


def test_fetch_help():
    runner = CliRunner()
    result = runner.invoke(main, ["fetch", "--help"])
    assert result.exit_code == 0
    assert "urls-file" in result.output
    assert "retry-failed" in result.output

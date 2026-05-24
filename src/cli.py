"""Click CLI entry point: wiki ingest, query, lint, stats."""

from __future__ import annotations

import asyncio
import logging
import sys

import click

from src.config import get_settings

logger = logging.getLogger(__name__)


def _setup_logging() -> None:
    settings = get_settings()
    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
        stream=sys.stderr,
    )


@click.group()
def main() -> None:
    """LLM Wiki — Git-backed knowledge base maintained by LLM."""
    _setup_logging()


@main.command()
@click.argument("source")
@click.option("--fresh", is_flag=True, help="Ignore checkpoint, start from scratch.")
@click.option("--max-pages", default=None, type=int, help="Max concept/entity pages per type (default: 3).")
def ingest(source: str, fresh: bool, max_pages: int | None) -> None:
    """Ingest a source file or URL into the wiki."""
    import os

    from src.ingest import run_ingest
    from src.progress import RichIngestProgress

    if max_pages is not None:
        os.environ["WIKI_MAX_PAGES_PER_TYPE"] = str(max_pages)

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


@main.command()
@click.argument("urls", nargs=-1, required=True)
@click.option("--urls-file", default=None, help="File with URLs, one per line.")
@click.option("--retry-failed", is_flag=True, help="Re-fetch previously failed URLs.")
@click.option("--browser", is_flag=True, help="Enable Playwright browser fallback.")
@click.option("--concurrency", default=10, type=int, help="Max concurrent requests.")
def fetch(
    urls: tuple[str, ...],
    urls_file: str | None,
    retry_failed: bool,
    browser: bool,
    concurrency: int,
) -> None:
    """Fetch URL(s) and cache content to data/web/."""
    from src.fetcher import run_fetch

    settings = get_settings()
    web_dir = settings.sources_dir.parent / "data" / "web"

    results = asyncio.run(
        run_fetch(
            list(urls),
            web_dir,
            urls_file=urls_file,
            retry_failed=retry_failed,
            use_browser=browser,
            concurrency=concurrency,
        )
    )

    ok = sum(1 for r in results if r.status == "ok")
    failed = sum(1 for r in results if r.status != "ok")

    for r in results:
        if r.status == "ok":
            color = "green"
        elif r.status in ("duplicate", "low_quality"):
            color = "yellow"
        else:
            color = "red"
        click.secho(f"  [{r.status}] {r.url}", fg=color)
        if r.title and r.status == "ok":
            click.echo(f"    title: {r.title}")
        if r.error:
            click.echo(f"    error: {r.error}")

    click.echo()
    if failed:
        click.secho(f"Done: {ok} fetched, {failed} issues", fg="yellow")
    else:
        click.secho(f"Done: {ok} fetched, {failed} issues", fg="green")


@main.command(name="ingest-all")
@click.option("--glob", "pattern", default="*", help="Glob pattern to match source files.")
@click.option("--fresh", is_flag=True, help="Ignore checkpoint, start from scratch.")
@click.option("--max-pages", default=None, type=int, help="Max concept/entity pages per type (default: 3).")
def ingest_all(pattern: str, fresh: bool, max_pages: int | None) -> None:
    """Ingest all matching files from the sources directory."""
    import os
    from pathlib import Path

    from rich.console import Console

    from src.ingest import run_ingest
    from src.progress import RichIngestProgress, build_ingest_summary_table

    if max_pages is not None:
        os.environ["WIKI_MAX_PAGES_PER_TYPE"] = str(max_pages)

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


@main.command()
@click.argument("question")
def query(question: str) -> None:
    """Query the wiki and get a synthesized answer."""
    from src.query import run_query

    result = asyncio.run(run_query(question))
    errors = result.get("errors", [])

    if errors:
        click.secho(f"Errors: {len(errors)}", fg="red")
        for err in errors:
            click.echo(f"  - {err}")
        raise SystemExit(1)

    click.secho("Answer:", fg="green", bold=True)
    click.echo(result.get("answer", "No answer generated."))

    citations = result.get("citations", [])
    if citations:
        click.echo()
        click.secho("Citations:", fg="cyan")
        for c in citations:
            click.echo(f"  - {c}")

    follow_ups = result.get("follow_up_queries", [])
    if follow_ups:
        click.echo()
        click.secho("Follow-up questions:", fg="yellow")
        for q in follow_ups:
            click.echo(f"  - {q}")

    if result.get("persisted_page"):
        click.echo()
        click.secho(f"Persisted as: wiki/{result['persisted_page']}", fg="green")


@main.command()
def lint() -> None:
    """Check wiki health: orphans, broken links, missing fields."""
    from src.lint import lint_wiki

    issues = lint_wiki()

    if not issues:
        click.secho("No issues found.", fg="green")
        return

    severity_colors = {"error": "red", "warning": "yellow", "info": "cyan"}

    for issue in issues:
        color = severity_colors.get(issue.severity, "white")
        click.secho(f"[{issue.severity.upper()}] {issue.page}: {issue.message}", fg=color)
        if issue.suggestion:
            click.echo(f"  → {issue.suggestion}")

    errors = sum(1 for i in issues if i.severity == "error")
    warnings = sum(1 for i in issues if i.severity == "warning")
    click.echo()
    click.echo(f"Total: {len(issues)} issues ({errors} errors, {warnings} warnings)")

    if errors:
        raise SystemExit(1)


@main.command()
def stats() -> None:
    """Show wiki statistics."""
    from src.wiki import extract_wikilinks, list_pages, read_all_pages

    settings = get_settings()
    paths = list_pages(settings.wiki_dir)
    pages = read_all_pages(settings.wiki_dir)

    if not pages:
        click.echo("Wiki is empty. Run 'wiki ingest' to add content.")
        return

    # Count types
    type_counts: dict[str, int] = {}
    tag_counts: dict[str, int] = {}
    total_links = 0

    for page in pages:
        ptype = page.frontmatter.page_type.value
        type_counts[ptype] = type_counts.get(ptype, 0) + 1

        for tag in page.frontmatter.tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

        total_links += len(extract_wikilinks(page.body))

    click.secho("Wiki Statistics", fg="green", bold=True)
    click.echo(f"  Pages: {len(paths)}")
    click.echo(f"  Links: {total_links}")
    click.echo(f"  Link density: {total_links / len(pages):.1f} per page")

    click.echo()
    click.secho("Page types:", fg="cyan")
    for ptype, count in sorted(type_counts.items()):
        click.echo(f"  {ptype}: {count}")

    click.echo()
    click.secho("Top tags:", fg="cyan")
    for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        click.echo(f"  {tag}: {count}")

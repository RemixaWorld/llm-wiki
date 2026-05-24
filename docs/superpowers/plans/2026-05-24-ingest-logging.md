# Ingest Enhanced Logging Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add per-source timing and page operation decision statistics to the ingest pipeline, with a summary log line for single-source ingest and an aggregate summary for `ingest-all`.

**Architecture:** Add an `IngestStats` Pydantic model to carry operation counts and page_type distribution. Collect stats inside `process_batches_node` using local counters at each decision point. Add `stats` field to `IngestState`. Wrap `run_ingest` with `time.perf_counter()` for timing. Aggregate in `cli.py` for `ingest-all`.

**Tech Stack:** Python stdlib (`time.perf_counter`, `collections.Counter`, `collections.defaultdict`), Pydantic, existing test patterns (pytest + AsyncMock + monkeypatch).

---

### Task 1: Add IngestStats model to models.py

**Files:**
- Modify: `src/models.py` (after line 219, before EOF)
- Test: `tests/test_models.py`

- [ ] **Step 1: Write the failing test**

Add to `tests/test_models.py`:

```python
class TestIngestStats:
    def test_create_with_defaults(self) -> None:
        from src.models import IngestStats

        stats = IngestStats()
        assert stats.duration_s == 0.0
        assert stats.new == 0
        assert stats.merge == 0
        assert stats.skip == 0
        assert stats.skip_fuzzy_new == 0
        assert stats.page_types == {}

    def test_create_with_values(self) -> None:
        from src.models import IngestStats

        stats = IngestStats(
            duration_s=12.34,
            new=5,
            merge=2,
            skip=1,
            skip_fuzzy_new=0,
            page_types={"concept": 4, "entity": 2, "source_summary": 1},
        )
        assert stats.duration_s == 12.34
        assert stats.new == 5
        assert stats.merge == 2
        assert stats.skip == 1
        assert stats.page_types == {"concept": 4, "entity": 2, "source_summary": 1}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_models.py::TestIngestStats -v`
Expected: FAIL with `ImportError: cannot import name 'IngestStats' from 'src.models'`

- [ ] **Step 3: Write minimal implementation**

Add to `src/models.py` after the `ExtractedSource` class (after line 219):

```python
class IngestStats(BaseModel):
    """Statistics from a single source ingest run."""

    duration_s: float = 0.0
    new: int = 0
    merge: int = 0
    skip: int = 0
    skip_fuzzy_new: int = 0
    page_types: dict[str, int] = {}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_models.py::TestIngestStats -v`
Expected: PASS (2 tests)

- [ ] **Step 5: Commit**

```bash
git add src/models.py tests/test_models.py
git commit -m "feat(models): add IngestStats model for ingest pipeline statistics"
```

---

### Task 2: Add stats field to IngestState and collect counters in process_batches_node

**Files:**
- Modify: `src/ingest.py:99-108` (IngestState), `src/ingest.py:274-517` (process_batches_node)
- Test: `tests/test_ingest.py`

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_ingest.py`. Import `IngestStats` at the top of the file:

```python
from src.models import (
    # ... existing imports ...
    IngestStats,
)
```

Add new test class at the end of the file:

```python
class TestIngestStats:
    @pytest.mark.asyncio
    async def test_stats_new_pages(
        self, tmp_path: Path, mock_ingest_result: IngestResult, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """All pages are new (no collisions) → stats.new == 3, page_types counted."""
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        import src.config

        src.config._settings = None

        state = {
            "chunks": ["Source text about transformers and BERT."],
            "source_path": "test.txt",
            "source_title": "Test Source",
            "fresh": True,
        }

        with patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = mock_ingest_result
            result = await process_batches_node(state)

        stats = result.get("stats")
        assert stats is not None
        assert isinstance(stats, IngestStats)
        assert stats.new == 3  # source_summary + concept + entity
        assert stats.merge == 0
        assert stats.skip == 0
        assert stats.skip_fuzzy_new == 0
        assert stats.page_types.get("source_summary") == 1
        assert stats.page_types.get("concept") == 1
        assert stats.page_types.get("entity") == 1

        src.config._settings = None

    @pytest.mark.asyncio
    async def test_stats_with_merge(
        self, tmp_path: Path, mock_ingest_result: IngestResult, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """One exact collision → MERGE → stats.merge == 1, stats.new == 2."""
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        import src.config

        src.config._settings = None

        # Pre-create BERT page → exact collision
        existing_fm = WikiFrontmatter(
            title="BERT",
            page_type=PageType.ENTITY,
            sources=["old/source.pdf"],
            tags=["nlp"],
            created=date(2026, 1, 1),
            updated=date(2026, 1, 1),
            confidence=Confidence.HIGH,
            brief="Bidirectional encoder model.",
        )
        write_page(existing_fm, "# BERT\n\nOld content.", wiki_dir)

        from src.models import EditOp, PatchedPage

        mock_patched = PatchedPage(
            edits=[
                EditOp(
                    old_string="# BERT\n\nOld content.",
                    new_string="# BERT\n\nMerged content.",
                ),
            ],
            tags_to_add=["pre-training"],
            confidence=Confidence.HIGH,
        )

        state = {
            "chunks": ["Source text about BERT."],
            "source_path": "new-source.txt",
            "source_title": "New Source",
            "fresh": True,
        }

        with (
            patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm,
            patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_merge_llm,
        ):
            mock_llm.return_value = mock_ingest_result
            mock_merge_llm.side_effect = [
                BatchCollisionDecision(
                    decisions=[
                        CollisionDecision(
                            new_title="BERT", action="MERGE", reason="new info"
                        ),
                    ]
                ),
                mock_patched,
                BriefOutput(brief="BERT merged."),
            ]
            result = await process_batches_node(state)

        stats = result.get("stats")
        assert stats is not None
        assert stats.merge == 1
        assert stats.new == 2  # source_summary + concept (no entity, merged)
        assert stats.skip == 0
        assert stats.skip_fuzzy_new == 0
        assert stats.page_types.get("entity") == 1  # the merged entity

        src.config._settings = None

    @pytest.mark.asyncio
    async def test_stats_with_exact_skip(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Exact collision → LLM says SKIP → stats.skip == 1."""
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        import src.config

        src.config._settings = None

        # Pre-create BERT page
        write_page(
            WikiFrontmatter(
                title="BERT",
                page_type=PageType.ENTITY,
                sources=["old.pdf"],
                tags=["nlp"],
                created=date(2026, 1, 1),
                updated=date(2026, 1, 1),
                confidence=Confidence.HIGH,
                brief="Bidirectional encoder.",
            ),
            "# BERT\n\nBody.",
            wiki_dir,
        )

        ingest_result = IngestResult(
            source_summary=GeneratedPage(
                title="Summary",
                page_type=PageType.SOURCE_SUMMARY,
                tags=[],
                confidence=Confidence.HIGH,
                body="Summary.",
            ),
            concept_pages=[],
            entity_pages=[
                GeneratedPage(
                    title="BERT",
                    page_type=PageType.ENTITY,
                    tags=["nlp"],
                    confidence=Confidence.HIGH,
                    body="# BERT\n\nDetails.",
                    brief="BERT details.",
                ),
            ],
        )

        state = {
            "chunks": ["Text about BERT."],
            "source_path": "test.txt",
            "source_title": "Test",
            "fresh": True,
        }

        with (
            patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm,
            patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_merge_llm,
        ):
            mock_llm.return_value = ingest_result
            mock_merge_llm.return_value = BatchCollisionDecision(
                decisions=[
                    CollisionDecision(new_title="BERT", action="SKIP", reason="already covered"),
                ]
            )
            result = await process_batches_node(state)

        stats = result.get("stats")
        assert stats is not None
        assert stats.skip == 1
        assert stats.new == 1  # just the summary
        assert stats.merge == 0
        assert stats.page_types.get("entity") == 1  # the skipped entity

        src.config._settings = None

    @pytest.mark.asyncio
    async def test_stats_with_fuzzy_skip_new(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Fuzzy collision → LLM says SKIP → written as new → stats.skip_fuzzy_new == 1."""
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        import src.config

        src.config._settings = None

        # Create 3+ pages for BM25 IDF
        for title, brief in [
            ("Flash Attention", "IO-aware exact attention algorithm using tiling."),
            ("Reinforcement Learning", "Agent learns through environment interaction."),
            ("Gradient Descent", "Optimization algorithm for minimizing loss."),
        ]:
            write_page(
                WikiFrontmatter(
                    title=title,
                    page_type=PageType.CONCEPT,
                    sources=["old.pdf"],
                    tags=[],
                    created=date(2026, 1, 1),
                    updated=date(2026, 1, 1),
                    confidence=Confidence.HIGH,
                    brief=brief,
                ),
                f"# {title}\n\nBody.",
                wiki_dir,
            )

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
                    title="Memory-Efficient Attention",
                    page_type=PageType.CONCEPT,
                    tags=["attention"],
                    confidence=Confidence.HIGH,
                    body="# Memory-Efficient Attention\n\nDetails.",
                    brief="Attention optimization using memory tiling techniques.",
                ),
            ],
            entity_pages=[],
        )

        state = {
            "chunks": ["Text about memory-efficient attention."],
            "source_path": "test.txt",
            "source_title": "Test",
            "fresh": True,
        }

        with (
            patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm,
            patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_merge_llm,
        ):
            mock_llm.return_value = ingest_result
            mock_merge_llm.return_value = BatchCollisionDecision(
                decisions=[
                    CollisionDecision(
                        new_title="Memory-Efficient Attention",
                        action="SKIP",
                        reason="different topic",
                    ),
                ]
            )
            result = await process_batches_node(state)

        stats = result.get("stats")
        assert stats is not None
        assert stats.skip_fuzzy_new == 1
        assert stats.new == 1  # just the summary
        assert stats.merge == 0
        assert stats.skip == 0
        assert stats.page_types.get("concept") == 1  # the fuzzy-skipped concept

        src.config._settings = None

    @pytest.mark.asyncio
    async def test_stats_zero_on_empty_chunks(self) -> None:
        """No chunks → no stats field (early return with errors)."""
        state = {"chunks": [], "source_path": "test.txt"}
        result = await process_batches_node(state)
        assert "errors" in result
        # Early return path doesn't set stats
        assert "stats" not in result or result.get("stats") is None
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_ingest.py::TestIngestStats -v`
Expected: FAIL — `stats` not in result (process_batches_node doesn't return stats yet)

- [ ] **Step 3: Implement stats collection in ingest.py**

Three changes to `src/ingest.py`:

**Change 1:** Add import at top of file (around line 7):

```python
import time
from collections import Counter, defaultdict
```

**Change 2:** Add `stats` field to `IngestState` (line 99-108):

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
```

Also add `IngestStats` to the import from `src.models` (line 18-25):

```python
from src.models import (
    Checkpoint,
    CollisionPair,
    GeneratedPage,
    IngestResult,
    IngestStats,
    WikiFrontmatter,
    WikiPage,
)
```

**Change 3:** Add counter tracking inside `process_batches_node`. After the line `errors = list(state.get("errors", []))` (line 321), add:

```python
op_counts: dict[str, Counter] = defaultdict(Counter)
```

At each decision point, add a counter increment:

After `new_pages.append(gen_page)` (line 414):
```python
op_counts["new"][gen_page.page_type.value] += 1
```

After `merge_tasks.append(...)` (line 442):
```python
op_counts["merge"][gen_page.page_type.value] += 1
```

After the `logger.info("batch skip ...")` call (line 446-450), inside the `else` block:
```python
op_counts["skip"][gen_page.page_type.value] += 1
```

After `skip_fuzzy.append(...)` (line 444):
```python
op_counts["skip_fuzzy_new"][gen_page.page_type.value] += 1
```

**Change 4:** Build `IngestStats` at the end of `process_batches_node`. Before `result_state: IngestState = {"written_paths": all_written}` (line 514), add:

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
```

Change the `result_state` construction to include stats:

```python
result_state: IngestState = {"written_paths": all_written, "stats": stats}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_ingest.py::TestIngestStats -v`
Expected: PASS (5 tests)

- [ ] **Step 5: Run existing tests to verify no regressions**

Run: `uv run pytest tests/test_ingest.py -v`
Expected: All tests pass (existing + 5 new)

- [ ] **Step 6: Commit**

```bash
git add src/ingest.py tests/test_ingest.py
git commit -m "feat(ingest): collect page operation decision stats in process_batches_node"
```

---

### Task 3: Add timing and summary log to run_ingest

**Files:**
- Modify: `src/ingest.py:584-597` (run_ingest function)
- Test: `tests/test_ingest.py`

- [ ] **Step 1: Write the failing test**

Add to `tests/test_ingest.py`:

```python
class TestRunIngestStats:
    @pytest.mark.asyncio
    async def test_run_ingest_returns_stats_with_duration(
        self,
        sample_source: Path,
        mock_ingest_result: IngestResult,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """run_ingest populates stats.duration_s and logs the summary."""
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"

        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        import src.config

        src.config._settings = None

        with (
            patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm,
            patch("src.ingest.logger") as mock_logger,
        ):
            mock_llm.return_value = mock_ingest_result
            result = await run_ingest(str(sample_source))

        stats = result.get("stats")
        assert stats is not None
        assert stats.duration_s > 0
        assert stats.new == 3

        # Verify summary log was called
        mock_logger.info.assert_any_call(
            "ingest complete source=%s duration=%.2fs new=%d merge=%d skip=%d skip_fuzzy_new=%d page_types=%s",
            str(sample_source),
            stats.duration_s,
            stats.new,
            stats.merge,
            stats.skip,
            stats.skip_fuzzy_new,
            stats.page_types,
        )

        src.config._settings = None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_ingest.py::TestRunIngestStats -v`
Expected: FAIL — `stats` is None or no duration (run_ingest doesn't add timing yet)

- [ ] **Step 3: Implement timing in run_ingest**

Replace the `run_ingest` function (lines 584-597) in `src/ingest.py`:

```python
async def run_ingest(source_path: str, *, fresh: bool = False) -> IngestState:
    """Run the full ingest pipeline on a source."""
    graph = build_ingest_graph()
    app = graph.compile()

    initial_state: IngestState = {
        "source_path": source_path,
        "fresh": fresh,
        "errors": [],
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
    return result
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_ingest.py::TestRunIngestStats -v`
Expected: PASS

- [ ] **Step 5: Run full test suite for regressions**

Run: `uv run pytest tests/test_ingest.py -v`
Expected: All tests pass

- [ ] **Step 6: Commit**

```bash
git add src/ingest.py tests/test_ingest.py
git commit -m "feat(ingest): add per-source timing and summary log in run_ingest"
```

---

### Task 4: Add aggregate summary log to ingest-all CLI

**Files:**
- Modify: `src/cli.py:107-169` (ingest_all command)
- Test: `tests/test_ingest.py` (or new `tests/test_cli_ingest_all.py`)

- [ ] **Step 1: Write the failing test**

Add to `tests/test_ingest.py`:

```python
class TestIngestAllStats:
    @pytest.mark.asyncio
    async def test_ingest_all_aggregate_log(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """ingest-all logs aggregate stats after all sources complete."""
        from src.cli import main
        from click.testing import CliRunner

        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        sources_dir = tmp_path / "sources"
        sources_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"

        # Create two source files
        (sources_dir / "a.txt").write_text("Text about topic A.", encoding="utf-8")
        (sources_dir / "b.txt").write_text("Text about topic B.", encoding="utf-8")

        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_SOURCES_DIR", str(sources_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        import src.config

        src.config._settings = None

        mock_result_a = IngestResult(
            source_summary=GeneratedPage(
                title="Summary A",
                page_type=PageType.SOURCE_SUMMARY,
                tags=["a"],
                confidence=Confidence.HIGH,
                body="Summary A.",
            ),
            concept_pages=[],
            entity_pages=[],
        )
        mock_result_b = IngestResult(
            source_summary=GeneratedPage(
                title="Summary B",
                page_type=PageType.SOURCE_SUMMARY,
                tags=["b"],
                confidence=Confidence.HIGH,
                body="Summary B.",
            ),
            concept_pages=[],
            entity_pages=[],
        )

        call_count = 0

        async def mock_llm_fn(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return mock_result_a
            return mock_result_b

        with (
            patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm,
            patch("src.cli.logger") as mock_logger,
        ):
            mock_llm.side_effect = mock_llm_fn
            runner = CliRunner()
            result = runner.invoke(main, ["ingest-all"])

        assert result.exit_code == 0, result.output

        # Find the aggregate log call
        aggregate_calls = [
            c for c in mock_logger.info.call_args_list
            if len(c.args) > 0 and "ingest-all complete" in c.args[0]
        ]
        assert len(aggregate_calls) == 1

        call = aggregate_calls[0]
        # sources=2, duration > 0, avg > 0, new=2, merge=0, skip=0, skip_fuzzy_new=0
        assert call.args[1] == 2  # num_sources
        assert call.args[2] > 0  # total_duration
        assert call.args[3] > 0  # avg_duration
        assert call.args[4] == 2  # total_new
        assert call.args[5] == 0  # total_merge
        assert call.args[6] == 0  # total_skip
        assert call.args[7] == 0  # total_skip_fuzzy_new

        src.config._settings = None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_ingest.py::TestIngestAllStats::test_ingest_all_aggregate_log -v`
Expected: FAIL — no aggregate log call found

- [ ] **Step 3: Implement aggregate stats in cli.py**

In `src/cli.py`, add `IngestStats` import:

```python
from src.models import IngestStats
```

Then in the `ingest_all` function, after the results aggregation loop (after line 163 `total_pages += len(written)`), add stats aggregation and logging. Replace the existing results loop (lines 147-163) with:

```python
    total_pages = 0
    total_errors = 0
    total_duration = 0.0
    total_new = total_merge = total_skip = total_skip_fuzzy_new = 0
    total_page_types: dict[str, int] = {}
    num_sources_with_stats = 0

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

            # Aggregate stats
            stats = result.get("stats")
            if stats is not None:
                num_sources_with_stats += 1
                total_duration += stats.duration_s
                total_new += stats.new
                total_merge += stats.merge
                total_skip += stats.skip
                total_skip_fuzzy_new += stats.skip_fuzzy_new
                for pt, count in stats.page_types.items():
                    total_page_types[pt] = total_page_types.get(pt, 0) + count

    if num_sources_with_stats > 0:
        avg_duration = round(total_duration / num_sources_with_stats, 2)
        logger.info(
            "ingest-all complete sources=%d duration=%.2fs avg=%.2fs/source "
            "new=%d merge=%d skip=%d skip_fuzzy_new=%d page_types=%s",
            num_sources_with_stats,
            total_duration,
            avg_duration,
            total_new,
            total_merge,
            total_skip,
            total_skip_fuzzy_new,
            total_page_types,
        )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_ingest.py::TestIngestAllStats::test_ingest_all_aggregate_log -v`
Expected: PASS

- [ ] **Step 5: Run full test suite**

Run: `uv run pytest tests/test_ingest.py tests/test_models.py -v`
Expected: All tests pass

- [ ] **Step 6: Commit**

```bash
git add src/cli.py tests/test_ingest.py
git commit -m "feat(cli): add aggregate stats log to ingest-all command"
```

---

### Task 5: Lint and final verification

**Files:** All modified files

- [ ] **Step 1: Run linter**

Run: `uv run ruff check src/ tests/ && uv run ruff format --check src/ tests/`
Expected: No errors

- [ ] **Step 2: Fix any lint issues**

If ruff reports issues, fix them and re-run.

- [ ] **Step 3: Run full test suite**

Run: `uv run pytest -v`
Expected: All tests pass, coverage >= 70%

- [ ] **Step 4: Commit any lint fixes**

```bash
git add -A
git commit -m "style: ruff format and lint fixes for ingest logging"
```

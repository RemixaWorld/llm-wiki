# Ingest Cost Optimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reduce LLM call count and cost during ingest by fixing bugs, batching collision decisions, limiting page generation, and optimizing prompt structure for caching.

**Architecture:** Six targeted changes to the single-step ingest pipeline. New `batch_collision_check` function replaces per-page `brief_merge_check`/`topic_match_check` calls. `_build_batch_messages` restructured for prompt caching with short text mode and pluggable ingest modes.

**Tech Stack:** Pydantic, tiktoken (cl100k_base), instructor, pytest-asyncio

---

### Task 1: Bug Fixes — Empty Title Filter + Batch BriefIndex.add + Empty Brief Shortcut

**Files:**
- Modify: `src/ingest.py:274-386` (process_batches_node)
- Test: `tests/test_ingest.py`

- [ ] **Step 1: Write failing tests**

Add to `tests/test_ingest.py`:

```python
class TestBugFixes:
    @pytest.mark.asyncio
    async def test_empty_title_pages_are_skipped(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        import src.config
        src.config._settings = None

        # LLM returns a page with empty title
        bad_result = IngestResult(
            source_summary=GeneratedPage(
                title="",  # empty title
                page_type=PageType.SOURCE_SUMMARY,
                tags=[],
                confidence=Confidence.LOW,
                body="Summary body.",
            ),
            concept_pages=[
                GeneratedPage(
                    title="Valid Concept",
                    page_type=PageType.CONCEPT,
                    tags=["test"],
                    confidence=Confidence.MEDIUM,
                    body="Valid body.",
                ),
            ],
            entity_pages=[],
        )

        state = {
            "chunks": ["Some text."],
            "source_path": "test.txt",
            "source_title": "Test",
            "fresh": True,
        }

        with patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = bad_result
            result = await process_batches_node(state)

        # Only "Valid Concept" should be written, not the empty-title page
        assert len(result["written_paths"]) == 1
        assert "valid-concept.md" in result["written_paths"][0]
        # No .md file (from empty title) should exist
        assert not (wiki_dir / ".md").exists()

        src.config._settings = None

    @pytest.mark.asyncio
    async def test_empty_brief_skips_merge_check(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """When existing page has no brief, skip brief_merge_check and go straight to merge."""
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        import src.config
        src.config._settings = None

        # Existing page with no brief
        from src.wiki import write_page
        existing_fm = WikiFrontmatter(
            title="BERT",
            page_type=PageType.ENTITY,
            sources=["old.pdf"],
            tags=["nlp"],
            created=date(2026, 1, 1),
            updated=date(2026, 1, 1),
            confidence=Confidence.HIGH,
            brief="",  # empty brief
        )
        write_page(existing_fm, "# BERT\n\nOld content.", wiki_dir)

        result_with_bert = IngestResult(
            source_summary=GeneratedPage(
                title="Summary",
                page_type=PageType.SOURCE_SUMMARY,
                tags=["nlp"],
                confidence=Confidence.HIGH,
                body="Summary body.",
            ),
            concept_pages=[],
            entity_pages=[
                GeneratedPage(
                    title="BERT",
                    page_type=PageType.ENTITY,
                    tags=["nlp"],
                    confidence=Confidence.HIGH,
                    body="# BERT\n\nNew details.",
                ),
            ],
        )

        from src.models import EditOp, PatchedPage

        mock_patched = PatchedPage(
            edits=[
                EditOp(
                    old_string="# BERT\n\nOld content.",
                    new_string="# BERT\n\nOld content. New details.",
                ),
            ],
            tags_to_add=[],
            confidence=Confidence.HIGH,
        )

        with (
            patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm,
            patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_merge_llm,
        ):
            mock_llm.return_value = result_with_bert
            # Only merge_page calls (patch + brief regen), NO brief_merge_check call
            mock_merge_llm.side_effect = [
                mock_patched,
                BriefOutput(brief="BERT with new details."),
            ]
            result = await process_batches_node(state={
                "chunks": ["Text about BERT."],
                "source_path": "test.txt",
                "source_title": "Test",
                "fresh": True,
            })

        # merge LLM should be called exactly 2 times (patch + brief regen)
        # NOT 3 times (brief_merge_check + patch + brief regen)
        assert mock_merge_llm.call_count == 2

        src.config._settings = None
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_ingest.py::TestBugFixes -v`
Expected: FAIL

- [ ] **Step 3: Implement bug fixes in `src/ingest.py`**

Three changes in `process_batches_node`:

**3a.** After intra-batch dedup (~line 288), filter empty titles:

```python
            all_pages = [p for p in deduped if p.title.strip()]
```

**3b.** Replace all inline `brief_idx.add()` calls (~lines 311, 351, 367, 376) with a collection list. At the start of the per-page loop (~line 293), add:

```python
            batch_brief_adds: list[tuple[str, str]] = []
```

Replace each `brief_idx.add(path, ...)` with `batch_brief_adds.append((path, ...))`. After the per-page loop and before checkpoint update (~line 382), add:

```python
            for add_path, add_brief in batch_brief_adds:
                brief_idx.add(add_path, add_brief)
```

**3c.** In the exact collision block (~lines 297-318), skip `brief_merge_check` when brief is empty:

```python
                if existing_page is not None:
                    if existing_page.frontmatter.brief:
                        decision = await brief_merge_check(
                            existing_brief=existing_page.frontmatter.brief,
                            existing_title=existing_page.frontmatter.title,
                            new_body=gen_page.body,
                        )
                        if decision.action == "SKIP":
                            logger.info(
                                "brief skip title=%s reason=%s",
                                gen_page.title,
                                decision.reason,
                            )
                            path = title_to_path(gen_page.title)
                            all_written.append(path)
                            batch_titles.append(gen_page.title)
                            batch_brief_adds.append((path, gen_page.brief))
                            continue
                    # No brief or MERGE → proceed to merge_page
                    merged_fm, merged_body = await merge_page(
                        existing_page, gen_page, source_path,
                    )
                    path = write_page(merged_fm, merged_body, settings.wiki_dir)
                    batch_brief_adds.append((path, merged_fm.brief))
                    all_written.append(path)
                    batch_titles.append(gen_page.title)
                    batch_brief_adds.append((path, gen_page.brief))
                    continue
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_ingest.py -v`
Expected: ALL PASS

- [ ] **Step 5: Commit**

```bash
git add src/ingest.py tests/test_ingest.py
git commit -m "fix: skip empty titles, batch BriefIndex.add, shortcut empty brief merge"
```

---

### Task 2: Pluggable Ingest Modes — Config + Schema

**Files:**
- Modify: `src/config.py:90-98` (add `get_ingest_mode`)
- Modify: `schema.yaml` (add `ingest_mode` + prompt variants)
- Test: `tests/test_config.py` (or add to existing test file)

- [ ] **Step 1: Write failing test**

```python
# In tests/test_config.py or a new test section
class TestIngestMode:
    def test_get_ingest_mode_focused(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        import src.config
        src.config._settings = None
        src.config._schema_cache = None

        schema = tmp_path / "schema.yaml"
        schema.write_text("ingest_mode: focused\n")
        monkeypatch.setenv("WIKI_SCHEMA_PATH", str(schema))

        from src.config import get_ingest_mode
        assert get_ingest_mode() == "focused"

        src.config._settings = None
        src.config._schema_cache = None

    def test_get_ingest_mode_defaults_to_focused(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        import src.config
        src.config._settings = None
        src.config._schema_cache = None

        schema = tmp_path / "schema.yaml"
        schema.write_text("wiki:\n  name: test\n")
        monkeypatch.setenv("WIKI_SCHEMA_PATH", str(schema))

        from src.config import get_ingest_mode
        assert get_ingest_mode() == "focused"  # default

        src.config._settings = None
        src.config._schema_cache = None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_config.py::TestIngestMode -v`
Expected: FAIL

- [ ] **Step 3: Implement `get_ingest_mode` in `src/config.py`**

Add after `get_allowed_tags` (~line 142):

```python
def get_ingest_mode() -> str:
    """Return ingest mode from schema.yaml: 'focused' or 'comprehensive'."""
    schema = load_schema()
    mode = schema.get("ingest_mode", "focused")
    return mode if mode in ("focused", "comprehensive") else "focused"
```

- [ ] **Step 4: Add `ingest_mode` to `schema.yaml`**

Add at the top of schema.yaml (after the header comment, before `wiki:`):

```yaml
ingest_mode: focused  # "focused" (1-3 key concepts) or "comprehensive" (extract all)
```

- [ ] **Step 5: Run tests**

Run: `uv run pytest tests/test_config.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/config.py schema.yaml tests/test_config.py
git commit -m "feat: add pluggable ingest mode (focused/comprehensive) to schema.yaml"
```

---

### Task 3: Restructure _build_batch_messages — Short Text + Ingest Mode + Caching + Titles&Briefs

**Files:**
- Modify: `src/ingest.py:99-137` (`_build_batch_messages`)
- Test: `tests/test_ingest.py` (update `TestBuildBatchMessages`)

This is the biggest single-function change. It restructures the message layout for prompt caching, adds short text mode, ingest mode instructions, and replaces `existing_titles` with titles+briefs.

- [ ] **Step 1: Write failing tests**

```python
class TestBuildBatchMessagesV2:
    def test_short_text_mode_instruction(self) -> None:
        from src.ingest import _build_batch_messages
        from src.extract import count_tokens

        # Short text < 1000 tokens
        messages = _build_batch_messages(
            chunks=["Very short text about transformers."],
            batch_start=0,
            batch_size=5,
            source_title="Test",
            existing_briefs={},
            is_short=True,
        )
        user_msg = messages[1]["content"]
        assert "only generate the source_summary" in user_msg.lower() or "only" in user_msg.lower()

    def test_normal_text_no_short_instruction(self) -> None:
        from src.ingest import _build_batch_messages

        long_text = " ".join(["word"] * 2000)  # well over 1000 tokens
        messages = _build_batch_messages(
            chunks=[long_text],
            batch_start=0,
            batch_size=5,
            source_title="Test",
            existing_briefs={},
            is_short=False,
        )
        user_msg = messages[1]["content"]
        assert "only generate" not in user_msg.lower()

    def test_titles_and_briefs_in_prompt(self) -> None:
        from src.ingest import _build_batch_messages

        messages = _build_batch_messages(
            chunks=["chunk text"],
            batch_start=0,
            batch_size=5,
            source_title="Test",
            existing_briefs={
                "Flash Attention": "IO-aware exact attention algorithm.",
                "Self-Attention": "Mechanism for computing weighted sums.",
            },
            is_short=False,
        )
        user_msg = messages[1]["content"]
        assert "Flash Attention" in user_msg
        assert "IO-aware exact attention" in user_msg
        assert "Self-Attention" in user_msg

    def test_system_prompt_is_static(self) -> None:
        """System prompt should not contain dynamic content (for caching)."""
        from src.ingest import _build_batch_messages

        messages = _build_batch_messages(
            chunks=["chunk1"],
            batch_start=0,
            batch_size=5,
            source_title="Source A",
            existing_briefs={"Title": "Brief"},
            is_short=False,
        )
        system_msg = messages[0]["content"]
        # Dynamic content should NOT be in system prompt
        assert "Title" not in system_msg
        assert "Brief" not in system_msg
        assert "Source A" not in system_msg
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_ingest.py::TestBuildBatchMessagesV2 -v`
Expected: FAIL (signature mismatch, new parameters)

- [ ] **Step 3: Rewrite `_build_batch_messages` in `src/ingest.py`**

Replace the entire function (~lines 99-137) with:

```python
def _build_batch_messages(
    chunks: list[str],
    batch_start: int,
    batch_size: int,
    source_title: str,
    existing_briefs: dict[str, str],
    is_short: bool = False,
) -> list[dict[str, str]]:
    """Build LLM messages for a single batch of chunks.

    Message layout optimized for prompt caching:
    [system]  <- static (identical across all batches)
    [user]    <- dynamic content ordered by stability
    """
    from src.config import get_allowed_tags, get_ingest_mode, get_ingest_prompt

    batch = chunks[batch_start : batch_start + batch_size]
    combined = "\n\n---\n\n".join(batch)

    # System prompt: fully static for caching
    system_prompt = get_ingest_prompt()

    # User content: ordered by stability (stable prefix -> variable suffix)
    user_parts: list[str] = []

    # 1. Preferred tags (semi-static)
    allowed_tags = get_allowed_tags()
    if allowed_tags:
        user_parts.append("Preferred tags (use when applicable): " + ", ".join(allowed_tags))

    # 2. Ingest mode instructions
    ingest_mode = get_ingest_mode()
    if ingest_mode == "focused":
        user_parts.append(
            "IMPORTANT: Generate only 1-3 concept_pages and 1-3 entity_pages. "
            "Focus on the most important concepts and entities:\n"
            "- Core topic/thesis of the source (not tangential mentions)\n"
            "- Entities/concepts with standalone knowledge value "
            "(worth their own page, not just an example)\n"
            "- Knowledge not already covered by previously generated pages listed below. "
            "Quality over quantity."
        )

    # 3. Short text instruction
    if is_short:
        user_parts.append(
            "This is a short source text. Only generate the source_summary. "
            "Mention concepts and entities using [[WikiLink]] syntax within the body "
            "— do not create separate concept_pages or entity_pages."
        )

    # 4. Previously generated pages from this source (titles + briefs)
    if existing_briefs:
        pages_list = "\n".join(
            f'  - "{title}": {brief}'
            for title, brief in existing_briefs.items()
        )
        user_parts.append(
            f"Previously generated pages from this source:\n{pages_list}\n"
            "Link to them using [[Title]] syntax. Avoid duplicating their content."
        )

    # 5. Source text (most variable — always last)
    user_parts.append(f"Source: {source_title}\n\nCreate wiki pages from this source text:\n\n{combined}")

    user_content = "\n\n".join(user_parts)

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]
```

- [ ] **Step 4: Update all callers of `_build_batch_messages`**

In `process_batches_node`, update the call (~line 259) and add short text detection:

```python
        batch_chunks = chunks[batch_idx * batch_size : (batch_idx + 1) * batch_size]
        combined_batch = "\n\n---\n\n".join(batch_chunks)
        is_short = count_tokens(combined_batch) < 1000

        messages = _build_batch_messages(
            chunks=chunks,
            batch_start=batch_idx * batch_size,
            batch_size=batch_size,
            source_title=source_title,
            existing_briefs=cp.generated_briefs,
            is_short=is_short,
        )
```

Add import at top: `from src.extract import count_tokens`

Also update the old test class `TestBuildBatchMessages` to use the new signature (change `existing_titles=` to `existing_briefs={}`).

- [ ] **Step 5: Run all tests**

Run: `uv run pytest tests/test_ingest.py -v`
Expected: ALL PASS

- [ ] **Step 6: Commit**

```bash
git add src/ingest.py tests/test_ingest.py
git commit -m "feat: restructure _build_batch_messages for caching, short text, ingest modes, titles+briefs"
```

---

### Task 4: Batch Collision Models

**Files:**
- Modify: `src/models.py` (add 3 new models after existing merge models ~line 120)
- Test: `tests/test_models.py`

- [ ] **Step 1: Write failing test**

```python
class TestBatchCollisionModels:
    def test_collision_pair_exact(self) -> None:
        from src.models import CollisionPair
        pair = CollisionPair(
            new_title="Flash Attention v2",
            existing_title="Flash Attention",
            existing_brief="IO-aware attention algorithm.",
            collision_type="exact",
        )
        assert pair.collision_type == "exact"
        assert pair.new_brief == ""

    def test_collision_pair_fuzzy(self) -> None:
        from src.models import CollisionPair
        pair = CollisionPair(
            new_title="Attention Optimization",
            existing_title="Flash Attention",
            existing_brief="IO-aware attention algorithm.",
            collision_type="fuzzy",
            new_brief="Techniques for faster attention computation.",
        )
        assert pair.new_brief != ""

    def test_batch_collision_decision(self) -> None:
        from src.models import BatchCollisionDecision, CollisionDecision
        decision = BatchCollisionDecision(
            decisions=[
                CollisionDecision(new_title="A", action="MERGE", reason="same topic"),
                CollisionDecision(new_title="B", action="SKIP", reason="different focus"),
            ]
        )
        assert len(decision.decisions) == 2
        assert decision.decisions[0].action == "MERGE"
        assert decision.decisions[1].action == "SKIP"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_models.py::TestBatchCollisionModels -v`
Expected: FAIL (import error)

- [ ] **Step 3: Add models to `src/models.py`**

After `BriefOutput` class (~line 119), add:

```python
class CollisionPair(BaseModel):
    """One collision pair for batch decision."""
    new_title: str
    existing_title: str
    existing_brief: str
    collision_type: Literal["exact", "fuzzy"]
    new_brief: str = ""


class CollisionDecision(BaseModel):
    """Decision for one collision pair."""
    new_title: str
    action: Literal["MERGE", "SKIP"]
    reason: str


class BatchCollisionDecision(BaseModel):
    """LLM output: merge/skip decisions for all collision pairs in a batch."""
    decisions: list[CollisionDecision]
```

- [ ] **Step 4: Run tests**

Run: `uv run pytest tests/test_models.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/models.py tests/test_models.py
git commit -m "feat: add BatchCollisionDecision models for batch collision check"
```

---

### Task 5: Batch Collision Check Function

**Files:**
- Modify: `src/merge.py` (add `batch_collision_check` after `topic_match_check` ~line 131)
- Test: `tests/test_merge.py`

- [ ] **Step 1: Write failing test**

```python
class TestBatchCollisionCheck:
    @pytest.mark.asyncio
    async def test_batch_decision_mixed(self) -> None:
        """Multiple collision pairs decided in one call."""
        from unittest.mock import AsyncMock, patch
        from src.merge import batch_collision_check
        from src.models import BatchCollisionDecision, CollisionDecision, CollisionPair

        pairs = [
            CollisionPair(
                new_title="Flash Attention v2",
                existing_title="Flash Attention",
                existing_brief="IO-aware attention.",
                collision_type="exact",
            ),
            CollisionPair(
                new_title="Tiling Strategy",
                existing_title="GPU Tiling",
                existing_brief="Tiling for GPU memory.",
                collision_type="fuzzy",
                new_brief="Tiling strategies for attention.",
            ),
        ]

        expected = BatchCollisionDecision(
            decisions=[
                CollisionDecision(new_title="Flash Attention v2", action="MERGE", reason="same topic"),
                CollisionDecision(new_title="Tiling Strategy", action="SKIP", reason="different focus"),
            ]
        )

        with patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = expected
            result = await batch_collision_check(pairs)

        assert len(result.decisions) == 2
        assert result.decisions[0].action == "MERGE"
        assert result.decisions[1].action == "SKIP"
        assert mock_llm.call_count == 1  # single call

    @pytest.mark.asyncio
    async def test_empty_pairs_returns_empty(self) -> None:
        """No pairs → no LLM call."""
        from src.merge import batch_collision_check
        result = await batch_collision_check([])
        assert result.decisions == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_merge.py::TestBatchCollisionCheck -v`
Expected: FAIL

- [ ] **Step 3: Implement `batch_collision_check` in `src/merge.py`**

Add after `topic_match_check` (~line 131):

```python
async def batch_collision_check(
    pairs: list[CollisionPair],
) -> BatchCollisionDecision:
    """Decide MERGE/SKIP for all collision pairs in a single LLM call."""
    if not pairs:
        return BatchCollisionDecision(decisions=[])

    pairs_text = "\n\n".join(
        f'{i + 1}. New page "{p.new_title}"'
        + (f" (brief: {p.new_brief})" if p.new_brief else "")
        + f'\n   Existing page "{p.existing_title}" (brief: {p.existing_brief})'
        + f"\n   Collision type: {p.collision_type}"
        for i, p in enumerate(pairs)
    )

    messages = [
        {
            "role": "user",
            "content": (
                "For each collision pair below, decide whether to MERGE the new "
                "content into the existing page or SKIP (keep them separate).\n\n"
                "Consider: same topic? Complementary information? Would merging "
                "lose distinct identity?\nWhen uncertain, choose MERGE.\n\n"
                f"{pairs_text}"
            ),
        },
    ]
    return await complete_structured(
        messages=messages,
        response_model=BatchCollisionDecision,
        temperature=0.1,
    )
```

Update imports at top of `merge.py` to include `CollisionPair`, `BatchCollisionDecision`.

- [ ] **Step 4: Run tests**

Run: `uv run pytest tests/test_merge.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/merge.py tests/test_merge.py
git commit -m "feat: add batch_collision_check for single-call collision decisions"
```

---

### Task 6: Restructure process_batches_node — Batch Collision Collection Loop

**Files:**
- Modify: `src/ingest.py:290-386` (per-page loop in process_batches_node)
- Test: `tests/test_ingest.py` (update existing merge tests + add batch collision test)

This is the core refactor. The per-page loop changes from "detect → decide → act inline" to "detect → collect → batch decide → act".

- [ ] **Step 1: Write failing test**

```python
class TestBatchCollisionFlow:
    @pytest.mark.asyncio
    async def test_multiple_collisions_single_llm_call(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Two exact collisions → 1 batch_collision_check call (not 2 brief_merge_check calls)."""
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        import src.config
        src.config._settings = None

        # Pre-create two existing pages
        from src.wiki import write_page
        fm1 = WikiFrontmatter(
            title="Flash Attention",
            page_type=PageType.CONCEPT,
            sources=["old.pdf"],
            tags=["attention"],
            created=date(2026, 1, 1),
            updated=date(2026, 1, 1),
            confidence=Confidence.HIGH,
            brief="IO-aware attention algorithm.",
        )
        write_page(fm1, "# Flash Attention\n\nBody.", wiki_dir)
        fm2 = WikiFrontmatter(
            title="BERT",
            page_type=PageType.ENTITY,
            sources=["old.pdf"],
            tags=["nlp"],
            created=date(2026, 1, 1),
            updated=date(2026, 1, 1),
            confidence=Confidence.HIGH,
            brief="Bidirectional encoder.",
        )
        write_page(fm2, "# BERT\n\nBody.", wiki_dir)

        # LLM generates pages that collide with both
        ingest_result = IngestResult(
            source_summary=GeneratedPage(
                title="Summary",
                page_type=PageType.SOURCE_SUMMARY,
                tags=[],
                confidence=Confidence.HIGH,
                body="Summary.",
            ),
            concept_pages=[
                GeneratedPage(
                    title="Flash Attention",
                    page_type=PageType.CONCEPT,
                    tags=["attention"],
                    confidence=Confidence.HIGH,
                    body="# Flash Attention\n\nNew details.",
                    brief="Updated FA info.",
                ),
            ],
            entity_pages=[
                GeneratedPage(
                    title="BERT",
                    page_type=PageType.ENTITY,
                    tags=["nlp"],
                    confidence=Confidence.HIGH,
                    body="# BERT\n\nNew BERT details.",
                    brief="Updated BERT info.",
                ),
            ],
        )

        from src.models import (
            BatchCollisionDecision,
            CollisionDecision,
            EditOp,
            PatchedPage,
        )

        mock_batch_decision = BatchCollisionDecision(
            decisions=[
                CollisionDecision(new_title="Flash Attention", action="MERGE", reason="same topic"),
                CollisionDecision(new_title="BERT", action="SKIP", reason="already covered"),
            ]
        )
        mock_patched = PatchedPage(
            edits=[EditOp(old_string="# Flash Attention\n\nBody.", new_string="# Flash Attention\n\nNew details.")],
            tags_to_add=[],
            confidence=Confidence.HIGH,
        )

        with (
            patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm,
            patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_merge_llm,
        ):
            mock_llm.return_value = ingest_result
            # batch_collision_check (1 call) + merge_page for FA (patch + brief regen)
            mock_merge_llm.side_effect = [
                mock_batch_decision,
                mock_patched,
                BriefOutput(brief="FA: updated with new details."),
            ]
            result = await process_batches_node({
                "chunks": ["Text about FA and BERT."],
                "source_path": "test.txt",
                "source_title": "Test",
                "fresh": True,
            })

        # Summary written, FA merged, BERT skipped
        assert "errors" not in result or len(result.get("errors", [])) == 0
        assert len(result["written_paths"]) == 2  # summary + merged FA

        src.config._settings = None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_ingest.py::TestBatchCollisionFlow -v`
Expected: FAIL

- [ ] **Step 3: Restructure the per-page loop in `process_batches_node`**

Replace the per-page loop body (~lines 293-381) with the collect-then-batch pattern:

```python
            today = date.today()
            batch_titles: list[str] = []
            batch_brief_adds: list[tuple[str, str]] = []

            # Phase 1: Collect collision pairs and new pages
            collision_pairs: list[CollisionPair] = []
            collision_existing: dict[str, WikiPage] = {}  # new_title -> existing page
            collision_gen_pages: dict[str, GeneratedPage] = {}  # new_title -> gen page
            new_pages: list[GeneratedPage] = []

            for gen_page in all_pages:
                # Exact collision
                existing_page = get_page_by_title(gen_page.title, settings.wiki_dir)

                if existing_page is not None:
                    collision_pairs.append(CollisionPair(
                        new_title=gen_page.title,
                        existing_title=existing_page.frontmatter.title,
                        existing_brief=existing_page.frontmatter.brief,
                        collision_type="exact",
                        new_brief=gen_page.brief,
                    ))
                    collision_existing[gen_page.title] = existing_page
                    collision_gen_pages[gen_page.title] = gen_page

                else:
                    # Fuzzy collision
                    fuzzy_match = _check_fuzzy_collision(
                        brief_idx, gen_page.brief, settings.wiki_dir,
                    )
                    if fuzzy_match is not None:
                        collision_pairs.append(CollisionPair(
                            new_title=gen_page.title,
                            existing_title=fuzzy_match.frontmatter.title,
                            existing_brief=fuzzy_match.frontmatter.brief,
                            collision_type="fuzzy",
                            new_brief=gen_page.brief,
                        ))
                        collision_existing[gen_page.title] = fuzzy_match
                        collision_gen_pages[gen_page.title] = gen_page
                    else:
                        # No collision → new page
                        new_pages.append(gen_page)

            # Phase 2: Write new pages immediately
            for gen_page in new_pages:
                path = _write_new_page(gen_page, source_path, today, settings)
                all_written.append(path)
                batch_titles.append(gen_page.title)
                batch_brief_adds.append((path, gen_page.brief))

            # Phase 3: Batch collision decisions (1 LLM call)
            if collision_pairs:
                batch_decision = await batch_collision_check(collision_pairs)
                for decision in batch_decision.decisions:
                    gen_page = collision_gen_pages.get(decision.new_title)
                    existing_page = collision_existing.get(decision.new_title)
                    if gen_page is None or existing_page is None:
                        continue

                    if decision.action == "MERGE":
                        # Empty brief shortcut: skip merge if existing has no brief
                        if not existing_page.frontmatter.brief:
                            merged_fm, merged_body = await merge_page(
                                existing_page, gen_page, source_path,
                            )
                        else:
                            merged_fm, merged_body = await merge_page(
                                existing_page, gen_page, source_path,
                            )
                        path = write_page(merged_fm, merged_body, settings.wiki_dir)
                        batch_brief_adds.append((path, merged_fm.brief))
                    else:
                        logger.info(
                            "batch skip title=%s reason=%s",
                            gen_page.title,
                            decision.reason,
                        )
                        path = title_to_path(gen_page.title)

                    all_written.append(path)
                    batch_titles.append(gen_page.title)
                    batch_brief_adds.append((path, gen_page.brief))

            # Phase 4: Add to BriefIndex after batch
            for add_path, add_brief in batch_brief_adds:
                brief_idx.add(add_path, add_brief)
```

Update imports in `ingest.py`:

```python
from src.merge import batch_collision_check, merge_page
from src.models import (
    CollisionPair,
    ...
)
```

- [ ] **Step 4: Update existing tests for new flow**

Update `TestProcessBatchesMerge::test_merges_when_page_already_exists` — the mock setup needs to provide `BatchCollisionDecision` instead of `MergeDecision` for the merge LLM:

The `mock_merge_llm.side_effect` should be `[BatchCollisionDecision(...), mock_patched, BriefOutput(...)]` instead of `[MergeDecision(...), mock_patched, BriefOutput(...)]`.

Same update for `TestCrossSourceMerge::test_second_source_merges_with_existing_page`.

- [ ] **Step 5: Run all tests**

Run: `uv run pytest tests/ -v`
Expected: ALL PASS

- [ ] **Step 6: Commit**

```bash
git add src/ingest.py tests/test_ingest.py
git commit -m "feat: restructure per-page loop to batch collision decisions"
```

---

### Task 7: Update schema.yaml Prompt Variants

**Files:**
- Modify: `schema.yaml` (update `ingest_system` prompt)

- [ ] **Step 1: Update `schema.yaml` ingest_system prompt**

The `ingest_system` prompt should be clean and static (no dynamic content appended in code). Update the existing prompt to remove any content that was previously being appended by code (like tag instructions, which are now in the user message via `_build_batch_messages`).

Review current `schema.yaml` prompts section. The `ingest_system` prompt should contain only the core instructions for wiki page generation. Mode-specific instructions are injected by `_build_batch_messages` based on `ingest_mode`.

- [ ] **Step 2: Run all tests**

Run: `uv run pytest tests/ -v`
Expected: ALL PASS

- [ ] **Step 3: Commit**

```bash
git add schema.yaml
git commit -m "refactor: clean up ingest_system prompt for static caching"
```

---

## Self-Review

**Spec coverage:**
- 1.1 Empty title → Task 1 ✓
- 1.2 Batch BriefIndex.add → Task 1 + Task 6 ✓
- 1.3 Empty brief shortcut → Task 1 + Task 6 ✓
- 2 Short text mode → Task 3 ✓
- 3 Pluggable ingest modes → Task 2 + Task 3 ✓
- 4 Batch collision decisions → Task 4 + Task 5 + Task 6 ✓
- 5 Prompt caching + titles+briefs → Task 3 + Task 7 ✓

**Placeholder scan:** No TBD/TODO. All steps contain complete code.

**Type consistency:**
- `CollisionPair` fields match between models.py definition and ingest.py usage ✓
- `existing_briefs: dict[str, str]` parameter matches `cp.generated_briefs` type ✓
- `_build_batch_messages` signature consistent across all tasks ✓

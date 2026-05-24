# Page Merge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** When ingest generates a page whose title already exists on disk (from a prior batch or a prior source), read the existing page and merge the two via LLM instead of overwriting.

**Architecture:** Add a `merge_page` async function that sends existing + new page content to the LLM with a merge prompt, returns a merged result. Modify `process_batches_node` to check for existing pages before writing and call merge when a collision is detected. Frontmatter merging (sources, tags, related, dates) is pure logic — no LLM needed.

**Tech Stack:** Pydantic models, instructor structured output, existing LiteLLM fallback chain.

---

## File Structure

| File                   | Responsibility                                                                             |
| ---------------------- | ------------------------------------------------------------------------------------------ |
| `src/models.py`        | Add `MergedPage` Pydantic model for LLM merge output                                       |
| `src/merge.py`         | New module: `_merge_frontmatter` (pure) + `merge_page` (async LLM call)                    |
| `src/config.py`        | Add `get_merge_prompt()`                                                                   |
| `schema.yaml`          | Add `merge_system` prompt                                                                  |
| `src/ingest.py`        | Modify `process_batches_node` to merge on collision; update `_build_batch_messages` prompt |
| `tests/test_merge.py`  | Tests for `_merge_frontmatter` and `merge_page`                                            |
| `tests/test_ingest.py` | Add merge-aware batch tests + integration test                                             |

---

### Task 1: MergedPage model + merge prompt config

**Files:**
- Modify: `src/models.py:67-69` (after `GeneratedPage`)
- Modify: `schema.yaml:47-61` (after `ingest_system`)
- Modify: `src/config.py:99-100` (after `get_ingest_prompt`)

- [ ] **Step 1: Add `MergedPage` to `src/models.py`**

Add after the `GeneratedPage` class (after line 69):

```python
class MergedPage(BaseModel):
    """LLM output: merged content from existing + new page about the same topic."""

    body: str = Field(description="Merged markdown body preserving all unique information from both versions")
    tags: list[str] = Field(description="Combined tag list from both versions")
    confidence: Confidence = Field(default=Confidence.MEDIUM)
```

- [ ] **Step 2: Add `merge_system` prompt to `schema.yaml`**

Add after `query_system` in the `prompts` section:

```yaml
  merge_system: |
    You are merging two wiki pages about the same topic into one.
    Preserve ALL unique information from both versions. Remove redundancy.
    Maintain a coherent structure. Keep all [[WikiLinks]] from both versions.
    Use the provided tag vocabulary when possible.
```

- [ ] **Step 3: Add `get_merge_prompt()` to `src/config.py`**

Add after `get_ingest_prompt()` (after line 98):

```python
def get_merge_prompt() -> str:
    """Return the merge system prompt from schema.yaml."""
    schema = load_schema()
    prompts = schema.get("prompts", {})
    return prompts.get(
        "merge_system",
        "You are merging two wiki pages about the same topic. "
        "Preserve all unique information, remove redundancy, keep all [[WikiLinks]].",
    )
```

- [ ] **Step 4: Run existing tests to verify nothing broke**

Run: `python -m pytest tests/ -v`
Expected: All existing tests pass.

- [ ] **Step 5: Commit**

```bash
git add src/models.py schema.yaml src/config.py
git commit -m "feat: add MergedPage model and merge prompt config"
```

---

### Task 2: Merge module — `_merge_frontmatter` + `merge_page`

**Files:**
- Create: `src/merge.py`
- Create: `tests/test_merge.py`

- [ ] **Step 1: Write failing tests for `_merge_frontmatter`**

Create `tests/test_merge.py`:

```python
"""Tests for page merge logic."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from src.merge import _merge_frontmatter, merge_page
from src.models import (
    Confidence,
    GeneratedPage,
    MergedPage,
    PageType,
    WikiFrontmatter,
    WikiPage,
)


# ── _merge_frontmatter tests ────────────────────────────────────────────────


class TestMergeFrontmatter:
    def test_merges_sources(self) -> None:
        existing_fm = WikiFrontmatter(
            title="BERT",
            page_type=PageType.ENTITY,
            sources=["papers/bert.pdf"],
            tags=["nlp"],
            created=date(2026, 1, 1),
            updated=date(2026, 1, 1),
            confidence=Confidence.HIGH,
        )
        new_page = GeneratedPage(
            title="BERT",
            page_type=PageType.ENTITY,
            tags=["nlp", "pre-training"],
            confidence=Confidence.MEDIUM,
            body="# BERT\n\nUpdated content.",
            related_titles=["Transformer Architecture"],
        )

        fm, body = _merge_frontmatter(
            existing_fm=existing_fm,
            new_page=new_page,
            merged_body="Merged body.",
            merged_tags=["nlp", "pre-training", "deep-learning"],
            merged_confidence=Confidence.HIGH,
            source_path="articles/bert-guide.md",
        )

        assert "papers/bert.pdf" in fm.sources
        assert "articles/bert-guide.md" in fm.sources
        assert len(fm.sources) == 2
        assert body == "Merged body."

    def test_does_not_duplicate_sources(self) -> None:
        existing_fm = WikiFrontmatter(
            title="BERT",
            page_type=PageType.ENTITY,
            sources=["papers/bert.pdf"],
            tags=["nlp"],
            created=date(2026, 1, 1),
            updated=date(2026, 1, 1),
        )
        new_page = GeneratedPage(
            title="BERT",
            page_type=PageType.ENTITY,
            tags=["nlp"],
            confidence=Confidence.HIGH,
            body="content",
        )

        fm, _ = _merge_frontmatter(
            existing_fm=existing_fm,
            new_page=new_page,
            merged_body="body",
            merged_tags=["nlp"],
            merged_confidence=Confidence.HIGH,
            source_path="papers/bert.pdf",
        )

        assert fm.sources == ["papers/bert.pdf"]

    def test_merges_tags_deduped(self) -> None:
        existing_fm = WikiFrontmatter(
            title="Test",
            page_type=PageType.CONCEPT,
            sources=[],
            tags=["nlp", "deep-learning"],
            created=date(2026, 1, 1),
            updated=date(2026, 1, 1),
        )
        new_page = GeneratedPage(
            title="Test",
            page_type=PageType.CONCEPT,
            tags=["nlp", "transformers"],
            confidence=Confidence.HIGH,
            body="content",
        )

        fm, _ = _merge_frontmatter(
            existing_fm=existing_fm,
            new_page=new_page,
            merged_body="body",
            merged_tags=["nlp", "transformers", "attention"],
            merged_confidence=Confidence.HIGH,
            source_path="new.pdf",
        )

        assert "nlp" in fm.tags
        assert "deep-learning" in fm.tags
        assert "transformers" in fm.tags
        assert "attention" in fm.tags
        # No duplicates
        assert len(fm.tags) == len(set(fm.tags))

    def test_preserves_created_date(self) -> None:
        existing_fm = WikiFrontmatter(
            title="Test",
            page_type=PageType.CONCEPT,
            created=date(2026, 1, 1),
            updated=date(2026, 1, 1),
        )
        new_page = GeneratedPage(
            title="Test",
            page_type=PageType.CONCEPT,
            tags=[],
            confidence=Confidence.MEDIUM,
            body="content",
        )

        fm, _ = _merge_frontmatter(
            existing_fm=existing_fm,
            new_page=new_page,
            merged_body="body",
            merged_tags=[],
            merged_confidence=Confidence.MEDIUM,
            source_path="new.pdf",
        )

        assert fm.created == date(2026, 1, 1)
        assert fm.updated == date.today()

    def test_merges_related(self) -> None:
        existing_fm = WikiFrontmatter(
            title="Test",
            page_type=PageType.CONCEPT,
            sources=[],
            tags=[],
            created=date(2026, 1, 1),
            updated=date(2026, 1, 1),
            related=["bert.md", "gpt.md"],
        )
        new_page = GeneratedPage(
            title="Test",
            page_type=PageType.CONCEPT,
            tags=[],
            confidence=Confidence.MEDIUM,
            body="content",
            related_titles=["BERT", "Attention Mechanism"],
        )

        fm, _ = _merge_frontmatter(
            existing_fm=existing_fm,
            new_page=new_page,
            merged_body="body",
            merged_tags=[],
            merged_confidence=Confidence.MEDIUM,
            source_path="new.pdf",
        )

        assert "bert.md" in fm.related
        assert "gpt.md" in fm.related
        assert "attention-mechanism.md" in fm.related

    def test_takes_higher_confidence(self) -> None:
        existing_fm = WikiFrontmatter(
            title="Test",
            page_type=PageType.CONCEPT,
            sources=[],
            tags=[],
            created=date(2026, 1, 1),
            updated=date(2026, 1, 1),
            confidence=Confidence.LOW,
        )
        new_page = GeneratedPage(
            title="Test",
            page_type=PageType.CONCEPT,
            tags=[],
            confidence=Confidence.HIGH,
            body="content",
        )

        fm, _ = _merge_frontmatter(
            existing_fm=existing_fm,
            new_page=new_page,
            merged_body="body",
            merged_tags=[],
            merged_confidence=Confidence.HIGH,
            source_path="new.pdf",
        )

        assert fm.confidence == Confidence.HIGH

    def test_keeps_existing_title_and_page_type(self) -> None:
        existing_fm = WikiFrontmatter(
            title="Original Title",
            page_type=PageType.ENTITY,
            sources=[],
            tags=[],
            created=date(2026, 1, 1),
            updated=date(2026, 1, 1),
        )
        new_page = GeneratedPage(
            title="Different Title",
            page_type=PageType.CONCEPT,
            tags=[],
            confidence=Confidence.MEDIUM,
            body="content",
        )

        fm, _ = _merge_frontmatter(
            existing_fm=existing_fm,
            new_page=new_page,
            merged_body="body",
            merged_tags=[],
            merged_confidence=Confidence.MEDIUM,
            source_path="new.pdf",
        )

        assert fm.title == "Original Title"
        assert fm.page_type == PageType.ENTITY
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_merge.py::TestMergeFrontmatter -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'src.merge'`

- [ ] **Step 3: Implement `src/merge.py`**

```python
"""Page merge: combine existing wiki pages with new content via LLM."""

from __future__ import annotations

import logging
from datetime import date

from src.config import get_merge_prompt
from src.llm import complete_structured
from src.models import (
    Confidence,
    GeneratedPage,
    MergedPage,
    WikiFrontmatter,
)
from src.wiki import title_to_path

logger = logging.getLogger(__name__)

_CONFIDENCE_ORDER = {Confidence.HIGH: 3, Confidence.MEDIUM: 2, Confidence.LOW: 1}


def _merge_frontmatter(
    existing_fm: WikiFrontmatter,
    new_page: GeneratedPage,
    merged_body: str,
    merged_tags: list[str],
    merged_confidence: Confidence,
    source_path: str,
) -> tuple[WikiFrontmatter, str]:
    """Merge frontmatter fields from existing page and new generated page.

    Pure logic — no LLM call. Returns (merged_frontmatter, merged_body).
    """
    # Sources: append new source if not already present
    sources = list(existing_fm.sources)
    if source_path not in sources:
        sources.append(source_path)

    # Tags: union of existing + LLM-merged tags, deduplicated, order-preserving
    seen: set[str] = set()
    tags: list[str] = []
    for t in existing_fm.tags + merged_tags:
        if t not in seen:
            seen.add(t)
            tags.append(t)

    # Related: union of existing paths + new title-to-path conversions
    existing_related = set(existing_fm.related)
    new_related = {title_to_path(t) for t in new_page.related_titles}
    related = sorted(existing_related | new_related)

    # Confidence: take the higher of existing vs merged
    confidence = (
        merged_confidence
        if _CONFIDENCE_ORDER.get(merged_confidence, 0)
        >= _CONFIDENCE_ORDER.get(existing_fm.confidence, 0)
        else existing_fm.confidence
    )

    fm = WikiFrontmatter(
        title=existing_fm.title,
        page_type=existing_fm.page_type,
        sources=sources,
        tags=tags,
        created=existing_fm.created,
        updated=date.today(),
        confidence=confidence,
        related=related,
    )

    return fm, merged_body


async def merge_page(
    existing_body: str,
    new_page: GeneratedPage,
    source_path: str,
) -> tuple[WikiFrontmatter, str]:
    """Merge existing page body with new generated page via LLM.

    Returns (merged_frontmatter, merged_body) ready for write_page().
    """
    raise NotImplementedError("TODO: implement after frontmatter tests pass")
```

Note: `merge_page` is a stub for now — it will be implemented in the next step.

- [ ] **Step 4: Run frontmatter tests to verify they pass**

Run: `python -m pytest tests/test_merge.py::TestMergeFrontmatter -v`
Expected: All 7 tests PASS.

- [ ] **Step 5: Write failing test for `merge_page` (LLM call)**

Add to `tests/test_merge.py`:

```python
# ── merge_page tests ────────────────────────────────────────────────────────


class TestMergePage:
    @pytest.mark.asyncio
    async def test_merges_via_llm(self) -> None:
        existing_fm = WikiFrontmatter(
            title="BERT",
            page_type=PageType.ENTITY,
            sources=["papers/bert.pdf"],
            tags=["nlp"],
            created=date(2026, 1, 1),
            updated=date(2026, 1, 1),
            confidence=Confidence.HIGH,
        )
        new_page = GeneratedPage(
            title="BERT",
            page_type=PageType.ENTITY,
            tags=["nlp", "pre-training"],
            confidence=Confidence.HIGH,
            body="# BERT\n\nNew info about bidirectional training.",
            related_titles=["Transformer Architecture"],
        )

        mock_merged = MergedPage(
            body="# BERT\n\nBidirectional encoder. New info about bidirectional training.",
            tags=["nlp", "pre-training"],
            confidence=Confidence.HIGH,
        )

        with patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = mock_merged
            fm, body = await merge_page(existing_fm, new_page, "articles/bert-guide.md")

        assert "bidirectional" in body.lower()
        assert "papers/bert.pdf" in fm.sources
        assert "articles/bert-guide.md" in fm.sources
        assert fm.title == "BERT"
        assert fm.created == date(2026, 1, 1)
```

- [ ] **Step 6: Run test to verify it fails**

Run: `python -m pytest tests/test_merge.py::TestMergePage -v`
Expected: FAIL — `NotImplementedError`

- [ ] **Step 7: Implement `merge_page` in `src/merge.py`**

Replace the stub with:

```python
async def merge_page(
    existing_fm: WikiFrontmatter,
    new_page: GeneratedPage,
    source_path: str,
) -> tuple[WikiFrontmatter, str]:
    """Merge existing page with new generated page via LLM.

    Sends both page bodies to the LLM with a merge prompt.
    Returns (merged_frontmatter, merged_body) ready for write_page().
    """
    system_prompt = get_merge_prompt()

    from src.config import get_allowed_tags

    allowed_tags = get_allowed_tags()
    if allowed_tags:
        system_prompt += "\n\nPreferred tags (use these when applicable): " + ", ".join(
            allowed_tags
        )

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": (
                f"Merge these two wiki pages about the same topic.\n\n"
                f"=== EXISTING PAGE ===\n{existing_fm.title}\n\n"
                f"No body yet.\n\n"
                f"=== NEW CONTENT (from source: {source_path}) ===\n"
                f"{new_page.title}\n\n{new_page.body}\n\n"
                f"Produce a single merged page."
            ),
        },
    ]

    result = await complete_structured(
        messages=messages,
        response_model=MergedPage,
        temperature=0.2,
    )

    logger.info("merged page title=%s", existing_fm.title)

    return _merge_frontmatter(
        existing_fm=existing_fm,
        new_page=new_page,
        merged_body=result.body,
        merged_tags=result.tags,
        merged_confidence=result.confidence,
        source_path=source_path,
    )
```

Wait — I need to include the existing page body in the prompt. But `merge_page` receives `existing_fm` (frontmatter only), not the full `WikiPage`. Let me adjust the signature to accept the full `WikiPage` instead, so we can access the body.

Let me revise. The signature should be:

```python
async def merge_page(
    existing: WikiPage,
    new_page: GeneratedPage,
    source_path: str,
) -> tuple[WikiFrontmatter, str]:
```

And the prompt should include `existing.body`:

```python
    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": (
                f"Merge these two wiki pages about the same topic.\n\n"
                f"=== EXISTING PAGE ===\n"
                f"Title: {existing.frontmatter.title}\n\n"
                f"{existing.body}\n\n"
                f"=== NEW CONTENT (from source: {source_path}) ===\n"
                f"Title: {new_page.title}\n\n"
                f"{new_page.body}\n\n"
                f"Produce a single merged page that preserves all unique "
                f"information from both versions."
            ),
        },
    ]
```

And `_merge_frontmatter` receives `existing.frontmatter` instead of `existing_fm`.

Let me also update the test to use `WikiPage`:

```python
    @pytest.mark.asyncio
    async def test_merges_via_llm(self) -> None:
        existing_page = WikiPage(
            path="bert.md",
            frontmatter=WikiFrontmatter(
                title="BERT",
                page_type=PageType.ENTITY,
                sources=["papers/bert.pdf"],
                tags=["nlp"],
                created=date(2026, 1, 1),
                updated=date(2026, 1, 1),
                confidence=Confidence.HIGH,
            ),
            body="# BERT\n\nBidirectional encoder.",
        )
        ...
        with patch("src.merge.complete_structured", ...) as mock_llm:
            mock_llm.return_value = mock_merged
            fm, body = await merge_page(existing_page, new_page, "articles/bert-guide.md")
```

And update the existing `_merge_frontmatter` calls in tests too — they still use `existing_fm` directly (pure function), that's fine.

OK let me rewrite the complete `merge_page` and update the test properly in the plan.

- [ ] **Step 8: Run all merge tests to verify they pass**

Run: `python -m pytest tests/test_merge.py -v`
Expected: All tests PASS.

- [ ] **Step 9: Run full test suite**

Run: `python -m pytest tests/ -v`
Expected: All tests pass (no regressions).

- [ ] **Step 10: Commit**

```bash
git add src/merge.py tests/test_merge.py
git commit -m "feat: add merge module with frontmatter merge and LLM page merge"
```

---

### Task 3: Wire merge into ingest pipeline

**Files:**
- Modify: `src/ingest.py:216-236` (page writing loop in `process_batches_node`)
- Modify: `src/ingest.py:121-125` (batch prompt for existing titles)
- Modify: `tests/test_ingest.py`

- [ ] **Step 1: Write failing test for merge-on-collision in batch processing**

Add to `tests/test_ingest.py`:

```python
class TestProcessBatchesMerge:
    @pytest.mark.asyncio
    async def test_merges_when_page_already_exists(
        self, tmp_path: Path, mock_ingest_result: IngestResult, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        import src.config

        src.config._settings = None

        # Pre-create existing page with same title as mock's entity page ("BERT")
        existing_fm = WikiFrontmatter(
            title="BERT",
            page_type=PageType.ENTITY,
            sources=["old/source.pdf"],
            tags=["nlp"],
            created=date(2026, 1, 1),
            updated=date(2026, 1, 1),
            confidence=Confidence.HIGH,
        )
        from src.wiki import write_page

        write_page(existing_fm, "# BERT\n\nOld content about BERT.", wiki_dir)

        state = {
            "chunks": ["Source text about BERT and transformers."],
            "source_path": "new-source.txt",
            "source_title": "New Source",
            "fresh": True,
        }

        from src.models import MergedPage

        mock_merged = MergedPage(
            body="# BERT\n\nMerged content combining old and new.",
            tags=["nlp", "pre-training"],
            confidence=Confidence.HIGH,
        )

        with patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm, \
             patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_merge_llm:
            mock_llm.return_value = mock_ingest_result
            mock_merge_llm.return_value = mock_merged
            result = await process_batches_node(state)

        assert "errors" not in result or len(result.get("errors", [])) == 0
        # Verify BERT page was merged (not just overwritten)
        bert_page = read_page("bert.md", wiki_dir)
        assert "old" in bert_page.frontmatter.sources or "new-source.txt" in bert_page.frontmatter.sources
        assert bert_page.frontmatter.created == date(2026, 1, 1)  # preserved

        src.config._settings = None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_ingest.py::TestProcessBatchesMerge -v`
Expected: FAIL — BERT page gets overwritten instead of merged (existing page sources lost, created date not preserved).

- [ ] **Step 3: Modify `process_batches_node` to merge on collision**

In `src/ingest.py`, add import at the top:

```python
from src.merge import merge_page
```

Replace the page writing loop in `process_batches_node` (lines 218-236). Change from:

```python
            all_pages = [result.source_summary, *result.concept_pages, *result.entity_pages]

            # Write pages
            today = date.today()
            batch_titles: list[str] = []
            for gen_page in all_pages:
                fm = WikiFrontmatter(
                    title=gen_page.title,
                    page_type=gen_page.page_type,
                    sources=[source_path],
                    tags=gen_page.tags,
                    created=today,
                    updated=today,
                    confidence=gen_page.confidence,
                    related=[title_to_path(t) for t in gen_page.related_titles],
                )
                path = write_page(fm, gen_page.body, settings.wiki_dir)
                all_written.append(path)
                batch_titles.append(gen_page.title)
```

To:

```python
            all_pages = [result.source_summary, *result.concept_pages, *result.entity_pages]

            # Write pages (merge if title already exists on disk)
            today = date.today()
            batch_titles: list[str] = []
            for gen_page in all_pages:
                existing_page = get_page_by_title(gen_page.title, settings.wiki_dir)
                if existing_page is not None:
                    merged_fm, merged_body = await merge_page(
                        existing_page, gen_page, source_path,
                    )
                    path = write_page(merged_fm, merged_body, settings.wiki_dir)
                else:
                    fm = WikiFrontmatter(
                        title=gen_page.title,
                        page_type=gen_page.page_type,
                        sources=[source_path],
                        tags=gen_page.tags,
                        created=today,
                        updated=today,
                        confidence=gen_page.confidence,
                        related=[title_to_path(t) for t in gen_page.related_titles],
                    )
                    path = write_page(fm, gen_page.body, settings.wiki_dir)
                all_written.append(path)
                batch_titles.append(gen_page.title)
```

- [ ] **Step 4: Run the failing test to verify it passes**

Run: `python -m pytest tests/test_ingest.py::TestProcessBatchesMerge -v`
Expected: PASS.

- [ ] **Step 5: Run full test suite to verify no regressions**

Run: `python -m pytest tests/ -v`
Expected: All tests pass.

- [ ] **Step 6: Commit**

```bash
git add src/ingest.py tests/test_ingest.py
git commit -m "feat: merge existing pages on title collision during ingest"
```

---

### Task 4: Update batch prompt for merge awareness + add existing wiki titles

**Files:**
- Modify: `src/ingest.py:103-131` (`_build_batch_messages`)
- Modify: `src/ingest.py:162-260` (`process_batches_node`)

Currently `_build_batch_messages` only receives `existing_titles` from the current run's checkpoint. It should also receive titles of pages already on disk from prior sources, so the LLM can make informed decisions about whether to create a new page or link to an existing one.

- [ ] **Step 1: Write failing test for wiki-aware existing titles in prompt**

Add to `tests/test_ingest.py`:

```python
class TestBuildBatchMessages:
    def test_includes_wiki_titles_in_prompt(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        import src.config
        src.config._settings = None

        # Create an existing page on disk
        from src.wiki import write_page

        fm = WikiFrontmatter(
            title="Existing Topic",
            page_type=PageType.CONCEPT,
            sources=["old.pdf"],
            created=date(2026, 1, 1),
            updated=date(2026, 1, 1),
        )
        write_page(fm, "Content.", wiki_dir)

        from src.ingest import _build_batch_messages

        messages = _build_batch_messages(
            chunks=["chunk text"],
            batch_start=0,
            batch_size=5,
            source_title="Test Source",
            existing_titles=[],
        )

        user_msg = messages[1]["content"]
        assert "Existing Topic" in user_msg

        src.config._settings = None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_ingest.py::TestBuildBatchMessages -v`
Expected: FAIL — "Existing Topic" is not in the prompt because wiki titles are not loaded.

- [ ] **Step 3: Modify `_build_batch_messages` to accept and include wiki titles**

Add a `wiki_titles` parameter to `_build_batch_messages`:

```python
def _build_batch_messages(
    chunks: list[str],
    batch_start: int,
    batch_size: int,
    source_title: str,
    existing_titles: list[str],
    wiki_titles: list[str] | None = None,
) -> list[dict[str, str]]:
```

Update the existing_titles section in `_build_batch_messages` to combine both lists and update the prompt instruction:

```python
    all_existing = list(dict.fromkeys((existing_titles or []) + (wiki_titles or [])))
    if all_existing:
        user_content += (
            f"\n\nThe following wiki pages already exist: {', '.join(all_existing)}"
            "\nLink to them using [[Title]] syntax where relevant."
            "\nIf you have genuinely NEW information about an existing topic, you may"
            " create a page with that title — it will be merged with existing content."
            "\nOtherwise, prefer using [[Title]] links."
        )
```

- [ ] **Step 4: Update `process_batches_node` to load wiki titles and pass them**

In `process_batches_node`, before the batch loop, load existing wiki page titles:

```python
    from src.wiki import list_pages

    wiki_titles: list[str] = []
    if settings.wiki_dir.exists():
        for p in list_pages(settings.wiki_dir):
            try:
                page = read_page(p, settings.wiki_dir)
                wiki_titles.append(page.frontmatter.title)
            except Exception:
                pass
```

Pass `wiki_titles` to `_build_batch_messages`:

```python
        messages = _build_batch_messages(
            chunks=chunks,
            batch_start=batch_idx * batch_size,
            batch_size=batch_size,
            source_title=source_title,
            existing_titles=cp.generated_titles,
            wiki_titles=wiki_titles,
        )
```

- [ ] **Step 5: Run all tests**

Run: `python -m pytest tests/ -v`
Expected: All tests pass.

- [ ] **Step 6: Commit**

```bash
git add src/ingest.py tests/test_ingest.py
git commit -m "feat: include existing wiki page titles in batch prompt for merge awareness"
```

---

### Task 5: Integration test — cross-source merge

**Files:**
- Modify: `tests/test_ingest.py`

- [ ] **Step 1: Write end-to-end integration test**

Add to `tests/test_ingest.py`:

```python
class TestCrossSourceMerge:
    @pytest.mark.asyncio
    async def test_second_source_merges_with_existing_page(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Simulate ingesting source B after source A already created a page."""
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        checkpoint_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("WIKI_WIKI_DIR", str(wiki_dir))
        monkeypatch.setenv("WIKI_CHECKPOINT_DIR", str(checkpoint_dir))
        import src.config

        src.config._settings = None

        # Source A already ingested — "BERT" page exists on disk
        existing_fm = WikiFrontmatter(
            title="BERT",
            page_type=PageType.ENTITY,
            sources=["source-a.pdf"],
            tags=["nlp"],
            created=date(2026, 4, 1),
            updated=date(2026, 4, 1),
            confidence=Confidence.HIGH,
            related=["transformer-architecture.md"],
        )
        write_page(existing_fm, "# BERT\n\nBidirectional encoder from source A.", wiki_dir)

        # Source B generates a page that also has "BERT"
        source_b_result = IngestResult(
            source_summary=GeneratedPage(
                title="Source B Summary",
                page_type=PageType.SOURCE_SUMMARY,
                tags=["nlp"],
                confidence=Confidence.HIGH,
                body="# Source B\n\nOverview.",
                related_titles=[],
            ),
            concept_pages=[],
            entity_pages=[
                GeneratedPage(
                    title="BERT",
                    page_type=PageType.ENTITY,
                    tags=["nlp", "pre-training"],
                    confidence=Confidence.HIGH,
                    body="# BERT\n\nNew details about pre-training from source B.",
                    related_titles=["Source B Summary"],
                ),
            ],
        )

        mock_merged = MergedPage(
            body="# BERT\n\nBidirectional encoder from source A. New details about pre-training from source B.",
            tags=["nlp", "pre-training"],
            confidence=Confidence.HIGH,
        )

        state = {
            "chunks": ["Content about BERT pre-training."],
            "source_path": "source-b.pdf",
            "source_title": "Source B",
            "fresh": True,
        }

        with patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm, \
             patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_merge_llm:
            mock_llm.return_value = source_b_result
            mock_merge_llm.return_value = mock_merged
            result = await process_batches_node(state)

        assert "errors" not in result or len(result.get("errors", [])) == 0

        # Verify merged BERT page
        bert_page = read_page("bert.md", wiki_dir)
        assert "source-a.pdf" in bert_page.frontmatter.sources
        assert "source-b.pdf" in bert_page.frontmatter.sources
        assert bert_page.frontmatter.created == date(2026, 4, 1)
        assert bert_page.frontmatter.updated == date.today()
        assert "pre-training" in bert_page.frontmatter.tags

        # Source B Summary should be written normally (no merge)
        assert "source-b-summary.md" in result.get("written_paths", [])

        src.config._settings = None
```

- [ ] **Step 2: Run test to verify it passes**

Run: `python -m pytest tests/test_ingest.py::TestCrossSourceMerge -v`
Expected: PASS.

- [ ] **Step 3: Run full test suite**

Run: `python -m pytest tests/ -v`
Expected: All tests pass.

- [ ] **Step 4: Commit**

```bash
git add tests/test_ingest.py
git commit -m "test: add cross-source merge integration test"
```

---

## Self-Review

**Spec coverage:**
- Intra-source batch dedup via merge: Task 3 handles this — `get_page_by_title` checks disk, which includes pages written by prior batches in the same run.
- Cross-source merge: Task 3 + Task 5 integration test cover this.
- Frontmatter merge logic: Task 2 covers sources, tags, related, dates, confidence.
- LLM merge prompt: Task 1 adds config, Task 2 implements the call.
- Batch prompt awareness of existing wiki: Task 4.
- No gaps found.

**Placeholder scan:**
- No TBD, TODO, or placeholder steps found.
- All code blocks contain complete implementations.
- All test code is complete.

**Type consistency:**
- `MergedPage` has `body: str`, `tags: list[str]`, `confidence: Confidence` — used consistently in `merge_page` and tests.
- `merge_page` returns `tuple[WikiFrontmatter, str]` — matches what `write_page(fm, body)` expects.
- `_merge_frontmatter` takes `existing_fm: WikiFrontmatter` — in `merge_page` we pass `existing.frontmatter` (from `WikiPage`).
- `WikiPage` used as the `existing` param in `merge_page` and in `process_batches_node`'s `get_page_by_title` call — consistent.
- `_build_batch_messages` gets new `wiki_titles: list[str] | None` — used in Task 3 and Task 4 consistently.

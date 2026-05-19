# Edit/Patch Mechanism Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the full-rewrite merge with an edit/patch mechanism where LLM generates `old_string`/`new_string` operations, with 3 retries and rewrite fallback.

**Architecture:** New `src/patch.py` module for pure edit application logic. `merge_page()` rewritten to try patch-first (3 attempts with error injection), then fall back to existing full rewrite. New Pydantic models `EditOp` and `PatchedPage` for structured LLM output. New `edit_system` prompt in `schema.yaml`.

**Tech Stack:** Python 3.13+, Pydantic, instructor (existing), pytest + pytest-asyncio (existing)

---

## File Structure

| File | Responsibility |
|------|----------------|
| `src/models.py` | Add `EditOp`, `PatchedPage` models |
| `src/patch.py` | **New** — `apply_edits()`, `PatchError` |
| `src/config.py` | Add `get_edit_prompt()` |
| `schema.yaml` | Add `edit_system` prompt |
| `src/merge.py` | Rewrite `merge_page()` — 3x patch → rewrite fallback |
| `tests/test_patch.py` | **New** — unit tests for `apply_edits()` |
| `tests/test_merge.py` | Update merge tests for new patch-first flow |

---

### Task 1: Add EditOp and PatchedPage models

**Files:**
- Modify: `src/models.py:53-79` (after existing LLM models section)
- Test: `tests/test_models.py`

- [ ] **Step 1: Write the failing test**

Add to `tests/test_models.py`:

```python
class TestEditOp:
    def test_create_edit_op(self) -> None:
        from src.models import EditOp

        op = EditOp(old_string="hello", new_string="world")
        assert op.old_string == "hello"
        assert op.new_string == "world"
        assert op.replace_all is False

    def test_create_edit_op_replace_all(self) -> None:
        from src.models import EditOp

        op = EditOp(old_string="foo", new_string="bar", replace_all=True)
        assert op.replace_all is True


class TestPatchedPage:
    def test_create_patched_page(self) -> None:
        from src.models import Confidence, EditOp, PatchedPage

        page = PatchedPage(
            edits=[
                EditOp(old_string="old text", new_string="new text"),
                EditOp(old_string="another", new_string="replacement"),
            ],
            tags_to_add=["transformers"],
            confidence=Confidence.HIGH,
        )
        assert len(page.edits) == 2
        assert page.tags_to_add == ["transformers"]
        assert page.confidence == Confidence.HIGH

    def test_patched_page_defaults(self) -> None:
        from src.models import Confidence, PatchedPage

        page = PatchedPage(edits=[])
        assert page.tags_to_add == []
        assert page.confidence == Confidence.MEDIUM
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_models.py::TestEditOp tests/test_models.py::TestPatchedPage -v`
Expected: FAIL with ImportError (models not defined)

- [ ] **Step 3: Write minimal implementation**

Add to `src/models.py` after the `MergedPage` class (after line 79):

```python
class EditOp(BaseModel):
    """Single edit operation: exact string replacement."""

    old_string: str = Field(description="Exact text from existing body to replace, must be unique")
    new_string: str = Field(description="Replacement text. Empty string = deletion")
    replace_all: bool = Field(default=False, description="True to replace all occurrences")


class PatchedPage(BaseModel):
    """LLM output: a batch of edit operations + metadata delta."""

    edits: list[EditOp] = Field(description="Edit operations to apply in order")
    tags_to_add: list[str] = Field(default_factory=list, description="Tags to add (incremental)")
    confidence: Confidence = Confidence.MEDIUM
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_models.py::TestEditOp tests/test_models.py::TestPatchedPage -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/models.py tests/test_models.py
git commit -m "feat: add EditOp and PatchedPage models for patch-based page updates"
```

---

### Task 2: Create patch.py with apply_edits and PatchError

**Files:**
- Create: `src/patch.py`
- Create: `tests/test_patch.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_patch.py`:

```python
"""Tests for edit/patch application logic."""

from __future__ import annotations

import pytest

from src.models import EditOp
from src.patch import PatchError, apply_edits


class TestApplyEditsSingleEdit:
    def test_replaces_single_match(self) -> None:
        body = "Hello world"
        edits = [EditOp(old_string="Hello", new_string="Goodbye")]
        assert apply_edits(body, edits) == "Goodbye world"

    def test_deletion_with_empty_new_string(self) -> None:
        body = "Hello brave new world"
        edits = [EditOp(old_string="brave new ", new_string="")]
        assert apply_edits(body, edits) == "Hello world"

    def test_preserves_surrounding_content(self) -> None:
        body = "Line 1\nLine 2\nLine 3"
        edits = [EditOp(old_string="Line 2", new_string="Modified Line 2")]
        assert apply_edits(body, edits) == "Line 1\nModified Line 2\nLine 3"


class TestApplyEditsMultipleEdits:
    def test_applies_edits_sequentially(self) -> None:
        body = "alpha beta gamma"
        edits = [
            EditOp(old_string="alpha", new_string="ONE"),
            EditOp(old_string="ONE beta", new_string="TWO"),
        ]
        assert apply_edits(body, edits) == "TWO gamma"

    def test_second_edit_sees_result_of_first(self) -> None:
        body = "foo bar"
        edits = [
            EditOp(old_string="foo", new_string="baz"),
            EditOp(old_string="baz bar", new_string="done"),
        ]
        assert apply_edits(body, edits) == "done"

    def test_empty_edits_list_returns_body_unchanged(self) -> None:
        body = "unchanged"
        assert apply_edits(body, []) == "unchanged"


class TestApplyEditsReplaceAll:
    def test_replace_all_true_replaces_every_occurrence(self) -> None:
        body = "spam and spam with spam"
        edits = [EditOp(old_string="spam", new_string="eggs", replace_all=True)]
        assert apply_edits(body, edits) == "eggs and eggs with eggs"

    def test_replace_all_false_rejects_multiple_matches(self) -> None:
        body = "spam and spam with spam"
        edits = [EditOp(old_string="spam", new_string="eggs")]
        with pytest.raises(PatchError, match="matches 3 times"):
            apply_edits(body, edits)


class TestApplyEditsErrors:
    def test_old_string_not_found(self) -> None:
        body = "Hello world"
        edits = [EditOp(old_string="Goodbye", new_string="Hello")]
        with pytest.raises(PatchError, match="old_string not found"):
            apply_edits(body, edits)

    def test_error_includes_edit_index(self) -> None:
        body = "Hello world"
        edits = [
            EditOp(old_string="Hello", new_string="Hi"),
            EditOp(old_string="missing", new_string="oops"),
        ]
        with pytest.raises(PatchError, match="Edit #1"):
            apply_edits(body, edits)

    def test_atomic_on_failure_first_applied_second_fails(self) -> None:
        body = "original"
        edits = [
            EditOp(old_string="original", new_string="modified"),
            EditOp(old_string="not-found", new_string="x"),
        ]
        with pytest.raises(PatchError):
            apply_edits(body, edits)
        # Function returns nothing on error (raises), so no partial state to check
        # The key contract is: raises PatchError, does NOT return a partial result

    def test_old_string_must_be_unique_without_replace_all(self) -> None:
        body = "aaa bbb aaa"
        edits = [EditOp(old_string="aaa", new_string="ccc")]
        with pytest.raises(PatchError, match="matches 2 times"):
            apply_edits(body, edits)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_patch.py -v`
Expected: FAIL with ImportError

- [ ] **Step 3: Write minimal implementation**

Create `src/patch.py`:

```python
"""Edit/patch application: apply structured edit operations to wiki page bodies."""

from __future__ import annotations

from src.models import EditOp


class PatchError(Exception):
    """Raised when an edit operation cannot be applied."""


def apply_edits(body: str, edits: list[EditOp]) -> str:
    """Apply edits sequentially to an in-memory copy. Raises PatchError on any failure."""
    working = body
    for i, edit in enumerate(edits):
        count = working.count(edit.old_string)
        if count == 0:
            raise PatchError(f"Edit #{i}: old_string not found")
        if count > 1 and not edit.replace_all:
            raise PatchError(f"Edit #{i}: matches {count} times, set replace_all=True")
        if edit.replace_all:
            working = working.replace(edit.old_string, edit.new_string)
        else:
            working = working.replace(edit.old_string, edit.new_string, 1)
    return working
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_patch.py -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
git add src/patch.py tests/test_patch.py
git commit -m "feat: add patch module with apply_edits and PatchError"
```

---

### Task 3: Add get_edit_prompt to config

**Files:**
- Modify: `src/config.py:100-109` (after `get_merge_prompt`)
- Modify: `schema.yaml:47-75` (prompts section)

- [ ] **Step 1: Write the failing test**

Add to `tests/test_config.py` (the file already exists — check its structure first and add a new test class):

```python
class TestGetEditPrompt:
    def test_returns_default_when_not_in_schema(self, tmp_path: Path) -> None:
        import yaml

        schema_file = tmp_path / "schema.yaml"
        schema_file.write_text(yaml.dump({"prompts": {"ingest_system": "x"}}))

        from src.config import Settings, get_edit_prompt, load_schema

        # Override settings
        import src.config as cfg

        old_settings = cfg._settings
        old_schema = cfg._schema_cache
        cfg._settings = Settings(schema_path=schema_file)
        cfg._schema_cache = None
        try:
            result = get_edit_prompt()
            assert "edit" in result.lower() or "patch" in result.lower()
        finally:
            cfg._settings = old_settings
            cfg._schema_cache = old_schema
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_config.py::TestGetEditPrompt -v`
Expected: FAIL with ImportError or AttributeError

- [ ] **Step 3: Write minimal implementation**

Add to `src/config.py` after `get_merge_prompt()`:

```python
def get_edit_prompt() -> str:
    """Return the edit/patch system prompt from schema.yaml."""
    schema = load_schema()
    prompts = schema.get("prompts", {})
    return prompts.get(
        "edit_system",
        "You are a knowledge engineer updating wiki pages. Compare the existing page "
        "with new content and generate minimal edit operations. Each old_string must be "
        "an exact verbatim snippet from the existing body (including whitespace and "
        "newlines). Only modify what needs changing. Preserve all [[WikiLinks]].",
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_config.py::TestGetEditPrompt -v`
Expected: PASS

- [ ] **Step 5: Add edit_system prompt to schema.yaml**

Add to `schema.yaml` in the `prompts:` section, after `merge_system:`:

```yaml
  edit_system: |
    You are a knowledge engineer updating wiki pages with minimal edits.
    Compare the existing page body with the new content and generate only
    the edit operations needed to merge new information.

    Rules:
    - old_string must be an EXACT verbatim snippet from the existing body
      (whitespace, newlines, indentation must match perfectly)
    - Each old_string must be unique in the body unless replace_all=True
    - Only generate edits for content that actually needs to change
    - Preserve all [[WikiLinks]] from both versions
    - Use the provided tag vocabulary when suggesting tags_to_add
```

- [ ] **Step 6: Commit**

```bash
git add src/config.py schema.yaml tests/test_config.py
git commit -m "feat: add edit_system prompt and get_edit_prompt config"
```

---

### Task 4: Rewrite merge_page with patch-first flow

**Files:**
- Modify: `src/merge.py` (full rewrite of `merge_page()`)
- Modify: `tests/test_merge.py` (update `TestMergePage`)

- [ ] **Step 1: Write the failing tests**

Replace the `TestMergePage` class in `tests/test_merge.py` with:

```python
class TestMergePagePatchSuccess:
    @pytest.mark.asyncio
    async def test_patch_succeeds_on_first_attempt(self) -> None:
        from unittest.mock import AsyncMock, patch

        from src.models import EditOp, PatchedPage

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
        new_page = GeneratedPage(
            title="BERT",
            page_type=PageType.ENTITY,
            tags=["nlp", "pre-training"],
            confidence=Confidence.HIGH,
            body="# BERT\n\nBidirectional encoder with masked language modeling.",
            related_titles=["Transformer Architecture"],
        )

        mock_patched = PatchedPage(
            edits=[
                EditOp(
                    old_string="Bidirectional encoder.",
                    new_string="Bidirectional encoder with masked language modeling.",
                ),
            ],
            tags_to_add=["pre-training"],
            confidence=Confidence.HIGH,
        )

        with patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = mock_patched
            fm, body = await merge_page(existing_page, new_page, "articles/bert-guide.md")

        assert "masked language modeling" in body
        assert "pre-training" in fm.tags
        assert mock_llm.call_count == 1

    @pytest.mark.asyncio
    async def test_patch_retries_on_failure_then_succeeds(self) -> None:
        from unittest.mock import AsyncMock, patch

        from src.models import EditOp, PatchedPage
        from src.patch import PatchError

        existing_page = WikiPage(
            path="bert.md",
            frontmatter=WikiFrontmatter(
                title="BERT",
                page_type=PageType.ENTITY,
                sources=["papers/bert.pdf"],
                tags=["nlp"],
                created=date(2026, 1, 1),
                updated=date(2026, 1, 1),
            ),
            body="# BERT\n\nBidirectional encoder.",
        )
        new_page = GeneratedPage(
            title="BERT",
            page_type=PageType.ENTITY,
            tags=["nlp"],
            confidence=Confidence.MEDIUM,
            body="# BERT\n\nUpdated content.",
        )

        # First call: bad edit (old_string not in body)
        bad_patch = PatchedPage(
            edits=[EditOp(old_string="NOT IN BODY", new_string="x")],
            tags_to_add=[],
            confidence=Confidence.MEDIUM,
        )
        # Second call: good edit
        good_patch = PatchedPage(
            edits=[EditOp(old_string="Bidirectional encoder.", new_string="Updated content.")],
            tags_to_add=[],
            confidence=Confidence.MEDIUM,
        )

        with patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.side_effect = [bad_patch, good_patch]
            fm, body = await merge_page(existing_page, new_page, "new.pdf")

        assert body == "Updated content."
        assert mock_llm.call_count == 2

    @pytest.mark.asyncio
    async def test_falls_back_to_rewrite_after_3_patch_failures(self) -> None:
        from unittest.mock import AsyncMock, patch

        from src.models import PatchedPage
        from src.patch import PatchError

        existing_page = WikiPage(
            path="bert.md",
            frontmatter=WikiFrontmatter(
                title="BERT",
                page_type=PageType.ENTITY,
                sources=["papers/bert.pdf"],
                tags=["nlp"],
                created=date(2026, 1, 1),
                updated=date(2026, 1, 1),
            ),
            body="# BERT\n\nBidirectional encoder.",
        )
        new_page = GeneratedPage(
            title="BERT",
            page_type=PageType.ENTITY,
            tags=["nlp"],
            confidence=Confidence.MEDIUM,
            body="# BERT\n\nUpdated content.",
        )

        # All 3 patch attempts fail
        bad_patch = PatchedPage(
            edits=[EditOp(old_string="NOT IN BODY", new_string="x")],
            tags_to_add=[],
            confidence=Confidence.MEDIUM,
        )
        mock_merged = MergedPage(
            body="# BERT\n\nBidirectional encoder. Updated content.",
            tags=["nlp"],
            confidence=Confidence.MEDIUM,
        )

        with patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.side_effect = [bad_patch, bad_patch, bad_patch, mock_merged]
            fm, body = await merge_page(existing_page, new_page, "new.pdf")

        assert "Updated content" in body
        assert mock_llm.call_count == 4  # 3 patch + 1 rewrite


class TestMergeFrontmatter:
    """Keep all existing _merge_frontmatter tests unchanged."""
```

Note: The existing `TestMergeFrontmatter` class stays as-is. Only `TestMergePage` is replaced.

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_merge.py::TestMergePagePatchSuccess -v`
Expected: FAIL (old `merge_page` doesn't use patch logic yet)

- [ ] **Step 3: Rewrite merge_page implementation**

Replace the `merge_page()` function in `src/merge.py` (lines 76-127) with:

```python
async def merge_page(
    existing: WikiPage,
    new_page: GeneratedPage,
    source_path: str,
) -> tuple[WikiFrontmatter, str]:
    """Merge existing page with new generated page via edit/patch or full rewrite.

    Tries patch-first (up to 3 attempts with error context on retry).
    Falls back to full rewrite via MergedPage if all patch attempts fail.
    """
    from src.patch import PatchError, apply_edits

    max_patch_attempts = 3
    last_error: str | None = None

    for attempt in range(max_patch_attempts):
        messages = _build_patch_messages(existing, new_page, source_path, last_error)
        result = await complete_structured(
            messages=messages,
            response_model=PatchedPage,
            temperature=0.2,
        )

        try:
            body = apply_edits(existing.body, result.edits)
            logger.info(
                "patched page title=%s attempt=%d edits=%d",
                existing.frontmatter.title,
                attempt + 1,
                len(result.edits),
            )
            return _merge_frontmatter(
                existing_fm=existing.frontmatter,
                new_page=new_page,
                merged_body=body,
                merged_tags=list(existing.frontmatter.tags) + result.tags_to_add,
                merged_confidence=result.confidence,
                source_path=source_path,
            )
        except PatchError as e:
            last_error = str(e)
            logger.warning("patch attempt %d failed for title=%s: %s", attempt + 1, existing.frontmatter.title, e)

    # Fallback: full rewrite
    logger.info("falling back to rewrite for title=%s", existing.frontmatter.title)
    messages = _build_rewrite_messages(existing, new_page, source_path)
    result = await complete_structured(
        messages=messages,
        response_model=MergedPage,
        temperature=0.2,
    )

    logger.info("rewrote page title=%s", existing.frontmatter.title)
    return _merge_frontmatter(
        existing_fm=existing.frontmatter,
        new_page=new_page,
        merged_body=result.body,
        merged_tags=result.tags,
        merged_confidence=result.confidence,
        source_path=source_path,
    )
```

Add the two helper functions to `src/merge.py`:

```python
def _build_patch_messages(
    existing: WikiPage,
    new_page: GeneratedPage,
    source_path: str,
    last_error: str | None = None,
) -> list[dict[str, str]]:
    """Build LLM messages for patch-mode merge."""
    system_prompt = get_edit_prompt()
    allowed_tags = get_allowed_tags()
    if allowed_tags:
        system_prompt += "\n\nPreferred tags (use these when applicable): " + ", ".join(allowed_tags)

    user_content = (
        f"Compare the existing wiki page with new content and generate edit operations to merge them.\n\n"
        f"=== EXISTING PAGE ===\n"
        f"Title: {existing.frontmatter.title}\n\n"
        f"{existing.body}\n\n"
        f"=== NEW CONTENT (from source: {source_path}) ===\n"
        f"Title: {new_page.title}\n\n"
        f"{new_page.body}\n\n"
        f"Generate minimal edit operations to add new information to the existing page."
    )

    if last_error:
        user_content += (
            f"\n\nPrevious edit attempt failed with error: {last_error}\n"
            f"Check that old_string exactly matches text in the existing page "
            f"(including spaces, newlines, indentation) and correct it."
        )

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]


def _build_rewrite_messages(
    existing: WikiPage,
    new_page: GeneratedPage,
    source_path: str,
) -> list[dict[str, str]]:
    """Build LLM messages for rewrite-mode merge (fallback)."""
    system_prompt = get_merge_prompt()
    allowed_tags = get_allowed_tags()
    if allowed_tags:
        system_prompt += "\n\nPreferred tags (use these when applicable): " + ", ".join(allowed_tags)

    return [
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

Update the imports at the top of `src/merge.py`:

```python
from src.models import (
    Confidence,
    GeneratedPage,
    MergedPage,
    PatchedPage,
    WikiFrontmatter,
    WikiPage,
)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_merge.py -v`
Expected: All PASS (both old frontmatter tests and new patch tests)

- [ ] **Step 5: Run full test suite to check for regressions**

Run: `uv run pytest -v`
Expected: All PASS

- [ ] **Step 6: Commit**

```bash
git add src/merge.py tests/test_merge.py
git commit -m "feat: rewrite merge_page with patch-first, retry, rewrite-fallback flow"
```

---

### Task 5: Run full test suite and lint

**Files:** None (validation only)

- [ ] **Step 1: Run full test suite**

Run: `uv run pytest -v`
Expected: All PASS

- [ ] **Step 2: Run lint**

Run: `make lint`
Expected: No errors

- [ ] **Step 3: Commit if any lint fixes needed**

```bash
git add -A
git commit -m "style: lint fixes for edit/patch feature"
```

---

### Task 6: Real source end-to-end test

**Files:** None (manual validation)

- [ ] **Step 1: Create a minimal test source file**

Create a small markdown file in `sources/` with content that overlaps with an existing wiki topic, so ingest triggers the merge path.

- [ ] **Step 2: Run ingest and check logs**

Run: `uv run wiki ingest <source-file> --verbose` (or check log output)
Expected: Log shows "patched page" (patch path) or "falling back to rewrite" (rewrite fallback)

- [ ] **Step 3: Verify wiki page content**

Run: `uv run wiki stats` and read the updated page to confirm content was correctly merged.

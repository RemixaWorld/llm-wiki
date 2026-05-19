# Edit/Patch Mechanism for Wiki Page Updates

## Problem

The current `merge_page()` sends both the full existing body and full new body to the LLM, which returns a completely rewritten body. This wastes tokens and is inefficient — most merges only need small, targeted changes.

## Design

Replace the full-rewrite merge with an edit/patch mechanism inspired by Claude Code's Edit/MultiEdit tools. LLM generates `old_string`/`new_string` edit operations instead of rewriting the entire page body.

### Strategy: Patch-first with Retry + Rewrite Fallback

1. **Attempt 1–3**: LLM returns `PatchedPage` (edit operations), program applies them
2. **Retry with error context**: Each failure injects the error message into the next LLM call so it can correct the `old_string`
3. **Fallback**: After 3 patch failures, degrade to full rewrite via `MergedPage`
4. **Final failure**: If rewrite also fails, raise exception and log

### Data Models (`src/models.py`)

```python
class EditOp(BaseModel):
    """Single edit: exact string replacement."""
    old_string: str = Field(description="Exact text from existing body to replace, must be unique")
    new_string: str = Field(description="Replacement text. Empty string = deletion")
    replace_all: bool = Field(default=False, description="True to replace all occurrences")

class PatchedPage(BaseModel):
    """LLM output: a batch of edit operations + metadata delta."""
    edits: list[EditOp] = Field(description="Edit operations to apply in order")
    tags_to_add: list[str] = Field(default_factory=list, description="Tags to add (incremental)")
    confidence: Confidence = Confidence.MEDIUM
```

`MergedPage` (existing) is reused as the rewrite fallback model.

### Application Logic (`src/patch.py` — new module)

```python
class PatchError(Exception): ...

def apply_edits(body: str, edits: list[EditOp]) -> str:
    """Apply edits sequentially to an in-memory copy. Raises PatchError on any failure."""
    working = body
    for i, edit in enumerate(edits):
        count = working.count(edit.old_string)
        if count == 0:
            raise PatchError(f"Edit #{i}: old_string not found")
        if count > 1 and not edit.replace_all:
            raise PatchError(f"Edit #{i}: matches {count} times, set replace_all=True")
        working = working.replace(edit.old_string, edit.new_string, -1 if edit.replace_all else 1)
    return working
```

- Sequential application: each edit operates on the result of the previous edit
- Atomic: any edit failure aborts the entire batch, nothing written to disk

### Merge Flow (`src/merge.py`)

`merge_page()` rewritten to:

1. Build patch prompt with existing page + new content
2. Loop up to 3 times:
   - Call LLM with `response_model=PatchedPage`
   - Try `apply_edits()` on the existing body
   - On success: merge frontmatter deterministically and return
   - On `PatchError`: log warning, inject error into next attempt's prompt
3. After 3 failures: call LLM with `response_model=MergedPage` (full rewrite, existing `merge_system` prompt)
4. `_merge_frontmatter()` reused unchanged for both paths

Frontmatter merge remains deterministic (no LLM): sources union, tags union, confidence takes higher, updated set to today.

### Prompts (`schema.yaml`)

New `edit_system` prompt:
- Role: knowledge engineer (same as ingest)
- Instruction: analyze diff between existing and new content, generate minimal edit operations
- Constraints:
  - `old_string` must be an exact verbatim snippet from the existing body (whitespace, newlines, indentation must match)
  - Each `old_string` must be unique in the body unless `replace_all=True`
  - Only modify what needs changing; leave unchanged content alone
  - Preserve wikilink syntax `[[title]]`

Retry prompt augmentation:
```
Previous edit attempt failed with error: {last_error}
Check that old_string exactly matches text in the existing page (including spaces, newlines, indentation) and correct it.
```

The existing `merge_system` prompt is reused for the rewrite fallback path.

### File Changes

| File | Change |
|------|--------|
| `src/patch.py` | **New** — `apply_edits()`, `PatchError` |
| `src/models.py` | Add `EditOp`, `PatchedPage` |
| `src/merge.py` | Rewrite `merge_page()` — 3x patch → rewrite fallback |
| `src/config.py` | Add `get_edit_prompt()` |
| `schema.yaml` | Add `edit_system` prompt |
| `src/ingest.py` | No changes (calls `merge_page()` transparently) |

### Testing Strategy

**Phase 1: Mock unit tests (no API keys)**
- `apply_edits()`: single edit, multiple sequential edits, match failure, `replace_all`, empty body
- `merge_page()`: mock LLM returning `PatchedPage` — verify patch success path, 3-retry path, rewrite fallback path

**Phase 2: Real source end-to-end test**
- Pick 1-2 existing source files from `data/` or `sources/`
- Run `wiki ingest` to trigger merge on pages that already exist
- Verify patch path activates (check logs for patch success vs rewrite fallback)
- Verify page content is correctly merged

### Future Extension

- Query persistence: when `query.py` needs to update existing pages, reuse `merge_page()` directly
- Lint auto-fix: edit operations could be used for automated wiki page corrections

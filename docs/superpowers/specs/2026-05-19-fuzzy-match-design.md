# Fuzzy Matching for apply_edits()

## Problem

LLM-generated `old_string` often has minor whitespace or quote differences from the actual wiki page body (trailing whitespace on lines, curly vs straight quotes). The current `apply_edits()` only does exact matching, causing unnecessary retry cycles that consume LLM tokens.

## Design

Add fuzzy matching inside `apply_edits()` as a transparent fallback after exact matching fails, following Claude Code's Edit tool implementation pattern.

### 4-Level Fallback

Within each patch attempt:

1. **Exact match** — `str.find()` on raw body
2. **Fuzzy match** — normalize trailing whitespace + quotes, then match
3. **Error retry** — inject error context into next LLM call (up to 3 attempts)
4. **Full rewrite** — degrade to `MergedPage` after 3 failures

Levels 1–2 are inside `apply_edits()` (no LLM call). Levels 3–4 remain in `merge_page()` unchanged.

### Fuzzy Matching Algorithm

Following Claude Code's approach — two normalizations, no heuristics:

1. **Trailing whitespace stripping**: strip each line's trailing whitespace
2. **Quote normalization**: curly quotes (`' ' " "`) → straight quotes (`' "`)

Both body and old_string are normalized, then matched via `str.find()`. A position offset map (`offsets[i]` = normalized position `i` → original position) maps the match back to the original body for replacement.

### New Functions in `src/patch.py`

```python
def _normalize_with_offsets(s: str) -> tuple[str, list[int]]:
    """Normalize string and return position mapping.

    Returns (normalized, offsets) where offsets[i] is the position in the
    original string corresponding to position i in the normalized string.
    Normalization: strip trailing whitespace per line, curly quotes → straight.
    """

def _fuzzy_replace(body: str, old_string: str, new_string: str, replace_all: bool) -> str:
    """Try fuzzy match + replace on body. Raises PatchError on no match or ambiguity."""
```

`apply_edits()` changes to: exact match first per edit → if fails, call `_fuzzy_replace()` → if also fails, raise `PatchError`.

### Unchanged Files

- `src/merge.py` — no changes (fuzzy matching is transparent inside `apply_edits()`)
- `src/models.py` — no changes (`EditOp`, `PatchedPage` unchanged)
- `schema.yaml` — no changes

### Testing

New tests in `tests/test_patch.py`:

- Trailing whitespace difference: body has trailing spaces, old_string doesn't → fuzzy match succeeds
- Curly quote difference: body has straight quotes, old_string has curly → fuzzy match succeeds
- Exact match found: fuzzy logic not triggered (verify via no fallback)
- Fuzzy match uniqueness: normalized old_string matches multiple locations → PatchError
- Combined: trailing whitespace + curly quotes together
- `replace_all=True` with fuzzy matching

### File Changes

| File | Change |
|------|--------|
| `src/patch.py` | Rewrite `apply_edits()` with exact→fuzzy fallback; add `_normalize_with_offsets()`, `_fuzzy_replace()` |
| `tests/test_patch.py` | Add fuzzy matching tests |

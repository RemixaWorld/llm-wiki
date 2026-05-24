# Fuzzy Matching Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add fuzzy matching (trailing whitespace stripping + quote normalization) as a transparent fallback inside `apply_edits()`, reducing unnecessary LLM retry cycles.

**Architecture:** Two new private functions in `src/patch.py` — `_normalize_with_offsets()` builds a normalized string with position mapping, `_fuzzy_replace()` uses it for match-and-replace. `apply_edits()` tries exact match first, then falls back to `_fuzzy_replace()`. No changes to `merge.py` or `models.py`.

**Tech Stack:** Python 3.13+, pytest, existing `EditOp`/`PatchError` types.

---

### Task 1: `_normalize_with_offsets()` helper

**Files:**
- Modify: `src/patch.py`
- Test: `tests/test_patch.py`

- [ ] **Step 1: Write failing tests for `_normalize_with_offsets()`**

Add to `tests/test_patch.py` — import the new function and add a new test class:

```python
from src.patch import PatchError, _normalize_with_offsets, apply_edits


class TestNormalizeWithOffsets:
    def test_no_change_needed(self) -> None:
        text = "hello world"
        norm, offsets = _normalize_with_offsets(text)
        assert norm == "hello world"
        assert offsets == list(range(len(text)))

    def test_strips_trailing_spaces_per_line(self) -> None:
        text = "line1   \nline2  \nline3"
        norm, offsets = _normalize_with_offsets(text)
        assert norm == "line1\nline2\nline3"

    def test_curly_quotes_to_straight(self) -> None:
        text = "‘hello’ “world”"
        norm, offsets = _normalize_with_offsets(text)
        assert norm == "'hello' \"world\""

    def test_offsets_map_back_to_original(self) -> None:
        text = "ab  \ncd"
        norm, offsets = _normalize_with_offsets(text)
        # norm = "ab\ncd", offsets maps each norm position to original
        assert offsets[0] == 0  # 'a'
        assert offsets[1] == 1  # 'b'
        assert offsets[2] == 2  # '\n' (original pos 4, trailing spaces stripped)
        assert offsets[3] == 5  # 'c'
        assert offsets[4] == 6  # 'd'

    def test_combined_trailing_ws_and_quotes(self) -> None:
        text = "‘hi’  \n“bye”"
        norm, offsets = _normalize_with_offsets(text)
        assert norm == "'hi'\n\"bye\""
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_patch.py::TestNormalizeWithOffsets -v`
Expected: FAIL — `ImportError: cannot import name '_normalize_with_offsets'`

- [ ] **Step 3: Implement `_normalize_with_offsets()`**

Add to `src/patch.py` after the `PatchError` class:

```python
def _normalize_with_offsets(s: str) -> tuple[str, list[int]]:
    """Normalize string and return position mapping.

    Returns (normalized, offsets) where offsets[i] is the position in the
    original string corresponding to position i in the normalized string.
    Normalization: strip trailing whitespace per line, curly quotes -> straight.
    """
    CURLY_QUOTES = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"'})

    lines = s.split("\n")
    norm_chars: list[str] = []
    offsets: list[int] = []

    pos = 0
    for line_idx, line in enumerate(lines):
        stripped = line.rstrip()
        translated = stripped.translate(CURLY_QUOTES)
        for j, ch in enumerate(translated):
            norm_chars.append(ch)
            offsets.append(pos + j)
        pos += len(line)
        if line_idx < len(lines) - 1:
            norm_chars.append("\n")
            offsets.append(pos)
            pos += 1  # skip the \n in original

    return "".join(norm_chars), offsets
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_patch.py::TestNormalizeWithOffsets -v`
Expected: 5 PASSED

- [ ] **Step 5: Commit**

```bash
git add src/patch.py tests/test_patch.py
git commit -m "feat: add _normalize_with_offsets() helper for fuzzy matching"
```

---

### Task 2: `_fuzzy_replace()` helper

**Files:**
- Modify: `src/patch.py`
- Test: `tests/test_patch.py`

- [ ] **Step 1: Write failing tests for `_fuzzy_replace()`**

Add to `tests/test_patch.py`:

```python
from src.patch import PatchError, _fuzzy_replace, _normalize_with_offsets, apply_edits


class TestFuzzyReplace:
    def test_trailing_whitespace_difference(self) -> None:
        body = "line1  \nline2  \nline3"
        result = _fuzzy_replace(body, "line1\nline2", "AAA\nBBB", replace_all=False)
        assert result == "AAA\nBBB  \nline3"

    def test_curly_quote_difference(self) -> None:
        body = "He said “hello”"
        result = _fuzzy_replace(body, 'He said "hello"', "She replied", replace_all=False)
        assert result == "She replied"

    def test_exact_match_still_works(self) -> None:
        body = "exact match here"
        result = _fuzzy_replace(body, "exact match", "perfect", replace_all=False)
        assert result == "perfect here"

    def test_ambiguous_match_raises(self) -> None:
        body = "line1  \nline2  \nline1  \nline2"
        with pytest.raises(PatchError, match="fuzzy match"):
            _fuzzy_replace(body, "line1\nline2", "x", replace_all=False)

    def test_no_match_raises(self) -> None:
        body = "something else entirely"
        with pytest.raises(PatchError, match="fuzzy match"):
            _fuzzy_replace(body, "not here", "x", replace_all=False)

    def test_replace_all_with_fuzzy(self) -> None:
        body = "foo  \nbar  \nfoo  \nbar"
        result = _fuzzy_replace(body, "foo\nbar", "X\nY", replace_all=True)
        assert result == "X\nY  \nX\nY"

    def test_combined_trailing_ws_and_quotes(self) -> None:
        body = "‘hello’  \nworld"
        result = _fuzzy_replace(body, "'hello'\nworld", "HI", replace_all=False)
        assert result == "HI"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_patch.py::TestFuzzyReplace -v`
Expected: FAIL — `ImportError: cannot import name '_fuzzy_replace'`

- [ ] **Step 3: Implement `_fuzzy_replace()`**

Add to `src/patch.py` after `_normalize_with_offsets()`:

```python
def _fuzzy_replace(body: str, old_string: str, new_string: str, replace_all: bool) -> str:
    """Try fuzzy match + replace on body. Raises PatchError on no match or ambiguity."""
    norm_body, body_offsets = _normalize_with_offsets(body)
    norm_old, _old_offsets = _normalize_with_offsets(old_string)

    if not replace_all:
        idx = norm_body.find(norm_old)
        if idx == -1:
            raise PatchError("fuzzy match: old_string not found after normalization")
        next_idx = norm_body.find(norm_old, idx + 1)
        if next_idx != -1:
            raise PatchError("fuzzy match: old_string matches multiple locations after normalization")
        orig_start = body_offsets[idx]
        orig_end = body_offsets[idx + len(norm_old) - 1] + 1
        return body[:orig_start] + new_string + body[orig_end:]

    # replace_all: find all non-overlapping matches
    parts: list[str] = []
    last_end = 0
    search_start = 0
    while True:
        idx = norm_body.find(norm_old, search_start)
        if idx == -1:
            break
        orig_start = body_offsets[idx]
        orig_end = body_offsets[idx + len(norm_old) - 1] + 1
        parts.append(body[last_end:orig_start])
        parts.append(new_string)
        last_end = orig_end
        search_start = idx + len(norm_old)
    if not parts:
        raise PatchError("fuzzy match: old_string not found after normalization")
    parts.append(body[last_end:])
    return "".join(parts)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_patch.py::TestFuzzyReplace -v`
Expected: 7 PASSED

- [ ] **Step 5: Commit**

```bash
git add src/patch.py tests/test_patch.py
git commit -m "feat: add _fuzzy_replace() helper for fuzzy matching"
```

---

### Task 3: Integrate fuzzy fallback into `apply_edits()`

**Files:**
- Modify: `src/patch.py` (rewrite `apply_edits()`)
- Test: `tests/test_patch.py`

- [ ] **Step 1: Write failing tests for fuzzy fallback in `apply_edits()`**

Add to `tests/test_patch.py`:

```python
class TestApplyEditsFuzzyFallback:
    def test_fuzzy_match_used_when_exact_fails(self) -> None:
        """Body has trailing spaces, old_string doesn't — fuzzy fallback succeeds."""
        body = "Hello   \nWorld"
        edits = [EditOp(old_string="Hello\nWorld", new_string="Hi\nEarth")]
        assert apply_edits(body, edits) == "Hi   \nEarth"

    def test_fuzzy_match_with_curly_quotes(self) -> None:
        body = "He said “hello” to me"
        edits = [EditOp(old_string='He said "hello" to me', new_string="She said goodbye")]
        assert apply_edits(body, edits) == "She said goodbye"

    def test_exact_match_preferred_no_fuzzy(self) -> None:
        """When exact match works, fuzzy is not needed — result is exact."""
        body = "exact match here"
        edits = [EditOp(old_string="exact match", new_string="perfect")]
        assert apply_edits(body, edits) == "perfect here"

    def test_fuzzy_ambiguous_raises_patch_error(self) -> None:
        body = "line1  \nline2  \nline1  \nline2"
        edits = [EditOp(old_string="line1\nline2", new_string="x")]
        with pytest.raises(PatchError):
            apply_edits(body, edits)

    def test_fuzzy_combined_ws_and_quotes(self) -> None:
        body = "‘hello’   \nworld  "
        edits = [EditOp(old_string="'hello'\nworld", new_string="greetings")]
        assert apply_edits(body, edits) == "greetings   \nworld  "

    def test_fuzzy_replace_all(self) -> None:
        body = "foo  \nbar  \nfoo  \nbar"
        edits = [EditOp(old_string="foo\nbar", new_string="X\nY", replace_all=True)]
        assert apply_edits(body, edits) == "X\nY  \nX\nY"

    def test_no_match_at_all_raises_patch_error(self) -> None:
        body = "completely different content"
        edits = [EditOp(old_string="not here at all", new_string="x")]
        with pytest.raises(PatchError, match="old_string not found"):
            apply_edits(body, edits)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_patch.py::TestApplyEditsFuzzyFallback -v`
Expected: Some tests FAIL — current `apply_edits()` has no fuzzy fallback.

- [ ] **Step 3: Rewrite `apply_edits()` with exact → fuzzy fallback**

Replace the entire `apply_edits()` function in `src/patch.py`:

```python
def apply_edits(body: str, edits: list[EditOp]) -> str:
    """Apply edits sequentially to an in-memory copy. Raises PatchError on any failure.

    For each edit, tries exact match first, then falls back to fuzzy match
    (trailing whitespace stripping + quote normalization).
    """
    working = body
    for i, edit in enumerate(edits):
        count = working.count(edit.old_string)
        if count == 1 or (count > 1 and edit.replace_all):
            if edit.replace_all:
                working = working.replace(edit.old_string, edit.new_string)
            else:
                working = working.replace(edit.old_string, edit.new_string, 1)
        elif count == 0:
            try:
                working = _fuzzy_replace(working, edit.old_string, edit.new_string, edit.replace_all)
            except PatchError:
                raise PatchError(f"Edit #{i}: old_string not found")
        else:
            # count > 1 and not replace_all
            raise PatchError(f"Edit #{i}: matches {count} times, set replace_all=True")
    return working
```

- [ ] **Step 4: Run all tests to verify everything passes**

Run: `uv run pytest tests/test_patch.py -v`
Expected: All tests PASS (existing 12 + new 19 = 31 total).

- [ ] **Step 5: Commit**

```bash
git add src/patch.py tests/test_patch.py
git commit -m "feat: integrate fuzzy matching fallback into apply_edits()"
```

---

### Task 4: Final verification

**Files:** None (verification only)

- [ ] **Step 1: Run full test suite**

Run: `uv run pytest tests/ -v`
Expected: All tests PASS.

- [ ] **Step 2: Run linter**

Run: `make lint`
Expected: No errors.

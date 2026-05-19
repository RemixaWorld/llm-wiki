"""Edit/patch application: apply structured edit operations to wiki page bodies."""

from __future__ import annotations

from src.models import EditOp


class PatchError(Exception):
    """Raised when an edit operation cannot be applied."""


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

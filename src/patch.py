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

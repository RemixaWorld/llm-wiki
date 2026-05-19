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

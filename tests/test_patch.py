"""Tests for edit/patch application logic."""

from __future__ import annotations

import pytest

from src.models import EditOp
from src.patch import PatchError, _normalize_with_offsets, apply_edits


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

    def test_old_string_must_be_unique_without_replace_all(self) -> None:
        body = "aaa bbb aaa"
        edits = [EditOp(old_string="aaa", new_string="ccc")]
        with pytest.raises(PatchError, match="matches 2 times"):
            apply_edits(body, edits)


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
        assert offsets[2] == 4  # '\n' (original pos 4)
        assert offsets[3] == 5  # 'c'
        assert offsets[4] == 6  # 'd'

    def test_combined_trailing_ws_and_quotes(self) -> None:
        text = "‘hi’  \n“bye”"
        norm, offsets = _normalize_with_offsets(text)
        assert norm == "'hi'\n\"bye\""

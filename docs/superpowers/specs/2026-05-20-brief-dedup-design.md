# Brief-Based Merge Decision & Dedup Design

## Problem

Two issues with the current merge pipeline:

1. **Scalability**: Every ingest batch injects ALL existing wiki page titles into the LLM prompt. With thousands of pages, this becomes prohibitively expensive and the LLM struggles to use the list effectively.
2. **Unnecessary merges**: Any title collision triggers the full merge pipeline (patch/rewrite), even when the new source adds no new information about the topic.

## Design

Add a `brief` metadata field to wiki pages. Replace the global title list injection with a brief-based collision analysis mechanism that decides whether merging is worthwhile. Additionally, use brief similarity to detect title variants (different names for the same topic).

### Data Model Changes

**`WikiFrontmatter`** — new field:

```python
brief: str = ""  # short summary of what this page covers
```

**`GeneratedPage`** — new field:

```python
brief: str  # LLM generates this alongside the page
```

**`Checkpoint`** — new field:

```python
generated_briefs: dict[str, str] = {}  # {title: brief} for titles generated in previous batches
```

Needed because a skipped page (brief analysis said SKIP) is not on disk, but subsequent batches within the same source still need its brief for consistency.

New models for LLM output:

```python
class MergeDecision(BaseModel):
    """Scenario A: should we merge new content into existing page?"""
    action: Literal["MERGE", "SKIP"]
    reason: str

class TopicMatchDecision(BaseModel):
    """Scenario B: do two briefs describe the same topic?"""
    same_topic: bool
    reason: str
```

### Ingest Pipeline Changes

**Remove global title list**: Delete the `list_wiki_pages` loop and `wiki_titles` parameter. Keep `existing_titles` (intra-source batch titles) so the LLM uses consistent titles within the same source.

**Per-GeneratedPage processing in `process_batches_node`:**

```
For each GeneratedPage:

  1. Exact collision: get_page_by_title(title) → exists on disk?
     If yes → Scenario A (brief analysis with full context)

  2. No exact collision → BM25 brief search → similar briefs found?
     If yes → Scenario B (brief vs brief comparison)
       If SAME topic → Scenario A (brief analysis with full context)
       If DIFFERENT → new page

  3. No collision at all → new page
```

**MERGE**: Existing `merge_page()` patch→rewrite flow. After merge, LLM regenerates brief (body changed, old brief may be inaccurate).

**SKIP**: No disk write, no merge call. Record title + brief in `cp.generated_briefs` for subsequent batch reference.

**NEW**: Write page to disk (with brief), update checkpoint, add brief to BM25 index.

### Brief Analysis Mechanism

**Scenario A — Exact collision (or fuzzy collision confirmed as same topic):**

One lightweight LLM call. Input: existing page's brief + new GeneratedPage's full body.

```
Existing page "{title}" covers: {brief}
New content generated about this topic: {body}

Does the new content add significant information not covered by the existing page?
Answer MERGE or SKIP. When uncertain, choose MERGE.
```

Output: `MergeDecision(action="MERGE"|"SKIP", reason=...)`

**Scenario B — Fuzzy collision (BM25 found similar brief):**

One lightweight LLM call. Input: existing page candidate's brief + new page's brief.

```
Existing page "{title}" covers: {existing_brief}
New page "{new_title}" covers: {new_brief}

Are these about the same topic?
Answer SAME or DIFFERENT.
```

Output: `TopicMatchDecision(same_topic=True|False, reason=...)`

If SAME → proceeds to Scenario A with full body context.

**Risk mitigation**: Both prompts include "when uncertain, choose MERGE" to prevent false skips.

**Model selection**: Use the cheapest available provider (MiniMax or Groq) for brief analysis — simple task, structured output.

### BM25 Brief Index

New `BriefIndex` class in `src/search.py`, parallel to the existing body BM25 index.

```python
class BriefIndex:
    def build(wiki_dir: Path) -> None:
        """Build index from all wiki page frontmatter.brief fields."""

    def search(query: str, top_k: int = 3) -> list[tuple[str, float]]:
        """Search briefs, return [(page_path, score), ...]."""

    def add(title: str, brief: str) -> None:
        """Incrementally add a single entry (called after new page write)."""
```

- **Build time**: Once at the start of `process_batches_node`, shared across all batches within a source.
- **Incremental update**: After each batch, `add()` for newly written pages. Skipped pages are NOT added (not on disk, should not be discoverable by other sources).
- **Threshold**: BM25 score below threshold → not a candidate. Start permissive (prefer false positives over missed dedup).
- **Cost**: Minimal — briefs are one sentence to a short paragraph each.

### Brief Lifecycle

**Creation**: LLM produces brief as part of `GeneratedPage` in `IngestResult`. Schema.yaml ingest prompt updated to require brief output. Brief length is flexible — one sentence to a short paragraph, as long as it covers the content.

**Merge**: After `merge_page()` completes, LLM regenerates brief via a lightweight call (input: merged body → output: new brief). Accuracy matters because brief drives future collision decisions.

**Skip**: Brief unchanged, page unchanged.

**Frontmatter rendering**: `render_page()` always outputs the `brief` field. `_merge_frontmatter()` delegates brief to the post-merge LLM call rather than union/max logic.

### Schema.yaml Updates

- **ingest prompt**: Add brief generation requirement for each page.
- **merge prompt**: Add brief regeneration instruction after body merge.
- **No new prompts**: Brief analysis uses inline prompts in code, not schema.yaml entries (they're simple, unlikely to need tuning).

### File Changes

| File | Change |
|------|--------|
| `src/models.py` | Add `brief` to `WikiFrontmatter`, `GeneratedPage`, `Checkpoint`; add `MergeDecision`, `TopicMatchDecision` models |
| `src/ingest.py` | Remove `wiki_titles` loading/injection; add exact collision → Scenario A, fuzzy collision → Scenario B logic in `process_batches_node` |
| `src/merge.py` | Add post-merge brief regeneration step in `merge_page()`; update `_merge_frontmatter()` for brief field |
| `src/search.py` | Add `BriefIndex` class (build / search / add) |
| `src/wiki.py` | Update `render_page()` to output `brief` field |
| `src/patch.py` | No changes |
| `schema.yaml` | Update ingest prompt (brief output), merge prompt (brief regeneration) |
| `tests/test_*.py` | New tests for brief analysis, BriefIndex, brief lifecycle |

### Out of Scope

- **Wikilink resolution**: LLM-generated `[[Title]]` may point to non-existent pages. Tracked in `learnable_docs/wikilink-resolution.md`. Deferred to future iteration.

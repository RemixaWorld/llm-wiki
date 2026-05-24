# Ingest Cost Optimization Design

**Goal:** Reduce LLM call count and cost during ingest by fixing bugs, batching decisions, limiting page generation, and optimizing prompt structure for provider caching.

**Architecture:** Six targeted changes to the existing single-step ingest pipeline. No new pipeline stages.

**Tech Stack:** Pydantic (structured output schema), tiktoken (token counting), instructor (LLM structured output)

---

## 1. Bug Fixes (planned fixes from e2e testing)

### 1.1 Skip empty title pages

**Problem:** LLM may generate `GeneratedPage` with empty `title`, written as `.md` file.

**Change:** In `process_batches_node`, after flattening `all_pages` and intra-batch dedup, skip pages where `title.strip()` is empty.

```python
# After dedup loop
all_pages = [p for p in deduped if p.title.strip()]
```

**Files:** `src/ingest.py`

### 1.2 Move BriefIndex.add() to batch end

**Problem:** `brief_idx.add()` called after each page write causes same-batch pages to fuzzy-match each other, triggering unnecessary topic_match_check → merge.

**Change:** Collect `(path, brief)` pairs during per-page processing. Call `brief_idx.add()` once after all pages in the batch are processed.

```python
batch_brief_adds: list[tuple[str, str]] = []
# ... per-page loop ...
    batch_brief_adds.append((path, gen_page.brief))
# After loop
for path, brief in batch_brief_adds:
    brief_idx.add(path, brief)
```

**Files:** `src/ingest.py`

### 1.3 Skip brief_merge_check when existing brief is empty

**Problem:** Old pages without briefs pass empty string to `brief_merge_check`, which always returns MERGE — wasting an LLM call.

**Change:** In the exact collision path, check if `existing_page.frontmatter.brief` is empty. If so, skip `brief_merge_check` and go directly to `merge_page`.

```python
if existing_page is not None:
    if existing_page.frontmatter.brief:
        decision = await brief_merge_check(...)
        if decision.action == "SKIP":
            # skip logic
            continue
    # else: no brief → always merge
    merged_fm, merged_body = await merge_page(existing_page, gen_page, source_path)
```

**Files:** `src/ingest.py`

---

## 2. Short Text Mode (< 1000 tokens)

**Problem:** 117 tokens of input generated 6+ pages. Short inputs produce disproportionate LLM calls.

**Change:** Before building batch messages, count tokens of the combined chunk text. If < 1000 tokens, use a simplified prompt that instructs the LLM to only generate `source_summary`. Concepts and entities are mentioned as `[[WikiLink]]` in the source_summary body instead of separate pages.

**Implementation:**
- Token counting uses existing `count_tokens()` from `src/extract.py`
- In `_build_batch_messages`, add `is_short: bool` parameter
- When `is_short=True`, append instruction to system prompt: "This is a short source text. Only generate the source_summary. Mention concepts and entities using [[WikiLink]] syntax within the body — do not create separate concept_pages or entity_pages."
- IngestResult model already allows empty `concept_pages` and `entity_pages` (both are lists)

**Token threshold:** 1000 tokens (measured by tiktoken cl100k_base, matching existing chunk_text logic).

**Files:** `src/ingest.py` (`_build_batch_messages`, `process_batches_node`)

---

## 3. Pluggable Ingest Modes + Importance Criteria

**Problem:** IngestResult has no limit on concept_pages or entity_pages length. LLM generates too many low-value pages. User wants to switch between modes based on available compute resources.

**Change:** Add `ingest_mode` to `schema.yaml` with two prompt variants:

```yaml
# schema.yaml
ingest_mode: focused  # "focused" or "comprehensive"
```

- **`focused` (new default):** Prompt constrains concept_pages and entity_pages to 1-3 each. Defines "important" as:
  - Core topic/thesis of the source text (not tangential mentions)
  - Entities/concepts with standalone knowledge value (worth their own page, not just an example or citation)
  - Knowledge not already covered by previously generated pages (see section 5 for titles+briefs from prior batches)

- **`comprehensive` (original behavior):** Current prompt with no limits. Extracts all concepts and entities found in the source.

**Implementation:**
- `config.py` reads `ingest_mode` from schema.yaml, exposes via `get_ingest_mode()`
- `_build_batch_messages` appends mode-specific instructions to the user message (not system prompt, for caching stability)
- IngestResult model unchanged — no `max_length` hard cap, prompt-only constraint

**Files:** `schema.yaml`, `src/config.py` (new `get_ingest_mode()`), `src/ingest.py` (`_build_batch_messages`)

---

## 4. Batch Collision Decisions (single LLM call)

**Problem:** Each collision triggers a separate `brief_merge_check` or `topic_match_check` call. N collisions = N LLM calls.

**Change:** After generating all pages in a batch, collect all collision pairs (both exact and fuzzy) before making any LLM calls. Send all pairs in a single LLM call to get MERGE/SKIP decisions. Then execute merge_page for each MERGE individually.

### New model

```python
class CollisionPair(BaseModel):
    """One collision pair for batch decision."""
    new_title: str
    existing_title: str
    existing_brief: str
    collision_type: Literal["exact", "fuzzy"]
    new_brief: str = ""  # empty for exact collisions (not needed)

class BatchCollisionDecision(BaseModel):
    """LLM output: merge/skip decisions for all collision pairs in a batch."""
    decisions: list[CollisionDecision]

class CollisionDecision(BaseModel):
    """Decision for one collision pair."""
    new_title: str
    action: Literal["MERGE", "SKIP"]
    reason: str
```

### Flow change

Current (per-page inline):
```
for each page:
    if exact collision → brief_merge_check → maybe merge_page
    if fuzzy collision → topic_match_check → brief_merge_check → maybe merge_page
    else → write new page
```

New (collect then batch):
```
collision_pairs = []
new_pages = []

for each page:
    if exact collision → add to collision_pairs
    elif fuzzy collision → add to collision_pairs
    else → add to new_pages, write immediately

if collision_pairs:
    batch_decision = await batch_collision_check(collision_pairs)  # 1 call
    for decision in batch_decision.decisions:
        if MERGE → merge_page(existing, new_page)  # per-merge call
        if SKIP → skip

for page in new_pages:
    write_page(page)
```

**Note:** Fuzzy collisions no longer need separate `topic_match_check`. The batch collision call receives all pairs with briefs and decides MERGE/SKIP in one shot — topic matching is implicit in the MERGE/SKIP judgment.

### Prompt for batch collision check

```
For each collision pair below, decide whether to MERGE the new content into
the existing page or SKIP (keep them separate).

Consider: same topic? Complementary information? Would merging lose distinct identity?
When uncertain, choose MERGE.
```

**Files:** `src/models.py` (new models), `src/merge.py` (new `batch_collision_check` function), `src/ingest.py` (restructured per-page loop)

---

## 5. Prompt Caching Optimization + Titles+Briefs for Intra-Source Context

**Problem:** Provider-side prompt caching (KV cache reuse) requires stable prompt prefixes. Dynamic content mixed into system prompts breaks caching. Also, LLM lacks visibility into what previous batches already covered, leading to duplicate concepts.

**Change:** Ensure all prompt construction follows the prefix-stability principle:

1. **System prompt:** fully static. No dynamic content appended.
   - Move `allowed_tags` injection out of system prompt into a separate user message prefix
   - `get_ingest_prompt()` result is always the same string → cacheable

2. **Message ordering:** stable prefix first, variable content last
   ```
   [system]  ← static, identical across all batches
   [user]    ← "Preferred tags: ..."              ← semi-static (same across batches in one run)
   [user]    ← "Previously generated pages:\n     ← grows per batch (titles + briefs)
               - Title: brief\n..."
   [user]    ← "Source text: ..."                 ← changes per batch
   ```

3. **Titles + briefs from prior batches:** Replace `existing_titles` (title-only list) with a structured list of titles and their briefs from `cp.generated_briefs`. This gives the LLM intra-source context — it can see what knowledge has already been extracted and focus on genuinely new concepts.

   ```python
   # Instead of:
   # "The following wiki pages already exist: A, B, C"
   # Use:
   # "Previously generated pages from this source:
   #  - "Attention Mechanism": Brief summary of attention...
   #  - "Self-Attention": How self-attention works..."
   ```

   This is within-source context only (from `cp.generated_briefs`), not the entire wiki. Growth is bounded by batch count × 3 pages per batch, manageable for typical sources.

4. **For batch collision check call:** system prompt is a static instruction template. Collision pairs are in the user message.

**Files:** `src/ingest.py` (`_build_batch_messages`), `src/merge.py` (new prompt for `batch_collision_check`), `schema.yaml` (if prompt structure changes)

---

## What's NOT in scope

- Two-step pipeline (analyze → generate) — recorded in `learnable_docs/two-step-pipeline-research.md` for future work
- MiniMax cold start / warmup
- Merging collision decisions with merge_page execution (would cause context explosion)
- Changing the patch-based merge mechanism to rewrite-only
- Source-level hash dedup (current checkpoint mechanism is sufficient)

---

## Files changed summary

| File | Changes |
|------|---------|
| `src/models.py` | New BatchCollisionDecision/CollisionPair/CollisionDecision models |
| `src/config.py` | New `get_ingest_mode()` reading `ingest_mode` from schema.yaml |
| `src/ingest.py` | Empty title filter, batch BriefIndex.add(), empty brief shortcut, short text mode, batch collision collection, prompt structure, ingest mode selection, titles+briefs context |
| `src/merge.py` | New `batch_collision_check()` function |
| `schema.yaml` | `ingest_mode` config, focused/comprehensive prompt variants, short text prompt |
| `tests/test_ingest.py` | Tests for all changes |
| `tests/test_merge.py` | Tests for batch_collision_check |

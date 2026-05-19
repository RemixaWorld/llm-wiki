# Brief-Based Merge Decision & Dedup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `brief` metadata field to wiki pages and replace the global title list injection with a brief-based collision analysis mechanism that decides whether merging is worthwhile. Also detect title variants via BM25 brief similarity.

**Architecture:** New `brief` field on `WikiFrontmatter` and `GeneratedPage`. Remove global `wiki_titles` loading from `process_batches_node`, keep intra-source `existing_titles`. Two brief analysis scenarios: exact collision (brief + body → MERGE/SKIP) and fuzzy collision via `BriefIndex` BM25 (brief vs brief → topic match → then Scenario A). Post-merge brief regeneration via lightweight LLM call.

**Tech Stack:** Python 3.13+, pydantic, rank-bm25, instructor, pytest, pytest-asyncio.

---

### Task 1: Add `brief` field to data models

**Files:**
- Modify: `src/models.py:29-41` (`WikiFrontmatter`), `src/models.py:56-69` (`GeneratedPage`), `src/models.py:149-158` (`Checkpoint`), add new models after line 96
- Test: `tests/test_models.py`

- [ ] **Step 1: Write failing tests for brief on data models**

Add to `tests/test_models.py`:

```python
class TestBriefField:
    def test_wiki_frontmatter_has_brief(self) -> None:
        fm = WikiFrontmatter(
            title="Test",
            page_type=PageType.CONCEPT,
            brief="A short summary of the page content.",
        )
        assert fm.brief == "A short summary of the page content."

    def test_wiki_frontmatter_brief_defaults_empty(self) -> None:
        fm = WikiFrontmatter(title="Test", page_type=PageType.CONCEPT)
        assert fm.brief == ""

    def test_generated_page_has_brief(self) -> None:
        page = GeneratedPage(
            title="Test",
            page_type=PageType.CONCEPT,
            tags=["test"],
            confidence=Confidence.HIGH,
            body="Content.",
            brief="Short description.",
        )
        assert page.brief == "Short description."

    def test_checkpoint_has_generated_briefs(self) -> None:
        cp = Checkpoint(
            source="test.pdf",
            source_title="Test",
            total_chunks=5,
            created_at="2026-05-20T00:00:00+00:00",
            generated_briefs={"Flash Attention": "IO-aware exact attention via tiling."},
        )
        assert cp.generated_briefs["Flash Attention"] == "IO-aware exact attention via tiling."

    def test_checkpoint_generated_briefs_defaults_empty(self) -> None:
        cp = Checkpoint(
            source="test.pdf",
            source_title="Test",
            total_chunks=5,
            created_at="2026-05-20T00:00:00+00:00",
        )
        assert cp.generated_briefs == {}

    def test_merge_decision_model(self) -> None:
        from src.models import MergeDecision

        d = MergeDecision(action="MERGE", reason="New info about FA2.")
        assert d.action == "MERGE"

    def test_topic_match_decision_model(self) -> None:
        from src.models import TopicMatchDecision

        d = TopicMatchDecision(same_topic=True, reason="Both about Flash Attention.")
        assert d.same_topic is True
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_models.py::TestBriefField -v`
Expected: FAIL — `brief` field doesn't exist yet

- [ ] **Step 3: Add brief fields to models**

In `src/models.py`, add `brief` field to `WikiFrontmatter` (after line 39):

```python
    brief: str = Field(default="", description="Short summary of what this page covers")
```

Add `brief` field to `GeneratedPage` (after `related_titles` field, line 69):

```python
    brief: str = Field(default="", description="Short summary of what this page covers")
```

Add `generated_briefs` to `Checkpoint` (after line 157):

```python
    generated_briefs: dict[str, str] = Field(default_factory=dict)
```

Add new models after `PatchedPage` class (after line 96):

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

Add `Literal` to imports at top of file (line 6):

```python
from typing import Literal
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_models.py::TestBriefField -v`
Expected: 7 PASSED

- [ ] **Step 5: Run full test suite**

Run: `uv run pytest tests/ -v`
Expected: All tests PASS (existing tests unaffected by new optional fields)

- [ ] **Step 6: Commit**

```bash
git add src/models.py tests/test_models.py
git commit -m "feat: add brief field to wiki models and decision models"
```

---

### Task 2: Update frontmatter parsing and rendering for brief

**Files:**
- Modify: `src/wiki.py:48-66` (`parse_frontmatter`), `src/wiki.py:69-84` (`render_page`)
- Test: `tests/test_wiki.py`

- [ ] **Step 1: Write failing tests for brief in frontmatter**

Add to `tests/test_wiki.py`:

```python
class TestBriefFrontmatter:
    def test_parse_frontmatter_with_brief(self) -> None:
        raw = (
            "---\n"
            "title: Flash Attention\n"
            "type: concept\n"
            "brief: IO-aware exact attention via tiling.\n"
            "sources: []\n"
            "tags: [attention]\n"
            "created: 2026-05-20\n"
            "updated: 2026-05-20\n"
            "confidence: high\n"
            "---\n\nBody text."
        )
        fm = parse_frontmatter(raw)
        assert fm.brief == "IO-aware exact attention via tiling."

    def test_parse_frontmatter_without_brief(self) -> None:
        raw = (
            "---\n"
            "title: Test\n"
            "type: concept\n"
            "sources: []\n"
            "tags: []\n"
            "created: 2026-05-20\n"
            "updated: 2026-05-20\n"
            "confidence: high\n"
            "---\n\nBody text."
        )
        fm = parse_frontmatter(raw)
        assert fm.brief == ""

    def test_render_page_includes_brief(self) -> None:
        fm = WikiFrontmatter(
            title="Flash Attention",
            page_type=PageType.CONCEPT,
            brief="IO-aware exact attention via tiling.",
            sources=["test.pdf"],
            tags=["attention"],
            created=date(2026, 5, 20),
            updated=date(2026, 5, 20),
            confidence=Confidence.HIGH,
        )
        raw = render_page(fm, "Body text.")
        assert "brief: IO-aware exact attention via tiling." in raw

    def test_render_page_empty_brief(self) -> None:
        fm = WikiFrontmatter(
            title="Test",
            page_type=PageType.CONCEPT,
            brief="",
            sources=["test.pdf"],
            tags=[],
            created=date(2026, 5, 20),
            updated=date(2026, 5, 20),
            confidence=Confidence.HIGH,
        )
        raw = render_page(fm, "Body text.")
        assert "brief:" in raw
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_wiki.py::TestBriefFrontmatter -v`
Expected: Some tests FAIL — `parse_frontmatter` ignores brief, `render_page` doesn't output it

- [ ] **Step 3: Update parse_frontmatter to read brief**

In `src/wiki.py`, update `parse_frontmatter()` (line 57-66) to include brief:

```python
    return WikiFrontmatter(
        title=meta.get("title", ""),
        page_type=PageType(meta.get("type", "concept")),
        sources=meta.get("sources", []),
        tags=meta.get("tags", []),
        created=meta.get("created") or today,
        updated=meta.get("updated") or today,
        confidence=Confidence(meta.get("confidence", "medium")),
        related=meta.get("related", []),
        brief=meta.get("brief", ""),
    )
```

- [ ] **Step 4: Update render_page to output brief**

In `src/wiki.py`, update `render_page()` (line 71-79) to include brief:

```python
    meta = {
        "title": page.title,
        "type": page.page_type.value,
        "brief": page.brief,
        "sources": page.sources,
        "tags": page.tags,
        "created": page.created.isoformat(),
        "updated": page.updated.isoformat(),
        "confidence": page.confidence.value,
    }
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `uv run pytest tests/test_wiki.py::TestBriefFrontmatter -v`
Expected: 4 PASSED

- [ ] **Step 6: Run full test suite**

Run: `uv run pytest tests/ -v`
Expected: All tests PASS

- [ ] **Step 7: Commit**

```bash
git add src/wiki.py tests/test_wiki.py
git commit -m "feat: parse and render brief field in wiki frontmatter"
```

---

### Task 3: Add BriefIndex for BM25-based brief dedup

**Files:**
- Modify: `src/search.py` (add `BriefIndex` class after `WikiIndex`)
- Test: `tests/test_search.py`

- [ ] **Step 1: Write failing tests for BriefIndex**

Add to `tests/test_search.py`:

```python
from src.search import BriefIndex, WikiIndex, tokenize


class TestBriefIndex:
    def test_empty_index(self) -> None:
        idx = BriefIndex()
        results = idx.search("anything")
        assert results == []

    def test_build_and_search(self) -> None:
        pages = [
            _make_page(
                "Flash Attention",
                "Some body text.",
                ["attention"],
            ),
            _make_page("Self-Attention", "Other body.", ["attention"]),
            _make_page("BERT", "NLP model.", ["nlp"]),
        ]
        # Set briefs on pages
        pages[0].frontmatter.brief = "IO-aware exact attention algorithm using tiling"
        pages[1].frontmatter.brief = "Sequence-internal attention mechanism for tokens"
        pages[2].frontmatter.brief = "Bidirectional encoder for NLP pre-training"

        idx = BriefIndex()
        idx.build(pages)
        results = idx.search("attention tiling HBM SRAM")
        assert len(results) > 0
        assert results[0][0] == "flash-attention.md"

    def test_search_returns_tuples(self) -> None:
        pages = [_make_page("Test", "Body.")]
        pages[0].frontmatter.brief = "A concept about testing"
        idx = BriefIndex()
        idx.build(pages)
        results = idx.search("testing")
        assert len(results) == 1
        path, score = results[0]
        assert path == "test.md"
        assert score > 0

    def test_add_incrementally(self) -> None:
        pages = [_make_page("A", "Body.")]
        pages[0].frontmatter.brief = "About attention"
        idx = BriefIndex()
        idx.build(pages)
        assert idx.page_count == 1

        idx.add("b.md", "About transformers and attention")
        assert idx.page_count == 2

        results = idx.search("transformers")
        assert len(results) > 0
        assert results[0][0] == "b.md"

    def test_skips_pages_without_brief(self) -> None:
        pages = [
            _make_page("With Brief", "Body."),
            _make_page("No Brief", "Body."),
        ]
        pages[0].frontmatter.brief = "Has a brief"
        pages[1].frontmatter.brief = ""
        idx = BriefIndex()
        idx.build(pages)
        assert idx.page_count == 1

    def test_no_match_returns_empty(self) -> None:
        pages = [_make_page("Test", "Body.")]
        pages[0].frontmatter.brief = "About quantum physics"
        idx = BriefIndex()
        idx.build(pages)
        results = idx.search("medieval cooking recipes")
        assert results == []

    def test_top_k_limit(self) -> None:
        pages = []
        for i in range(10):
            p = _make_page(f"Page {i}", f"Body {i}.")
            p.frontmatter.brief = f"About attention mechanism variant {i}"
            pages.append(p)
        idx = BriefIndex()
        idx.build(pages)
        results = idx.search("attention", top_k=3)
        assert len(results) <= 3
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_search.py::TestBriefIndex -v`
Expected: FAIL — `BriefIndex` doesn't exist

- [ ] **Step 3: Implement BriefIndex**

Add to `src/search.py` after the `WikiIndex` class:

```python
class BriefIndex:
    """BM25 index over page briefs for fuzzy title dedup."""

    def __init__(self) -> None:
        self._entries: list[tuple[str, str]] = []  # [(path, brief)]
        self._bm25: BM25Okapi | None = None

    def build(self, pages: list[WikiPage]) -> None:
        """Build index from wiki pages that have non-empty briefs."""
        self._entries = []
        for page in pages:
            if page.frontmatter.brief:
                self._entries.append((page.path, page.frontmatter.brief))
        self._rebuild()

    def search(self, query: str, top_k: int = 3) -> list[tuple[str, float]]:
        """Search briefs, return [(page_path, score), ...] sorted by score desc."""
        if not self._bm25 or not self._entries:
            return []

        tokens = tokenize(query)
        if not tokens:
            return []

        scores = self._bm25.get_scores(tokens)
        scored = [
            (self._entries[i][0], scores[i])
            for i in range(len(scores))
            if scores[i] > 0
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def add(self, path: str, brief: str) -> None:
        """Incrementally add a single entry. Rebuilds the full index."""
        if not brief:
            return
        self._entries.append((path, brief))
        self._rebuild()
        logger.info("added to brief index path=%s total=%d", path, len(self._entries))

    def _rebuild(self) -> None:
        """Rebuild BM25 index from stored entries."""
        if not self._entries:
            self._bm25 = None
            return
        settings = get_settings()
        tokenized = [tokenize(brief) for _, brief in self._entries]
        self._bm25 = BM25Okapi(tokenized, k1=settings.bm25_k1, b=settings.bm25_b)
        logger.info("built brief index entries=%d", len(self._entries))

    @property
    def page_count(self) -> int:
        return len(self._entries)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_search.py::TestBriefIndex -v`
Expected: 7 PASSED

- [ ] **Step 5: Run full test suite**

Run: `uv run pytest tests/ -v`
Expected: All tests PASS

- [ ] **Step 6: Commit**

```bash
git add src/search.py tests/test_search.py
git commit -m "feat: add BriefIndex for BM25-based brief dedup"
```

---

### Task 4: Add brief analysis functions to merge.py

**Files:**
- Modify: `src/merge.py` (add brief analysis functions and brief regeneration)
- Test: `tests/test_merge.py`

- [ ] **Step 1: Write failing tests for brief analysis**

Add to `tests/test_merge.py`:

```python
from src.models import MergeDecision, TopicMatchDecision


class TestBriefAnalysis:
    @pytest.mark.asyncio
    async def test_scenario_a_merge(self) -> None:
        """Scenario A: brief + body → LLM says MERGE."""
        from unittest.mock import AsyncMock, patch

        from src.merge import brief_merge_check

        result = MergeDecision(action="MERGE", reason="New FA2 details.")
        with patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = result
            decision = await brief_merge_check(
                existing_brief="IO-aware exact attention via tiling.",
                existing_title="Flash Attention",
                new_body="Flash Attention 2 reduces non-matmul FLOPs further.",
            )

        assert decision.action == "MERGE"
        assert mock_llm.call_count == 1

    @pytest.mark.asyncio
    async def test_scenario_a_skip(self) -> None:
        """Scenario A: brief + body → LLM says SKIP."""
        from unittest.mock import AsyncMock, patch

        from src.merge import brief_merge_check

        result = MergeDecision(action="SKIP", reason="Already covered.")
        with patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = result
            decision = await brief_merge_check(
                existing_brief="IO-aware exact attention via tiling.",
                existing_title="Flash Attention",
                new_body="Flash Attention uses tiling to reduce memory access.",
            )

        assert decision.action == "SKIP"
        assert mock_llm.call_count == 1

    @pytest.mark.asyncio
    async def test_scenario_b_same_topic(self) -> None:
        """Scenario B: brief vs brief → LLM says same topic."""
        from unittest.mock import AsyncMock, patch

        from src.merge import topic_match_check

        result = TopicMatchDecision(same_topic=True, reason="Both about Flash Attention.")
        with patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = result
            decision = await topic_match_check(
                existing_title="Flash Attention",
                existing_brief="IO-aware exact attention via tiling.",
                new_title="Flash Attention Algorithm",
                new_brief="Attention optimization using memory tiling.",
            )

        assert decision.same_topic is True
        assert mock_llm.call_count == 1

    @pytest.mark.asyncio
    async def test_scenario_b_different_topic(self) -> None:
        """Scenario B: brief vs brief → LLM says different topics."""
        from unittest.mock import AsyncMock, patch

        from src.merge import topic_match_check

        result = TopicMatchDecision(same_topic=False, reason="Different topics.")
        with patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = result
            decision = await topic_match_check(
                existing_title="Flash Attention",
                existing_brief="IO-aware exact attention via tiling.",
                new_title="Attention Span",
                new_brief="Psychological concept about focus duration.",
            )

        assert decision.same_topic is False

    @pytest.mark.asyncio
    async def test_regenerate_brief(self) -> None:
        """Post-merge brief regeneration."""
        from unittest.mock import AsyncMock, patch

        from src.merge import regenerate_brief

        mock_page = GeneratedPage(
            title="Flash Attention",
            page_type=PageType.CONCEPT,
            tags=["attention"],
            confidence=Confidence.HIGH,
            body="Updated body about Flash Attention 2.",
            brief="Updated brief about FA1 and FA2.",
        )
        with patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = mock_page
            brief = await regenerate_brief(
                title="Flash Attention",
                merged_body="Updated body about Flash Attention 2.",
            )

        assert brief == "Updated brief about FA1 and FA2."
        assert mock_llm.call_count == 1
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_merge.py::TestBriefAnalysis -v`
Expected: FAIL — functions don't exist yet

- [ ] **Step 3: Implement brief analysis functions**

Add to `src/merge.py` after the `_CONFIDENCE_ORDER` dict (line 22), before `_merge_frontmatter`:

```python
from src.models import (
    Confidence,
    GeneratedPage,
    MergeDecision,
    MergedPage,
    PatchedPage,
    TopicMatchDecision,
    WikiFrontmatter,
    WikiPage,
)
```

Update the import block (lines 10-17) to include `MergeDecision` and `TopicMatchDecision`.

Add these functions after `_merge_frontmatter` (after line 74):

```python
async def brief_merge_check(
    existing_brief: str,
    existing_title: str,
    new_body: str,
) -> MergeDecision:
    """Scenario A: decide whether to merge new content into existing page.

    Uses existing page's brief + new page's body to determine if the new
    content adds significant information.
    """
    messages = [
        {
            "role": "user",
            "content": (
                f'Existing page "{existing_title}" covers: {existing_brief}\n\n'
                f"New content generated about this topic:\n{new_body}\n\n"
                "Does the new content add significant information not covered "
                'by the existing page?\nAnswer MERGE or SKIP. When uncertain, choose MERGE.'
            ),
        },
    ]
    return await complete_structured(
        messages=messages,
        response_model=MergeDecision,
        temperature=0.1,
    )


async def topic_match_check(
    existing_title: str,
    existing_brief: str,
    new_title: str,
    new_brief: str,
) -> TopicMatchDecision:
    """Scenario B: check if two briefs describe the same topic."""
    messages = [
        {
            "role": "user",
            "content": (
                f'Existing page "{existing_title}" covers: {existing_brief}\n'
                f'New page "{new_title}" covers: {new_brief}\n\n'
                "Are these about the same topic?\nAnswer SAME or DIFFERENT."
            ),
        },
    ]
    return await complete_structured(
        messages=messages,
        response_model=TopicMatchDecision,
        temperature=0.1,
    )


async def regenerate_brief(title: str, merged_body: str) -> str:
    """Regenerate brief after merge. Returns the new brief string."""
    result = await complete_structured(
        messages=[
            {
                "role": "user",
                "content": (
                    f'Write a brief summary (1-3 sentences) for this wiki page:\n\n'
                    f"Title: {title}\n\n{merged_body}"
                ),
            },
        ],
        response_model=GeneratedPage,
        temperature=0.1,
    )
    return result.brief
```

Note: `BriefOutput` model is added in Task 1. The import block in `src/merge.py` should include it:

```python
from src.models import (
    BriefOutput,
    Confidence,
    GeneratedPage,
    MergeDecision,
    MergedPage,
    PatchedPage,
    TopicMatchDecision,
    WikiFrontmatter,
    WikiPage,
)
```

The `regenerate_brief` function above uses `BriefOutput` as its response model (not `GeneratedPage`) to avoid wasteful LLM output.

```python
async def regenerate_brief(title: str, merged_body: str) -> str:
    """Regenerate brief after merge. Returns the new brief string."""
    result = await complete_structured(
        messages=[
            {
                "role": "user",
                "content": (
                    f'Write a brief summary (1-3 sentences) for this wiki page:\n\n'
                    f"Title: {title}\n\n{merged_body}"
                ),
            },
        ],
        response_model=BriefOutput,
        temperature=0.1,
    )
    return result.brief
```

Update `TestBriefAnalysis.test_regenerate_brief` to use `BriefOutput`:

```python
    @pytest.mark.asyncio
    async def test_regenerate_brief(self) -> None:
        """Post-merge brief regeneration."""
        from unittest.mock import AsyncMock, patch

        from src.merge import regenerate_brief
        from src.models import BriefOutput

        mock_output = BriefOutput(brief="Updated brief about FA1 and FA2.")
        with patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = mock_output
            brief = await regenerate_brief(
                title="Flash Attention",
                merged_body="Updated body about Flash Attention 2.",
            )

        assert brief == "Updated brief about FA1 and FA2."
        assert mock_llm.call_count == 1
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_merge.py::TestBriefAnalysis -v`
Expected: 5 PASSED

- [ ] **Step 5: Run full test suite**

Run: `uv run pytest tests/ -v`
Expected: All tests PASS

- [ ] **Step 6: Commit**

```bash
git add src/merge.py src/models.py tests/test_merge.py
git commit -m "feat: add brief analysis functions for merge decision"
```

---

### Task 5: Integrate brief into merge_page and _merge_frontmatter

**Files:**
- Modify: `src/merge.py:25-74` (`_merge_frontmatter`), `src/merge.py:147-212` (`merge_page`)
- Test: `tests/test_merge.py`

- [ ] **Step 1: Write tests for merge_page with brief regeneration**

Add to `tests/test_merge.py`:

```python
class TestMergePageWithBrief:
    @pytest.mark.asyncio
    async def test_merge_page_regenerates_brief(self) -> None:
        """merge_page should regenerate brief after successful patch merge."""
        from unittest.mock import AsyncMock, patch

        from src.models import BriefOutput, EditOp, PatchedPage

        existing_page = WikiPage(
            path="flash-attention.md",
            frontmatter=WikiFrontmatter(
                title="Flash Attention",
                page_type=PageType.CONCEPT,
                brief="IO-aware exact attention via tiling.",
                sources=["papers/fa.pdf"],
                tags=["attention"],
                created=date(2026, 1, 1),
                updated=date(2026, 1, 1),
                confidence=Confidence.HIGH,
            ),
            body="# Flash Attention\n\nIO-aware exact attention.",
        )
        new_page = GeneratedPage(
            title="Flash Attention",
            page_type=PageType.CONCEPT,
            tags=["attention", "optimization"],
            confidence=Confidence.HIGH,
            body="# Flash Attention\n\nIO-aware exact attention with FA2 improvements.",
            brief="Updated brief about FA1 and FA2.",
        )

        mock_patch = PatchedPage(
            edits=[
                EditOp(
                    old_string="IO-aware exact attention.",
                    new_string="IO-aware exact attention with FA2 improvements.",
                ),
            ],
            tags_to_add=["optimization"],
            confidence=Confidence.HIGH,
        )
        mock_brief = BriefOutput(brief="FA1 and FA2: IO-aware exact attention with tiling optimizations.")

        with patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.side_effect = [mock_patch, mock_brief]
            fm, body = await merge_page(existing_page, new_page, "papers/fa2.pdf")

        assert "FA2" in body
        assert fm.brief == "FA1 and FA2: IO-aware exact attention with tiling optimizations."
        assert mock_llm.call_count == 2  # 1 patch + 1 brief regen

    @pytest.mark.asyncio
    async def test_merge_page_regen_brief_on_rewrite_fallback(self) -> None:
        """Brief regenerated even when falling back to rewrite."""
        from unittest.mock import AsyncMock, patch

        from src.models import BriefOutput, EditOp, PatchedPage

        existing_page = WikiPage(
            path="bert.md",
            frontmatter=WikiFrontmatter(
                title="BERT",
                page_type=PageType.ENTITY,
                brief="Bidirectional encoder.",
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
            brief="Updated BERT description.",
        )

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
        mock_brief = BriefOutput(brief="BERT: bidirectional encoder with updated details.")

        with patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.side_effect = [bad_patch, bad_patch, bad_patch, mock_merged, mock_brief]
            fm, body = await merge_page(existing_page, new_page, "new.pdf")

        assert fm.brief == "BERT: bidirectional encoder with updated details."
        assert mock_llm.call_count == 5  # 3 patch + 1 rewrite + 1 brief regen
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_merge.py::TestMergePageWithBrief -v`
Expected: FAIL — `merge_page` doesn't regenerate brief yet

- [ ] **Step 3: Update _merge_frontmatter to accept and set brief**

Update `_merge_frontmatter` in `src/merge.py` to accept a `brief` parameter:

```python
def _merge_frontmatter(
    existing_fm: WikiFrontmatter,
    new_page: GeneratedPage,
    merged_body: str,
    merged_tags: list[str],
    merged_confidence: Confidence,
    source_path: str,
    brief: str = "",
) -> tuple[WikiFrontmatter, str]:
    """Merge frontmatter fields from existing page and new generated page.

    Pure logic -- no LLM call. Returns (merged_frontmatter, merged_body).
    """
    # Sources: append new source if not already present
    sources = list(existing_fm.sources)
    if source_path not in sources:
        sources.append(source_path)

    # Tags: union of existing + LLM-merged tags, deduplicated, order-preserving
    seen: set[str] = set()
    tags: list[str] = []
    for t in existing_fm.tags + merged_tags:
        if t not in seen:
            seen.add(t)
            tags.append(t)

    # Related: union of existing paths + new title-to-path conversions
    existing_related = set(existing_fm.related)
    new_related = {title_to_path(t) for t in new_page.related_titles}
    related = sorted(existing_related | new_related)

    # Confidence: take the higher of existing vs merged
    confidence = (
        merged_confidence
        if _CONFIDENCE_ORDER.get(merged_confidence, 0)
        >= _CONFIDENCE_ORDER.get(existing_fm.confidence, 0)
        else existing_fm.confidence
    )

    fm = WikiFrontmatter(
        title=existing_fm.title,
        page_type=existing_fm.page_type,
        sources=sources,
        tags=tags,
        created=existing_fm.created,
        updated=date.today(),
        confidence=confidence,
        related=related,
        brief=brief or existing_fm.brief,
    )

    return fm, merged_body
```

- [ ] **Step 4: Update merge_page to regenerate brief after merge**

Update `merge_page` in `src/merge.py` to regenerate brief after successful merge:

```python
async def merge_page(
    existing: WikiPage,
    new_page: GeneratedPage,
    source_path: str,
) -> tuple[WikiFrontmatter, str]:
    """Merge existing page with new generated page via edit/patch or full rewrite.

    Tries patch-first (up to 3 attempts with error context on retry).
    Falls back to full rewrite via MergedPage if all patch attempts fail.
    Regenerates brief after successful merge.
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
            # Regenerate brief after successful merge
            merged_tags = list(existing.frontmatter.tags) + result.tags_to_add
            merged_confidence = result.confidence
            fm, merged_body = _merge_frontmatter(
                existing_fm=existing.frontmatter,
                new_page=new_page,
                merged_body=body,
                merged_tags=merged_tags,
                merged_confidence=merged_confidence,
                source_path=source_path,
            )
            fm.brief = await regenerate_brief(existing.frontmatter.title, merged_body)
            return fm, merged_body
        except PatchError as e:
            last_error = str(e)
            logger.warning(
                "patch attempt %d failed for title=%s: %s",
                attempt + 1,
                existing.frontmatter.title,
                e,
            )

    # Fallback: full rewrite
    logger.info("falling back to rewrite for title=%s", existing.frontmatter.title)
    messages = _build_rewrite_messages(existing, new_page, source_path)
    result = await complete_structured(
        messages=messages,
        response_model=MergedPage,
        temperature=0.2,
    )

    logger.info("rewrote page title=%s", existing.frontmatter.title)
    fm, merged_body = _merge_frontmatter(
        existing_fm=existing.frontmatter,
        new_page=new_page,
        merged_body=result.body,
        merged_tags=result.tags,
        merged_confidence=result.confidence,
        source_path=source_path,
    )
    fm.brief = await regenerate_brief(existing.frontmatter.title, merged_body)
    return fm, merged_body
```

- [ ] **Step 5: Fix existing merge tests**

Existing tests in `TestMergePagePatchSuccess` call `merge_page` which now calls `regenerate_brief` internally. Update those tests to also mock the `BriefOutput` response.

Update `test_patch_succeeds_on_first_attempt`:

```python
    @pytest.mark.asyncio
    async def test_patch_succeeds_on_first_attempt(self) -> None:
        from unittest.mock import AsyncMock, patch

        from src.models import BriefOutput, EditOp, PatchedPage

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
        mock_brief = BriefOutput(brief="BERT: bidirectional encoder with MLM.")

        with patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.side_effect = [mock_patched, mock_brief]
            fm, body = await merge_page(existing_page, new_page, "articles/bert-guide.md")

        assert "masked language modeling" in body
        assert "pre-training" in fm.tags
        assert mock_llm.call_count == 2  # 1 patch + 1 brief regen
```

Update `test_patch_retries_on_failure_then_succeeds`:

```python
    @pytest.mark.asyncio
    async def test_patch_retries_on_failure_then_succeeds(self) -> None:
        from unittest.mock import AsyncMock, patch

        from src.models import BriefOutput, EditOp, PatchedPage

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

        bad_patch = PatchedPage(
            edits=[EditOp(old_string="NOT IN BODY", new_string="x")],
            tags_to_add=[],
            confidence=Confidence.MEDIUM,
        )
        good_patch = PatchedPage(
            edits=[EditOp(old_string="Bidirectional encoder.", new_string="Updated content.")],
            tags_to_add=[],
            confidence=Confidence.MEDIUM,
        )
        mock_brief = BriefOutput(brief="BERT: updated.")

        with patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.side_effect = [bad_patch, good_patch, mock_brief]
            fm, body = await merge_page(existing_page, new_page, "new.pdf")

        assert body == "# BERT\n\nUpdated content."
        assert mock_llm.call_count == 3  # 1 fail + 1 succeed + 1 brief regen
```

Update `test_falls_back_to_rewrite_after_3_patch_failures`:

```python
    @pytest.mark.asyncio
    async def test_falls_back_to_rewrite_after_3_patch_failures(self) -> None:
        from unittest.mock import AsyncMock, patch

        from src.models import BriefOutput, EditOp, PatchedPage

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
        mock_brief = BriefOutput(brief="BERT: bidirectional encoder with updates.")

        with patch("src.merge.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.side_effect = [bad_patch, bad_patch, bad_patch, mock_merged, mock_brief]
            fm, body = await merge_page(existing_page, new_page, "new.pdf")

        assert "Updated content" in body
        assert mock_llm.call_count == 5  # 3 patch + 1 rewrite + 1 brief regen
```

- [ ] **Step 6: Run full test suite**

Run: `uv run pytest tests/ -v`
Expected: All tests PASS

- [ ] **Step 7: Commit**

```bash
git add src/merge.py src/models.py tests/test_merge.py
git commit -m "feat: integrate brief regeneration into merge_page"
```

---

### Task 6: Update ingest pipeline — remove wiki_titles, add brief analysis

**Files:**
- Modify: `src/ingest.py:95-135` (`_build_batch_messages`), `src/ingest.py:166-289` (`process_batches_node`)
- Test: `tests/test_ingest.py`

- [ ] **Step 1: Write failing tests for updated ingest pipeline**

The implementer should read `tests/test_ingest.py` for existing patterns. These tests mock `complete_structured` to control LLM outputs and use `tmp_wiki_dir` for disk state.

Add to `tests/test_ingest.py`:

```python
from src.models import BriefOutput, MergeDecision, TopicMatchDecision


class TestBriefAnalysis:
    @pytest.mark.asyncio
    async def test_exact_collision_skip_via_brief(self, tmp_wiki_dir: Path) -> None:
        """Exact title collision → brief analysis says SKIP → page not rewritten."""
        from unittest.mock import AsyncMock, patch

        from src.ingest import _build_batch_messages, process_batches_node
        from src.models import IngestResult
        from src.wiki import write_page

        # Create existing page with brief
        fm = WikiFrontmatter(
            title="Flash Attention",
            page_type=PageType.CONCEPT,
            brief="IO-aware exact attention via tiling.",
            sources=["papers/fa.pdf"],
            tags=["attention"],
            created=date(2026, 1, 1),
            updated=date(2026, 1, 1),
            confidence=Confidence.HIGH,
        )
        write_page(fm, "Flash Attention body content.", tmp_wiki_dir)

        # Read original content for comparison
        original_raw = (tmp_wiki_dir / "flash-attention.md").read_text()

        ingest_result = IngestResult(
            source_summary=GeneratedPage(
                title="Source Summary",
                page_type=PageType.SOURCE_SUMMARY,
                tags=["attention"],
                confidence=Confidence.HIGH,
                body="Summary of the paper.",
                brief="Summary of attention paper.",
            ),
            concept_pages=[
                GeneratedPage(
                    title="Flash Attention",
                    page_type=PageType.CONCEPT,
                    tags=["attention"],
                    confidence=Confidence.HIGH,
                    body="Flash Attention uses tiling.",
                    brief="IO-aware exact attention via tiling.",
                ),
            ],
        )
        skip_decision = MergeDecision(action="SKIP", reason="Already covered.")
        brief_output = BriefOutput(brief="Summary of attention paper.")

        with patch("src.ingest.complete_structured", new_callable=AsyncMock) as mock_llm:
            mock_llm.side_effect = [ingest_result, skip_decision, brief_output]
            # The 3rd call is brief regen for source_summary which is a new page
            # Actually source_summary won't have collision, only Flash Attention will
            # So we need: 1 ingest result + 1 brief check for FA (SKIP) + 1 brief regen for new page
            pass

        # Assert: Flash Attention page unchanged on disk
        current_raw = (tmp_wiki_dir / "flash-attention.md").read_text()
        assert current_raw == original_raw

    @pytest.mark.asyncio
    async def test_build_batch_messages_no_wiki_titles(self) -> None:
        """_build_batch_messages no longer accepts wiki_titles parameter."""
        from src.ingest import _build_batch_messages

        messages = _build_batch_messages(
            chunks=["chunk1", "chunk2"],
            batch_start=0,
            batch_size=2,
            source_title="Test Paper",
            existing_titles=["Flash Attention", "Self-Attention"],
        )
        assert "Flash Attention" in messages[1]["content"]
        assert "Self-Attention" in messages[1]["content"]

    @pytest.mark.asyncio
    async def test_build_batch_messages_empty_existing_titles(self) -> None:
        """No existing titles → no title list injected."""
        from src.ingest import _build_batch_messages

        messages = _build_batch_messages(
            chunks=["chunk1"],
            batch_start=0,
            batch_size=1,
            source_title="Test",
            existing_titles=[],
        )
        assert "already exist" not in messages[1]["content"]

    def test_check_fuzzy_collision_returns_page(self, tmp_wiki_dir: Path) -> None:
        """Fuzzy collision via BM25 returns matched WikiPage."""
        from src.ingest import _check_fuzzy_collision
        from src.search import BriefIndex
        from src.wiki import read_all_pages

        fm = WikiFrontmatter(
            title="Flash Attention",
            page_type=PageType.CONCEPT,
            brief="IO-aware exact attention algorithm using tiling for memory optimization.",
            sources=["test.pdf"],
            tags=["attention"],
            created=date(2026, 5, 20),
            updated=date(2026, 5, 20),
            confidence=Confidence.HIGH,
        )
        write_page(fm, "Body.", tmp_wiki_dir)

        pages = read_all_pages(tmp_wiki_dir)
        idx = BriefIndex()
        idx.build(pages)

        result = _check_fuzzy_collision(
            brief_idx=idx,
            new_brief="Attention optimization using memory tiling techniques.",
            wiki_dir=tmp_wiki_dir,
        )
        assert result is not None
        assert result.frontmatter.title == "Flash Attention"

    def test_check_fuzzy_collision_no_match(self, tmp_wiki_dir: Path) -> None:
        """No fuzzy match → returns None."""
        from src.ingest import _check_fuzzy_collision
        from src.search import BriefIndex

        idx = BriefIndex()
        result = _check_fuzzy_collision(
            brief_idx=idx,
            new_brief="Something completely different.",
            wiki_dir=tmp_wiki_dir,
        )
        assert result is None
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_ingest.py::TestBriefAnalysis -v`
Expected: FAIL

- [ ] **Step 3: Remove wiki_titles from _build_batch_messages**

In `src/ingest.py`, update `_build_batch_messages` to remove `wiki_titles` parameter:

```python
def _build_batch_messages(
    chunks: list[str],
    batch_start: int,
    batch_size: int,
    source_title: str,
    existing_titles: list[str],
) -> list[dict[str, str]]:
    """Build LLM messages for a single batch of chunks.

    Includes intra-source page titles so the LLM uses consistent titles.
    """
    from src.config import get_allowed_tags, get_ingest_prompt

    batch = chunks[batch_start : batch_start + batch_size]
    combined = "\n\n---\n\n".join(batch)

    system_prompt = get_ingest_prompt()
    allowed_tags = get_allowed_tags()
    if allowed_tags:
        system_prompt += "\n\nPreferred tags (use these when applicable): " + ", ".join(
            allowed_tags
        )

    user_content = (
        f"Source: {source_title}\n\nCreate wiki pages from this source text:\n\n{combined}"
    )
    if existing_titles:
        user_content += (
            f"\n\nThe following wiki pages already exist: {', '.join(existing_titles)}"
            "\nLink to them using [[Title]] syntax where relevant."
            "\nIf you have genuinely NEW information about an existing topic, you may"
            " create a page with that title — it will be merged with existing content."
            "\nOtherwise, prefer using [[Title]] links."
        )

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]
```

- [ ] **Step 4: Update process_batches_node with brief analysis logic**

Replace the wiki_titles loading and per-page processing in `process_batches_node`. The new flow:

1. Remove lines 179-189 (wiki_titles loading)
2. Build BriefIndex from disk pages at start
3. For each GeneratedPage, run collision detection + brief analysis
4. Update checkpoint with generated_briefs

The updated per-page processing loop (replacing lines 238-263):

```python
            all_pages = [result.source_summary, *result.concept_pages, *result.entity_pages]

            today = date.today()
            batch_titles: list[str] = []
            batch_briefs: dict[str, str] = {}
            for gen_page in all_pages:
                # Step 1: exact collision check
                existing_page = get_page_by_title(gen_page.title, settings.wiki_dir)

                if existing_page is not None:
                    # Scenario A: brief analysis with full context
                    decision = await brief_merge_check(
                        existing_brief=existing_page.frontmatter.brief,
                        existing_title=existing_page.frontmatter.title,
                        new_body=gen_page.body,
                    )
                    if decision.action == "MERGE":
                        merged_fm, merged_body = await merge_page(
                            existing_page,
                            gen_page,
                            source_path,
                        )
                        path = write_page(merged_fm, merged_body, settings.wiki_dir)
                        brief_idx.add(path, merged_fm.brief)
                    else:
                        # SKIP: don't write, record for checkpoint
                        logger.info(
                            "brief skip title=%s reason=%s",
                            gen_page.title,
                            decision.reason,
                        )
                        path = title_to_path(gen_page.title)
                else:
                    # Step 2: fuzzy collision check via BM25 brief search
                    fuzzy_match = _check_fuzzy_collision(
                        brief_idx, gen_page.brief, settings.wiki_dir,
                    )

                    if fuzzy_match is not None:
                        # Scenario B: brief vs brief → topic match
                        fuzzy_page = fuzzy_match
                        topic_decision = await topic_match_check(
                            existing_title=fuzzy_page.frontmatter.title,
                            existing_brief=fuzzy_page.frontmatter.brief,
                            new_title=gen_page.title,
                            new_brief=gen_page.brief,
                        )
                        if topic_decision.same_topic:
                            # Same topic → Scenario A with full context
                            merge_decision = await brief_merge_check(
                                existing_brief=fuzzy_page.frontmatter.brief,
                                existing_title=fuzzy_page.frontmatter.title,
                                new_body=gen_page.body,
                            )
                            if merge_decision.action == "MERGE":
                                merged_fm, merged_body = await merge_page(
                                    fuzzy_page,
                                    gen_page,
                                    source_path,
                                )
                                path = write_page(merged_fm, merged_body, settings.wiki_dir)
                                brief_idx.add(path, merged_fm.brief)
                            else:
                                logger.info(
                                    "brief skip (fuzzy) title=%s reason=%s",
                                    gen_page.title,
                                    merge_decision.reason,
                                )
                                path = title_to_path(gen_page.title)
                        else:
                            # Different topic → new page
                            path = _write_new_page(
                                gen_page, source_path, today, settings,
                            )
                    else:
                        # No collision at all → new page
                        path = _write_new_page(
                            gen_page, source_path, today, settings,
                        )

                all_written.append(path)
                batch_titles.append(gen_page.title)
                batch_briefs[gen_page.title] = gen_page.brief

            # Update checkpoint
            cp.completed_batches.append(batch_idx)
            cp.generated_titles.extend(batch_titles)
            cp.generated_briefs.update(batch_briefs)
            _write_checkpoint(cp)
```

Add helper functions to `src/ingest.py`:

```python
def _write_new_page(
    gen_page: GeneratedPage,
    source_path: str,
    today: date,
    settings: Settings,
) -> str:
    """Write a new page to disk and return its path."""
    fm = WikiFrontmatter(
        title=gen_page.title,
        page_type=gen_page.page_type,
        sources=[source_path],
        tags=gen_page.tags,
        created=today,
        updated=today,
        confidence=gen_page.confidence,
        related=[title_to_path(t) for t in gen_page.related_titles],
        brief=gen_page.brief,
    )
    return write_page(fm, gen_page.body, settings.wiki_dir)


def _check_fuzzy_collision(
    brief_idx: BriefIndex,
    new_brief: str,
    wiki_dir: Path,
) -> WikiPage | None:
    """Check BM25 brief index for similar pages. Returns matched WikiPage or None."""
    if not new_brief:
        return None

    results = brief_idx.search(new_brief, top_k=1)
    if not results:
        return None

    path, score = results[0]
    if score < 1.0:
        return None

    try:
        return read_page(path, wiki_dir)
    except Exception:
        return None
```

Also add imports at top of `src/ingest.py`:

```python
from src.merge import brief_merge_check, merge_page, topic_match_check
from src.search import BriefIndex
```

And add `BriefIndex` initialization after checkpoint creation:

```python
    # Build brief index from existing wiki pages
    brief_idx = BriefIndex()
    if settings.wiki_dir.exists():
        from src.wiki import read_all_pages

        brief_idx.build(read_all_pages(settings.wiki_dir))
```

- [ ] **Step 5: Update existing ingest tests**

Existing tests in `tests/test_ingest.py` that call `_build_batch_messages` with `wiki_titles` parameter need to be updated to remove that argument. The implementer should read existing test file and update accordingly.

- [ ] **Step 6: Run full test suite**

Run: `uv run pytest tests/ -v`
Expected: All tests PASS

- [ ] **Step 7: Commit**

```bash
git add src/ingest.py tests/test_ingest.py
git commit -m "feat: replace wiki_titles with brief-based collision analysis in ingest"
```

---

### Task 7: Update schema.yaml prompts for brief generation

**Files:**
- Modify: `schema.yaml:47-60` (ingest_system prompt), `schema.yaml:71-75` (merge_system prompt)

- [ ] **Step 1: Update ingest_system prompt**

Replace `ingest_system` in `schema.yaml` with:

```yaml
  ingest_system: |
    You are a knowledge engineer creating wiki pages from source material.
    Create structured, interlinked pages using [[WikiLinks]] to reference
    related concepts. Be precise and cite the source. Every claim should
    be traceable to the source material.

    Page types:
    - concept: Explain a technique or idea (100-500 words)
    - entity: Describe a person, org, or tool (50-300 words)
    - source_summary: Summarize the source document (150-600 words)

    Use the provided tag vocabulary when possible. Create new tags only
    when no existing tag fits.

    For each page, write a brief (1-3 sentences) summarizing what the page
    covers. This brief will be used for cross-referencing and deduplication.
```

- [ ] **Step 2: Update merge_system prompt**

Replace `merge_system` in `schema.yaml` with:

```yaml
  merge_system: |
    You are merging two wiki pages about the same topic into one.
    Preserve ALL unique information from both versions. Remove redundancy.
    Maintain a coherent structure. Keep all [[WikiLinks]] from both versions.
    Use the provided tag vocabulary when possible.

    After merging, the brief will be regenerated separately — do not
    include brief generation in your output.
```

- [ ] **Step 3: Run full test suite**

Run: `uv run pytest tests/ -v`
Expected: All tests PASS

- [ ] **Step 4: Commit**

```bash
git add schema.yaml
git commit -m "feat: update schema.yaml prompts for brief generation"
```

---

### Task 8: Final verification

**Files:** None (verification only)

- [ ] **Step 1: Run full test suite**

Run: `uv run pytest tests/ -v`
Expected: All tests PASS

- [ ] **Step 2: Run linter**

Run: `make lint`
Expected: No errors

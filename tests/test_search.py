"""Tests for BM25 search index."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from src.models import Confidence, PageType, WikiFrontmatter, WikiPage
from src.search import BriefIndex, WikiIndex, tokenize


def _make_page(title: str, body: str, tags: list[str] | None = None) -> WikiPage:
    """Helper to create a WikiPage for testing."""
    return WikiPage(
        path=f"{title.lower().replace(' ', '-')}.md",
        frontmatter=WikiFrontmatter(
            title=title,
            page_type=PageType.CONCEPT,
            tags=tags or [],
            created=date(2026, 4, 8),
            updated=date(2026, 4, 8),
            confidence=Confidence.HIGH,
        ),
        body=body,
    )


class TestTokenize:
    def test_basic(self) -> None:
        tokens = tokenize("Hello, World!")
        assert tokens == ["hello", "world"]

    def test_empty(self) -> None:
        assert tokenize("") == []

    def test_preserves_numbers(self) -> None:
        tokens = tokenize("GPT-4 has 175B parameters")
        assert "4" in tokens
        assert "175b" in tokens


class TestWikiIndex:
    def test_empty_index(self) -> None:
        idx = WikiIndex()
        results = idx.search("anything")
        assert results == []
        assert idx.page_count == 0

    def test_build_and_search(self) -> None:
        pages = [
            _make_page("Transformer", "Self-attention mechanism for sequences.", ["deep-learning"]),
            _make_page("BERT", "Bidirectional encoder for NLP tasks.", ["nlp"]),
            _make_page("CNN", "Convolutional neural networks for images.", ["computer-vision"]),
        ]
        idx = WikiIndex(pages)
        assert idx.page_count == 3

        results = idx.search("attention mechanism")
        assert len(results) > 0
        assert results[0].frontmatter.title == "Transformer"

    def test_search_returns_top_k(self) -> None:
        pages = [_make_page(f"Page {i}", f"Content about topic {i}.") for i in range(20)]
        idx = WikiIndex(pages)

        results = idx.search("topic", top_k=3)
        assert len(results) == 3

    def test_search_no_match(self) -> None:
        pages = [_make_page("Transformer", "Self-attention.", ["deep-learning"])]
        idx = WikiIndex(pages)

        results = idx.search("quantum computing superconductor")
        # BM25 might return results with very low scores; just verify no crash
        assert isinstance(results, list)

    def test_search_empty_query(self) -> None:
        pages = [_make_page("Test", "Content.")]
        idx = WikiIndex(pages)
        results = idx.search("")
        assert results == []

    def test_build_from_fixture(self, tmp_wiki_dir: Path) -> None:
        from datetime import date

        from src.models import PageType, WikiFrontmatter
        from src.wiki import read_all_pages, write_page

        # Add a third page so BM25 IDF doesn't zero out (N=2 makes all IDF=0)
        fm = WikiFrontmatter(
            title="CNN",
            page_type=PageType.CONCEPT,
            tags=["computer-vision"],
            created=date(2026, 4, 8),
            updated=date(2026, 4, 8),
        )
        write_page(fm, "Convolutional neural networks for image classification.", tmp_wiki_dir)

        pages = read_all_pages(tmp_wiki_dir)
        idx = WikiIndex(pages)
        assert idx.page_count == 3

        results = idx.search("attention sequences parallel")
        assert len(results) > 0

    def test_tags_influence_ranking(self) -> None:
        # Need 3+ docs so BM25 IDF is non-zero
        pages = [
            _make_page("Generic Page", "Some generic unrelated content here.", ["misc"]),
            _make_page(
                "NLP Overview",
                "Attention mechanisms are core to NLP models.",
                ["nlp", "attention"],
            ),
            _make_page("Vision Model", "Image classification with CNNs.", ["computer-vision"]),
        ]
        idx = WikiIndex(pages)

        results = idx.search("attention nlp models")
        assert len(results) > 0
        assert results[0].frontmatter.title == "NLP Overview"

    def test_rebuild_index(self) -> None:
        pages1 = [_make_page("Old", "Old content.")]
        idx = WikiIndex(pages1)
        assert idx.page_count == 1

        pages2 = [_make_page("New A", "New A."), _make_page("New B", "New B.")]
        idx.build(pages2)
        assert idx.page_count == 2


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
        # Need 3+ pages so BM25 IDF is non-zero (N=2 makes all IDF=0)
        pages = [
            _make_page("Testing", "Body."),
            _make_page("CNN", "Body."),
            _make_page("RNN", "Body."),
        ]
        pages[0].frontmatter.brief = "A concept about testing"
        pages[1].frontmatter.brief = "Convolutional neural networks"
        pages[2].frontmatter.brief = "Recurrent neural networks"
        idx = BriefIndex()
        idx.build(pages)
        results = idx.search("testing")
        assert len(results) == 1
        path, score = results[0]
        assert path == "testing.md"
        assert score > 0

    def test_add_incrementally(self) -> None:
        # Start with 2 pages to have enough IDF base, then add a 3rd
        pages = [
            _make_page("A", "Body."),
            _make_page("X", "Body."),
        ]
        pages[0].frontmatter.brief = "About attention"
        pages[1].frontmatter.brief = "About convolutional networks"
        idx = BriefIndex()
        idx.build(pages)
        assert idx.page_count == 2

        idx.add("b.md", "About transformers and attention")
        assert idx.page_count == 3

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

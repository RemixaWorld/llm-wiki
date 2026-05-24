# URL Fetcher Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port sanctumz's web fetching capabilities into llm-wiki as an independent `src/fetcher/` module with disk-based caching and CLI integration.

**Architecture:** New `src/fetcher/` package ported from sanctumz with adaptations (Pydantic models, stdlib logging, no notebook dependency). `wiki fetch` command for standalone fetching; `wiki ingest <url>` auto-fetches to cache then runs standard ingest pipeline.

**Tech Stack:** httpx, trafilatura, beautifulsoup4, html2text, playwright (optional)

---

### Task 1: Types and Dependencies

**Files:**

- Create: `src/fetcher/__init__.py`
- Create: `src/fetcher/types.py`
- Modify: `pyproject.toml`
- Test: `tests/test_fetcher_types.py`
- **Step 1: Add dependencies to pyproject.toml**

In `dependencies`, add after the `trafilatura` line:

```toml
    "beautifulsoup4>=4.12,<5.0",
    "html2text>=2024.2,<2025.0",
```

Add a new optional dependency group:

```toml
[project.optional-dependencies]
browser = ["playwright>=1.40,<2.0"]
```

Keep existing `dev` group under optional-dependencies too.

- **Step 2: Run `uv sync` to install new deps**

Run: `uv sync`
Expected: dependencies installed successfully

- **Step 3: Write `src/fetcher/__init__.py`**

```python
from __future__ import annotations
```

- **Step 4: Write `src/fetcher/types.py`**

```python
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class FetchResult(BaseModel):
    url: str
    status: str  # ok | dead | failed | paywalled | unavailable | low_quality | duplicate
    title: str | None = None
    content: str | None = None
    domain: str
    fetch_date: datetime
    error: str | None = None


class QualityResult(BaseModel):
    passed: bool
    reason: str | None = None
```

- **Step 5: Write failing test**

```python
from __future__ import annotations

from datetime import datetime

from src.fetcher.types import FetchResult, QualityResult


def test_fetch_result_creation():
    now = datetime.now()
    r = FetchResult(url="https://example.com", status="ok", content="hello", domain="example.com", fetch_date=now)
    assert r.url == "https://example.com"
    assert r.status == "ok"
    assert r.error is None


def test_quality_result_defaults():
    q = QualityResult(passed=True)
    assert q.reason is None
```

- **Step 6: Run tests**

Run: `uv run pytest tests/test_fetcher_types.py -v`
Expected: PASS

- **Step 7: Commit**

```bash
git add src/fetcher/__init__.py src/fetcher/types.py tests/test_fetcher_types.py pyproject.toml uv.lock
git commit -m "feat(fetcher): add types module and dependencies"
```

---

### Task 2: URL Utilities and Content Extractor

**Files:**

- Create: `src/fetcher/url_utils.py`
- Create: `src/fetcher/content_extractor.py`
- Test: `tests/test_fetcher_url_utils.py`
- **Step 1: Write `src/fetcher/url_utils.py`**

```python
from __future__ import annotations

import hashlib
from urllib.parse import urlparse


MEDIUM_DOMAINS = {
    "medium.com", "levelup.gitconnected.com",
    "ai.gopubby.com", "pub.towardsai.net", "generativeai.pub",
    "blog.devgenius.io", "python.plainenglish.io", "ai.plainenglish.io",
    "blog.gopenai.com", "blog.stackademic.com",
}

SKIP_DOMAINS = ("twitter.com", "x.com", "reddit.com", "www.reddit.com", "old.reddit.com")


def url_to_filename(url: str) -> str:
    url_hash = hashlib.sha256(url.encode()).hexdigest()[:8]
    return f"{url_hash}.md"


def get_domain_dir(url: str) -> str:
    domain = urlparse(url).netloc
    if domain in MEDIUM_DOMAINS:
        return "medium"
    return domain


def is_medium_url(url: str) -> bool:
    domain = urlparse(url).netloc
    return domain in MEDIUM_DOMAINS


def is_substack_url(url: str) -> bool:
    return ".substack.com/p/" in url
```

- **Step 2: Write `src/fetcher/content_extractor.py`**

```python
from __future__ import annotations

import trafilatura


def extract_content(html: str, url: str) -> str | None:
    if not html:
        return None
    return trafilatura.extract(html, output_format="markdown", include_images=True)
```

- **Step 3: Write tests**

```python
from __future__ import annotations

from src.fetcher.url_utils import (
    get_domain_dir,
    is_medium_url,
    is_substack_url,
    url_to_filename,
)


def test_url_to_filename_deterministic():
    assert url_to_filename("https://example.com/a") == url_to_filename("https://example.com/a")


def test_url_to_filename_different_urls():
    assert url_to_filename("https://a.com") != url_to_filename("https://b.com")


def test_url_to_filename_format():
    name = url_to_filename("https://example.com")
    assert name.endswith(".md")
    assert len(name) == 12  # 8 hex chars + ".md"


def test_get_domain_dir_regular():
    assert get_domain_dir("https://www.pinecone.io/learn/chunking") == "www.pinecone.io"


def test_get_domain_dir_medium():
    assert get_domain_dir("https://medium.com/test") == "medium"
    assert get_domain_dir("https://levelup.gitconnected.com/test") == "medium"


def test_is_medium_url():
    assert is_medium_url("https://medium.com/something")
    assert not is_medium_url("https://example.com")


def test_is_substack_url():
    assert is_substack_url("https://kaitchup.substack.com/p/grpo-train")
    assert not is_substack_url("https://substack.com")
```

- **Step 4: Run tests**

Run: `uv run pytest tests/test_fetcher_url_utils.py -v`
Expected: PASS

- **Step 5: Commit**

```bash
git add src/fetcher/url_utils.py src/fetcher/content_extractor.py tests/test_fetcher_url_utils.py
git commit -m "feat(fetcher): add URL utilities and content extractor"
```

---

### Task 3: Content Filter and Dedup

**Files:**

- Create: `src/fetcher/content_filter.py`
- Create: `src/fetcher/dedup.py`
- Test: `tests/test_fetcher_filter_dedup.py`
- **Step 1: Write `src/fetcher/content_filter.py`**

```python
from __future__ import annotations

from src.fetcher.types import QualityResult


def check_quality(text: str | None) -> QualityResult:
    if not text:
        return QualityResult(passed=False, reason="too_short")

    stripped = text.strip()
    lower = stripped.lower()

    if len(stripped) < 500:
        for pattern in ("403 forbidden", "access denied", "404 not found", "cloudflare"):
            if pattern in lower:
                return QualityResult(passed=False, reason="error_page")

    if len(stripped) < 100:
        words = lower.split()
        if len(words) <= 2:
            for pattern in ("nginx", "error", "forbidden"):
                if pattern in words:
                    return QualityResult(passed=False, reason="error_page")

    if len(stripped) < 200:
        return QualityResult(passed=False, reason="too_short")

    return QualityResult(passed=True)
```

- **Step 2: Write `src/fetcher/dedup.py`**

```python
from __future__ import annotations

import hashlib
from pathlib import Path


def _stable_hash(s: str) -> int:
    return int.from_bytes(hashlib.md5(s.encode("utf-8")).digest()[:8], "little")


def minhash(text: str, num_perm: int = 128) -> set[int]:
    if not text:
        return set()

    content = text.strip()[:8192]
    shingles = [content[i:i + 4] for i in range(max(len(content) - 3, 0))]
    if not shingles:
        return set()

    hashes = {_stable_hash(s) for s in shingles}
    return set(sorted(hashes)[:num_perm])


def jaccard_similarity(a: set[int], b: set[int]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


class DedupIndex:
    def __init__(self, output_path: Path, threshold: float = 0.85):
        import yaml

        self._threshold = threshold
        self._index: dict[str, dict[str, set[int]]] = {}

        if not output_path.exists():
            return

        for domain_dir in output_path.iterdir():
            if not domain_dir.is_dir():
                continue
            domain = domain_dir.name
            self._index[domain] = {}
            for fp in domain_dir.glob("*.md"):
                text = fp.read_text(encoding="utf-8")
                if not text.startswith("---"):
                    continue
                end = text.find("---", 3)
                if end == -1:
                    continue
                meta = yaml.safe_load(text[3:end])
                if meta.get("status") != "ok":
                    continue
                body = text[end + 3:].strip()
                if body:
                    self._index[domain][fp.name] = minhash(body)

    def check(self, domain: str, content: str) -> str | None:
        domain_index = self._index.get(domain)
        if not domain_index or not content:
            return None

        sig = minhash(content)
        for filename, existing_sig in domain_index.items():
            if jaccard_similarity(sig, existing_sig) >= self._threshold:
                return filename
        return None

    def add(self, domain: str, filename: str, content: str) -> None:
        if not content:
            return
        self._index.setdefault(domain, {})[filename] = minhash(content)
```

- **Step 3: Write tests**

```python
from __future__ import annotations

from pathlib import Path

import pytest

from src.fetcher.content_filter import check_quality
from src.fetcher.dedup import DedupIndex, jaccard_similarity, minhash


class TestCheckQuality:
    def test_none_text(self):
        assert check_quality(None).passed is False

    def test_empty_text(self):
        assert check_quality("").passed is False

    def test_short_text(self):
        assert check_quality("short").passed is False

    def test_error_page_403(self):
        assert check_quality("403 Forbidden").passed is False

    def test_error_page_404(self):
        assert check_quality("404 Not Found").passed is False

    def test_valid_content(self):
        text = "x" * 300
        assert check_quality(text).passed is True

    def test_error_page_not_flagged_in_long_content(self):
        # "cloudflare" in long content should NOT be flagged (only short content)
        text = "cloudflare " * 100
        assert check_quality(text).passed is True


class TestMinhash:
    def test_empty_text(self):
        assert minhash("") == set()

    def test_deterministic(self):
        assert minhash("hello world") == minhash("hello world")

    def test_similar_texts_have_high_jaccard(self):
        a = minhash("The quick brown fox jumps over the lazy dog")
        b = minhash("The quick brown fox jumps over the lazy cat")
        assert jaccard_similarity(a, b) > 0.5


class TestDedupIndex:
    def test_empty_dir(self, tmp_path: Path):
        idx = DedupIndex(tmp_path / "web")
        assert idx.check("example.com", "some content") is None

    def test_detect_duplicate(self, tmp_path: Path):
        web = tmp_path / "web" / "example.com"
        web.mkdir(parents=True)
        (web / "abc12345.md").write_text("---\nstatus: ok\n---\nHello world this is some content for testing")
        idx = DedupIndex(tmp_path / "web")
        result = idx.check("example.com", "Hello world this is some content for testing")
        assert result is not None

    def test_no_duplicate(self, tmp_path: Path):
        web = tmp_path / "web" / "example.com"
        web.mkdir(parents=True)
        (web / "abc12345.md").write_text("---\nstatus: ok\n---\nCompletely different topic about quantum physics")
        idx = DedupIndex(tmp_path / "web")
        assert idx.check("example.com", "Cooking recipes with Italian pasta and tomatoes") is None
```

- **Step 4: Run tests**

Run: `uv run pytest tests/test_fetcher_filter_dedup.py -v`
Expected: PASS

- **Step 5: Commit**

```bash
git add src/fetcher/content_filter.py src/fetcher/dedup.py tests/test_fetcher_filter_dedup.py
git commit -m "feat(fetcher): add content filter and MinHash dedup"
```

---

### Task 4: Medium and Substack Extractors

**Files:**

- Create: `src/fetcher/medium_fetcher.py`
- Create: `src/fetcher/substack_fetcher.py`
- Test: `tests/test_fetcher_site_extractors.py`
- **Step 1: Write `src/fetcher/medium_fetcher.py`**

Port from sanctumz with these changes:

- Replace `import structlog` / `structlog.get_logger()` with `logging.getLogger(__name__)`
- Add `from __future__ import annotations`
- Keep all extraction logic (`extract_medium_content`, helpers) unchanged

Full file content — copy from sanctumz `src/sanctumz/fetcher/medium_fetcher.py` (168 lines) with the logging adaptation above.

- **Step 2: Write `src/fetcher/substack_fetcher.py`**

Port from sanctumz with these changes:

- Replace `structlog` with `logging.getLogger(__name__)`
- Change `from sanctumz.fetcher.types import FetchResult` to `from src.fetcher.types import FetchResult`
- Convert `SubstackAuth` from dataclass to Pydantic `BaseModel`
- Add `from __future__ import annotations`
- Keep all API logic (`fetch_substack`, `_extract_body_html`, `_slug_from_url`) unchanged

Full file content — copy from sanctumz `src/sanctumz/fetcher/substack_fetcher.py` (186 lines) with the adaptations above.

- **Step 3: Write tests**

```python
from __future__ import annotations

from src.fetcher.medium_fetcher import extract_medium_content, is_medium_url
from src.fetcher.substack_fetcher import _slug_from_url, is_substack_url


class TestMediumExtractor:
    def test_extract_from_html(self):
        html = "<html><body><article><h1>Test Title</h1><p>This is a test paragraph with enough content to pass quality checks.</p></article></body></html>"
        result = extract_medium_content(html)
        assert result is not None
        assert "Test Title" in result

    def test_extract_empty_html(self):
        assert extract_medium_content("") is None
        assert extract_medium_content(None) is None

    def test_is_medium_url():
        assert is_medium_url("https://medium.com/test")
        assert is_medium_url("https://blog.devgenius.io/test")
        assert not is_medium_url("https://example.com")


class TestSubstackHelpers:
    def test_slug_from_url(self):
        pub, slug = _slug_from_url("https://kaitchup.substack.com/p/grpo-train-llms")
        assert pub == "kaitchup"
        assert slug == "grpo-train-llms"

    def test_slug_from_bad_url(self):
        pub, slug = _slug_from_url("https://example.com/no-slug")
        assert pub == ""
        assert slug == ""

    def test_is_substack_url(self):
        assert is_substack_url("https://pub.substack.com/p/article")
        assert not is_substack_url("https://substack.com")
```

- **Step 4: Run tests**

Run: `uv run pytest tests/test_fetcher_site_extractors.py -v`
Expected: PASS

- **Step 5: Commit**

```bash
git add src/fetcher/medium_fetcher.py src/fetcher/substack_fetcher.py tests/test_fetcher_site_extractors.py
git commit -m "feat(fetcher): add Medium and Substack extractors"
```

---

### Task 5: Core Fetcher (httpx)

**Files:**

- Create: `src/fetcher/fetcher.py`
- Test: `tests/test_fetcher_core.py`
- **Step 1: Write `src/fetcher/fetcher.py`**

Port from sanctumz `fetcher.py` (146 lines) with these changes:

- Replace `structlog` with `logging.getLogger(__name__)`
- Change imports from `sanctumz.fetcher.*` to `src.fetcher.*`
- Import URL utilities from `src.fetcher.url_utils` instead of inline
- Keep the core logic: `fetch_urls()` with semaphore concurrency, retry with exponential backoff, URL routing (Twitter/X/Reddit skip, Substack → API, Medium → browser queue, others → httpx + trafilatura)
- **Step 2: Write tests**

```python
from __future__ import annotations

from datetime import datetime
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from src.fetcher.fetcher import fetch_urls, get_domain_dir, url_to_filename
from src.fetcher.types import FetchResult


@pytest.fixture
def mock_httpx_client():
    with patch("src.fetcher.fetcher.httpx.AsyncClient") as mock_cls:
        client = AsyncMock()
        mock_cls.return_value.__aenter__ = AsyncMock(return_value=client)
        mock_cls.return_value.__aexit__ = AsyncMock(return_value=False)
        yield client


class TestFetchUrls:
    @pytest.mark.asyncio
    async def test_skip_twitter(self, mock_httpx_client):
        results = await fetch_urls(["https://twitter.com/user/status/123"])
        assert results[0].status == "unavailable"

    @pytest.mark.asyncio
    async def test_skip_reddit(self, mock_httpx_client):
        results = await fetch_urls(["https://reddit.com/r/test"])
        assert results[0].status == "unavailable"

    @pytest.mark.asyncio
    async def test_medium_marked_failed(self, mock_httpx_client):
        results = await fetch_urls(["https://medium.com/test-article"])
        assert results[0].status == "failed"
        assert "browser" in results[0].error.lower()

    @pytest.mark.asyncio
    async def test_dead_url_404(self, mock_httpx_client):
        resp = httpx.Response(404, request=httpx.Request("GET", "https://example.com"))
        mock_httpx_client.get = AsyncMock(return_value=resp)
        results = await fetch_urls(["https://example.com/gone"])
        assert results[0].status == "dead"

    @pytest.mark.asyncio
    async def test_successful_fetch(self, mock_httpx_client):
        resp = httpx.Response(200, text="<html><body><p>Content here</p></body></html>", request=httpx.Request("GET", "https://example.com"))
        mock_httpx_client.get = AsyncMock(return_value=resp)
        with patch("src.fetcher.fetcher.extract_content", return_value="Content here"):
            results = await fetch_urls(["https://example.com/article"])
        assert results[0].status == "ok"
        assert results[0].domain == "example.com"

    @pytest.mark.asyncio
    async def test_retry_on_network_error(self, mock_httpx_client):
        mock_httpx_client.get = AsyncMock(side_effect=httpx.ConnectError("timeout"))
        with patch("src.fetcher.fetcher.asyncio.sleep", new_callable=AsyncMock):
            results = await fetch_urls(["https://example.com/fail"], max_retries=2)
        assert results[0].status == "failed"

    @pytest.mark.asyncio
    async def test_substack_routing(self, mock_httpx_client):
        with patch("src.fetcher.fetcher.fetch_substack", new_callable=AsyncMock) as mock_sub:
            mock_sub.return_value = FetchResult(
                url="https://pub.substack.com/p/test", status="ok",
                content="hello", domain="pub.substack.com",
                fetch_date=datetime.now(),
            )
            results = await fetch_urls(["https://pub.substack.com/p/test"])
        assert results[0].status == "ok"
        mock_sub.assert_called_once()
```

- **Step 3: Run tests**

Run: `uv run pytest tests/test_fetcher_core.py -v`
Expected: PASS

- **Step 4: Commit**

```bash
git add src/fetcher/fetcher.py tests/test_fetcher_core.py
git commit -m "feat(fetcher): add core httpx fetcher with URL routing"
```

---

### Task 6: Browser Fetcher

**Files:**

- Create: `src/fetcher/browser_fetcher.py`
- Test: `tests/test_fetcher_browser.py`
- **Step 1: Write `src/fetcher/browser_fetcher.py`**

Port from sanctumz `browser_fetcher.py` (85 lines) with these changes:

- Replace `structlog` with `logging.getLogger(__name__)`
- Convert `BrowserFetchResult` dataclass to Pydantic `BaseModel`
- Add `from __future__ import annotations`
- Keep all Playwright logic unchanged
- **Step 2: Write tests**

```python
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.fetcher.browser_fetcher import parse_cookie_string


def test_parse_cookie_string():
    cookies = parse_cookie_string("sid=abc123; token=xyz", "example.com")
    assert len(cookies) == 2
    assert cookies[0]["name"] == "sid"
    assert cookies[0]["value"] == "abc123"
    assert cookies[0]["domain"] == "example.com"


def test_parse_cookie_string_empty():
    assert parse_cookie_string("", "example.com") == []


def test_parse_cookie_string_single():
    cookies = parse_cookie_string("key=val", "example.com")
    assert len(cookies) == 1
    assert cookies[0]["name"] == "key"
```

- **Step 3: Run tests**

Run: `uv run pytest tests/test_fetcher_browser.py -v`
Expected: PASS

- **Step 4: Commit**

```bash
git add src/fetcher/browser_fetcher.py tests/test_fetcher_browser.py
git commit -m "feat(fetcher): add Playwright browser fetcher"
```

---

### Task 7: URL Collector

**Files:**

- Create: `src/fetcher/url_collector.py`
- Test: `tests/test_fetcher_url_collector.py`
- **Step 1: Write `src/fetcher/url_collector.py`**

Port from sanctumz `url_collector.py` (111 lines) with these changes:

- Remove `_urls_from_notes()` and the `notes_dir` field from `UrlSource` (llm-wiki has no notebook parser)
- Convert `UrlSource` from dataclass to Pydantic `BaseModel`
- Keep `_urls_from_file`, `_urls_from_retry`, `collect_urls`
- In `collect_urls`, remove notes_dir branch entirely
- **Step 2: Write tests**

```python
from __future__ import annotations

from pathlib import Path

import pytest

from src.fetcher.url_collector import UrlSource, collect_urls


class TestCollectUrls:
    def test_direct_urls(self):
        src = UrlSource(urls=["https://a.com", "https://b.com"])
        urls, _ = collect_urls(src)
        assert urls == ["https://a.com", "https://b.com"]

    def test_dedup_preserves_order(self):
        src = UrlSource(urls=["https://a.com", "https://b.com", "https://a.com"])
        urls, _ = collect_urls(src)
        assert urls == ["https://a.com", "https://b.com"]

    def test_from_file(self, tmp_path: Path):
        f = tmp_path / "urls.txt"
        f.write_text("https://c.com\nhttps://d.com\n")
        src = UrlSource(urls_file=str(f))
        urls, _ = collect_urls(src)
        assert urls == ["https://c.com", "https://d.com"]

    def test_from_file_skips_blank_lines(self, tmp_path: Path):
        f = tmp_path / "urls.txt"
        f.write_text("https://c.com\n\n  \nhttps://d.com\n")
        src = UrlSource(urls_file=str(f))
        urls, _ = collect_urls(src)
        assert urls == ["https://c.com", "https://d.com"]

    def test_retry_failed(self, tmp_path: Path):
        web = tmp_path / "web" / "example.com"
        web.mkdir(parents=True)
        (web / "abc12345.md").write_text("---\nstatus: failed\nurl: https://example.com/fail\n---\n")
        (web / "def67890.md").write_text("---\nstatus: ok\nurl: https://example.com/ok\n---\n")
        src = UrlSource(retry_dir=tmp_path / "web")
        urls, _ = collect_urls(src)
        assert urls == ["https://example.com/fail"]

    def test_mixed_sources_dedup(self, tmp_path: Path):
        f = tmp_path / "urls.txt"
        f.write_text("https://a.com\n")
        src = UrlSource(urls=["https://a.com", "https://b.com"], urls_file=str(f))
        urls, _ = collect_urls(src)
        assert urls == ["https://a.com", "https://b.com"]
```

- **Step 3: Run tests**

Run: `uv run pytest tests/test_fetcher_url_collector.py -v`
Expected: PASS

- **Step 4: Commit**

```bash
git add src/fetcher/url_collector.py tests/test_fetcher_url_collector.py
git commit -m "feat(fetcher): add URL collector"
```

---

### Task 8: Cache Layer (read/write data/web/)

**Files:**

- Create: `src/fetcher/cache.py`
- Test: `tests/test_fetcher_cache.py`
- **Step 1: Write `src/fetcher/cache.py`**

```python
from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

import yaml

from src.fetcher.types import FetchResult
from src.fetcher.url_utils import get_domain_dir, url_to_filename

logger = logging.getLogger(__name__)


def cache_path_for_url(url: str, web_dir: Path) -> Path:
    domain_dir = get_domain_dir(url)
    filename = url_to_filename(url)
    return web_dir / domain_dir / filename


def read_cache(url: str, web_dir: Path) -> FetchResult | None:
    path = cache_path_for_url(url, web_dir)
    if not path.exists():
        return None
    try:
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            return None
        end = text.find("---", 3)
        if end == -1:
            return None
        meta = yaml.safe_load(text[3:end])
        body = text[end + 3:].strip()
        return FetchResult(
            url=meta.get("url", url),
            status=meta.get("status", "unknown"),
            title=meta.get("title"),
            content=body or None,
            domain=meta.get("domain", ""),
            fetch_date=meta.get("fetch_date", datetime.now()),
            error=meta.get("error"),
        )
    except Exception:
        logger.warning("corrupt cache file path=%s", path)
        return None


def write_cache(result: FetchResult, web_dir: Path) -> Path:
    path = cache_path_for_url(result.url, web_dir)
    path.parent.mkdir(parents=True, exist_ok=True)

    meta = {
        "url": result.url,
        "status": result.status,
        "domain": result.domain,
        "fetch_date": result.fetch_date.isoformat(),
    }
    if result.title:
        meta["title"] = result.title
    if result.error:
        meta["error"] = result.error

    frontmatter = yaml.dump(meta, default_flow_style=False).strip()
    body = result.content or ""
    content = f"---\n{frontmatter}\n---\n\n{body}\n"

    path.write_text(content, encoding="utf-8")
    return path


def is_cached_ok(url: str, web_dir: Path) -> bool:
    result = read_cache(url, web_dir)
    return result is not None and result.status == "ok"
```

- **Step 2: Write tests**

```python
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from src.fetcher.cache import is_cached_ok, read_cache, write_cache
from src.fetcher.types import FetchResult


class TestCache:
    def test_write_and_read(self, tmp_path: Path):
        web = tmp_path / "web"
        now = datetime.now()
        result = FetchResult(
            url="https://example.com/article",
            status="ok",
            title="Test Article",
            content="Hello world content",
            domain="example.com",
            fetch_date=now,
        )
        path = write_cache(result, web)
        assert path.exists()
        assert "example.com" in str(path)

        cached = read_cache("https://example.com/article", web)
        assert cached is not None
        assert cached.status == "ok"
        assert cached.title == "Test Article"
        assert "Hello world" in (cached.content or "")

    def test_read_missing(self, tmp_path: Path):
        assert read_cache("https://missing.com", tmp_path / "web") is None

    def test_is_cached_ok(self, tmp_path: Path):
        web = tmp_path / "web"
        now = datetime.now()
        ok_result = FetchResult(url="https://ok.com", status="ok", content="x" * 300, domain="ok.com", fetch_date=now)
        write_cache(ok_result, web)
        assert is_cached_ok("https://ok.com", web) is True
        assert is_cached_ok("https://missing.com", web) is False

    def test_write_failed_still_caches(self, tmp_path: Path):
        web = tmp_path / "web"
        now = datetime.now()
        result = FetchResult(url="https://fail.com", status="failed", domain="fail.com", fetch_date=now, error="timeout")
        path = write_cache(result, web)
        assert path.exists()
        cached = read_cache("https://fail.com", web)
        assert cached is not None
        assert cached.status == "failed"

    def test_is_cached_ok_false_for_failed(self, tmp_path: Path):
        web = tmp_path / "web"
        now = datetime.now()
        result = FetchResult(url="https://fail.com", status="failed", domain="fail.com", fetch_date=now)
        write_cache(result, web)
        assert is_cached_ok("https://fail.com", web) is False
```

- **Step 3: Run tests**

Run: `uv run pytest tests/test_fetcher_cache.py -v`
Expected: PASS

- **Step 4: Commit**

```bash
git add src/fetcher/cache.py tests/test_fetcher_cache.py
git commit -m "feat(fetcher): add disk cache layer for data/web/"
```

---

### Task 9: Fetcher Public API

**Files:**

- Modify: `src/fetcher/__init__.py`
- Test: `tests/test_fetcher_api.py`
- **Step 1: Update `src/fetcher/__init__.py`**

```python
from __future__ import annotations

import logging
from pathlib import Path

from src.fetcher.browser_fetcher import fetch_with_browser
from src.fetcher.cache import is_cached_ok, read_cache, write_cache
from src.fetcher.content_filter import check_quality
from src.fetcher.dedup import DedupIndex
from src.fetcher.fetcher import fetch_urls
from src.fetcher.medium_fetcher import extract_medium_content
from src.fetcher.types import FetchResult
from src.fetcher.url_collector import UrlSource, collect_urls
from src.fetcher.url_utils import is_medium_url

logger = logging.getLogger(__name__)


async def run_fetch(
    urls: list[str],
    web_dir: Path,
    *,
    urls_file: str | None = None,
    retry_failed: bool = False,
    use_browser: bool = False,
    concurrency: int = 10,
    cookies: dict[str, str] | None = None,
) -> list[FetchResult]:
    """Fetch URLs and cache results to data/web/. Returns all results."""
    src = UrlSource(
        urls=urls,
        urls_file=urls_file,
        retry_dir=web_dir if retry_failed else None,
    )
    collected, _ = collect_urls(src)

    if not collected:
        logger.info("no URLs to fetch")
        return []

    # Filter out already-cached ok URLs
    to_fetch = [u for u in collected if not is_cached_ok(u, web_dir)]
    logger.info("urls total=%d cached=%d to_fetch=%d", len(collected), len(collected) - len(to_fetch), len(to_fetch))

    if not to_fetch:
        return [r for u in collected if (r := read_cache(u, web_dir)) is not None]

    # Fetch via httpx
    results = await fetch_urls(to_fetch, cookies=cookies, concurrency=concurrency)

    # Quality filter + dedup
    dedup = DedupIndex(web_dir)
    for i, r in enumerate(results):
        if r.status != "ok" or not r.content:
            continue
        quality = check_quality(r.content)
        if not quality.passed:
            results[i] = r.model_copy(update={"status": quality.reason if quality.reason in ("error_page", "low_quality") else "low_quality"})
            continue
        dup = dedup.check(r.domain, r.content)
        if dup:
            results[i] = r.model_copy(update={"status": "duplicate", "error": f"duplicate of {dup}"})

    # Write all results to cache
    for r in results:
        write_cache(r, web_dir)

    # Browser retry
    browser_needed = [
        r for r in results
        if r.status == "failed" and (is_medium_url(r.url) or use_browser)
    ]
    if browser_needed:
        try:
            from playwright.async_api import async_playwright

            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                for r in browser_needed:
                    br = await fetch_with_browser(r.url, browser)
                    if br.status == "ok" and br.html:
                        content = extract_medium_content(br.html) if is_medium_url(r.url) else None
                        if content is None:
                            from src.fetcher.content_extractor import extract_content
                            content = extract_content(br.html, r.url)
                        quality = check_quality(content)
                        final_status = "ok" if quality.passed else "low_quality"
                        updated = r.model_copy(update={"status": final_status, "content": content})
                        write_cache(updated, web_dir)
                await browser.close()
        except ImportError:
            logger.warning("playwright not installed, skipping browser fetch. Install with: uv pip install playwright && playwright install chromium")

    # Return all results (including previously cached)
    final = []
    for u in collected:
        cached = read_cache(u, web_dir)
        if cached:
            final.append(cached)
    return final


async def fetch_single(url: str, web_dir: Path, *, use_browser: bool = False) -> FetchResult:
    """Fetch a single URL. Returns cached result if available, otherwise fetches."""
    cached = read_cache(url, web_dir)
    if cached and cached.status == "ok":
        return cached
    results = await run_fetch([url], web_dir, use_browser=use_browser)
    return results[0] if results else FetchResult(
        url=url, status="failed", domain="", fetch_date=__import__("datetime").datetime.now(), error="no result",
    )
```

- **Step 2: Write integration test**

```python
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from src.fetcher import fetch_single, run_fetch
from src.fetcher.types import FetchResult


class TestRunFetch:
    @pytest.mark.asyncio
    async def test_skip_cached_ok(self, tmp_path: Path):
        web = tmp_path / "web"
        now = datetime.now()
        cached = FetchResult(url="https://cached.com", status="ok", content="x" * 300, domain="cached.com", fetch_date=now)
        from src.fetcher.cache import write_cache
        write_cache(cached, web)

        results = await run_fetch(["https://cached.com"], web)
        assert len(results) == 1
        assert results[0].status == "ok"

    @pytest.mark.asyncio
    async def test_fetch_uncached(self, tmp_path: Path):
        web = tmp_path / "web"
        mock_result = FetchResult(url="https://new.com", status="ok", content="x" * 300, domain="new.com", fetch_date=datetime.now())
        with patch("src.fetcher.fetch_urls", new_callable=AsyncMock, return_value=[mock_result]):
            results = await run_fetch(["https://new.com"], web)
        assert len(results) == 1
        assert results[0].status == "ok"


class TestFetchSingle:
    @pytest.mark.asyncio
    async def test_returns_cached(self, tmp_path: Path):
        web = tmp_path / "web"
        now = datetime.now()
        cached = FetchResult(url="https://cached.com", status="ok", content="x" * 300, domain="cached.com", fetch_date=now)
        from src.fetcher.cache import write_cache
        write_cache(cached, web)

        result = await fetch_single("https://cached.com", web)
        assert result.status == "ok"
```

- **Step 3: Run tests**

Run: `uv run pytest tests/test_fetcher_api.py -v`
Expected: PASS

- **Step 4: Commit**

```bash
git add src/fetcher/__init__.py tests/test_fetcher_api.py
git commit -m "feat(fetcher): add public API with caching and browser retry"
```

---

### Task 10: Integrate into extract.py

**Files:**

- Modify: `src/extract.py:60-84` (replace `extract_url`) and `103-120` (modify `extract_source`)
- Test: `tests/test_extract.py` (extend existing or add new)
- **Step 1: Modify `extract_url` in `src/extract.py`**

Replace the existing `extract_url` function (lines 60-84) with:

```python
def extract_url(url: str) -> ExtractedSource:
    """Extract text from a URL. Uses data/web/ cache if available."""
    from src.fetcher.cache import is_cached_ok, read_cache
    from src.fetcher.url_utils import get_domain_dir, url_to_filename

    settings = get_settings()
    web_dir = settings.sources_dir.parent / "data" / "web"

    # Check cache first
    cached = read_cache(url, web_dir)
    if cached and cached.content:
        title = cached.title or url
        logger.info("extracted url from cache url=%s tokens=%d", url, count_tokens(cached.content))
        return ExtractedSource(
            content=cached.content,
            source_type="url",
            title=title,
            metadata={"url": url},
        )

    # Fallback to trafilatura (existing behavior)
    import trafilatura

    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        msg = f"failed to download URL: {url}"
        raise ValueError(msg)

    content = trafilatura.extract(downloaded)
    if not content:
        msg = f"no content extracted from URL: {url}"
        raise ValueError(msg)

    metadata = trafilatura.extract_metadata(downloaded)
    title = metadata.title if metadata and metadata.title else url

    logger.info("extracted url=%s tokens=%d", url, count_tokens(content))

    return ExtractedSource(
        content=content,
        source_type="url",
        title=title,
        metadata={"url": url},
    )
```

- **Step 2: Write test**

Add to existing `tests/test_extract.py` or create new test:

```python
def test_extract_url_uses_cache(tmp_path, monkeypatch):
    from src.fetcher.cache import write_cache
    from src.fetcher.types import FetchResult
    from src.config import Settings

    settings = Settings(sources_dir=tmp_path / "sources")
    monkeypatch.setattr("src.extract.get_settings", lambda: settings)

    web_dir = tmp_path / "data" / "web"
    now = __import__("datetime").datetime.now()
    cached = FetchResult(url="https://example.com/test", status="ok", content="cached content here", domain="example.com", fetch_date=now)
    write_cache(cached, web_dir)

    result = extract_url("https://example.com/test")
    assert result.content == "cached content here"
    assert result.source_type == "url"
```

- **Step 3: Run tests**

Run: `uv run pytest tests/test_extract.py -v`
Expected: PASS (all existing + new test)

- **Step 4: Commit**

```bash
git add src/extract.py tests/test_extract.py
git commit -m "feat: extract_url checks data/web/ cache before fetching"
```

---

### Task 11: CLI — `wiki fetch` Command

**Files:**

- Modify: `src/cli.py`
- Test: `tests/test_cli_fetch.py`
- **Step 1: Add `fetch` command to `src/cli.py`**

Add after the `ingest` command (after line 53):

```python
@main.command()
@click.argument("urls", nargs=-1, required=True)
@click.option("--urls-file", default=None, help="File with URLs, one per line.")
@click.option("--retry-failed", is_flag=True, help="Re-fetch previously failed URLs.")
@click.option("--browser", is_flag=True, help="Enable Playwright browser fallback.")
@click.option("--concurrency", default=10, type=int, help="Max concurrent requests.")
def fetch(urls: tuple[str, ...], urls_file: str | None, retry_failed: bool, browser: bool, concurrency: int) -> None:
    """Fetch URL(s) and cache content to data/web/."""
    from pathlib import Path

    from src.fetcher import run_fetch

    settings = get_settings()
    web_dir = settings.sources_dir.parent / "data" / "web"

    results = asyncio.run(run_fetch(
        list(urls),
        web_dir,
        urls_file=urls_file,
        retry_failed=retry_failed,
        use_browser=browser,
        concurrency=concurrency,
    ))

    ok = sum(1 for r in results if r.status == "ok")
    failed = sum(1 for r in results if r.status != "ok")

    for r in results:
        color = "green" if r.status == "ok" else "yellow" if r.status in ("duplicate", "low_quality") else "red"
        click.secho(f"  [{r.status}] {r.url}", fg=color)
        if r.title and r.status == "ok":
            click.echo(f"    title: {r.title}")
        if r.error:
            click.echo(f"    error: {r.error}")

    click.echo()
    click.secho(f"Done: {ok} fetched, {failed} issues", fg="green" if not failed else "yellow")
```

Also remove the dead `--url` flag from `ingest` command (line 34): remove the `@click.option("--url", ...)` decorator and the `url: bool` parameter.

- **Step 2: Write CLI test**

```python
from __future__ import annotations

from click.testing import CliRunner

from src.cli import main


def test_fetch_help():
    runner = CliRunner()
    result = runner.invoke(main, ["fetch", "--help"])
    assert result.exit_code == 0
    assert "urls-file" in result.output
    assert "retry-failed" in result.output
    assert "browser" in result.output
```

- **Step 3: Run tests**

Run: `uv run pytest tests/test_cli_fetch.py -v`
Expected: PASS

- **Step 4: Commit**

```bash
git add src/cli.py tests/test_cli_fetch.py
git commit -m "feat: add wiki fetch CLI command, remove dead --url flag"
```

---

### Task 12: Integration — `wiki ingest <url>` Auto-Fetch

**Files:**

- Modify: `src/ingest.py:235-245` (modify `extract_text_node`)
- Modify: `src/config.py` (add `web_data_dir` setting)
- Test: `tests/test_ingest_url.py`
- **Step 1: Add `web_data_dir` to `src/config.py` Settings class**

Add after `sources_dir` (line 19):

```python
    web_data_dir: Path = Path("data/web")
```

- **Step 2: Modify `extract_text_node` in `src/ingest.py`**

Replace lines 235-245 with:

```python
async def extract_text_node(state: IngestState) -> IngestState:
    """Extract text from the source file or URL."""
    try:
        source = state["source_path"]
        if source.startswith(("http://", "https://")):
            # Auto-fetch URL to cache if not already cached
            from src.fetcher import fetch_single

            settings = get_settings()
            result = await fetch_single(source, settings.web_data_dir)
            if result.status != "ok":
                msg = f"URL fetch failed: {source} status={result.status} error={result.error}"
                raise ValueError(msg)

            title = result.title or source
            return {
                "extracted_text": result.content or "",
                "source_title": title,
            }

        result = extract_source(source)
        return {
            "extracted_text": result.content,
            "source_title": result.title,
        }
    except Exception as exc:
        logger.error("extraction failed path=%s", state["source_path"], exc_info=True)
        return {"errors": [f"extraction failed: {exc}"]}
```

- **Step 3: Write test**

```python
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from src.fetcher.types import FetchResult
from src.ingest import extract_text_node


class TestExtractTextNode:
    @pytest.mark.asyncio
    async def test_url_auto_fetch(self):
        mock_result = FetchResult(
            url="https://example.com/test",
            status="ok",
            title="Test Page",
            content="Hello world content",
            domain="example.com",
            fetch_date=datetime.now(),
        )
        with patch("src.ingest.fetch_single", new_callable=AsyncMock, return_value=mock_result):
            state = await extract_text_node({"source_path": "https://example.com/test"})
        assert state["extracted_text"] == "Hello world content"
        assert state["source_title"] == "Test Page"

    @pytest.mark.asyncio
    async def test_url_fetch_failed(self):
        mock_result = FetchResult(
            url="https://fail.com",
            status="failed",
            domain="fail.com",
            fetch_date=datetime.now(),
            error="timeout",
        )
        with patch("src.ingest.fetch_single", new_callable=AsyncMock, return_value=mock_result):
            state = await extract_text_node({"source_path": "https://fail.com"})
        assert "errors" in state
        assert "failed" in state["errors"][0]

    @pytest.mark.asyncio
    async def test_file_path_unchanged(self, tmp_path: Path):
        f = tmp_path / "test.txt"
        f.write_text("file content here")
        state = await extract_text_node({"source_path": str(f)})
        assert state["extracted_text"] == "file content here"
```

- **Step 4: Run all tests**

Run: `uv run pytest -v`
Expected: ALL PASS

- **Step 5: Commit**

```bash
git add src/ingest.py src/config.py tests/test_ingest_url.py
git commit -m "feat: wiki ingest <url> auto-fetches via fetcher cache"
```

---

### Task 13: Run Full Test Suite + Lint

**Files:**

- None (verification only)
- **Step 1: Run full test suite**

Run: `uv run pytest -v`
Expected: ALL PASS

- **Step 2: Run linter**

Run: `uv run ruff check src/fetcher/ src/extract.py src/ingest.py src/config.py src/cli.py && uv run ruff format --check src/fetcher/ src/extract.py src/ingest.py src/config.py src/cli.py`
Expected: No errors

- **Step 3: Fix any lint issues**

If ruff reports issues, fix them and re-run.

---

## Self-Review

**Spec coverage:**

- Module structure (10 files) → Tasks 1-8
- `wiki fetch` CLI → Task 11
- `wiki ingest <url>` auto-fetch → Task 12
- Cache read/write in `data/web/` → Task 8
- Content filter + dedup → Task 3
- Medium extractor → Task 4
- Substack extractor → Task 4
- Browser fallback → Task 6, 9
- URL collector (file, retry, dedup) → Task 7
- Dependencies (httpx already in pyproject.toml, add bs4/html2text) → Task 1
- Error handling (retry, status marking) → Tasks 5, 9
- `--url` dead flag removal → Task 11

**No placeholders** — all code shown explicitly or described as "port from sanctumz file X with these specific changes."

**Type consistency** — `FetchResult` (Pydantic BaseModel) used consistently across all modules. `QualityResult` (Pydantic BaseModel) in content_filter. `UrlSource` (Pydantic BaseModel) in url_collector. `BrowserFetchResult` (Pydantic BaseModel) in browser_fetcher.
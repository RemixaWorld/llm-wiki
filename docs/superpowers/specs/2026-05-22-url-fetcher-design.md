# URL Fetcher Design

Port sanctumz's web fetching capabilities into llm-wiki as an independent `src/fetcher/` module, with disk-based caching in `data/web/` and seamless integration into the existing ingest pipeline.

## Architecture

### Module Structure

```
src/
  fetcher/                    # New module, ported from sanctumz
    __init__.py               # Public API: fetch_urls(), fetch_single()
    fetcher.py                # Core httpx fetcher + concurrency/retry/URL routing
    browser_fetcher.py        # Playwright browser fallback
    medium_fetcher.py         # Medium-family site extractor (BS4 + html2text)
    substack_fetcher.py       # Substack JSON API extractor
    content_extractor.py      # Generic trafilatura extraction
    content_filter.py         # Quality filter (min chars, error page detection)
    dedup.py                  # MinHash near-duplicate detection
    url_collector.py          # URL collection and dedup
    types.py                  # FetchResult and related models
  extract.py                  # Modified: URL path checks data/web/ cache first
  ingest.py                   # Modified: URL input triggers fetcher cache step
  cli.py                      # Modified: new wiki fetch command, improved wiki ingest --url
data/
  web/                        # Existing directory, fetch cache storage
    {domain}/{hash}.md        # Format identical to sanctumz output
```

### Data Flow

**`wiki fetch` flow:**

```
URL(s) input
  → url_collector: dedup, merge sources (CLI args / --urls-file / --retry-failed)
  → cache check: scan data/web/{domain}/{hash}.md, skip status=ok
  → fetcher.py: httpx batch fetch (10 concurrent, 3 retries exponential backoff)
      ├─ Twitter/X/Reddit → mark unavailable
      ├─ Substack → JSON API
      ├─ Medium → mark for browser retry
      └─ Others → httpx GET + trafilatura extract
  → content_filter: quality check (≥200 chars, not error page)
  → dedup: MinHash near-duplicate (same domain, Jaccard ≥ 0.85)
  → write data/web/{domain}/{hash}.md (YAML frontmatter + Markdown body)
  → browser_fetcher: Playwright retry (Medium always, others 403 + --browser flag)
  → update data/web/ files
```

**`wiki ingest <url>` flow (modified):**

```
URL input
  → check data/web/{domain}/{hash}.md exists with status=ok
      ├─ yes → use cached file as source
      └─ no → call fetcher to fetch and cache, then use cached file
  → standard ingest pipeline (extract → chunk → process_batches → update_links)
```

### Cache Format

Each cached file is Markdown with YAML frontmatter:

```yaml
---
url: https://example.com/article
status: ok  # ok / dead / failed / paywalled / unavailable / low_quality / duplicate
domain: example.com
fetch_date: "2026-05-22"
title: "Article Title"
---

Markdown content here...
```

Cache key rules:
- Domain directory: URL netloc, Medium-family 11 domains consolidated into `medium/`
- Filename: `SHA-256(url)[:8].md`

## CLI Interface

### `wiki fetch` — Fetch URL content

```bash
wiki fetch https://example.com/article                    # Single URL
wiki fetch url1 url2                                     # Multiple URLs
wiki fetch --urls-file urls.txt                          # Batch from file
wiki fetch --retry-failed                                # Retry previously failed
wiki fetch --browser https://medium.com/...              # Enable browser fallback
wiki fetch --concurrency 5 https://example.com/...       # Concurrency control
```

### `wiki ingest` — Modified URL handling

```bash
wiki ingest https://example.com/article                  # Auto-fetch cache + ingest
wiki ingest https://example.com/article --fresh           # Force re-fetch + ingest
wiki ingest path/to/file.pdf                             # File ingest unchanged
```

### `wiki ingest-all` — Unchanged

Batch processes files in `sources/`, no URL fetching involved.

## Dependencies

```toml
# Added to [project.dependencies]
"httpx>=0.27"           # Async HTTP client
"beautifulsoup4>=4.12"  # HTML parsing (Medium/Substack)
"html2text>=2024.2"     # HTML→Markdown (Medium/Substack)

# New optional dependency group
[project.optional-dependencies]
browser = ["playwright>=1.40"]
```

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Network error | httpx retries 3x with exponential backoff (1s, 2s, 4s), then `failed` |
| Browser error | 30s timeout, then `failed` |
| Low quality | Content < 200 chars → `low_quality` |
| Error page | Detect 403/404/Cloudflare text → appropriate status |
| Paywall | Substack `audience == "only_paid"` → `paywalled` |
| Duplicate | MinHash Jaccard ≥ 0.85 → `duplicate` |
| All failures | Still written to cache to avoid re-attempting known failures |

## Code Adaptation (from sanctumz)

When porting from sanctumz:

1. **Remove notebook dependency** — sanctumz's note fallback becomes plain `failed`
2. **Logging** — sanctumz uses `structlog`, adapt to `logging.getLogger(__name__)`
3. **Type system** — sanctumz uses dataclass, convert to Pydantic models
4. **Async** — keep async, consistent with llm-wiki LLM call style
5. **Cookies** — read from `cookies.json` (same format as sanctumz), silently skip if absent

## Testing

- **Unit tests** for fetcher module: mock httpx/playwright, no real network access
  - URL routing logic (Medium → browser, Substack → API, others → httpx)
  - Cache hit/skip logic
  - Quality filter and dedup
  - Error status marking and retry
- **Integration tests**: `wiki fetch` CLI end-to-end (mocked network), `wiki ingest <url>` cache-through flow
- **No changes to existing ingest tests** — core pipeline unchanged

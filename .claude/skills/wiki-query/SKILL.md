---
name: wiki-query
description: >
  Use when the user asks a question that may be answered from the project wiki.
  Do NOT answer from memory — always read wiki pages first.
  Triggers on: technical concept questions, "what does the wiki say about X",
  summarizing or comparing topics, knowledge retrieval from ingested sources.
  Does NOT trigger for: coding tasks, file edits, general conversation.
---

# Wiki Query

Answer questions by searching and reading wiki pages. The wiki is the source of truth.

## Pre-condition

Check that `wiki/` directory exists and contains `.md` files. If empty or missing, tell the user to run `wiki ingest` first.

## Process

### Step 1: Scout the wiki

Glob `wiki/*.md` to see available pages. Scan filenames — they are slugs (lowercase, hyphens) derived from page titles. This gives a map of what knowledge exists.

### Step 2: Iterative retrieval (max 3 rounds)

Repeat this loop up to 3 times. Break early when you have enough information.

**Round N:**

1. **Expand keywords**
   - Extract key terms from the question
   - Expand with: synonyms, Chinese↔English equivalents, abbreviations, domain jargon
   - In rounds 2+, incorporate vocabulary learned from previously read pages (frontmatter tags, linked page titles, technical terms encountered)

2. **Search**
   - grep the expanded keywords across `wiki/*.md` (both frontmatter and body)
   - Collect candidate pages not yet read in this session

3. **Read + follow links**
   - Read the most relevant candidates in full (up to 5 per round)
   - Follow `[[WikiLinks]]` one level deep for additional context
   - Track which pages have been read — do not re-read

4. **Sufficiency check**
   - Can you fully answer the question with what you've gathered?
   - If yes → break loop, proceed to synthesis
   - If no → continue to next round with expanded search terms

### Step 3: Synthesize

Write the answer following this format:

```
**Answer:**
[Synthesized response, grounded in wiki content]

**Sources:**
- [[Page Title 1]]
- [[Page Title 2]]

**Gaps:**
- [What the wiki doesn't cover yet, if anything]
```

Rules for synthesis:
- Every factual claim must trace back to a wiki page — cite as `[[Page Title]]`
- When pages disagree, note the disagreement
- When the wiki lacks coverage, say so explicitly
- Suggest follow-up questions or sources to ingest

## Fallback

If grep yields poor results after 2 rounds (vocabulary mismatch, topic not found by keywords), run:

```bash
uv run wiki query "question here"
```

This uses BM25 search as a complementary retrieval method. Use its output to identify pages you may have missed, then read those pages directly.

## Gotchas

- **Never answer from memory.** The wiki may contradict what you think you know. That contradiction is valuable signal.
- **grep frontmatter too.** Page titles, tags, and brief fields contain dense keyword information — don't only search body text.
- **Slug ≠ title.** Filenames are slugs (`rag-chunking.md`) but `[[WikiLinks]]` use original titles (`[[RAG Chunking]]`). Match accordingly.
- **Don't re-read pages.** Track what you've read across rounds to avoid wasting context.
- **Frontmatter format.** Each page starts with YAML between `---` markers. Key fields: `title`, `tags`, `brief`, `type`, `sources`, `related`.

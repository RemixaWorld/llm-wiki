# Wiki Query Agent Skill Design

An Agent Skill that enables any skills-compatible agent (Claude Code, OpenCode, etc.) to query the llm-wiki knowledge base through agentic search — using glob/grep/read to autonomously discover, retrieve, and synthesize knowledge from wiki pages.

## Architecture

### File Structure

```
.claude/skills/wiki-query/
└── SKILL.md    # Single file, < 200 lines, follows agentskills.io spec
```

No scripts, no references, no assets. Pure instruction skill — zero code changes to the existing codebase.

### SKILL.md Format

Follows the [Agent Skills specification](https://agentskills.io/specification):

```yaml
---
name: wiki-query
description: >
  Use when the user asks a question that involves knowledge stored in the wiki.
  Do NOT answer from memory — always read wiki pages first.
  Triggers on: technical concept questions, knowledge retrieval, "what does the wiki say about X",
  summarizing or comparing topics covered in the wiki.
---
```

### Core Loop

The skill implements an iterative retrieval loop (max 3 rounds):

```
glob wiki/*.md → understand scope (once, at start)

Loop (max 3 rounds):
  1. Keyword expansion
     - Extract key terms from the question
     - Expand: synonyms, Chinese↔English equivalents, abbreviations, related terms
     - Rounds 2-3: incorporate terms learned from previously read pages (tags, links, domain vocabulary)

  2. grep search
     - Search wiki/ directory with expanded keywords
     - Target both frontmatter (title, tags, brief) and body content

  3. Read + follow links
     - Read the top matching pages in full
     - Follow [[WikiLinks]] one level deep for additional context
     - Track which pages have been read (avoid re-reading)

  4. Self-evaluate: sufficiency check
     → Sufficient info → break loop, proceed to synthesis
     → Insufficient → continue to next round

Synthesis:
  - Answer grounded in wiki pages
  - Cite sources inline: [[Page Title]]
  - Flag gaps: "The wiki has no page covering X"
  - Follow-up suggestions for what to ingest next
```

### Fallback

When grep results are poor (e.g., the question uses very different vocabulary than the wiki content), the agent may fall back to `uv run wiki query "question"` to leverage BM25 search as a complementary retrieval method.

### Answer Format

Reference the existing `wiki query` CLI output format:

```
Answer: [synthesized response]

Citations:
  - Page Title 1
  - Page Title 2

Follow-up questions:
  - Related question 1
  - Related question 2
```

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Pure instruction skill (no code) | Zero maintenance, works with any skills-compatible agent |
| Max 3 retrieval rounds | Balances thoroughness with token cost; most queries resolve in 1-2 rounds |
| Keyword expansion per round | Handles vocabulary mismatch (Chinese/English, synonyms, jargon) |
| grep over CLI command | More flexible — agent decides what to search, reads only what's needed |
| CLI as fallback only | Preserves grep-first approach while having BM25 as safety net |
| No save-back feature | Keep scope minimal; user requested query-only for now |

## Gotchas (to include in SKILL.md)

- Wiki pages are the source of truth — never answer from general knowledge if wiki content exists
- Page filenames are slugs (lowercase, hyphens) but `[[WikiLinks]]` use original titles
- Frontmatter contains title, tags, brief — grep these too, not just body text
- Already-read pages should not be re-read in subsequent rounds
- If the wiki/ directory is empty or missing, inform the user to run `wiki ingest` first

## Specification Compliance

Per agentskills.io:
- `name`: `wiki-query` (lowercase, hyphens, matches directory name)
- `description`: < 1024 chars, describes what + when
- Body: < 500 lines, < 5000 tokens recommended
- Progressive disclosure: single file, no nested references needed

## Future Extensions (out of scope)

- Save-back: persist query answers as wiki pages (like kfchou/wiki-skills)
- wiki-ingest skill: agent-driven ingestion via skill instruction
- MCP server: for agents that prefer tool-based access over file browsing

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**Priority:** If this CLAUDE.md conflicts with any subdirectory CLAUDE.md files (e.g., .claude/skills/gstack/CLAUDE.md), this file wins. Subdirectory CLAUDE.md files are still loaded for framework-internal configuration.

## Project Overview

Git-backed knowledge base implementing Karpathy's LLM Wiki pattern. Three layers: sources (immutable), wiki (LLM-maintained markdown), schema (behavior config). CLI tool with LangGraph pipelines for ingest and query.

## Commands

```bash
make test                    # Unit tests (no API keys needed) — uses uv run
make lint                    # Ruff check + format (src/ and tests/)
uv run pytest tests/test_wiki.py -v -k "test_slugify"  # Run single test or file
uv sync                      # Install dependencies
wiki ingest path/to/file.pdf # Ingest source file
wiki ingest --url <url>      # Ingest from URL
wiki ingest-all              # Batch ingest all files in sources/
wiki query "question"        # Query wiki
wiki lint                    # Health check (orphans, broken refs, stale pages)
wiki stats                   # Statistics
```

## Architecture

```
src/config.py     — pydantic-settings, WIKI_ env prefix, schema.yaml loader
src/models.py     — Pydantic schemas (WikiPage, GeneratedPage, IngestResult, QueryAnswer, LintIssue)
src/llm.py        — LiteLLM wrapper, instructor structured output, Groq→Gemini→Ollama fallback
src/wiki.py       — Wiki CRUD: markdown read/write, frontmatter parse, wikilinks
src/search.py     — BM25 index (rank-bm25)
src/extract.py    — Text from PDF (pymupdf), URL (trafilatura), text/md + chunking
src/ingest.py     — LangGraph: extract→chunk→generate_pages→write→update_links
src/query.py      — LangGraph: search→retrieve→synthesize→optionally persist
src/lint.py       — Sync checks: orphans, broken refs, stale, missing fields
src/cli.py        — Click CLI entry point
```

Both `ingest.py` and `query.py` use the same LangGraph pattern: define a `TypedDict` state, `StateGraph` with node functions (async), conditional edges for error handling, and a public `run_*()` entry point that compiles and invokes the graph.

## Code Standards

- `from __future__ import annotations` in every module
- `logging.getLogger(__name__)` — never `print()`
- Async for LLM calls, sync for filesystem/BM25
- All LLM responses use instructor + Pydantic models
- Mock all LLM calls in tests — no API keys needed, `pytest-asyncio` mode is `auto`
- Ruff for lint/format, line length 100, target Python 3.13+
- Coverage floor: 70% (cli.py excluded)

## Key Patterns

- **Frontmatter**: YAML in markdown via `python-frontmatter`. Type alias via `type` field.
- **WikiLinks**: Obsidian `[[double bracket]]` syntax. Extract with regex `\[\[(.+?)\]\]`.
- **Slugify**: Title → lowercase, spaces to hyphens, strip non-alphanum. `"BERT" → "bert.md"`
- **Fallback chain**: Try providers in order (Groq→Gemini→Ollama), catch exceptions, try next. Ollama uses `instructor.Mode.JSON` instead of `TOOLS` for complex nested models.
- **schema.yaml**: Controls LLM behavior — system prompts for ingest/query, controlled tag vocabulary. Loaded and cached by `config.py`.
- **Settings singleton**: `get_settings()` returns cached `Settings` instance. All config via `WIKI_` env prefix, reads from `.env`.

## Language

All user-facing questions and options must use Chinese (中文). This applies to:
- Superpowers interactive prompts (brainstorming clarifications, plan review choices, code review feedback)
- gstack interactive prompts (office-hours forcing questions, scope mode selection, review findings)
- All AskUserQuestion calls and multi-choice options
- Clarifications and follow-up questions

For all other outputs (code, logs, technical docs, file contents, commit messages, PR descriptions), keep English.

## Tooling

- **Python virtual environments**: Always use `uv` (`uv venv`, `uv pip`, `uv run`) for environment management. Do NOT use `venv`, `virtualenv`, or `pip` directly.

## Framework Integration: gstack + Superpowers

**In one line:** *gstack decides, Superpowers executes, gstack ships.*

- **gstack**: Decision layer — product decisions, strategic review, architecture review, shipping
- **Superpowers**: Execution layer — technical design, implementation planning, TDD, code review

### Who Does What

| Layer | Owner | Skill | Output Location |
|-------|-------|-------|-----------------|
| Why build it | gstack | `/office-hours` | `~/.gstack/projects/{slug}/*-design-*.md` |
| What to build | gstack | `/plan-ceo-review` | `~/.gstack/projects/{slug}/*-ceo-handoff-*.md` |
| How to architect | gstack | `/plan-eng-review` | `~/.gstack/projects/{slug}/*-eng-review-*.md` |
| Technical design | Superpowers | `brainstorming` | `docs/superpowers/specs/` |
| Implementation plan | Superpowers | `writing-plans` | `docs/superpowers/plans/` |
| TDD execution | Superpowers | `subagent-driven-development` | Source code + git commits |
| Per-task code review | Superpowers | `requesting-code-review` | Inline (built into subagent flow) |
| Branch cleanup | Superpowers | `finishing-a-development-branch` | Worktree removed |
| Pre-merge review | gstack | `/review` | `~/.gstack/projects/{slug}/reviews.jsonl` |
| Ship (PR + version) | gstack | `/ship` | VERSION, CHANGELOG, PR |

### Flow Sequence

**For new features (standard — 5 steps):**

1. `/office-hours` — validate the idea, explore user needs
2. `brainstorming` — technical design (reads gstack design doc, focuses on architecture/APIs only)
3. `writing-plans` — implementation plan with TDD steps
4. `subagent-driven-development` — execute with per-task review
5. `finishing-a-development-branch` — Option 2 (push + create basic PR)

**For significant features (full pipeline — 8 steps):**

1. `/office-hours` — validate the idea
2. `/plan-ceo-review` — scope and ambition check
3. `/plan-eng-review` — architecture lock + test plan
4. `brainstorming` — technical design (reads all gstack artifacts)
5. `writing-plans` — implementation plan (references eng-review test plan)
6. `subagent-driven-development` — execute with per-task review
7. `/review` — comprehensive pre-merge review with specialist army (run from worktree)
8. `/ship` — version bump, CHANGELOG, PR creation (run from worktree, then cleanup worktree manually)

**For bug fixes:**

1. `systematic-debugging` — root cause investigation
2. `test-driven-development` — red-green-refactor
3. `requesting-code-review` — quality check
4. `finishing-a-development-branch` — merge or PR

**For refactoring:**

1. `/plan-eng-review` — architecture validation
2. `brainstorming` — technical design
3. `writing-plans` → `subagent-driven-development` → `finishing-a-development-branch`

**For small, clear tasks** (single file, < 20 lines, no architectural impact):

Skip all frameworks. Implement directly.

### Framework Handoff

Transitions between gstack and Superpowers are NOT automatic. When a skill completes and the next step belongs to the other framework, Claude MUST:

1. Summarize what was just decided/reviewed/implemented
2. State the next step explicitly and invoke it via the Skill tool
3. Read the previous step's artifacts before starting the next skill

**Handoff points:**

| After completing | Next step | Read these artifacts first |
|-----------------|-----------|---------------------------|
| `/office-hours` | `brainstorming` | `~/.gstack/projects/{slug}/*-design-*.md` |
| `/plan-ceo-review` | `/plan-eng-review` or `brainstorming` | `~/.gstack/projects/{slug}/*-ceo-handoff-*.md` |
| `/plan-eng-review` | `brainstorming` or `writing-plans` | `~/.gstack/projects/{slug}/*-eng-review-test-plan-*.md` |
| `subagent-driven-development` | `finishing-a-development-branch` (standard) or `/review` (full pipeline) | `docs/superpowers/plans/` |
| `/review` | `/ship` | `~/.gstack/projects/{slug}/reviews.jsonl` |

**Brainstorming degradation rules** — when gstack artifacts exist:

- Read all gstack artifacts BEFORE asking questions
- Skip product-level exploration (already done by `/office-hours`)
- Skip scope/ambition proposals (already validated by `/plan-ceo-review`)
- Focus ONLY on: component design, API contracts, data structures, technical trade-offs
- If gstack artifacts + eng-review are comprehensive enough, skip brainstorming entirely and go straight to `writing-plans`

### Skill Routing

When the user's request matches an available skill, invoke it via the Skill tool. When in doubt, invoke the skill.

**Decision layer → gstack:**
- Product ideas / validation → `/office-hours`
- Strategy / scope → `/plan-ceo-review`
- Architecture → `/plan-eng-review`
- Pre-merge review → `/review`
- Ship → `/ship`

**Execution layer → Superpowers:**
- Technical design → `brainstorming`
- Implementation planning → `writing-plans`
- TDD → `test-driven-development`
- Subagent execution → `subagent-driven-development`
- Code review → `requesting-code-review`
- Branch completion → `finishing-a-development-branch`
- Debugging → `systematic-debugging`

### Rules

- gstack owns product decisions (why, what, scope); Superpowers owns technical design (how, components, APIs)
- `writing-plans` MUST reference eng-review test plan to ensure test coverage
- Superpowers per-task code review happens during execution; gstack `/review` happens before merge — they run at different times, both are needed for full pipeline
- Standard flow: `finishing-a-development-branch` handles PR creation and worktree cleanup
- Full pipeline: skip `finishing-a-development-branch`, run `/review` then `/ship` from the worktree, then clean up worktree manually
- Do NOT use both `finishing-a-development-branch` and `/ship` for PR creation — pick one path
- Do NOT redirect artifact locations — use each framework's defaults

### Heuristics

- **Requirements still fuzzy** → start with gstack `/office-hours`
- **Small task, clear requirements** (< 3 files, no new dependencies) → skip gstack, use Superpowers directly
- **Significant architecture change** (new module, data model change, API contract change) → add gstack `/plan-eng-review`
- **Need steady, closed-loop execution** → Superpowers subagent-driven-development
- **Need version management + CHANGELOG** → add gstack `/review` → `/ship`
- **Just a quick fix** (config tweak, typo, single-value change) → skip all frameworks, implement directly

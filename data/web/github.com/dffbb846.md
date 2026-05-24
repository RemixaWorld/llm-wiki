---
domain: github.com
fetch_date: '2026-05-18T12:37:03.703861'
status: ok
url: https://github.com/Canner/WrenAI
---

📣

2026-05-07— Wren Engine has merged into this repo under`core/`

. The previous`Canner/wren-engine`

repo is archived. The previous WrenAI GenBI app is preserved on the`legacy/v1`

branch (tag`v1-final`

). Read the announcement →

WrenAI is the **open context layer** that gives your agents what schemas don't: business semantics, examples, memory, governance, and — soon — the unstructured corporate knowledge that lives in your docs, wikis, and chat threads. Built for the agent frameworks you already use.

**Open by default**— Apache-2.0 core, SDK, and skills.**Built for AI agents**— Skills, agentic architecutre, context retrieval are first-class. Ships as SDKs for the agent frameworks engineers already use.**Correctness as primitives**— rich schema retrieval, dry-plan validation, structured errors with hints, value profiling, eval runner. The agent orchestrates; the trace lives in the agent's reasoning.**Reviewable, reproducible context**— every definition, example, and mapping is versionable and evidence-linked. Git-friendly. Not chat history.**Sits on top of your existing stack**— warehouse, transformation pipelines, your existing semantic layer. Not another tool to maintain.

If you're building AI agents, embedded analytics, or natural-language data products on top of your enterprise databases, you've hit the same wall: there's no shared governed layer between your data and your consumers. Your agents query Postgres, MySQL, SQL Server, Oracle, Snowflake, BigQuery, or Databricks through raw SQL or MCP — and they hallucinate joins, guess at table semantics, and invent metric definitions every time. Your analysts and your apps each reinvent the same logic in their own dialect. Your local LLMs and cloud LLMs need the same governed context to produce trustworthy answers, but nothing today provides it. The result is a multiplication problem: N agents × M databases × K models = N×M×K brittle integrations, none of which agree. The missing piece is a context layer purpose-built for the agent era — open, MCP-native, and interoperable across every database and every model.

![The problem without context layer](https://private-user-images.githubusercontent.com/1216029/593510136-0fdb989a-e741-4d34-bcb9-4854787f73fb.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzkwNzkzMjYsIm5iZiI6MTc3OTA3OTAyNiwicGF0aCI6Ii8xMjE2MDI5LzU5MzUxMDEzNi0wZmRiOTg5YS1lNzQxLTRkMzQtYmNiOS00ODU0Nzg3ZjczZmIucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDUxOCUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjA1MThUMDQzNzA2WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9YzUwZThjM2M1MDUyYzBiMGQxNjM0ZTZjZTZjZjg4MWUyODIxNzIyYWIyMGU0NTc3NTIxZGZlNGVmOGY4Mjk5MSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmcmVzcG9uc2UtY29udGVudC10eXBlPWltYWdlJTJGcG5nIn0.X0EgbwmgFlgkugOsg2BBl1DR1RXy39CqxLU5KMcbR6o)

![before & after](https://private-user-images.githubusercontent.com/1216029/593656666-ab54ee9f-b652-4826-b6f5-0c22f601419e.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzkwNzkzMjYsIm5iZiI6MTc3OTA3OTAyNiwicGF0aCI6Ii8xMjE2MDI5LzU5MzY1NjY2Ni1hYjU0ZWU5Zi1iNjUyLTQ4MjYtYjZmNS0wYzIyZjYwMTQxOWUucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDUxOCUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjA1MThUMDQzNzA2WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9MzI2MTJlMzlhYWIyZmQxMGIyY2M2OTk5ZDZiYmMzZTdlY2QwZjc5ZjE1ZTMxOTgyMGIzMzNkNTllNzYwOThmNiZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmcmVzcG9uc2UtY29udGVudC10eXBlPWltYWdlJTJGcG5nIn0.oMtsHP9yf1IZsjFXspaL8pvE-AKW7B5zvuLikLCWB7k)

WrenAI is **agent-driven by design**: you install the skill bundle once, then let your AI coding agent (Claude Code, Openclaw, Hermes, Codex, etc.) drive the rest — Python deps, DB connection, project scaffold, and first query.

Skills are workflow guides that teach AI coding agents (Claude Code, Openclaw, Hermes, Codex, etc.) how to drive the Wren CLI for you.

`npx skills add Canner/WrenAI --skill '*'`

Have multiple AI coding agents installed and want the skills available in all of them? Pass `--agent '*'`

:

`npx skills add Canner/WrenAI --skill '*' --agent '*'`

Or via the install script:

`curl -fsSL https://raw.githubusercontent.com/Canner/WrenAI/main/skills/install.sh | bash`

See the Skills reference for the full list of skills installed and what each one does.

Open your agent in a project directory and ask:

Use the `/wren-onboarding`

skill to install and set up Wren AI.

The agent will check your environment, install `wren-engine`

, create a connection profile, scaffold the project, and run a first query — all in one flow.

Once onboarding finishes, give your project the business context schemas can't carry:

Use the `/wren-enrich-context`

skill in grill mode.

Two modes: **grill** (one question at a time, you in the loop) or **auto-pilot** (agent reads `<project>/raw/`

and proposes). Both modes write to MDL, instructions, queries, and memory — all reviewable, all Git-friendly.

```
# Ask any question
"who are our top 10 customers by sales this quarter?"
```

Or just ask your agent in natural language — it uses the context layer to resolve schema, recall similar past queries, and write governed SQL.

**Want to try it without your own database?** Ask your agent to run `/wren-onboarding`

with the bundled `jaffle_shop`

sample dataset — same flow, but you'll be querying a real warehouse end-to-end in a couple of minutes.

```
/wren-onboarding # Scaffold a Wren project from your DB (agent-driven)
/wren-enrich-context # One skill, two modes: (Under development)
# grill — one question at a time, you in the loop
# auto-pilot — agent reads <project>/raw/ and proposes
wren ask "..." # Query through the context layer
```

Fast at first. Deep when you need it. Always reviewable and Git-friendly.

**Modeling Definition Language (MDL)**— models, columns, relationships, views, cubes, metrics, row-level / column-level access control (RLAC / CLAC)**Engine**— Apache DataFusion based, 22+ data sources**Memory & examples**— LanceDB-backed, hybrid retrieval, versionable**Agent SDK**—`wren-langchain`

(LangChain / LangGraph),`wren-pydantic`

; reference Python integration for other stacks**Governed execution primitives**— functions, dry-plan, row limits, access control

**Context enrichment skill**—`/wren-enrich-context`

(grill + auto-pilot modes) hardened across MDL, instructions, queries, and memory**End-to-end correctness primitives**— value profiling, rich retrieval, structured errors, golden eval runner**Agent-native distribution**— first-class SDKs across major agent frameworks; see GitHub Discussions for what's prioritized next**Full governed execution**— audit logs, rate limits, approval workflow, data-flow inspector

Full roadmap and design notes: see the vision paper.

- Quickstart — from skill install to first answer
- Concepts — what context is, what MDL is, how memory works
- Connect a database — Postgres, BigQuery, Snowflake, DuckDB, and more
- Agent SDKs — what's shipping today, what's next

- 💬 Discord — chat with the team and other builders
- 🐙 GitHub Discussions — design conversations, RFCs, longer threads
- 🐦 Twitter / X — release notes and short updates
- 🗞 Blog — vision, post-mortems, deep dives

We build in the open. Issues, PRs, connector contributions, SDK integrations, docs fixes — all welcome.

- Contributor guide
- Connector ecosystem program — three-tier ownership: official, community-blessed, community-owned
- Architecture map — find the right place to land your change
- Looking for somewhere to start? Try the
`good first issue`

label.

**Project structure** — click to expand

```
core/
wren-core/ Rust semantic engine (Apache DataFusion)
wren-core-base/ Shared manifest types + MDL builder
wren-core-py/ Python bindings (PyPI: wren-core)
wren-core-wasm/ WebAssembly build (npm: wren-core-wasm)
wren/ Python SDK and CLI (PyPI: wren-engine)
wren-mdl/ MDL JSON schema
sdk/
wren-langchain/ Reference agent SDK integration
skills/ Agent skills for context authoring
docs/ Module documentation
examples/ Example projects
```


Apache 2.0. See LICENSE.

*Come build the context layer with us.*

**If WrenAI helps you, drop a ⭐ — it genuinely helps us grow!**

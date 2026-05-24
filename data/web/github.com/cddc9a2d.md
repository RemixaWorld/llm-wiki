---
domain: github.com
fetch_date: '2026-05-18T12:35:44.972399'
status: ok
url: https://github.com/mem0ai/mem0
---

Learn more · Join Discord · Demo

**📄 Benchmarking Mem0's token-efficient memory algorithm →**

| Benchmark | Old | New | Tokens | Latency p50 |
|---|---|---|---|---|
LoCoMo |
71.4 | 91.6 |
7.0K | 0.88s |
LongMemEval |
67.8 | 94.8 |
6.8K | 1.09s |
BEAM (1M) |
— | 64.1 |
6.7K | 1.00s |
BEAM (10M) |
— | 48.6 |
6.9K | 1.05s |

All benchmarks run on the same production-representative model stack. Single-pass retrieval (one call, no agentic loops).

**What changed:**

**Single-pass ADD-only extraction**-- one LLM call, no UPDATE/DELETE. Memories accumulate; nothing is overwritten.**Agent-generated facts are first-class**-- when an agent confirms an action, that information is now stored with equal weight.**Entity linking**-- entities are extracted, embedded, and linked across memories for retrieval boosting.**Multi-signal retrieval**-- semantic, BM25 keyword, and entity matching scored in parallel and fused.**Temporal Reasoning**-- time-aware retrieval that ranks the right dated instance for queries about current state, past events, and upcoming plans.

See the migration guide for upgrade instructions. The evaluation framework is open-sourced so anyone can reproduce the numbers.

**91.6 on LoCoMo**-- +20 points over the previous algorithm**94.8 on LongMemEval**-- +27 points, with +53.6 on assistant memory recall**64.1 on BEAM (1M)**-- production-scale memory evaluation at 1M tokens- Read the full paper

Mem0 ("mem-zero") enhances AI assistants and agents with an intelligent memory layer, enabling personalized AI interactions. It remembers user preferences, adapts to individual needs, and continuously learns over time—ideal for customer support chatbots, AI assistants, and autonomous systems.

**Core Capabilities:**

**Multi-Level Memory**: Seamlessly retains User, Session, and Agent state with adaptive personalization**Developer-Friendly**: Intuitive API, cross-platform SDKs, and a fully managed service option

**Applications:**

**AI Assistants**: Consistent, context-rich conversations**Customer Support**: Recall past tickets and user history for tailored help**Healthcare**: Track patient preferences and history for personalized care**Productivity & Gaming**: Adaptive workflows and environments based on user behavior

AI agents can mint a working Mem0 API key in under five seconds — no email, no dashboard, no OTP. Four commands end-to-end:

```
# 1. Install
npm install -g @mem0/cli # or: pip install mem0-cli
# 2. Sign up as an agent (replace `claude-code` with your name)
mem0 init --agent --agent-caller claude-code
# 3. Add a memory
mem0 add "I am using mem0"
# 4. Search
mem0 search "am I using mem0"
```

The human owner can claim the account later with `mem0 init --email <their-email>`

— same key, memories preserved. Full guide: Sign up as an agent.

| Library | Self-Hosted Server | Cloud Platform | |
|---|---|---|---|
Best for |
Testing, prototyping | Teams running on their own infrastructure | Zero-ops production use |
Setup |
`pip install mem0ai` |
`docker compose up` |
Sign up at app.mem0.ai |
Dashboard |
-- | Yes | Yes |
Auth & API Keys |
-- | Yes | Yes |
Advanced Features |
-- | Teasers | All included |

Just testing? Use the library. Building for a team? Self-hosted. Want zero ops? Cloud.

`pip install mem0ai`

For enhanced hybrid search with BM25 keyword matching and entity extraction, install with NLP support:

```
pip install mem0ai[nlp]
python -m spacy download en_core_web_sm
```

Install sdk via npm:

`npm install mem0ai`


Note:Self-hosted auth is on by default. Upgrading from a pre-auth build? Set`ADMIN_API_KEY`

, register an admin through the wizard, or`AUTH_DISABLED=true`

for local dev only. See upgrade notes.

```
# Recommended: one command — start the stack, create an admin, issue the first API key.
cd server && make bootstrap
# Manual: start the stack and finish setup via the browser wizard.
cd server && docker compose up -d # http://localhost:3000
```

See the self-hosted docs for configuration.

- Sign up on Mem0 Platform
- Embed the memory layer via SDK or API keys
- Using hosted Qdrant vectors? See the Platform migration guide to import them into Mem0 Platform.

Manage memories from your terminal:

```
npm install -g @mem0/cli # or: pip install mem0-cli
mem0 init
mem0 add "Prefers dark mode and vim keybindings" --user-id alice
mem0 search "What does Alice prefer?" --user-id alice
```

See the CLI documentation for the full command reference.

Teach your AI coding assistant (Claude Code, Codex, Cursor, Windsurf, OpenCode, OpenClaw, and any tool that supports the skills standard) how to build with Mem0. Two categories:

**Reference skills — always on** (SDK knowledge loaded into the assistant's context):

```
npx skills add https://github.com/mem0ai/mem0 --skill mem0
npx skills add https://github.com/mem0ai/mem0 --skill mem0-cli
npx skills add https://github.com/mem0ai/mem0 --skill mem0-vercel-ai-sdk
```

**Pipeline skills — run on demand** (execute an end-to-end workflow in an existing repo):

```
npx skills add https://github.com/mem0ai/mem0 --skill mem0-integrate
npx skills add https://github.com/mem0ai/mem0 --skill mem0-test-integration
```

Use `/mem0-integrate`

to wire Mem0 into an existing repo via a test-first pipeline, then `/mem0-test-integration`

to verify. See the skills catalog or Vibecoding with Mem0 for the full picture.

Mem0 requires an LLM to function, with `gpt-5-mini`

from OpenAI as the default. However, it supports a variety of LLMs; for details, refer to our Supported LLMs documentation.

Mem0 uses `text-embedding-3-small`

from OpenAI as the default embedding model. For best results with hybrid search (semantic + keyword + entity boosting), we recommend using at least Qwen 600M or a comparable embedding model. See Supported Embeddings for configuration details.

First step is to instantiate the memory:

```
from openai import OpenAI
from mem0 import Memory
openai_client = OpenAI()
memory = Memory()
def chat_with_memories(message: str, user_id: str = "default_user") -> str:
# Retrieve relevant memories
relevant_memories = memory.search(query=message, filters={"user_id": user_id}, top_k=3)
memories_str = "\n".join(f"- {entry['memory']}" for entry in relevant_memories["results"])
# Generate Assistant response
system_prompt = f"You are a helpful AI. Answer the question based on query and memories.\nUser Memories:\n{memories_str}"
messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": message}]
response = openai_client.chat.completions.create(model="gpt-5-mini", messages=messages)
assistant_response = response.choices[0].message.content
# Create new memories from the conversation
messages.append({"role": "assistant", "content": assistant_response})
memory.add(messages, user_id=user_id)
return assistant_response
def main():
print("Chat with AI (type 'exit' to quit)")
while True:
user_input = input("You: ").strip()
if user_input.lower() == 'exit':
print("Goodbye!")
break
print(f"AI: {chat_with_memories(user_input)}")
if __name__ == "__main__":
main()
```

For detailed integration steps, see the Quickstart and API Reference.

**ChatGPT with Memory**: Personalized chat powered by Mem0 (Live Demo)**Browser Extension**: Store memories across ChatGPT, Perplexity, and Claude (Chrome Extension)**Langgraph Support**: Build a customer bot with Langgraph + Mem0 (Guide)**CrewAI Integration**: Tailor CrewAI outputs with Mem0 (Example)

- Full docs: https://docs.mem0.ai
- Community: Discord · X (formerly Twitter)
- Contact: founders@mem0.ai

We now have a paper you can cite:

```
@article{mem0,
title={Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory},
author={Chhikara, Prateek and Khant, Dev and Aryan, Saket and Singh, Taranjeet and Yadav, Deshraj},
journal={arXiv preprint arXiv:2504.19413},
year={2025}
}
```

Apache 2.0 — see the LICENSE file for details.

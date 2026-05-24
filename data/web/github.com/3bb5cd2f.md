---
domain: github.com
fetch_date: '2026-05-18T12:34:51.041442'
status: ok
url: https://github.com/SciPhi-AI/R2R
---

![Screenshot 2025-03-27 at 6 35 02 AM](https://private-user-images.githubusercontent.com/68796651/427579002-10b530a6-527f-4335-b2e4-ceaa9fc1219f.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzkwNzkxOTMsIm5iZiI6MTc3OTA3ODg5MywicGF0aCI6Ii82ODc5NjY1MS80Mjc1NzkwMDItMTBiNTMwYTYtNTI3Zi00MzM1LWIyZTQtY2VhYTlmYzEyMTlmLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjA1MTglMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwNTE4VDA0MzQ1M1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWQ2ZmFlZmY3NGRiZWQxYzU4Yzk2Zjg2Y2U4YzAwODUzZDIxNjg1ZmY3N2Y5NjRiODg1NDQ1ODUyMTllMGI3YmMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JnJlc3BvbnNlLWNvbnRlbnQtdHlwZT1pbWFnZSUyRnBuZyJ9._No-A_d7fx6Gu8ZFDvqyCC13JjNpiX010vP-t30nEt4)

### The most advanced AI retrieval system.

Agentic Retrieval-Augmented Generation (RAG) with a RESTful API.

R2R is an advanced AI retrieval system supporting Retrieval-Augmented Generation (RAG) with production-ready features. Built around a RESTful API, R2R offers multimodal content ingestion, hybrid search, knowledge graphs, and comprehensive document management.

R2R also includes a **Deep Research API**, a multi-step reasoning system that fetches relevant data from your knowledgebase and/or the internet to deliver richer, context-aware answers for complex queries.

```
# Basic search
results = client.retrieval.search(query="What is DeepSeek R1?")
# RAG with citations
response = client.retrieval.rag(query="What is DeepSeek R1?")
# Deep Research RAG Agent
response = client.retrieval.agent(
message={"role":"user", "content": "What does deepseek r1 imply? Think about market, societal implications, and more."},
rag_generation_config={
"model": "anthropic/claude-3-7-sonnet-20250219",
"extended_thinking": True,
"thinking_budget": 4096,
"temperature": 1,
"top_p": None,
"max_tokens_to_sample": 16000,
},
)
```

```
# Quick install and run in light mode
pip install r2r
export OPENAI_API_KEY=sk-...
python -m r2r.serve
# Or run in full mode with Docker
# git clone git@github.com:SciPhi-AI/R2R.git && cd R2R
# export R2R_CONFIG_NAME=full OPENAI_API_KEY=sk-...
# docker compose -f compose.full.yaml --profile postgres up -d
```

For detailed self-hosting instructions, see the self-hosting docs.

## demo_2x_comp.mp4

```
# Install SDK
pip install r2r # Python
# or
npm i r2r-js # JavaScript
```

```
from r2r import R2RClient
client = R2RClient(base_url="http://localhost:7272")
```

```
const { r2rClient } = require('r2r-js');
const client = new r2rClient("http://localhost:7272");
```

```
# Ingest sample or your own document
client.documents.create(file_path="/path/to/file")
# List documents
client.documents.list()
```

**📁 Multimodal Ingestion**: Parse`.txt`

,`.pdf`

,`.json`

,`.png`

,`.mp3`

, and more**🔍 Hybrid Search**: Semantic + keyword search with reciprocal rank fusion**🔗 Knowledge Graphs**: Automatic entity & relationship extraction**🤖 Agentic RAG**: Reasoning agent integrated with retrieval**🔐 User & Access Management**: Complete authentication & collection system

- Join our Discord for support and discussion
- Submit feature requests or bug reports
- Open PRs for new features, improvements, or documentation

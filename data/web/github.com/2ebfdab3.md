---
domain: github.com
fetch_date: '2026-05-18T12:35:47.955027'
status: ok
url: https://github.com/jmanhype/Golden-Retriever
---

DSPy-based retrieval-augmented generation (RAG) system for domain-specific question answering. Implements the Golden-Retriever paper approach: identify jargon, recognize context, augment the question, then retrieve and generate.

**Jargon identification**-- extracts technical terms from the question**Dictionary lookup**-- checks a local dictionary, then Wikipedia, then GPT as fallback**Context recognition**-- identifies the relevant domain**Question augmentation**-- rewrites the question with jargon definitions and context**Retrieval**-- fetches passages via ColBERTv2 (hosted endpoint)**Answer generation**-- ChainOfThought produces reasoning and a final answer

| File | Purpose |
|---|---|
`app.py` |
All logic: RAG pipeline, jargon dictionary, training data, evaluation, interactive loop (~300 lines) |
`requirements.txt` |
Dependencies |

This is a single-file project.

dspy, openai, aiohttp, wikipedia, rouge, sentence-transformers, cachetools, nest-asyncio, backoff.

- Python 3.8+
`OPENAI_API_KEY`

in`.env`

- Network access to the ColBERTv2 endpoint at
`20.102.90.50:2017`


```
git clone https://github.com/jmanhype/Golden-Retriever.git
cd Golden-Retriever
pip install -r requirements.txt
cp .env-sample .env # add OPENAI_API_KEY
python app.py
```

The script compiles the RAG pipeline using BootstrapFewShotWithRandomSearch on 15 training examples, evaluates on 5, then enters an interactive question loop.

Uses ROUGE-L and semantic similarity (all-MiniLM-L6-v2) against 10 hardcoded Q&A pairs about storage technology (SSDs, NVMe, NAND flash).

Proof of concept. The training set is 10 manually written Q&A pairs, so the compiled pipeline is fitted to a narrow domain. The ColBERTv2 endpoint is a third-party hosted instance that may go offline. There are no tests.

MIT

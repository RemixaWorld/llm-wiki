---
domain: github.com
fetch_date: '2026-05-18T12:37:17.299059'
status: ok
url: https://github.com/leoneversberg/llm-chatbot-cag
---

A local LLM chatbot with CAG / Context Caching for PDF input files

Install dependencies with `pip install -r requirements.txt`


Run with `streamlit run src/app.py`


Start the vLLM OpenAI-compatible server with automatic prefix caching with

`vllm serve MODEL_NAME --api-key token-abc123 --enable-prefix-caching`

Or use Docker:

```
docker run --runtime nvidia --gpus all \
-v ~/.cache/huggingface:/root/.cache/huggingface \
--env "HUGGING_FACE_HUB_TOKEN=<secret>" \
-p 8000:8000 \
--ipc=host \
vllm/vllm-openai:latest \
--model MODEL_NAME \
--api-key token-abc123 \
--enable-prefix-caching
```

You need a CUDA compatible GPU for this.

---
domain: huggingface.co
fetch_date: '2026-05-18T12:36:14.802243'
status: ok
url: https://huggingface.co/jinaai/reader-lm-0.5b
---

### Instructions to use jinaai/reader-lm-0.5b with libraries, inference providers, notebooks, and local apps. Follow these links to get started.

- Libraries
- Transformers
How to use jinaai/reader-lm-0.5b with Transformers:

# Use a pipeline as a high-level helper from transformers import pipeline pipe = pipeline("text-generation", model="jinaai/reader-lm-0.5b") messages = [ {"role": "user", "content": "Who are you?"}, ] pipe(messages)

# Load model directly from transformers import AutoTokenizer, AutoModelForCausalLM tokenizer = AutoTokenizer.from_pretrained("jinaai/reader-lm-0.5b") model = AutoModelForCausalLM.from_pretrained("jinaai/reader-lm-0.5b") messages = [ {"role": "user", "content": "Who are you?"}, ] inputs = tokenizer.apply_chat_template( messages, add_generation_prompt=True, tokenize=True, return_dict=True, return_tensors="pt", ).to(model.device) outputs = model.generate(**inputs, max_new_tokens=40) print(tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:]))

- Inference
- Notebooks
- Google Colab
- Kaggle
- Local Apps
- vLLM
How to use jinaai/reader-lm-0.5b with vLLM:

##### Install from pip and serve model

# Install vLLM from pip: pip install vllm # Start the vLLM server: vllm serve "jinaai/reader-lm-0.5b" # Call the server using curl (OpenAI-compatible API): curl -X POST "http://localhost:8000/v1/chat/completions" \ -H "Content-Type: application/json" \ --data '{ "model": "jinaai/reader-lm-0.5b", "messages": [ { "role": "user", "content": "What is the capital of France?" } ] }'

##### Use Docker

docker model run hf.co/jinaai/reader-lm-0.5b

- SGLang
How to use jinaai/reader-lm-0.5b with SGLang:

##### Install from pip and serve model

# Install SGLang from pip: pip install sglang # Start the SGLang server: python3 -m sglang.launch_server \ --model-path "jinaai/reader-lm-0.5b" \ --host 0.0.0.0 \ --port 30000 # Call the server using curl (OpenAI-compatible API): curl -X POST "http://localhost:30000/v1/chat/completions" \ -H "Content-Type: application/json" \ --data '{ "model": "jinaai/reader-lm-0.5b", "messages": [ { "role": "user", "content": "What is the capital of France?" } ] }'

##### Use Docker images

docker run --gpus all \ --shm-size 32g \ -p 30000:30000 \ -v ~/.cache/huggingface:/root/.cache/huggingface \ --env "HF_TOKEN=<secret>" \ --ipc=host \ lmsysorg/sglang:latest \ python3 -m sglang.launch_server \ --model-path "jinaai/reader-lm-0.5b" \ --host 0.0.0.0 \ --port 30000 # Call the server using curl (OpenAI-compatible API): curl -X POST "http://localhost:30000/v1/chat/completions" \ -H "Content-Type: application/json" \ --data '{ "model": "jinaai/reader-lm-0.5b", "messages": [ { "role": "user", "content": "What is the capital of France?" } ] }'

- Docker Model Runner
How to use jinaai/reader-lm-0.5b with Docker Model Runner:

docker model run hf.co/jinaai/reader-lm-0.5b


![Jina AI: Your Search Foundation, Supercharged!](https://huggingface.co/datasets/jinaai/documentation-images/resolve/main/logo.webp)


**Trained by Jina AI.**

# Intro

Jina Reader-LM is a series of models that convert HTML content to Markdown content, which is useful for content conversion tasks. The model is trained on a curated collection of HTML content and its corresponding Markdown content.

# Models

| Name | Context Length | Download |
|---|---|---|
| reader-lm-0.5b | 256K | 🤗 Hugging Face |
| reader-lm-1.5b | 256K | 🤗 Hugging Face |

# Quick Start

## On Google Colab

The easiest way to experience reader-lm is by running our Colab notebook, where we demonstrate how to use reader-lm-1.5b to convert the HackerNews website into markdown. The notebook is optimized to run smoothly on Google Colab’s free T4 GPU tier. You can also load reader-lm-0.5b or change the URL to any website and explore the output. Note that the input (i.e., the prompt) to the model is the raw HTML—no prefix instruction is required.

## Local

To use this model, you need to install `transformers`

:

```
pip install transformers<=4.43.4
```


Then, you can use the model as follows:

```
# pip install transformers
from transformers import AutoModelForCausalLM, AutoTokenizer
checkpoint = "jinaai/reader-lm-0.5b"
device = "cuda" # for GPU usage or "cpu" for CPU usage
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device)
# example html content
html_content = "<html><body><h1>Hello, world!</h1></body></html>"
messages = [{"role": "user", "content": html_content}]
input_text=tokenizer.apply_chat_template(messages, tokenize=False)
print(input_text)
inputs = tokenizer.encode(input_text, return_tensors="pt").to(device)
outputs = model.generate(inputs, max_new_tokens=1024, temperature=0, do_sample=False, repetition_penalty=1.08)
print(tokenizer.decode(outputs[0]))
```


## AWS Sagemaker & Azure Marketplace

- Downloads last month
- 276

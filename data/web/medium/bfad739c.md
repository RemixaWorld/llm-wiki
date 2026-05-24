---
domain: medium.com
fetch_date: '2026-05-18T12:56:17.934750'
status: ok
url: https://medium.com/coding-nexus/ollm-how-i-ran-an-80b-model-on-my-8gb-gpu-501a5076fd0d
---

# oLLM: How I Ran an 80B Model on My 8GB GPU

[ ![Algo Insights](https://miro.medium.com/v2/resize:fill:64:64/1*kcZSvDRaxmbCAUerJnPTUw.png) ](</@algoinsights?source=post_page---byline--501a5076fd0d--------------------------------------->)

[Algo Insights](</@algoinsights?source=post_page---byline--501a5076fd0d--------------------------------------->)

3 min read

·

Sep 30, 2025

\--

\--

Listen

Share

More

I didn’t expect this. Running a 160GB model on a card with 8GB VRAM feels impossible.

Usually, you’d laugh and move on. But then I stumbled upon **oLLM** and thought, 'Fine, let’s see.'

Turns out… it works.

oLLM is a small Python library. It’s built on Hugging Face Transformers and PyTorch, but the trick is how it handles memory.

Instead of blowing up your GPU, it streams data from the SSD, offloads tasks to the CPU, and employs some clever attention tricks. No quantisation, just fp16/bf16.

So yeah — you can actually run **Qwen3-next-80B** or **GPT-OSS-20B** on a 3060 Ti.

![image](https://miro.medium.com/v2/resize:fit:520/1*ebdGVvDHvUZueH2yTUI3Hw.png)

## What Makes oLLM Interesting

The cool part is how it does this.

Instead of attempting to fit everything into GPU memory, it **streams weights directly from SSD to GPU**.

KV caches? Those go to disk, too. It even allows you to offload layers to CPU RAM when needed.

A few recent updates (version 0.4.2) make it even better:

* **Faster and lighter** : `.safetensor` Files no longer eat up your RAM through `mmap`.
* **Bigger models are now supported** : Qwen3-next-80B runs with DiskCache support.
* **Speed bump** : that same Qwen3-next-80B manages ~1 token every 2 seconds — which is insane for its size.
* **FlashAttention-2 everywhere** : boosts stability and lowers memory usage.
* **Chunked MLPs** : split up big intermediate layers so they don’t blow up your GPU.

It’s like the devs found every little bottleneck and patched it.

## Getting Started

I recommend a venv:

```python python3 -m venv ollm_envsource ollm_env/bin/activatepip install ollm ```

If you want the source version:

```python git clone https://github.com/Mega4alik/ollm.gitcd ollmpip install -e .pip install kvikio-cu12 # adjust CUDA version ```

⚠️ Heads up: if you plan on using **Qwen3-next** , you’ll need a special dev build of Transformers:

```python pip install git+https://github.com/huggingface/transformers.git ```

Slightly annoying, but necessary.

## First Test: Llama-3 on Local GPU

Here’s a quick example script I used. It’s the “hello world” of oLLM:

```python from ollm import Inference, TextStreamero = Inference("llama3-1B-chat", device="cuda:0", logging=True)o.ini_model(models_dir="./models/", force_download=False)# Offload layers if neededo.offload_layers_to_cpu(layers_num=2)# DiskCache helps with long contextspast_key_values = o.DiskCache(cache_dir="./kv_cache/")text_streamer = TextStreamer(o.tokenizer, skip_prompt=True, skip_special_tokens=False)messages = [ {"role": "system", "content": "You are a helpful AI assistant"}, {"role": "user", "content": "List the planets in our solar system"}]input_ids = o.tokenizer.apply_chat_template( messages, reasoning_effort="minimal", tokenize=True, add_generation_prompt=True, return_tensors="pt").to(o.device)outputs = o.model.generate( input_ids=input_ids, past_key_values=past_key_values, max_new_tokens=100, streamer=text_streamer).cpu()answer = o.tokenizer.decode(outputs[0][input_ids.shape[-1]:], skip_special_tokens=False)print(answer) ```

The output is streamed token by token, just like you’d expect from ChatGPT. On an 8GB card. That still blows my mind.

## How It Pulls This Off

Think of it like this: instead of keeping everything in one backpack (your GPU), oLLM spreads the load between your GPU, CPU, and SSD. A few tricks make this possible:

1. **Weights on demand:** Loads layer weights from SSD directly to the GPU one at a time.
2. **Disk-based KV cache:** Stores attention memory on SSD instead of GPU.
3. **CPU offloading:** Pushes heavy layers to RAM if your GPU gets cramped.
4. **FlashAttention-2: Maintains efficient attention without requiring large** matrices.
5. **Chunked MLPs:** Splits up giant layers so they don’t overflow GPU memory.

The result? Huge models that used to require a $10,000 server can now run on a $200 card.

## What You Can Actually Do With This

Running big models locally isn’t just for bragging rights. Some practical uses:

* **Legal work** : Feed an entire contract or compliance doc into one pass.
* **Healthcare** : Summarise years of patient records without chopping them up.
* **Security** : Parse massive logs or threat reports offline.
* **Customer Support** : Scan historical chats to identify the most common issues.

Basically, anything where you don’t want to lose context because the model keeps forgetting what came before.

## Performance on My 3060 Ti (8GB VRAM)

Here’s what I saw when testing:

ModelContextBaseline VRAMoLLM VRAMDisk (SSD)**Qwen3–80B** 50k~190GB~7.5GB180GB**GPT-OSS-20B** 10k~40GB~7.3GB15GB**Llama-3–1B** 100k~16GB~5GB15GB**Llama-3–8B** 100k~71GB~6.6GB69GB

That’s not a typo. A **160GB model with 8GB of VRAM**.

## What’s Next for oLLM

The roadmap looks ambitious. Coming soon:

* **Gemma-3–27B** (Sept 30)
* **Voxtral-small-24B ASR** (Oct 3)
* **Qwen3-VL (vision-language)** (Oct 10)
* **Multi-token prediction** for Qwen3-next (R&D)
* Faster weight loading (R&D)

So yeah, this thing is evolving quickly.

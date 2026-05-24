---
domain: huggingface.co
fetch_date: '2026-05-18T12:35:04.564021'
status: ok
url: https://huggingface.co/Sao10K/L3-8B-Stheno-v3.2
---

### Instructions to use Sao10K/L3-8B-Stheno-v3.2 with libraries, inference providers, notebooks, and local apps. Follow these links to get started.

- Libraries
- Transformers
How to use Sao10K/L3-8B-Stheno-v3.2 with Transformers:

# Use a pipeline as a high-level helper from transformers import pipeline pipe = pipeline("text-generation", model="Sao10K/L3-8B-Stheno-v3.2") messages = [ {"role": "user", "content": "Who are you?"}, ] pipe(messages)

# Load model directly from transformers import AutoTokenizer, AutoModelForCausalLM tokenizer = AutoTokenizer.from_pretrained("Sao10K/L3-8B-Stheno-v3.2") model = AutoModelForCausalLM.from_pretrained("Sao10K/L3-8B-Stheno-v3.2") messages = [ {"role": "user", "content": "Who are you?"}, ] inputs = tokenizer.apply_chat_template( messages, add_generation_prompt=True, tokenize=True, return_dict=True, return_tensors="pt", ).to(model.device) outputs = model.generate(**inputs, max_new_tokens=40) print(tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:]))

- Inference
- HuggingChat
- Notebooks
- Google Colab
- Kaggle
- Local Apps
- vLLM
How to use Sao10K/L3-8B-Stheno-v3.2 with vLLM:

##### Install from pip and serve model

# Install vLLM from pip: pip install vllm # Start the vLLM server: vllm serve "Sao10K/L3-8B-Stheno-v3.2" # Call the server using curl (OpenAI-compatible API): curl -X POST "http://localhost:8000/v1/chat/completions" \ -H "Content-Type: application/json" \ --data '{ "model": "Sao10K/L3-8B-Stheno-v3.2", "messages": [ { "role": "user", "content": "What is the capital of France?" } ] }'

##### Use Docker

docker model run hf.co/Sao10K/L3-8B-Stheno-v3.2

- SGLang
How to use Sao10K/L3-8B-Stheno-v3.2 with SGLang:

##### Install from pip and serve model

# Install SGLang from pip: pip install sglang # Start the SGLang server: python3 -m sglang.launch_server \ --model-path "Sao10K/L3-8B-Stheno-v3.2" \ --host 0.0.0.0 \ --port 30000 # Call the server using curl (OpenAI-compatible API): curl -X POST "http://localhost:30000/v1/chat/completions" \ -H "Content-Type: application/json" \ --data '{ "model": "Sao10K/L3-8B-Stheno-v3.2", "messages": [ { "role": "user", "content": "What is the capital of France?" } ] }'

##### Use Docker images

docker run --gpus all \ --shm-size 32g \ -p 30000:30000 \ -v ~/.cache/huggingface:/root/.cache/huggingface \ --env "HF_TOKEN=<secret>" \ --ipc=host \ lmsysorg/sglang:latest \ python3 -m sglang.launch_server \ --model-path "Sao10K/L3-8B-Stheno-v3.2" \ --host 0.0.0.0 \ --port 30000 # Call the server using curl (OpenAI-compatible API): curl -X POST "http://localhost:30000/v1/chat/completions" \ -H "Content-Type: application/json" \ --data '{ "model": "Sao10K/L3-8B-Stheno-v3.2", "messages": [ { "role": "user", "content": "What is the capital of France?" } ] }'

- Docker Model Runner
How to use Sao10K/L3-8B-Stheno-v3.2 with Docker Model Runner:

docker model run hf.co/Sao10K/L3-8B-Stheno-v3.2


*Just message me on discord if you want to host this privately for a service or something. We can talk.*

*Train used 1x H100 SXM for like a total of 24 Hours over multiple runs.*

Support me here if you're interested:

Ko-fi: https://ko-fi.com/sao10k

*wink* Euryale v2?

If not, that's fine too. Feedback would be nice.

Contact Me in Discord:
`sao10k`

// `Just ping me in the KoboldAI discord, I'll respond faster.`


`Art by navy_(navy.blue)`

- Danbooru

Stheno-v3.2-Zeta

I have done a test run with multiple variations of the models, merged back to its base at various weights, different training runs too, and this Sixth iteration is the one I like most.

Changes compared to v3.1

- Included a mix of SFW and NSFW Storywriting Data, thanks to Gryphe

- Included More Instruct / Assistant-Style Data

- Further cleaned up Roleplaying Samples from c2 Logs -> A few terrible, really bad samples escaped heavy filtering. Manual pass fixed it.

- Hyperparameter tinkering for training, resulting in lower loss levels.

Testing Notes - Compared to v3.1

- Handles SFW / NSFW seperately better. Not as overly excessive with NSFW now. Kinda balanced.

- Better at Storywriting / Narration.

- Better at Assistant-type Tasks.

- Better Multi-Turn Coherency -> Reduced Issues?

- Slightly less creative? A worthy tradeoff. Still creative.

- Better prompt / instruction adherence.

**Recommended Samplers:**

```
Temperature - 1.12-1.22
Min-P - 0.075
Top-K - 50
Repetition Penalty - 1.1
```


**Stopping Strings:**

```
\n\n{{User}} # Or Equivalent, depending on Frontend
<|eot_id|>
<|end_of_text|>
```


**Prompting Template - Llama-3-Instruct**

```
<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>
{input}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
{output}<|eot_id|>
```


**Basic Roleplay System Prompt**

```
You are an expert actor that can fully immerse yourself into any role given. You do not break character for any reason, even if someone tries addressing you as an AI or language model.
Currently your role is {{char}}, which is described in detail below. As {{char}}, continue the exchange with {{user}}.
```


- Downloads last month
- 8,878

---
domain: huggingface.co
fetch_date: '2026-05-18T12:35:18.452749'
status: ok
url: https://huggingface.co/cognitivecomputations/dolphin-2.9.3-Yi-1.5-34B-32k
---

### Instructions to use dphn/dolphin-2.9.3-Yi-1.5-34B-32k with libraries, inference providers, notebooks, and local apps. Follow these links to get started.

- Libraries
- Transformers
How to use dphn/dolphin-2.9.3-Yi-1.5-34B-32k with Transformers:

# Use a pipeline as a high-level helper from transformers import pipeline pipe = pipeline("text-generation", model="dphn/dolphin-2.9.3-Yi-1.5-34B-32k") messages = [ {"role": "user", "content": "Who are you?"}, ] pipe(messages)

# Load model directly from transformers import AutoTokenizer, AutoModelForCausalLM tokenizer = AutoTokenizer.from_pretrained("dphn/dolphin-2.9.3-Yi-1.5-34B-32k") model = AutoModelForCausalLM.from_pretrained("dphn/dolphin-2.9.3-Yi-1.5-34B-32k") messages = [ {"role": "user", "content": "Who are you?"}, ] inputs = tokenizer.apply_chat_template( messages, add_generation_prompt=True, tokenize=True, return_dict=True, return_tensors="pt", ).to(model.device) outputs = model.generate(**inputs, max_new_tokens=40) print(tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:]))

- Notebooks
- Google Colab
- Kaggle
- Local Apps
- vLLM
How to use dphn/dolphin-2.9.3-Yi-1.5-34B-32k with vLLM:

##### Install from pip and serve model

# Install vLLM from pip: pip install vllm # Start the vLLM server: vllm serve "dphn/dolphin-2.9.3-Yi-1.5-34B-32k" # Call the server using curl (OpenAI-compatible API): curl -X POST "http://localhost:8000/v1/chat/completions" \ -H "Content-Type: application/json" \ --data '{ "model": "dphn/dolphin-2.9.3-Yi-1.5-34B-32k", "messages": [ { "role": "user", "content": "What is the capital of France?" } ] }'

##### Use Docker

docker model run hf.co/dphn/dolphin-2.9.3-Yi-1.5-34B-32k

- SGLang
How to use dphn/dolphin-2.9.3-Yi-1.5-34B-32k with SGLang:

##### Install from pip and serve model

# Install SGLang from pip: pip install sglang # Start the SGLang server: python3 -m sglang.launch_server \ --model-path "dphn/dolphin-2.9.3-Yi-1.5-34B-32k" \ --host 0.0.0.0 \ --port 30000 # Call the server using curl (OpenAI-compatible API): curl -X POST "http://localhost:30000/v1/chat/completions" \ -H "Content-Type: application/json" \ --data '{ "model": "dphn/dolphin-2.9.3-Yi-1.5-34B-32k", "messages": [ { "role": "user", "content": "What is the capital of France?" } ] }'

##### Use Docker images

docker run --gpus all \ --shm-size 32g \ -p 30000:30000 \ -v ~/.cache/huggingface:/root/.cache/huggingface \ --env "HF_TOKEN=<secret>" \ --ipc=host \ lmsysorg/sglang:latest \ python3 -m sglang.launch_server \ --model-path "dphn/dolphin-2.9.3-Yi-1.5-34B-32k" \ --host 0.0.0.0 \ --port 30000 # Call the server using curl (OpenAI-compatible API): curl -X POST "http://localhost:30000/v1/chat/completions" \ -H "Content-Type: application/json" \ --data '{ "model": "dphn/dolphin-2.9.3-Yi-1.5-34B-32k", "messages": [ { "role": "user", "content": "What is the capital of France?" } ] }'

- Docker Model Runner
How to use dphn/dolphin-2.9.3-Yi-1.5-34B-32k with Docker Model Runner:

docker model run hf.co/dphn/dolphin-2.9.3-Yi-1.5-34B-32k


# Dolphin 2.9.3 Yi 1.5 34b 32k 🐬

Curated and trained by Eric Hartford, Lucas Atkins, and Fernando Fernandes, and Cognitive Computations

Discord: https://discord.gg/cognitivecomputations


![](https://cdn-uploads.huggingface.co/production/uploads/63111b2d88942700629f5771/ldkN1J0WIDQwU4vutGYiD.png)

Our appreciation for the sponsors of Dolphin 2.9.3:

- Crusoe Cloud - provided excellent on-demand 8xH100 node
- OnDemand - provided inference sponsorship

This model is based on Yi-1.5-34b-32k, and is governed by the apache 2.0 license.

The base model has 32k context, and our finetuning took place with 8192 sequence length.

Dolphin 2.9.3 uses ChatML prompt template format.

example:

```
<|im_start|>system
You are Dolphin, a helpful AI assistant.<|im_end|>
<|im_start|>user
{prompt}<|im_end|>
<|im_start|>assistant
```


Dolphin-2.9.3 has a variety of instruction following, conversational, and coding skills. It also has initial agentic abilities and supports function calling.

Dolphin is uncensored. We have filtered the dataset to remove alignment and bias. This makes the model more compliant. You are advised to implement your own alignment layer before exposing the model as a service. It will be highly compliant with any requests, even unethical ones. Please read my blog post about uncensored models. https://erichartford.com/uncensored-models You are responsible for any content you create using this model. Enjoy responsibly.

Dolphin is licensed according to apache 2.0 license. We grant permission for any use, including commercial. Dolphin was trained on data generated from GPT4, among other models.

## Evals

## Training

## See axolotl config

axolotl version: `0.4.0`


```
base_model: 01-ai/Yi-1.5-34B-32k
model_type: LlamaForCausalLM
tokenizer_type: LlamaTokenizer
trust_remote_code: true
# load_in_8bit: false
load_in_4bit: true
# strict: false
adapter: qlora
lora_modules_to_save: [embed_tokens, lm_head]
lora_r: 32
lora_alpha: 16
lora_dropout: 0.05
lora_target_linear: false
lora_fan_in_fan_out:
datasets:
- path: /workspace/datasets/dolphin-2.9.3/dolphin201-sharegpt2.jsonl
type: sharegpt
conversation: chatml
- path: /workspace/datasets/dolphin-2.9.3/SystemChat_filtered_sharegpt.jsonl
type: sharegpt
conversation: chatml
- path: /workspace/datasets/dolphin-2.9.3/SystemChat_multilingual_sharegpt.jsonl
type: sharegpt
conversation: chatml
- path: /workspace/datasets/dolphin-2.9.3/dolphin-coder-translate-sharegpt2.jsonl
type: sharegpt
conversation: chatml
- path: /workspace/datasets/dolphin-2.9.3/dolphin-coder-codegen-sharegpt2.jsonl
type: sharegpt
conversation: chatml
- path: /workspace/datasets/dolphin-2.9.3/m-a-p_Code-Feedback-sharegpt-unfiltered.jsonl
type: sharegpt
conversation: chatml
- path: /workspace/datasets/dolphin-2.9.3/m-a-p_CodeFeedback-Filtered-Instruction-sharegpt-unfiltered.jsonl
type: sharegpt
conversation: chatml
- path: /workspace/datasets/dolphin-2.9.3/not_samantha_norefusals.jsonl
type: sharegpt
conversation: chatml
- path: /workspace/datasets/dolphin-2.9.3/Orca-Math-resort-unfiltered.jsonl
type: sharegpt
conversation: chatml
- path: /workspace/datasets/dolphin-2.9.3/agent_instruct_react_unfiltered.jsonl
type: sharegpt
conversation: chatml
- path: /workspace/datasets/dolphin-2.9.3/toolbench_instruct_j1s1_3k_unfiltered.jsonl
type: sharegpt
conversation: chatml
- path: /workspace/datasets/dolphin-2.9.3/toolbench_negative_unfiltered.jsonl
type: sharegpt
conversation: chatml
- path: /workspace/datasets/dolphin-2.9.3/toolbench_react_10p_unfiltered.jsonl
type: sharegpt
conversation: chatml
- path: /workspace/datasets/dolphin-2.9.3/toolbench_tflan_cot_30p_unfiltered.jsonl
type: sharegpt
conversation: chatml
- path: /workspace/datasets/dolphin-2.9.3/openhermes200k_unfiltered.jsonl
type: sharegpt
conversation: chatml
chat_template: chatml
dataset_prepared_path: dolphin-2.9.3-yi34b-prepared
val_set_size: 0.01
output_dir: ./dolphin-2.9.3-out
sequence_len: 8192
sample_packing: true
pad_to_sequence_len: true
wandb_project: dolphin-2.9.3-yi-1.5-34b
wandb_watch:
wandb_run_id:
wandb_log_model:
gradient_accumulation_steps: 8
micro_batch_size: 1
num_epochs: 3
optimizer: adamw_8bit
lr_scheduler: cosine
learning_rate: 1e-5
train_on_inputs: false
group_by_length: false
bf16: auto
fp16:
tf32: false
gradient_checkpointing: true
gradient_checkpointing_kwargs:
use_reentrant: false
early_stopping_patience:
logging_steps: 1
xformers_attention:
flash_attention: true
warmup_steps: 10
# evals_per_epoch: 4
eval_table_size:
saves_per_epoch: 4
save_total_limit: 2
save_steps:
debug:
deepspeed: /workspace/axolotl/deepspeed_configs/zero3_bf16.json
weight_decay: 0.05
fsdp:
fsdp_config:
special_tokens:
bos_token: "<|startoftext|>"
eos_token: "<|im_end|>"
pad_token: "<unk>"
unk_token: "<unk>"
tokens:
- "<|im_start|>"
#unfrozen_parameters:
lora_target_modules:
# input_layernorm layers
# - model.layers.0.input_layernorm
# - model.layers.1.input_layernorm
# - model.layers.2.input_layernorm
# - model.layers.3.input_layernorm
# - model.layers.4.input_layernorm
# - model.layers.5.input_layernorm
# - model.layers.6.input_layernorm
# - model.layers.7.input_layernorm
# - model.layers.8.input_layernorm
# - model.layers.9.input_layernorm
# - model.layers.10.input_layernorm
# - model.layers.11.input_layernorm
# - model.layers.12.input_layernorm
# - model.layers.13.input_layernorm
# - model.layers.14.input_layernorm
# - model.layers.15.input_layernorm
# - model.layers.16.input_layernorm
# - model.layers.17.input_layernorm
# - model.layers.18.input_layernorm
# - model.layers.19.input_layernorm
# - model.layers.20.input_layernorm
# - model.layers.21.input_layernorm
# - model.layers.22.input_layernorm
# - model.layers.23.input_layernorm
# - model.layers.24.input_layernorm
# - model.layers.25.input_layernorm
# - model.layers.26.input_layernorm
# - model.layers.27.input_layernorm
# - model.layers.28.input_layernorm
# - model.layers.29.input_layernorm
- lm_head
# mlp.down_proj layers
- model.layers.44.mlp.down_proj
- model.layers.45.mlp.down_proj
- model.layers.46.mlp.down_proj
- model.layers.47.mlp.down_proj
- model.layers.43.mlp.down_proj
- model.layers.48.mlp.down_proj
- model.layers.49.mlp.down_proj
- model.layers.42.mlp.down_proj
- model.layers.50.mlp.down_proj
- model.layers.41.mlp.down_proj
- model.layers.51.mlp.down_proj
- model.layers.52.mlp.down_proj
- model.layers.39.mlp.down_proj
- model.layers.40.mlp.down_proj
- model.layers.53.mlp.down_proj
- model.layers.54.mlp.down_proj
- model.layers.38.mlp.down_proj
- model.layers.56.mlp.down_proj
- model.layers.55.mlp.down_proj
- model.layers.37.mlp.down_proj
- model.layers.36.mlp.down_proj
- model.layers.57.mlp.down_proj
- model.layers.35.mlp.down_proj
- model.layers.12.mlp.down_proj
- model.layers.13.mlp.down_proj
- model.layers.16.mlp.down_proj
- model.layers.14.mlp.down_proj
- model.layers.11.mlp.down_proj
- model.layers.34.mlp.down_proj
- model.layers.17.mlp.down_proj
# mlp.gate_proj layers
- model.layers.57.mlp.gate_proj
- model.layers.58.mlp.gate_proj
- model.layers.56.mlp.gate_proj
- model.layers.55.mlp.gate_proj
- model.layers.54.mlp.gate_proj
- model.layers.35.mlp.gate_proj
- model.layers.34.mlp.gate_proj
- model.layers.53.mlp.gate_proj
- model.layers.26.mlp.gate_proj
- model.layers.52.mlp.gate_proj
- model.layers.25.mlp.gate_proj
- model.layers.33.mlp.gate_proj
- model.layers.51.mlp.gate_proj
- model.layers.18.mlp.gate_proj
- model.layers.32.mlp.gate_proj
- model.layers.36.mlp.gate_proj
- model.layers.24.mlp.gate_proj
- model.layers.17.mlp.gate_proj
- model.layers.23.mlp.gate_proj
- model.layers.31.mlp.gate_proj
- model.layers.50.mlp.gate_proj
- model.layers.19.mlp.gate_proj
- model.layers.15.mlp.gate_proj
- model.layers.27.mlp.gate_proj
- model.layers.37.mlp.gate_proj
- model.layers.14.mlp.gate_proj
- model.layers.39.mlp.gate_proj
- model.layers.11.mlp.gate_proj
- model.layers.29.mlp.gate_proj
- model.layers.28.mlp.gate_proj
# mlp.up_proj layers
- model.layers.21.mlp.up_proj
- model.layers.48.mlp.up_proj
- model.layers.49.mlp.up_proj
- model.layers.24.mlp.up_proj
- model.layers.47.mlp.up_proj
- model.layers.25.mlp.up_proj
- model.layers.23.mlp.up_proj
- model.layers.50.mlp.up_proj
- model.layers.14.mlp.up_proj
- model.layers.46.mlp.up_proj
- model.layers.26.mlp.up_proj
- model.layers.27.mlp.up_proj
- model.layers.20.mlp.up_proj
- model.layers.13.mlp.up_proj
- model.layers.51.mlp.up_proj
- model.layers.28.mlp.up_proj
- model.layers.45.mlp.up_proj
- model.layers.22.mlp.up_proj
- model.layers.52.mlp.up_proj
- model.layers.12.mlp.up_proj
- model.layers.29.mlp.up_proj
- model.layers.44.mlp.up_proj
- model.layers.53.mlp.up_proj
- model.layers.11.mlp.up_proj
- model.layers.42.mlp.up_proj
- model.layers.30.mlp.up_proj
- model.layers.43.mlp.up_proj
- model.layers.19.mlp.up_proj
- model.layers.54.mlp.up_proj
- model.layers.40.mlp.up_proj
- model.embed_tokens
# model.norm layers
# post_attention_layernorm layers
# - model.layers.0.post_attention_layernorm
# - model.layers.1.post_attention_layernorm
# - model.layers.2.post_attention_layernorm
# - model.layers.3.post_attention_layernorm
# - model.layers.4.post_attention_layernorm
# - model.layers.5.post_attention_layernorm
# - model.layers.6.post_attention_layernorm
# - model.layers.7.post_attention_layernorm
# - model.layers.8.post_attention_layernorm
# - model.layers.9.post_attention_layernorm
# - model.layers.10.post_attention_layernorm
# - model.layers.11.post_attention_layernorm
# - model.layers.12.post_attention_layernorm
# - model.layers.13.post_attention_layernorm
# - model.layers.14.post_attention_layernorm
# - model.layers.15.post_attention_layernorm
# - model.layers.16.post_attention_layernorm
# - model.layers.17.post_attention_layernorm
# - model.layers.18.post_attention_layernorm
# - model.layers.19.post_attention_layernorm
# - model.layers.20.post_attention_layernorm
# - model.layers.21.post_attention_layernorm
# - model.layers.22.post_attention_layernorm
# - model.layers.23.post_attention_layernorm
# - model.layers.24.post_attention_layernorm
# - model.layers.25.post_attention_layernorm
# - model.layers.26.post_attention_layernorm
# - model.layers.27.post_attention_layernorm
# - model.layers.28.post_attention_layernorm
# - model.layers.29.post_attention_layernorm
# self_attn.k_proj layers
- model.layers.55.self_attn.k_proj
- model.layers.51.self_attn.k_proj
- model.layers.53.self_attn.k_proj
- model.layers.56.self_attn.k_proj
- model.layers.54.self_attn.k_proj
- model.layers.57.self_attn.k_proj
- model.layers.52.self_attn.k_proj
- model.layers.59.self_attn.k_proj
- model.layers.49.self_attn.k_proj
- model.layers.48.self_attn.k_proj
- model.layers.47.self_attn.k_proj
- model.layers.41.self_attn.k_proj
- model.layers.58.self_attn.k_proj
- model.layers.40.self_attn.k_proj
- model.layers.46.self_attn.k_proj
- model.layers.44.self_attn.k_proj
- model.layers.50.self_attn.k_proj
- model.layers.43.self_attn.k_proj
- model.layers.39.self_attn.k_proj
- model.layers.42.self_attn.k_proj
- model.layers.45.self_attn.k_proj
- model.layers.33.self_attn.k_proj
- model.layers.37.self_attn.k_proj
- model.layers.17.self_attn.k_proj
- model.layers.24.self_attn.k_proj
- model.layers.21.self_attn.k_proj
- model.layers.25.self_attn.k_proj
- model.layers.23.self_attn.k_proj
- model.layers.35.self_attn.k_proj
- model.layers.20.self_attn.k_proj
# self_attn.o_proj layers
- model.layers.53.self_attn.o_proj
- model.layers.55.self_attn.o_proj
- model.layers.54.self_attn.o_proj
- model.layers.42.self_attn.o_proj
- model.layers.52.self_attn.o_proj
- model.layers.51.self_attn.o_proj
- model.layers.50.self_attn.o_proj
- model.layers.1.self_attn.o_proj
- model.layers.40.self_attn.o_proj
- model.layers.37.self_attn.o_proj
- model.layers.34.self_attn.o_proj
- model.layers.36.self_attn.o_proj
- model.layers.41.self_attn.o_proj
- model.layers.35.self_attn.o_proj
- model.layers.46.self_attn.o_proj
- model.layers.27.self_attn.o_proj
- model.layers.33.self_attn.o_proj
- model.layers.30.self_attn.o_proj
- model.layers.43.self_attn.o_proj
- model.layers.39.self_attn.o_proj
- model.layers.17.self_attn.o_proj
- model.layers.28.self_attn.o_proj
- model.layers.48.self_attn.o_proj
- model.layers.31.self_attn.o_proj
- model.layers.29.self_attn.o_proj
- model.layers.38.self_attn.o_proj
- model.layers.47.self_attn.o_proj
- model.layers.56.self_attn.o_proj
- model.layers.32.self_attn.o_proj
- model.layers.4.self_attn.o_proj
# self_attn.q_proj layers
- model.layers.1.self_attn.q_proj
- model.layers.3.self_attn.q_proj
- model.layers.4.self_attn.q_proj
- model.layers.5.self_attn.q_proj
- model.layers.2.self_attn.q_proj
- model.layers.0.self_attn.q_proj
- model.layers.6.self_attn.q_proj
- model.layers.8.self_attn.q_proj
- model.layers.7.self_attn.q_proj
- model.layers.10.self_attn.q_proj
- model.layers.36.self_attn.q_proj
- model.layers.11.self_attn.q_proj
- model.layers.9.self_attn.q_proj
- model.layers.35.self_attn.q_proj
- model.layers.28.self_attn.q_proj
- model.layers.34.self_attn.q_proj
- model.layers.27.self_attn.q_proj
- model.layers.14.self_attn.q_proj
- model.layers.29.self_attn.q_proj
- model.layers.12.self_attn.q_proj
- model.layers.33.self_attn.q_proj
- model.layers.30.self_attn.q_proj
- model.layers.24.self_attn.q_proj
- model.layers.32.self_attn.q_proj
- model.layers.37.self_attn.q_proj
- model.layers.20.self_attn.q_proj
- model.layers.15.self_attn.q_proj
- model.layers.16.self_attn.q_proj
- model.layers.26.self_attn.q_proj
- model.layers.31.self_attn.q_proj
# self_attn.v_proj layers
- model.layers.7.self_attn.v_proj
- model.layers.8.self_attn.v_proj
- model.layers.9.self_attn.v_proj
- model.layers.10.self_attn.v_proj
- model.layers.12.self_attn.v_proj
- model.layers.13.self_attn.v_proj
- model.layers.14.self_attn.v_proj
- model.layers.15.self_attn.v_proj
- model.layers.16.self_attn.v_proj
- model.layers.17.self_attn.v_proj
- model.layers.21.self_attn.v_proj
- model.layers.23.self_attn.v_proj
- model.layers.39.self_attn.v_proj
- model.layers.46.self_attn.v_proj
- model.layers.48.self_attn.v_proj
- model.layers.49.self_attn.v_proj
- model.layers.51.self_attn.v_proj
- model.layers.52.self_attn.v_proj
- model.layers.53.self_attn.v_proj
- model.layers.54.self_attn.v_proj
- model.layers.55.self_attn.v_proj
- model.layers.56.self_attn.v_proj
- model.layers.22.self_attn.v_proj
- model.layers.18.self_attn.v_proj
- model.layers.50.self_attn.v_proj
- model.layers.47.self_attn.v_proj
- model.layers.44.self_attn.v_proj
- model.layers.45.self_attn.v_proj
- model.layers.57.self_attn.v_proj
- model.layers.41.self_attn.v_proj
```


# out-yi

This model is a fine-tuned version of 01-ai/Yi-1.5-34B on the None dataset. It achieves the following results on the evaluation set:

- Loss: 0.4425

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:

- learning_rate: 1e-05
- train_batch_size: 1
- eval_batch_size: 1
- seed: 42
- distributed_type: multi-GPU
- num_devices: 8
- gradient_accumulation_steps: 8
- total_train_batch_size: 64
- total_eval_batch_size: 8
- optimizer: Adam with betas=(0.9,0.999) and epsilon=1e-08
- lr_scheduler_type: cosine
- lr_scheduler_warmup_steps: 10
- num_epochs: 3

### Training results

| Training Loss | Epoch | Step | Validation Loss |
|---|---|---|---|
| 0.6265 | 0.0 | 1 | 0.6035 |
| 0.4674 | 0.25 | 327 | 0.4344 |
| 0.4337 | 0.5 | 654 | 0.4250 |
| 0.4346 | 0.75 | 981 | 0.4179 |
| 0.3985 | 1.0 | 1308 | 0.4118 |
| 0.3128 | 1.23 | 1635 | 0.4201 |
| 0.3261 | 1.48 | 1962 | 0.4157 |
| 0.3259 | 1.73 | 2289 | 0.4122 |
| 0.3126 | 1.98 | 2616 | 0.4079 |
| 0.2265 | 2.21 | 2943 | 0.4441 |
| 0.2297 | 2.46 | 3270 | 0.4427 |
| 0.2424 | 2.71 | 3597 | 0.4425 |

### Framework versions

- Transformers 4.40.0.dev0
- Pytorch 2.2.2+cu121
- Datasets 2.15.0
- Tokenizers 0.15.0

- Downloads last month
- 8,205

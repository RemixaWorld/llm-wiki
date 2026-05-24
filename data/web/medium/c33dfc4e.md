---
domain: medium.com
fetch_date: '2026-05-18T12:45:36.071909'
status: ok
url: https://medium.com/@zaiinn440/best-llm-inference-engine-tensorrt-vs-vllm-vs-lmdeploy-vs-mlc-llm-e8ff033d7615
---

# Best LLM Inference Engine? TensorRT vs vLLM vs LMDeploy vs MLC-LLM

[ ![Zain ul Abideen](https://miro.medium.com/v2/resize:fill:64:64/1*dvg1090xlLfVDuXCQdmMzQ.png) ](</@zaiinn440?source=post_page---byline--e8ff033d7615--------------------------------------->)

[Zain ul Abideen](</@zaiinn440?source=post_page---byline--e8ff033d7615--------------------------------------->)

6 min read

·

Jul 6, 2024

\--

\--

Listen

Share

More

Benchmarking various LLM Inference Engines.

![Source](https://miro.medium.com/v2/resize:fit:700/0*uCRDjMy2-gWC1BzC)

LLMs excel in text generation applications, such as chat and code completion models capable of high understanding and fluency. However, their large size also creates challenges for inference. Basic inference is slow because LLMs generate text tokens by token, requiring repeated calls for each next token. As the input sequence grows, the processing time increases. Additionally, LLMs have billions of parameters, making it difficult to store and manage all those weights in memory.

In the effort to optimize LLM inference and serving, there are multiple frameworks and packages and in this blog, I’ll use and compare the following inference engines

* TensorRT-LLM
* vLLM
* LMDeploy
* MLC-LLM

## 1\. TensorRT-LLM

## Introduction

TensorRT-LLM is another inference engine that accelerates and optimizes inference performance for the latest LLMs on NVIDIA GPUs. LLMs are compiled into TensorRT Engine and then deployed with a triton server to leverage inference optimizations such as In-Flight Batching (reduces wait time and allows higher GPU utilization), paged KV caching, MultiGPU-MultiNode Inference, and FP8 Support.

## Usage

We will compare the execution time, ROUGE scores, latency, and throughput across the HF model, TensorRT-model, and TensorRT-INT8 model (quantized).

You need to install Nvidia-container-toolkit for your Linux system, initialize Git LFS (to download HF Models), and download the necessary packages as follows:

```python !curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \ && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \ sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \ sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list!apt-get update!git clone https://github.com/NVIDIA/TensorRT-LLM/!apt-get update && apt-get -y install python3.10 python3-pip openmpi-bin libopenmpi-dev!pip3 install tensorrt_llm -U --pre --extra-index-url https://pypi.nvidia.com!pip install -r TensorRT-LLM/examples/phi/requirements.txt!pip install flash_attn pytest!curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash!apt-get install git-lfs ```

Now retrieve the model weights

```bash PHI_PATH="TensorRT-LLM/examples/phi"!rm -rf $PHI_PATH/7B!mkdir -p $PHI_PATH/7B && git clone https://huggingface.co/microsoft/Phi-3-small-128k-instruct $PHI_PATH/7B ```

Convert the model into TensorRT-LLM checkpoint format and and build the TensorRT-LLM from the checkpoint.

``` !python3 $PHI_PATH/convert_checkpoint.py --model_dir $PHI_PATH/7B/ \ --dtype bfloat16 \ --output_dir $PHI_PATH/7B/trt_ckpt/bf16/1-gpu/# Build TensorRT-LLM model from checkpoint!trtllm-build --checkpoint_dir $PHI_PATH/7B/trt_ckpt/bf16/1-gpu/ \ --gemm_plugin bfloat16 \ --output_dir $PHI_PATH/7B/trt_engines/bf16/1-gpu/ ```

Similarly, now apply INT8 weight-only quantization to the HF model and convert the checkpoint into TensorRT-LLM.

``` !python3 $PHI_PATH/convert_checkpoint.py --model_dir $PHI_PATH/7B \ --dtype bfloat16 \ --use_weight_only \ --output_dir $PHI_PATH/7B/trt_ckpt/int8_weight_only/1-gpu/!trtllm-build --checkpoint_dir $PHI_PATH/7B/trt_ckpt/int8_weight_only/1-gpu/ \ --gemm_plugin bfloat16 \ --output_dir $PHI_PATH/7B/trt_engines/int8_weight_only/1-gpu/ ```

Now test the base phi3 and two TensorRT models on the [summarization task](<https://github.com/NVIDIA/TensorRT-LLM/tree/main/examples/phi#3-summarization-using-the-phi-model>)

``` %%capture phi_hf_results# Huggingface!time python3 $PHI_PATH/../summarize.py --test_hf \ --hf_model_dir $PHI_PATH/7B/ \ --data_type bf16 \ --engine_dir $PHI_PATH/7B/trt_engines/bf16/1-gpu/%%capture phi_trt_results# TensorRT-LLM!time python3 $PHI_PATH/../summarize.py --test_trt_llm \ --hf_model_dir $PHI_PATH/7B/ \ --data_type bf16 \ --engine_dir $PHI_PATH/7B/trt_engines/bf16/1-gpu/%%capture phi_int8_results# TensorRT-LLM (INT8)!time python3 $PHI_PATH/../summarize.py --test_trt_llm \ --hf_model_dir $PHI_PATH/7B/ \ --data_type bf16 \ --engine_dir $PHI_PATH/7B/trt_engines/int8_weight_only/1-gpu/ ```

Now after capturing the results, you can parse the output and plot it to compare execution time, ROUGE scores, latency, and throughput across all models.

![image](https://miro.medium.com/v2/resize:fit:700/0*5kmLeBSeuoBN0GXv.png) ![Comparison of Latency and Throughput](https://miro.medium.com/v2/resize:fit:700/0*ZoTjVR32Rdn75R17.png)

## 2\. vLLM

## Introduction

vLLM offers LLM inferencing and serving with SOTA throughput, Paged Attention, Continuous batching, Quantization (GPTQ, AWQ, FP8), and optimized CUDA kernels.

## Usage

Let’s evaluate the throughput and latency of `microsoft/Phi3-mini-4k-instruct` . Start by setting up dependencies and importing libraries.

```python !pip install -q vllm!git clone https://github.com/vllm-project/vllm.git!pip install -q datasets!pip install transformers scipyfrom vllm import LLM, SamplingParamsfrom datasets import load_datasetimport timefrom tqdm import tqdmfrom transformers import AutoTokenizer ```

Now let’s load the model and generate its outputs on a small slice of the dataset.

```python dataset = load_dataset("akemiH/MedQA-Reason", split="train").select(range(10))prompts = []for sample in dataset: prompts.append(sample)sampling_params = SamplingParams(max_tokens=524)llm = LLM(model="microsoft/Phi-3-mini-4k-instruct", trust_remote_code=True)def generate_with_time(prompt): start = time.time() outputs = llm.generate(prompt, sampling_params) taken = time.time() - start generated_text = outputs[0].outputs[0].text return generated_text, takengenerated_text = []time_taken = 0for sample in tqdm(prompts): text, taken = generate_with_time(sample) time_taken += taken generated_text.append(text)# Tokenize the outputs and calculate the throughputtokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")token = 1for sample in generated_text: tokens = tokenizer(sample) tok = len(tokens.input_ids) token += tokprint(token)print("tok/s", token // time_taken) ``` ![image](https://miro.medium.com/v2/resize:fit:700/0*6QwBLhdWtwHIMZmx.png)

Let’s also benchmark the model’s performance through vLLM on the ShareGPT dataset

``` !wget https://huggingface.co/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered/resolve/main/ShareGPT_V3_unfiltered_cleaned_split.json%cd vllm!python benchmarks/benchmark_throughput.py --backend vllm --dataset ../ShareGPT_V3_unfiltered_cleaned_split.json --model microsoft/Phi-3-mini-4k-instruct --tokenizer microsoft/Phi-3-mini-4k-instruct --num-prompts=1000 ``` ![image](https://miro.medium.com/v2/resize:fit:700/0*649ENhmUZZp4UGK0.png)

## 3\. LMDeploy

## Introduction

This package also allows compressing, deploying, and serving LLMs while offering efficient inference (persistent batching, blocked KV cache, dynamic split&fuse, tensor parallelism, high-performance CUDA kernels), effective quantization (4-bit inference performance is 2.4x higher than FP16), effortless distribution server (deployment of multi-model services across multiple machines and cards) and interactive inference mode (remembers dialogue history and avoids repetitive processing of historical sessions). Furthermore, it also allows for profiling token latency and throughput, request throughput, API server, and triton inference server performance.

## Usage

Install dependencies and import packages.

```python !pip install -q lmdeploy!pip install nest_asyncioimport nest_asyncionest_asyncio.apply() ``` ``` !git clone --depth=1 https://github.com/InternLM/lmdeploy%cd lmdeploy/benchmark ```

LMdeploy has developed two inference engines [TurboMind](<https://github.com/InternLM/lmdeploy/blob/main/docs/en/inference/turbomind.md>) and [PyTorch](<https://github.com/InternLM/lmdeploy/blob/main/docs/en/inference/pytorch.md>).

Let’s profile the PyTorch engine on `microsoft/Phi3-mini-128k-instruct` .

``` !python3 profile_generation.py microsoft/Phi-3-mini-128k-instruct --backend pytorch ```

It profiles the engine over multiple rounds and reports the token latency & throughput for each round.

![image](https://miro.medium.com/v2/resize:fit:700/0*0ygY7y_lky3ARGe2.png)

Pytorch engine profile for token latency and throughput

## 4\. MLC-LLM

## Introduction

MLC-LLM offers a high performance deployment and inference engine, called MLCEngine.

## Usage

Let’s install dependencies which includes setting up dependencies with conda and creating a conda environment. Then clone the git repository and configure.

```python conda activate your-environmentpython -m pip install --pre -U -f https://mlc.ai/wheels mlc-llm-nightly-cu121 mlc-ai-nightly-cu121conda env remove -n mlc-chat-venvconda create -n mlc-chat-venv -c conda-forge \ "cmake>=3.24" \ rust \ git \ python=3.11conda activate mlc-chat-venvgit clone --recursive https://github.com/mlc-ai/mlc-llm.git && cd mlc-llm/mkdir -p build && cd buildpython ../cmake/gen_cmake_config.pycmake .. && cmake --build . --parallel $(nproc) && cd ..set(USE_FLASHINFER ON)conda activate your-own-envcd mlc-llm/pythonpip install -e . ```

To run a model with MLC LLM, we need to convert model weights into MLC format. Download the HF model to by Git LFS then convert weights.

``` mlc_llm convert_weight ./dist/models/Phi-3-small-128k-instruct/ \ --quantization q0f16 \ --model-type "phi3" \ -o ./dist/Phi-3-small-128k-instruct-q0f16-MLC ```

Now load you MLC format model into the MLC engine

```python from mlc_llm import MLCEngine# Create enginemodel = "HF://mlc-ai/Phi-3-mini-128k-instruct-q0f16-MLC"engine = MLCEngine(model)# Now let’s calculate throughputimport timefrom transformers import AutoTokenizerstart = time.time()response = engine.chat.completions.create( messages=[{"role": "user", "content": "What is the Machine Learning?"}], model=model, stream=False,)taken = time.time() - starttokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-128k-instruct")print("tok/s", 82 // taken) ``` ![image](https://miro.medium.com/v2/resize:fit:700/0*517fC4IATKkgQTBi.png)

## Summary

TensorRT INT8 models outperform HF models and regular TensorRT with respect to inference speed while the regular TensorRT model performed better on the summarization task with the highest ROUGE score among the three models. LMDeploy delivers up to 1.8x higher request throughput than vLLM on an A100.

**Special thanks to**[**QueryLoopAI**](<https://www.linkedin.com/company/queryloopai/>)**for sponsoring the compute of these experiments.**

_Also, feel free to drop me a message or:_

1. Connect and reach me on****[**LinkedIn**](<https://www.linkedin.com/in/zaiinulabideen/>)**** and [**Twitter**](<https://twitter.com/zaynismm>)
2. Follow me on 📚 [**Medium**](</@zaiinn440>)
3. Subscribe to my 📢 weekly [**AI newsletter**](<https://rethinkai.substack.com/>)!
4. Check out my 🤗 [**Hugging Face**](<https://huggingface.co/abideen>)

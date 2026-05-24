---
domain: newsletter.kaitchup.com
fetch_date: '2026-05-18T12:36:14.533581'
status: ok
url: https://newsletter.kaitchup.com/p/guidellm-is-your-server-ready
---

# GuideLLM: Is Your Server Ready for LLM Deployment?

### Simulate real-world inference workloads with GuideLLM

![GuideLLM User Flows GuideLLM User Flows](https://substackcdn.com/image/fetch/$s_!bimO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F998b8ac2-61f7-47ef-bb19-c319b2aa7227_1080x747.png)

We have numerous scripts and utilities available to benchmark the latency and inference throughput of large language models (LLMs). vLLM, TGI, and llama.cpp can all tell you how fast an LLM is on your machine. However, they are not designed to evaluate how well your server can handle real-world scenarios involving multiple simultaneous queries from users.

*How can you determine if your server is robust enough to manage the demands of real-world inference workloads?*

This is where GuideLLM is useful. Developed by Neural Magic, GuideLLM is a framework designed to evaluate LLM deployment by simulating real-world workloads under different load conditions. It helps you assess how your server handles concurrent or synchronous queries.

In this article, I will introduce **GuideLLM** and walk you through its key features. Next, I will explain how to install and run the framework, as well as how to interpret the performance reports it generates. To provide practical examples, I used GuideLLM to evaluate two different server configurations provided by RunPod (referral link):

A vLLM server running

**Llama 3.1 8B Instruct**, powered by an**A40 GPU**(48 GB of VRAM).A vLLM server running

**Qwen2-1.5B Instruct**, powered by an**RTX 3090 GPU**(24 GB of VRAM).

Through these examples, we will understand how GuideLLM can assess and compare the performance of different LLM setups.

The notebook implementing simple examples to generate reports with GuideLLM is here:

## Setting Up GuideLLM

GuideLLM is available here:

GitHub: neuralmagic/guidellm (Apache 2.0 license)


It can be installed with pip:

`pip install guidellm`


GuideLLM works server frameworks supporting the OpenAI API request format. For instance, vLLM and TGI support it.

If you want to test it with vLLM, install it as follows:

`pip install vLLM`


## Simulating Real-world Inference Workloads

GuideLLM evaluates server performance by simulating how it handles different types of workloads. It does this by sending requests to the server in various patterns:

**Synchronous**: Sends requests one after another, in sequence.**Throughput**: Sends requests as soon as they are created, without waiting for a response.**Constant Rate**: Sends requests at a steady rate.

By default, GuideLLM runs a "sweep" across all three patterns—synchronous, throughput, and constant (with different rates for this last one). In this article, I used the default settings.

GuideLLM uses the data from these requests to measure the LLM's latency under different workloads, providing a clear picture of how the server performs under varying conditions.

To generate the requests, you can use the `--data-type emulated`

option, which creates requests based on a specified prompt length. Alternatively, you can supply a file containing prompts or use a dataset from the Hugging Face Hub by providing its name.

## Simulating Workloads with GuideLLM for Qwen2 1.5B on an RTX 3090 GPU

First, let’s start a vLLM server for Qwen2 1.5B:

`vllm serve "Qwen/Qwen2-1.5B"`


This starts the server on localhost:8000.

Then, we run GuideLLM which will simulate workloads on this server:

```
guidellm \
--target "http://localhost:8000/v1" \
--model "Qwen/Qwen2-1.5B" \
--data-type emulated \
--data "prompt_tokens=512,generated_tokens=128"
```


It takes 20 minutes to generate the following report:

There are 4 tables.

**Requests Data by Benchmark**

In this table, you can check whether some requests failed. For instance, you might have some failure if a request is not well-formatted or if your server runs out of memory.

It also indicates the time it took to complete each test.

We can see here that there is no data for 8 asynchronous tests. That’s because GuideLLM detected that the server was too slow to handle such rates.

#### Tokens Data by Benchmark and Performance Stats by Benchmark

The second and third tables should be read together.

When using "emulated" data, the second table is not very informative. It tells you the length of the prompt and of the generated output. They are all the same length, almost. For some reason, while I set the prompt length at 512 and an output length at 128, the report indicates that some prompts had 513 tokens and some outputs had 129 or 130 tokens. I’m not sure whether this is a bug of GuideLLM, a bug of vLLM, or a feature that I don’t understand…

The third table tells how long it took to complete a request, to generate the first token, and to generate subsequent tokens.

For the synchronous configuration, the latency is quite stable, as expected since we sent the request one by one. In contrast, with "throughput", some requests took 10 seconds, probably the first ones sent, while others took 30 seconds, probably towards the end of the test as the server was getting overloaded by too many requests.

#### Performance Summary by Benchmark

This is the most interesting table.

It sums up the request latency, time to first token, inter-token latency, and inference throughput for each test.

I think the inference throughput can be very misleading here. I don’t know how they computed it. I assume that they didn’t normalize by the number of requests/sec. The "throughput" test appears faster but it had to deal with many more requests.

Request latency, time to first token, and inter-token latency are much more informative. Neural Magic wrote in the repository’s README.md that a time under 200 ms for time to first token and 50 ms for inter-token latency are acceptable. Given their expertise in this area, I would trust these thresholds.

2.76 req/sec seems to be acceptable. According to the table “Performance Stats by Benchmark”, 95% of the requests had a time to first token below 200 ms and an inter-token latency token below 50 ms. I assume 3 req/sec would also work.

Remember that these numbers are for prompts with 512 tokens and for generating up to 128 tokens. Using your own data instead of emulated data would provide you with much more insightful results.

## Simulating Workloads with GuideLLM for Llama 3.1 8B Instruct on an A40 GPU

For this benchmark, I used Llama 3.1 8B Instruct. It’s a larger LLM so I needed a GPU with more memory. I chose an A40 which has 48 GB of VRAM.

GuideLLM tried 4 different asynchronous tests sending up to 2.6 requests per second.

None of the tests achieved a time to first token below 200 ms while the inter token latency remains acceptable, below 50 ms, for only 50% of the requests.

In other words, the A40 is not good enough to process multiple requests for Llama 3.1 8B with the default configuration of vLLM. You might improve it by optimizing the KV cache, activating FlashAttention (if not already activated), etc..

## Conclusion

GuideLLM generates detailed reports that provide valuable insights into the types of workloads your server can handle effectively. If the results indicate that your server isn't fast enough for your use cases, there are several options you can consider to optimize performance:

Adjust your server framework configuration (e.g., KV cache size, GPU utilization settings).

Add more GPUs or upgrade to newer, more powerful GPUs.

Opt for a smaller, more efficient model.


GuideLLM is still young and evolving, with regular updates bringing new features and improvements. In the future, I believe it could benefit from incorporating recommendations within the reports, offering specific suggestions for improving server performance based on the results. This would make it even more useful for optimizing deployments.

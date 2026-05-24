---
domain: medium.com
fetch_date: '2026-05-18T12:56:26.686385'
status: ok
url: https://medium.com/@mgunton7/benchmarking-llm-inference-servers-9fc8a7eda28c
---

# Benchmarking LLM Inference Servers

## My Notes and Learnings from the Trenches

[ ![Matthew Gunton](https://miro.medium.com/v2/resize:fill:64:64/1*F8sHS2ai6w95qbGIZ9qM_g.png) ](</@mgunton7?source=post_page---byline--9fc8a7eda28c--------------------------------------->)

[Matthew Gunton](</@mgunton7?source=post_page---byline--9fc8a7eda28c--------------------------------------->)

5 min read

·

Oct 25, 2025

\--

\--

Listen

Share

More

![Image by Author — Flux.1 Schnell](https://miro.medium.com/v2/resize:fit:700/1*_huHsSWpfQYr6uybkDXSDg.jpeg)

Benchmarks are meant to be the gold standard. They should be repeatable, easy to understand, and ultimately be the data we use to drive decision making. Interestingly, benchmarking LLM inference systems is deceptively complex. There are many tunable settings, and [different benchmarks can even contradict each other](<https://www.reddit.com/r/LocalLLaMA/comments/1k45plp/a_collection_of_benchmarks_for_llm_inference/#:~:text=1,of%20the%20benchmarks%20matters%20more>).

We want to make it easy to see how fast an inference engine is. To that end, I’m opening sourcing our benchmarking tool at Luminal. While it’s certainly not perfect ( we will continue to iterate on it over time ), hopefully it will be one of the simpler and easier to understand tools for teams to use.

These are some notes from the trenches as I tried to make sense of benchmarking LLM inference servers. I’m not claiming to have the answers — but sharing what I’ve tried and what surprised me. This blog post will go through explaining the key decisions I made when putting this together.

## Points of View

Our benchmarking script tracks metrics from both the client and server point of view. The general thinking is to cover the entire experience during benchmarking so there’s as little difference between the metrics we announce and the metrics a user experiences.

There are really two points of view to consider when measuring this: the server’s and the client’s.

### Server Point of View

The server calculates tokens per second directly during the forward pass of the model. Modern inference engines use some form of paged attention to batch together requests, resulting in many tokens being generated simultaneously. The amount of tokens you can generate per second is called your throughput and generally your business is more cost-effective if your throughput is high. When the batch size is bigger, we have more tokens that we are processing at once, resulting in a higher throughput.

### Client Point of View

The client calculates tokens per second based on when it gets a response from the server. Consequently, this is factoring in network latencies, tokenizing time, and any pre- and post-processing that might occur on the server. For us at Luminal, this is the type of latency that matters most, as it directly impacts the customer experience.

The more time the server waits to process a bigger batch, the worse the latency is for the customer. Thus, we need to be aware of what kind of balance we’re striking between the two.

### Time to First Token (TTFT) and Inter-Token Latency (ITL)

There are two distinct phases of LLM inferencing: prefill and decode. Critically, prefill is compute-bound while decode is memory-bound. Each phase benefits from different kernel optimizations. In order to see how good the prefill stage is, we use the TTFT metric, as the output of the prefill stage is the first token. On the other hand, our decode stage is best tracked via ITL.

While both of these metrics can be tracked on the server-side, I decided to track them on the client-side via enabling ‘streaming’. This measurement is again about prioritizing tracking the actual customer experience. When your customer is streaming tokens, they won’t be happy until they actually get their tokens.

![Graph Comparing Percent of Time Spent in Decode vs Prefill](https://miro.medium.com/v2/resize:fit:700/1*AmSbfq22ichRsmuIRcWXWw.png)

## Match the Real World Closely

Benchmarks are only as good as they are predictive of what will really happen. To ensure our benchmarks accurately measure what a customer should expect, I did 2 things to push us closer to real-world load during benchmarking.

First, I chose to benchmark using the chat endpoint to include any overhead that a real chat request would incur (such as system/user prompt formatting, image preprocessing, etc.). This way, our numbers reflect what a user of the chat API would actually see. Some other benchmarks call the lower-level generate function to isolate model throughput; that’s useful for internal metrics but might be a bit optimistic for end-user experience measurements.

Second, I made our request data representative of the real world. For our vision language models, I used the `lmms-lab/COCO-Caption2017` dataset because of its variety and quality. Then I sent the requests via a poisson distribution as requests never come uniformly in the real world.

![Screen Capture from Hugging Face’s Hosting of lmms-lab/COCO-Caption2017](https://miro.medium.com/v2/resize:fit:700/1*hRVB5x7p9iQh_kcAvMsqBA.png)

## Load Testing

I chose requests per second to be the key load variable. This metric lets us figure out which loads require us to start scaling and how the customer experience changes when we are being hit by many different users at once.

## Server-Side Configurations

When benchmarking, there are certain configurations we want to hold constant throughout the run. If we do not, then our benchmarks will not give back consistent results.

Beyond benchmarking, the queue length and batch size settings are also how we ensure a minimum quality that we will serve to the user. Without this, it is practically impossible to make guarantees to the users about speed.

### Batch Size

The batch size is the maximum number of requests our paged attention kernel can handle at once. The larger this value is, the higher your potential throughput can be. Generally you set this as high as you can for your resources.

### Queue Length

A consequence of doing batched requests is the necessity of queue, and that queue quickly becomes a major source of latency. Any requests that come in while the current batch is being processed have to wait for it to finish. This introduces the largest latency as any request at the back of the line is going to have a significantly higher latency than any other request based solely off its place in line.

### Queue Saturation

The biggest lesson was how strongly queue saturation affects benchmark consistency. When the queue fills, latency naturally rises. If you run the same test with a different number of requests and don’t account for this, your results will vary.

To avoid this, keep your maximum queue length consistent and measure how long requests wait there. This way of testing also lets you put a floor on what the worst possible experience looks like.

![Early Benchmarking Results Showing Max Queue Size is an effective way to set a floor for quality](https://miro.medium.com/v2/resize:fit:700/1*sW5HB_HKh1xyCYpM-ajX-g.png)

## Github

I’ve open sourced the benchmarking software so others don’t have as much churn getting simple results like I did

The great strength of open source software is the ability to build with others. If you see any issues or have questions, please open an issue or email me at matthew [at] luminalai.com!

## [GitHub - luminal-ai/simple_benchmarking: Let's Keep It Simple With Benchmarking Inference ServersLet's Keep It Simple With Benchmarking Inference Servers - luminal-ai/simple_benchmarkinggithub.com](<https://github.com/luminal-ai/simple_benchmarking?source=post_page-----9fc8a7eda28c--------------------------------------->)

---
domain: ai.gopubby.com
fetch_date: '2026-05-18T12:50:48.342488'
status: ok
url: https://ai.gopubby.com/think-big-llm-models-cant-fit-small-gpus-think-again-ebbbb3bd0da7
---

# Think Big LLM Models Can’t Fit Small GPUs? Think Again!

## Calculations and Strategies for How to Fit LLMs into Limited GPU Resources

[ ![Muhammad Saad Uddin](https://miro.medium.com/v2/resize:fill:64:64/1*t9b5FONWnTKjojemZfazgw.jpeg) ](<https://medium.com/@itssaad.muhammad?source=post_page---byline--ebbbb3bd0da7--------------------------------------->)

[Muhammad Saad Uddin](<https://medium.com/@itssaad.muhammad?source=post_page---byline--ebbbb3bd0da7--------------------------------------->)

27 min read

·

Nov 14, 2024

\--

Listen

Share

More

Press enter or click to view image in full size

Image by Author via Dall-E

— — — — — — — — — — — — — — — — — — — — — — — — — — — — — — — —
_I believe this work could be valuable to you. Even if you’re not a Medium member, you can access the full article using this link:_[_For Non-member readers!_](</think-big-llm-models-cant-fit-small-gpus-think-again-ebbbb3bd0da7?sk=94c578fb0b74796f16dbba2ff609bd58>)
— — — — — — — — — — — — — — — — — — — — — — — — — — — — — — — —

[**In my last article**](</stop-guessing-heres-how-much-gpu-memory-you-really-need-for-llms-8e9b02bcdb62?sk=2c01ba82a0a0017a5ce0156b3bf25d9d>), I discussed why accurate memory estimation for deploying large language models is crucial and how tricky it can be to get those estimations right due to the complexities involved. Many of you appreciated the depth of research and practical formulas provided for calculating GPU memory requirements. so if you missed it, I highly recommend reading it for a solid foundation and comprehensive understanding of GPU memory calculations.

Following that article, I received numerous requests for advice on minimizing GPU memory usage for LLM during inference. Over the past two months, I dove into this area, analyzing recent research and experimenting with various techniques. The field is evolving rapidly, with new studies emerging constantly, making it challenging to cover every approach in one piece. However, I’ve tested some promising techniques myself and compiled the most effective strategies to share with you. Some methods I’ve implemented locally, while others are drawn from recent research papers (links provided for your reference). Please feel free to share your findings or corrections in the comments if you think I’ve missed something or made an error.

In this article, my aim is to empower you with actionable insights and methods to optimize GPU memory consumption during LLM inference. As we already discussed in [**last article**](</stop-guessing-heres-how-much-gpu-memory-you-really-need-for-llms-8e9b02bcdb62>) about the underlying factors that contribute to high memory usage**(**[**read it here**](</stop-guessing-heres-how-much-gpu-memory-you-really-need-for-llms-8e9b02bcdb62>)**)** and now you learn how to apply effective optimization techniques, you can deploy powerful language models even on hardware with limited GPU resources.

**What You’ll Learn:**

* **Understanding Key Optimization Techniques:** We start with the most impactful methods for reducing GPU memory usage, including VLLMs, quantization, Flash Attention, KV cache management and offloading, activation memory optimization, and model distillation and pruning.
* **Impact on Memory Requirements:** Through practical calculations and examples, I will show you how each technique affects the overall memory footprint. Using models like LLaMA-2 70B as case studies, you’ll see concrete numbers that illustrate the potential memory savings.

## 1\. vLLMs: Efficient Memory Management with PagedAttention

One of the most impactful techniques for reducing GPU memory consumption during LLM inference is the use of **vLLMs**[7] which are optimized for serving efficiency. At the heart of vLLMs lies a novel attention algorithm called **PagedAttention**[8], which reimagines how the key value (KV) cache is managed during inference.

Press enter or click to view image in full size

Illustration of generation process for a request with PagedAttention [7]

## Understanding PagedAttention

**PagedAttention** draws inspiration from the concept of virtual memory and paging in operating systems. In traditional LLM inference, the KV cache, a storage for key and value tensors generated during the attention mechanism, consumes a significant portion of GPU memory. The size of this cache scales linearly with both the model’s number of layers and the context window (the number of tokens processed). As context windows grow larger to accommodate more extensive inputs, the KV cache can quickly become a memory bottleneck.

PagedAttention addresses this challenge by:

* **Dividing the KV Cache into Fixed Size Blocks (Pages)** : Instead of allocating a monolithic chunk of memory for the entire KV cache, PagedAttention breaks it down into smaller, fixed size blocks. This allows for more flexible memory allocation and reduces fragmentation.
* **Non-Contiguous Memory Allocation** : By managing KV cache blocks independently, PagedAttention enables non-contiguous memory allocation. This means that the KV cache can be dynamically expanded or contracted without the need for continuous memory blocks.
* **Dynamic Growth Without Pre-Allocation** : There’s no need to pre-allocate memory for the maximum possible sequence length. The KV cache can grow as needed, allocating new pages when required.
* **Memory Sharing Across Requests** : KV cache pages can be shared across different requests and sequences, especially beneficial for batching and advanced decoding algorithms like beam search.

## How vLLM Reduces Memory Usage

By implementing PagedAttention, **vLLM significantly reduces the GPU memory footprint** during inference. Here’s how:

* **Eliminating Fragmentation** : Both internal (unused space within allocated memory) and external (inability to use free memory due to fragmentation) memory fragmentation are minimized.
* **Efficient KV Cache Management** : The dynamic allocation of KV cache pages means that memory is used only when needed and released when not, avoiding the waste associated with static allocation.
* **KV Cache Sharing** : By allowing multiple requests to share KV cache pages when possible, redundant memory usage is reduced.

Press enter or click to view image in full size

_PagedAttention:_ KV Cache are partitioned into blocks. Blocks do not need to be contiguous in memory space[7]

## Practical Impact on Memory Requirements

To quantify the benefits of vLLM and PagedAttention, let’s revisit our GPU memory calculations for the LLaMA-2 70B model across different context windows. We’ll compare the memory requirements **before and after** applying vLLM optimizations.

Press enter or click to view image in full size

Table from our last calculation (refer to previous article for calculations)

In my experiments with the 7B and 13B models, I discovered some impressive memory savings! Depending on the approach, the reductions ranged from **44.3%** to as high as **66.3%**.

Now I’ll perform an educated calculation using the provided data and interpolate the expected memory savings across different context window sizes.

### Interpolating Memory Savings

I will interpolate the memory savings percentage based on the context window size, assuming a linear relationship between the context window size and the memory savings.

> I compute the slope (mmm) of the linear relationship: **0.00017741935% per token.**
>
> The linear equation is:
> **y = 0.00017741935% × x + 43.5903%**

Based on this I calculated the memory savings for different context window (x=4k, 8k, 32k, 128k).

> **For 4k Tokens (x=4k)** :
>
> **y = 0.00017741935% × 4k + 43.5903% = 44.3%**
>
> **For 8k Tokens (x=8k)** :
> **y = 0.00017741935% × 8k + 43.5903% = 45.01%**
>
> **For 32k Tokens (x=32k)** :
> **y = 0.00017741935% × 32k + 43.5903% = 49.27%**
>
> **For 128k Tokens (x=128k)** :
> **y = 0.00017741935% × 128k + 43.5903% = 66.3%**

### Calculating Memory Usage After Applying vLLM Savings

I’ll apply the calculated memory savings to the original memory usage for each context window using:

> Memory After Saving = Original Memory × (1−100Memory Saving (%)​)

Results in Table:

Press enter or click to view image in full size

The significant reduction in memory usage highlights the importance of efficient KV cache management. By minimizing fragmentation and enabling dynamic memory allocation, vLLM with PagedAttention allows for more concurrent requests and better hardware utilization.

## 2\. Quantization

Deploying LLMs on hardware with limited GPU resources is a significant challenge due to their massive memory requirements. **Quantization**[2][3][9][17]**** emerges as a powerful technique to alleviate this issue by reducing the memory footprint without severely compromising model performance.

## What is Quantization?

**Quantization** involves approximating a high-precision (e.g., 32-bit floating-point) numerical value with a lower-precision representation (e.g., 8-bit or even 2-bit integers). This process reduces the amount of memory required to store and process these values, leading to:

* **Reduced Memory Usage** : Lower bit width representations consume less memory.
* **Increased Computational Efficiency** : Operations on lower precision data are faster and require less energy.
* **Potential Hardware Compatibility** : Some hardware accelerators are optimized for low precision arithmetic.

> However keep in mind that, quantization can introduce numerical errors, potentially degrading model performance. The key is to balance memory savings and computational efficiency with the maintenance of acceptable model accuracy.

## Types of Quantization Techniques

Quantization techniques for LLMs are broadly classified into two categories:

1. **Quantization Aware Training (QAT)**
2. **Post Training Quantization (PTQ)**

### 1\. Quantization Aware Training (QAT)

**Quantization Aware Training (QAT)** involves training the model with quantization effects simulated during the training process. The idea is to incorporate quantization into the forward and backward passes so that the model learns to cope with the reduced precision. By doing this, the model parameters adapt to the quantization noise, minimizing the loss in performance.

Press enter or click to view image in full size

QAT general principle [3]

### How It Works

* **Simulated Quantization** : During training, operations simulate low-precision arithmetic while maintaining high precision gradients.
* **Backpropagation** : Gradients are calculated as if the quantization was present, allowing the model to adjust weights accordingly.
* **Fine-Tuning** : The model is often pre-trained in high precision and then finetuned with QAT to adapt to quantization.

### Benefits

* **Performance Preservation** : Minimizes the accuracy loss due to quantization.
* **Optimization** : Allows for aggressive quantization while maintaining acceptable performance.

### Drawbacks

* **Computational Cost** : Requires additional training time and resources.
* **Data Requirement** : Necessitates access to the original training data.
* **Complexity** : Introduces additional complexity in the training pipeline.

### Examples

💥** _LLM-QAT_
** Applies standard QAT techniques to LLMs, incorporating self-distillation to improve performance.

**Key Features** :

* Uses teacher-student framework where the high-precision model guides the quantized model.
* Targets 8-bit or lower precision without significant loss in accuracy.

**Benefits** :

* Maintains model performance close to the full-precision counterpart.
* Suitable for a variety of downstream tasks.

💥** _BitDistiller_
** Enhances performance at sub-4-bit precision using asymmetric quantization and confidence-aware objectives.

**Key Features** :

* Employs asymmetric quantization to better represent weight distributions.
* Introduces a confidence-aware loss function to prioritize important parameters.

**Benefits** :

* Achieves competitive performance even at very low bit-widths.
* Reduces model size significantly, enabling deployment on edge devices.

💥** _OneBit_
** Implements 1-bit quantization with novel parameter representation and initialization strategies.

**Key Features** :

* Uses specialized binary representation of weights.
* Introduces techniques to stabilize training with extreme quantization.

**Benefits** :

* Drastically reduces model size.
* Suitable for applications where memory is extremely constrained.

## 2\. Post Training Quantization (PTQ)

**Post Training Quantization (PTQ)** converts a trained full-precision model to a quantized model without additional training or finetuning. PTQ methods analyze the statistics of the trained model and apply quantization to weights, activations, or both. PTQ is particularly valuable when retraining is impractical due to computational constraints or unavailability of the original training data.

PTQ general principle [3]

### How It Works

* **Static Quantization** : Quantization parameters (like scale and zero point) are determined from the model’s weights and a representative dataset.
* **Dynamic Quantization** : Quantization parameters are calculated on-the-fly during inference, useful for activations that vary widely.
* **Calibration** : A small calibration dataset may be used to compute the quantization ranges, ensuring minimal performance degradation.

### Benefits

* **Simplicity** : Easier to implement compared to QAT.
* **Efficiency** : Saves time and resources by avoiding retraining.
* **Versatility** : Can be applied to a wide range of models.

### Drawbacks

* **Performance Trade-offs** : May lead to greater accuracy loss compared to QAT.
* **Limited Optimization** : Less control over quantization effects, potentially limiting the lowest usable precision.

### Subtypes of PTQ

PTQ can be further divided based on the components of the model that are quantized:

1. **Weight Only Quantization**
2. **Weight Activation Quantization**
3. **KV Cache Quantization**

### a. Weight Only Quantization

**Quantizes only the model’s weights** , keeping activations and other components at full precision.

**How It Works**

* **Static Quantization of Weights** : Applies quantization to the weights using methods like uniform or non-uniform quantization.
* **Layer wise or Group wise Quantization** : Weights can be quantized differently across layers or groups for better accuracy.

**Benefits**

* **Significant Memory Savings** : Reduces the memory footprint of the model weights, which is substantial in large models.
* **Simplicity** : Easier to implement without affecting the inference pipeline significantly.
* **Compatibility** : Can often be integrated with existing inference frameworks.

**Drawbacks**

* **Limited Reduction** : Doesn’t reduce memory usage of activations or KV cache.
* **Potential Performance Loss** : Especially at very low bit-widths (e.g., 2-bit or 3-bit), may lead to noticeable accuracy degradation.

> **Methods: GPTQ**

### b. Weight Activation Quantization

**Quantizes both the model’s weights and activations** , leading to further memory and computational savings.

**How It Works**

* **Quantizing Activations** : Involves dynamic or static quantization of activations, which can vary widely during inference.
* **Addressing Activation Outliers** : Techniques are used to handle large activation values that can affect quantization quality.

**Benefits**

* **Greater Memory Reduction** : Lowers memory requirements for both model storage and intermediate computations.
* **Speed Improvements** : Low precision arithmetic operations can be faster on compatible hardware.

Drawbacks

* **Increased Complexity** : Quantizing activations introduces challenges due to their dynamic nature.
* **Potential for Accuracy Loss** : Requires careful handling to avoid significant performance degradation.

> **Methods: ZeroQuant**

### c. KV Cache Quantization

**Quantizes the Key-Value (KV) cache** used during inference, which stores intermediate computations necessary for the attention mechanism in transformers.

**How It Works**

* **Quantizing KV Cache Elements** : Reduces the precision of stored key and value vectors.
* **Managing Quantization Errors** : Techniques are used to minimize the impact on the model’s ability to focus on relevant information.

**Benefits**

* **Significant Memory Savings** : Especially impactful for models with large context windows where the KV cache dominates memory usage.
* **Scalability** : Enables the use of longer context windows without prohibitive memory costs.

**Drawbacks**

* **Complexity in Implementation** : Requires modifications to the inference pipeline to support quantized KV cache.
* **Potential Accuracy Impact** : If not carefully managed, quantizing the KV cache can degrade model performance.

> **Methods: KVQuant**

Press enter or click to view image in full size

Quantization techniques comparison, Table by Author

### Now we go for calculations:

### Our Focus: Applying Quantization Techniques to LLaMA-2 70B Model

I have tested the memory reduction on 7B and 13B models and from which can imply it on LLaMA-2 70B, I’ll apply these across different context window sizes (4k, 8k, 32k, and 128k tokens) and calculate the resulting memory reductions. We take the calculation of from my last article:

### Memory Components Breakdown

Before applying quantization, we break down the total memory into:

* **Model Memory (Weights)** : 140 GB

**KV Cache Memory** :

* **4k Tokens** : 10.74 GB
* **8k Tokens** : 21.47 GB
* **32k Tokens** : 85.90 GB
* **128k Tokens** : 343.60 GB

**Activations and Overheads** : Estimated as 10% of (Model Memory + KV Cache Memory)

### 1 - Weight Only Quantization (GPTQ Technique):

I used llama.cpp for quantization and got results like

**Memory Reductions** :

* **8-bit Quantization** : Reduces weight memory by **49%**
* **4-bit Quantization** : Reduces weight memory by **75%**
* **3-bit Quantization** : Reduces weight memory by **81.25%**

### **a. 8-bit Quantization (49% Reduction in Model Memory)**

* **New Model Memory** : 140 GB × 0.51 = **71.40 GB**

### **b. 4-bit Quantization (75% Reduction in Model Memory)**

* **New Model Memory** : 140 GB × 0.25 = **35.00 GB**

### **c. 3-bit Quantization (81.25% Reduction in Model Memory)**

* **New Model Memory** : 140 GB × 0.1875 = **26.25 GB**

the KV Cache memory remain unchanged here for all scenario’s, for understanding purpose I am sharing one calculation (you can do rest similarly)

**4k Tokens 8-bit Quantization**

* **KV Cache Memory** : 10.74 GB (unchanged)
* **Activations** : 10% × (71.40 + 10.74) = **8.21 GB**
* **Total Memory** : 71.40 + 10.74 + 8.21 = **90.35 GB**
* **Memory Reduction** : (165.81–90.35) / 165.81 × 100% = **45.5%**

### 2 - Weight Activation Quantization (ZeroQuant Technique)

**Memory Reduction** :

* **Overall Memory Usage Reduction** : Up to **75%**

**Calculations**

I’ll apply a **75% reduction** to both **Model Memory** and **Activations**.

* **New Model Memory** : 140 GB × 0.25 = **35 GB**
* **Activations** : Original Activations × 0.25

**Calculations for Each Context Window** :

**4k Tokens**

* **Original Activations** : 15.07 GB
* **New Activations** : 15.07 × 0.25 = **3.77 GB**
* **Total Memory** : 35.00 + 10.74 + 3.77 = **49.51 GB**
* **Memory Reduction** : **70.1%**

### **3 - KV Cache Quantization (KVQuant Technique)**

**Memory Reduction** :

* **KV Cache Memory Reduction** : Up to **87.5%** (reducing from 16 bits to 2 bits)

**Calculations**

We’ll apply an **87.5% reduction** to the **KV Cache Memory** only.

**Calculations for Each Context Window** :

**4k Tokens**

* **New KV Cache Memory** : 10.74 × 0.125 = **1.34 GB**
* **Activations** : 10% × (140.00 + 1.34) = **14.13 GB**
* **Total Memory** : 140.00 + 1.34 + 14.13 = **155.47 GB**
* **Memory Reduction** : **6.2%**

Now based on calculations for all context window:

Press enter or click to view image in full size

## Observations

🔍**Weight Only Quantization** :

* Provides significant memory savings at smaller context windows.
* Savings diminish at larger context windows due to the increasing proportion of KV Cache Memory.

🔍**Weight Activation Quantization** :

* Offers greater memory reductions than weight only quantization, especially at smaller context windows.
* Still less effective at larger context windows compared to KV Cache Quantization.

🔍**KV Cache Quantization** :

* Minimal impact at small context windows where KV Cache Memory is small.
* Substantial savings at larger context windows, making it highly effective when dealing with long sequences.

## **3\. FlashAttention**

**FlashAttention**[6] is an efficient algorithm designed to compute exact self-attention with reduced memory footprint and increased computational speed. It was introduced to mitigate the quadratic scaling of memory and computation associated with the standard attention mechanism, especially prominent with long input sequences.

Press enter or click to view image in full size

How FlashAttention works [6]

## Understanding Self Attention and Its Challenges

In transformer models, the self-attention mechanism allows each token to attend to all other tokens in the sequence. This involves computing similarity scores between all pairs of tokens, resulting in:

* **Quadratic Memory Complexity** : The memory required scales with the square of the sequence length **_(O(N²))_** , where **_N_** is the number of tokens.
* **Performance Bottlenecks** : Large intermediate matrices must be stored during computation, leading to increased GPU memory usage and slower processing times.

## FlashAttention: How It Works

**FlashAttention** restructures the computation of self attention to be more memory efficient and faster without approximations, yielding the exact same output as standard attention.

### Key Innovations

🔸**Tiling and Streaming Computation** :

* **Blocks and Tiles** : Input sequences are divided into smaller blocks or tiles that can fit into the GPU’s on-chip memory (SRAM).
* **Sequential Processing** : These blocks are processed sequentially, computing partial results and aggregating them on the fly.

🔸**Memory Efficient Algorithm** :

* **Avoiding Large Intermediate Matrices** : By computing attention scores and applying softmax within each block, FlashAttention eliminates the need to store the entire attention matrix.
* **InPlace Computation** : Intermediate results are overwritten when no longer needed, further reducing memory usage.

🔸**Leveraging GPU Architecture** :

* **Optimized for Modern GPUs** : Takes advantage of the high bandwidth and parallelism of modern GPU SRAM.
* **Efficient Memory Access Patterns** : Reduces latency by minimizing data transfers between slow GPU VRAM and fast on-chip memory.

### Practical Impact on Memory

I tested FlashAttention also on 7B and 13B models and found around 13.4% reduction in memory for both cases. So we use this as foundation for our calculation

### Estimated Memory Savings with FlashAttention

> Assuming an average memory reduction of **13.4% based on my tests
> ** Memory After FlashAttention = Original Memory × (1−0.134)

**4k Tokens**

Memory After FlashAttention = 165.81 GB × 0.866 = 143.61 GB

Now, Lets see the summary

Press enter or click to view image in full size

## Integration with Other Optimization Techniques

FlashAttention can be combined with other memory optimization strategies for compounded benefits:

* **Quantization**[12][13]: Reducing the precision of weights and activations can further decrease memory usage.
* **PagedAttention (vLLM)** : Efficient KV cache management complements FlashAttention by optimizing different components of the model’s memory footprint.
* **KV Cache Quantization**[12][14]: Reducing the memory consumed by the KV cache can be particularly impactful for long sequences.

## 4\. CachedAttention

**CachedAttention** is a technique designed to optimize the storage and retrieval of KV caches in transformer based models during inference. By intelligently managing the KV cache across different storage tiers, GPU memory (HBM), host memory (RAM), and disk storage. CachedAttention reduces the memory footprint on GPUs and accelerates inference, particularly in multiturn conversations and scenarios with long input sequences.

Architecture overview of CachedAttention [5]

## CachedAttention: Design and Mechanisms

**CachedAttention** addresses these challenges through a hierarchical KV caching system called **AttentionStore** , which efficiently manages KV cache storage and retrieval across different memory tiers.

### Key Components of CachedAttention

🔹**AttentionStore Hierarchy** :

* **HBM (GPU Memory)** : Fastest but most limited in capacity.
* **Host Memory (RAM)** : Larger capacity than HBM but slower access times.
* **Disk Storage** : Largest capacity but slowest access times.
* **Function** : KV caches are offloaded to host memory or disk when not actively needed and reloaded when required.

🔹**Layer wise Preloading** :

* **Concept** : Loads KV caches layer by layer, overlapping data transfer with GPU computation to minimize overhead.
* **Benefit** : Reduces waiting time for KV cache loading, improving inference speed.

🔹**Asynchronous Saving** :

* **Concept** : Saves KV caches asynchronously while computations are ongoing, preventing delays in job scheduling.
* **Benefit** : Efficiently utilizes GPU resources without idle times.

🔹**Scheduler Aware Fetching and Eviction** :

* **Fetching** : Predicts which KV caches will be needed soon based on the job scheduler’s hints and prefetches them.
* **Eviction** : Intelligently evicts less valuable KV caches to make room for more critical ones, optimizing memory usage.

🔹**Positional Encoding Decoupling** :

* **Problem** : Truncating tokens due to context window overflow can invalidate KV caches because of embedded positional encodings.
* **Solution** : Decouples positional encoding from the KV caches, allowing for truncation without invalidating the cached KV tensors.

### Memory Reduction with CachedAttention

From my experiment I’ve found that CachedAttention can do upto 39% memory reduction

_Applying the_** _39% reduction_** _:_

> **Memory After CachedAttention = Original Memory × (1−0.39)**

**Calculations** :

**4k Tokens**

> **Memory After CachedAttention = 165.81 GB × 0.61 = 101.14 GB**

Press enter or click to view image in full size

## Additional Benefits of CachedAttention

Beyond memory savings, CachedAttention offers several performance enhancements:

🥉**Reduced Time to First Token (TTFT)** :

* **Improvement** : Decreases TTFT by up to **87%** , providing faster responses to users.
* **Explanation** : By eliminating redundant computations of KV caches, the model can generate the first token more quickly.

🥉**Increased Throughput** :

* **Improvement** : Increases prompt prefilling throughput by up to **7.8×**.
* **Explanation** : Efficient KV cache management allows the model to handle more requests in parallel without exhausting GPU memory.

🥉**Lower Inference Cost** :

* **Improvement** : Reduces end-to-end inference cost by up to **70%**.
* **Explanation** : Efficient resource utilization and reduced computational overhead lower the operational costs associated with running the model.

🥉**Scalability:**

* **Benefit** : Supports more concurrent sessions without additional GPU resources.
* **Explanation** : By offloading KV caches, the limited GPU memory is no longer a bottleneck for scaling up the number of active conversations.

**Just a heads up** , the techniques beyond this point are not ones I’ve personally tested; instead, I’ve used values from research studies. This means there could be some chance for slight inaccuracies, so If any of you have run these experiments and can share your findings I’d love to include them here for more precise insights!

## 5\. HCACHE

**HCache**[4] is designed to efficiently restore LLM states by caching and reusing hidden states instead of the full KV caches. The key components of HCache include:

### 📌**Hidden State Caching** :

* **Concept** : Instead of storing the full KV caches, HCache stores the hidden states generated after each transformer layer during inference.

**Benefits** :

* **Reduced Storage Size** : Hidden states are approximately half the size of KV caches, saving significant storage space.
* **Efficient Restoration** : Restoring KV caches from hidden states requires less computation and I/O overhead compared to recomputing from input tokens.

Overview of HCACHE[4]

### 📌**Restoration Process** :

**Computation** :

* **Lightweight Linear Projections** : KV caches are restored by performing linear projections on the cached hidden states.

**Pipeline Execution** :

* **Overlap of I/O and Computation** : HCache pipelines the I/O transfer of hidden states with the computation of restoring KV caches, efficiently utilizing both computational and I/O resources.

### 📌**Bubble Free Restoration Scheduler:**

**Challenge** :

* **Pipeline Bubbles** : Mismatches between computation and I/O speeds can cause stalls (bubbles) in the pipeline, leading to idle resources.

**Solution** :

* **Dynamic Layer Partitioning** : The scheduler dynamically partitions the model’s layers between different restoration methods (hidden states, KV offload, token recomputation) to balance computation and I/O, eliminating pipeline bubbles.

### 📌**Chunk Based Storage Manager** :

**Challenge** :

* **Storage Format Mismatch** : The storage order of hidden states (layer-before-token during saving) differs from the access pattern needed during restoration (token-before-layer), causing inefficient I/O operations.

**Solution** :

* **Optimized Storage Format** : HCache uses a chunk-based storage format that organizes hidden states to enable efficient batch retrieval during restoration, improving I/O efficiency.

### Calculating Total Memory with HCache

Since HCache reduces the storage requirements for KV caches by **1.92× to 2.40×** , we can calculate the new KV cache memory usage:

> **KV Cache Memory with HCache** = Original KV Cache Memory ÷ Reduction Factor

I took the average of the reduction factors **1.92×** and **2.40×** , we get: **2.16**

**Calculations:**

The total memory with HCache is the sum of:

* **Model Memory** : Remains at **140 GB**.
* **New KV Cache Memory** : Calculated below.
* **Activations** : Estimated as **10%** of the sum of Model Memory and New KV Cache Memory.

**For 4k Tokens**

> New KV Cache Memory = 10.74 GB / 2.16 ≈ 4.97 GB

Now lets see the whole table:

Press enter or click to view image in full size

Looks good for Longer context!

## 6\. Distillation

### What is Knowledge Distillation?

**Knowledge Distillation**[1][2][3][10][12]**(KD)** is a model compression technique where a smaller model (called the **student model**) is trained to replicate the behavior of a larger, more complex model (called the **teacher model**). The goal is to transfer the knowledge from the teacher to the student so that the student can achieve similar performance with reduced computational and memory requirements.

An illustration of a pipeline to distill knowledge from a LLM to a student model [10]

### Types of Knowledge Distillation

Knowledge Distillation methods can be broadly classified into two categories:

1. **Black Box Knowledge Distillation**
2. **White Box Knowledge Distillation**

### 🔹Black Box Knowledge Distillation

In **Black Box Knowledge Distillation** , only the outputs of the teacher model are accessible. The internal parameters or structures of the teacher are not available. This scenario is common when distilling knowledge from proprietary or closed source models, such as OpenAI’s GPT-4 or ChatGPT.

**How It Works**

* **Dataset Generation** : The teacher model is used to generate a synthetic dataset by providing outputs for a variety of inputs.
* **Training the Student** : The student model is trained on this dataset, learning to mimic the outputs of the teacher.

### 🔹White Box Knowledge Distillation

In **White Box Knowledge Distillation** , the internal parameters, intermediate representations, and output distributions of the teacher model are accessible. This allows for a deeper transfer of knowledge, as the student can learn not just the outputs but also the internal workings of the teacher.

### How It Works

* **Parameter Access** : The student model has access to the teacher’s weights and can compute losses based on intermediate activations.
* **Loss Functions** : Specialized loss functions are used to align the student’s behavior with the teacher’s at various levels.

Press enter or click to view image in full size

Illustration of teacher-student framework for knowledge distillation[1]

### Calculating Total Memory with KD

I take the 40% reduction in model size via distillation from DistilBERT[3][10][23]

**Model Memory Reduction** : Reduce the model memory component by **40%**.

* **Original Model Memory** : 140 GB
* **Reduced Model Memory** : 140 GB × 0.60 = **84 GB**
* **KV Cache Memory** : Remains unchanged.
* **Activations** : Estimated as 10% of (Model Memory + KV Cache Memory).

Press enter or click to view image in full size

Press enter or click to view image in full size

Treemap for LLM compression techniques, image by Author

Press enter or click to view image in full size

How Pruning and Quantization differ. Image by Author

## 7\. Pruning

**pruning**[3][14][16] emerges as an effective technique to reduce model size and, consequently, GPU memory requirements during inference. By removing redundant or less important parameters from the model, pruning can achieve substantial memory savings while maintaining acceptable performance levels.

General overview of **Pruning** techniques [3]

## Understanding Pruning and Its Types

Pruning techniques can be broadly classified into two categories:

1. **Unstructured Pruning**
2. **Structured Pruning**

I will focus on these two types and analyze their impact on memory reduction.

## 🔖Unstructured Pruning

**Unstructured Pruning** removes individual weights from the model regardless of their position, leading to a sparse weight matrix. This type of pruning identifies and eliminates weights that contribute least to the model’s performance, often based on criteria like magnitude.

### How It Works

* **Weight Selection** : Weights with the smallest magnitudes or least importance are identified for removal.
* **Sparsity Level** : Methods like **SparseGPT** can achieve up to **50% sparsity** , meaning 50% of the weights are set to zero.
* **One-Shot Pruning** : Some techniques perform pruning in a single step without retraining, making it efficient for large models.

### Drawbacks

* **Irregular Weight Matrices** : Leads to sparse matrices that may not be efficiently stored or processed without specialized hardware or software optimizations.
* **Limited Hardware Support** : Not all hardware accelerators are optimized for unstructured sparsity.

## 🔖Structured Pruning

**Structured Pruning** removes entire structures within the model, such as neurons, filters, attention heads, or even layers. This results in a smaller, denser model that is more hardware-friendly.

### How It Works

* **Component Removal** : Identifies and removes less important structures based on criteria like importance scores or sensitivity analysis.
* **Model Size Reduction** : Methods like **LLM-Pruner** achieve around **20% reduction** in model size.

### Drawbacks

* **Potential Performance Degradation** : Removing entire structures can have a more significant impact on model performance.
* **Need for Retraining** : Often requires fine-tuning or retraining to recover lost performance.

## Calculations

I found from studies that Unstructured pruning reduces the model’s weights by 50% and structured pruning reduces the model’s weights by **20%. [3]**

### New Model Memory

* **Reduced Model Memory structured pruning** : 140 GB × 0.80 = **112 GB**
* **Reduced Model Memory Unstructured pruning** : 140 GB × 0.50 = **70 GB**

KV Cache Memory will remain unchanged and we have impact on activations which can be calculated in same way as I did before and get:

Press enter or click to view image in full size

Now, I do same for Unstructured Pruning:

Press enter or click to view image in full size

Pruning seems effective for model with small context window!

## 8\. FastGen

**FastGen**[9]**** introduces an adaptive KV cache compression method that leverages the intrinsic structure of attention modules to reduce GPU memory consumption during inference, achieving up to **40%** memory [9] reduction with minimal impact on generation quality.

## How FastGen Works

### 1\. Attention Profiling

* **Purpose** : To discern the intrinsic structure and behavior of each attention head.
* **Method** : During the prompt encoding phase, FastGen conducts lightweight profiling to analyze attention patterns.
* **Outcome** : Classifies attention heads based on their focus, such as whether they emphasize local contexts, special tokens, or attend broadly to all tokens.

### 2\. Adaptive KV Cache Compression

Based on the profiling results, FastGen applies different compression policies to each attention head:

* **Tailored Strategies** : Instead of uniformly storing all KV vectors, it adapts the cache content according to the specific needs of each attention head.
* **Dynamic Management** : During token generation, FastGen manages the KV cache adaptively, deciding which tokens to keep or discard for each attention head.

## Calculations

I will estimate the potential memory savings for the **LLaMA-2 70B** model across different context window sizes by applying the **40% memory reduction** achieved by FastGen.

FastGen reduces the KV cache memory by **40%** while maintaining model weights and activations.

New KV Cache Memory

* **Reduced KV Cache Memory** : Original KV Cache Memory × 0.60

All calculations will be same, so let’s look at output table:

Press enter or click to view image in full size

The percentage of memory reduction increases with larger context windows because the KV cache constitutes a larger portion of the total memory at these scales.

## 9\. LoRD

Before explaining LoRD[21], I would go a little back and start with **Low Rank Factorization**[3][20][22] techniques which offer a promising avenue for compressing these models by decomposing large weight matrices into products of smaller matrices, reducing the number of parameters without inducing sparsity. This approach not only decreases memory usage but can also accelerate inference on modern hardware.

Press enter or click to view image in full size

General overview of **Low Rank Factorization** techniques [3]

## Overview of Low Rank Factorization Techniques

Several low-rank factorization methods have been proposed to compress LLMs:

➡️**LPLR (Low-Precision and Low-Rank)**

* Combines low-rank decomposition with low-precision representations to further reduce memory footprint.

➡️**ASVD (Activation-Aware Singular Value Decomposition)**

* Applies singular value decomposition (SVD) to weight matrices while considering activation distributions to minimize performance loss.

➡️**LASER (Layer-Selective Rank Reduction)**

* Selectively reduces the rank of specific layers based on their sensitivity to rank reduction.

➡️**LoRD (Low-Rank Decomposition)**

* Focuses on decomposing weight matrices into lower-rank forms, reducing parameters without sparsity and maintaining differentiability.

In this article, I will focus on **LoRD** and explore how it can be applied to compress the LLaMA-2 70B model.

**LoRD** proposes compressing LLMs by decomposing large weight matrices into products of two smaller matrices, effectively reducing the rank of these matrices. Unlike pruning or quantization, LoRD maintains the dense structure of the model weights, which allows for efficient computation on modern hardware without the need for specialized sparse matrix operations.

## Calculations

we found from paper that LoRD achieves up to **39.58%**[21] reduction in weight parameters.

**New Model Memory (Weights)**

* **Reduced Model Memory** = 140 GB × (1−0.3958) = 84.59 GB

Other calculations will be same:

Press enter or click to view image in full size

## Advantages of LoRD

🥈**Parameter Reduction without Sparsity** :

* Maintains dense matrices, which are more compatible with existing hardware and software optimizations.
* Avoids the need for specialized sparse matrix operations.

🥈**Inference Speedup** :

* Reduced model size leads to decreased memory bandwidth requirements.
* Experiments report up to **22.35%** speedup in inference.

🥈**Compatibility with Quantization** :

* LoRD models can be further compressed using quantization techniques like SpQR.
* Allows for additional memory savings and efficiency gains.

## 10\. GemFilter

**GemFilter**[11] is a novel method designed to address these challenges by intelligently compressing the input context, leading to significant reductions in GPU memory usage — up to **70%** — and substantial inference speedups.

Press enter or click to view image in full size

How GemFilter works [11]

### Key Components of GemFilter

🔹**Early Layer Filtering**

* **Observation** : In the initial layers of an LLM, the model begins to focus on tokens most relevant to generating an answer.
* **Filter Layers** : Designated early layers (e.g., layers 13 to 19 in a 32-layer model) analyze the full input context to determine token importance.
* **Attention Matrices** : By examining the attention scores — particularly the last row corresponding to the query token — GemFilter identifies tokens that the model attends to the most.

🔹**Token Selection and Compression**

* **Selecting Top-K Tokens** : GemFilter selects the top kkk tokens with the highest attention scores from the filter layers.
* **Compressed Input** : The selected tokens form a compressed version of the input context, dramatically reducing the sequence length (e.g., from 128,000 tokens down to 100 tokens).

🔹**Second Inference Run with Compressed Input**

* **Re-Feeding the Model** : The compressed input is fed back into the full LLM for standard inference and generation.
* **Positional Embeddings** : Positional embeddings are recalculated for the shorter input sequence, improving efficiency.

## Calculations

From experimental results, GemFilter achieves up to **70%** reduction[11] in GPU memory usage when processing long-context inputs.

Since GemFilter reduces the context length significantly, the KV cache memory and activations will decrease accordingly.

* **Reduced KV Cache Memory** : 30% of the original KV cache memory (since 70% reduction)
* **Reduced Activations** : 30% of the original activations
* **Model Memory (Weights)** : 140 GB (remains unchanged with GemFilter)

using same calculation formula, we get:

Press enter or click to view image in full size

GemFilter provides substantial GPU memory reductions, especially for very long context windows (e.g., over **51%** reduction at 128k tokens).

Throughout our exploration, we’ve covered several techniques to reduce the memory footprint of LLMs, in this case for **LLaMA-2 70B**. Methods such as **Knowledge Distillation** and **Pruning** are particularly effective for smaller context windows, significantly reducing model size and memory usage with minimal performance loss. In contrast, techniques like **HCache** , **FastGen** , and **GemFilter** become increasingly beneficial as the context window grows larger, optimizing KV cache usage and compressing input sequences to achieve substantial memory savings.

Press enter or click to view image in full size

Comparison table for several techniques, table by Author

The choice of which technique to employ depends on your specific needs and the context window size of your application. Like, if you’re working with shorter sequences and require minimal performance degradation, **Knowledge Distillation** might be the ideal approach. Conversely, for applications involving long context inputs where the KV cache becomes a significant memory bottleneck, **FastGen** or **GemFilter** could offer the most advantages.

### Considerations for CPU memory when offloading KV caches

When offloading the key-value (KV) cache from GPU to CPU memory to reduce GPU memory usage such as **vLLM’s PagedAttention** , **CachedAttention** , or **HCache** , it’s crucial to ensure that your system has sufficient CPU RAM to handle the offloaded data. LLMs like LLaMA-2 70B with extensive context windows and multiple concurrent requests can require hundreds of gigabytes of CPU memory to store the KV caches. High speed RAM is also important to minimize latency during data transfers between the CPU and GPU. Configuring multi-channel memory setups and considering Non-Uniform Memory Access (NUMA) architectures can help optimize memory access patterns and improve performance.

Equally important is the bandwidth of the connection between the CPU and GPU, as data transfers occur over the PCI Express (PCIe) bus. Higher PCIe versions offer greater bandwidth, which is essential for moving large amounts of data without creating bottlenecks. For instance, PCIe 3.0 x16 provides approximately 16 GB/s, PCIe 4.0 x16 offers about 32 GB/s, and PCIe 5.0 x16 delivers up to 64 GB/s of bidirectional bandwidth. Utilizing systems with PCIe 4.0 or 5.0 can significantly reduce data transfer times when offloading KV caches. Implementing efficient data transfer techniques such as asynchronous transfers, data compression, and intelligent caching can further minimize latency and ensure that the offloading process does not adversely affect inference performance.

### Combining multiple techniques

After reading tons of paper in this direction, I now think of trying to combine some of these techniques to see the results (can be a good research direction) and who knows this combination can lead to even greater memory reductions. For example from my understanding , applying **LoRD** for low rank decomposition alongside **Quantization** can compound memory savings while maintaining model performance. Similarly, integrating **FastGen** with **FlashAttention** might further optimize memory usage during attention computations.

I encourage you to experiment with these techniques, both individually and in combination, to find the optimal balance for your specific use case. And please share your results here so we can keep updating this article with new insights and better results together.

I could go on with more insights and details, but I’ll be honest, I’m a bit worn out and could use a break! 😅 There’s a lot to digest, and I want to make sure each point gets the time it deserves. I’ll definitely be back to add more updates, new findings, and fresh examples as I continue exploring, so stay tuned. Your thoughts and contributions are welcome in the meantime!

**_That’s it for today, But rest assured, our journey is far from over! If you enjoyed this article and want to learn more, make sure to follow me. I’ll be back with more detailed and interesting write-ups that promise to be both fun and educational. Don’t forget to follow me for more outstanding content. Additionally:_**

* **👏 Clap for the story (50 claps) to help this article be featured**
* **🔔 Follow Me:**[**LinkedIn**](<https://www.linkedin.com/in/muhammad-saad17/>)**|**[**Medium**](<https://medium.com/@itssaad.muhammad>)**|**[**Website**](<https://saadresume.streamlit.app/>)
* **🌟 Need help in converting these prototypes to products?**[**Contact Me!**](<https://topmate.io/saad_muhammad>)

## 🔹References

[1] [Knowledge Distillation: A Survey](<https://arxiv.org/pdf/2006.05525>)
[2] [MODEL COMPRESSION VIA DISTILLATION AND QUANTIZATION](<https://arxiv.org/pdf/1802.05668>)
[3] [A Survey on Model Compression for Large Language Models](<https://arxiv.org/html/2308.07633v4>)
[4] [Fast State Restoration in LLM Serving with HCache](<https://arxiv.org/html/2410.05004v1>)
[5] [Cost-Efficient Large Language Model Serving for Multi-turn Conversations with CachedAttention](<https://arxiv.org/html/2403.19708v3#bib.bib54>)
[6] [FlashAttention: Fast and Memory-Efficient Exact Attention
with IO-Awareness](<https://arxiv.org/pdf/2205.14135>)
[7] <https://blog.vllm.ai/2023/06/20/vllm.html>
[8] [Efficient Memory Management for Large Language Model Serving with PagedAttention](<https://arxiv.org/pdf/2309.06180>)
[9] [Contemporary Model Compression on Large Language Models Inference](<https://arxiv.org/html/2409.01990v1>)
[10] [A Survey on Knowledge Distillation of Large Language Models](<https://arxiv.org/html/2402.13116v1>)
[11] [Discovering the Gems in Early Layers: Accelerating Long-Context LLMs with 1000x Input Token Reduction](<https://arxiv.org/html/2409.17422v1#bib.bib27>)
[12] <https://huggingface.co/blog/optimize-llm>
[13] <https://unfoldai.com/gpu-memory-requirements-for-llms/>
[14] <https://developer.nvidia.com/blog/mastering-llm-techniques-inference-optimization/>
[15] [Self-Supervised Quantization-Aware Knowledge Distillation](<https://arxiv.org/pdf/2403.11106>)
[16] <https://www.artfintel.com/p/efficient-llm-inference>
[17] [The case for 4-bit precision: k-bit Inference Scaling Laws](<https://arxiv.org/pdf/2212.09720>)
[18] [Stateful Large Language Model Serving with Pensieve](<https://arxiv.org/pdf/2312.05516>)
[19] [MODEL TELLS YOU WHAT TO DISCARD: ADAPTIVE KV CACHE COMPRESSION FOR LLMS](<https://arxiv.org/pdf/2310.01801>)
[20] [H2O: Heavy-Hitter Oracle for Efficient Generative Inference of Large Language Models](<https://arxiv.org/pdf/2306.14048>)
[21] [LORD: LOW RANK DECOMPOSITION OF MONOLINGUAL CODE LLMS FOR ONE-SHOT COMPRESSION](<https://arxiv.org/pdf/2309.14021>)
[22] [Characterizing the Accuracy-Efficiency Trade-off of Low-rank Decomposition in Language Models](<https://arxiv.org/pdf/2405.06626>)
[23] [DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter](<https://arxiv.org/abs/1910.01108>)

---
domain: levelup.gitconnected.com
fetch_date: '2026-05-18T12:53:04.267312'
status: ok
url: https://levelup.gitconnected.com/fanformer-is-the-new-game-changing-architecture-for-llms-d56999fab7f2
---

# ‘FANformer’ Is The New Game-Changing Architecture For LLMs

## A deep dive into how FANFormer architecture works and what makes it so powerful compared to Transformers

[ ![Dr. Ashish Bamania](https://miro.medium.com/v2/resize:fill:64:64/1*5R3sTJ1KZkaD9s6XmBNsQA@2x.jpeg) ](<https://bamania-ashish.medium.com/?source=post_page---byline--d56999fab7f2--------------------------------------->)

[Dr. Ashish Bamania](<https://bamania-ashish.medium.com/?source=post_page---byline--d56999fab7f2--------------------------------------->)

10 min read

·

Mar 9, 2025

\--

Listen

Share

More

Image generated with DALL-E 3

LLMs have always surprised us with their capabilities, with many speculating that [scaling](<https://arxiv.org/abs/2001.08361>) them would lead to AGI.

But such expectations have led to disappointments in the last few days, with [GPT-4.5, the largest and best model for chat from OpenAI](<https://openai.com/index/introducing-gpt-4-5/>), performing worse than many smaller models on multiple benchmarks.

While DeepSeek-V3 scores 39.2% Pass@1 accuracy on [AIME 2024](<https://huggingface.co/datasets/HuggingFaceH4/aime_2024>) and 42% accuracy on [SWE-bench Verified](<https://www.swebench.com/>), GPT-4.5 scores 36.7% and 38% on these benchmarks, respectively.

Press enter or click to view image in full size

Performance of DeepSeek-V3 in comparison with other LLMs (Image from ArXiv research paper titled ‘[DeepSeek-V3 Technical Report](<https://arxiv.org/pdf/2412.19437v1>)’)

Press enter or click to view image in full size

Performance of GPT-4.5 in comparison with other OpenAI models (Image from OpenAI’s blog post titled ‘[Introducing GPT-4.5](<https://openai.com/index/introducing-gpt-4-5/>)’)

This raises the question: _Do we need a better LLM architecture to scale further?_

Luckily, we have a strong candidate that has been [put forward by researchers recently](<https://www.arxiv.org/abs/2502.21309>).

Called **FANformer** , this architecture is built by combining the powerful [Fourier Analysis Network (FAN)](<https://intoai.pub/p/fourier-analysis-networks-fans-are>) into the [Attention mechanism](<https://intoai.pub/i/157243999/we-start-our-journey-with-attention>) of Transformers.

The results of experiments performed with them are very promising, with FANformers consistently outperforming Transformer when scaling up model size and training tokens.

As seen in the plot below, a FANformer with 1 billion parameters performs better than other open-source LLMs of comparable size and training tokens.

Press enter or click to view image in full size

Here’s a story where we deep dive into how a FANFormer works and discuss all the architectural modifications that make it so powerful.

Let’s begin!

## We Begin With ‘Fourier Analysis Networks’

[Standard deep neural networks/ MLPs](<https://intoai.pub/i/144432996/but-first-what-even-are-mlps>) do very well at capturing and modelling (“learning”) most patterns from training data, but there’s one domain where they largely fall short.

This is — **Modelling Periodicity in data**.

Since most data contain hidden periodic patterns, this hinders the learning efficiency of traditional neural networks.

Check out the following example where a Transformer struggles to model this simple `mod` function even when given sufficient training resources.

Press enter or click to view image in full size

Comparison of the performance of Transformer and FANformer on periodicity modeling

This is fixed by [Fourier Analysis Networks (FANs)](<https://arxiv.org/abs/2410.02675>), which use the principles of [Fourier Analysis](<https://en.wikipedia.org/wiki/Fourier_analysis>) to encode periodic patterns directly within the neural network.

This can be seen in the following example, where a FAN can better model a periodic `sin` function compared to [MLP](<https://intoai.pub/i/144432996/but-first-what-even-are-mlps>), [KAN](<https://intoai.pub/i/144432996/now-coming-to-kans-and-how-they-work>) and [Transformer](<https://arxiv.org/abs/1706.03762>).

Press enter or click to view image in full size

Performance comparison between different neural network architectures within and outside the domain of their training data for a sine function (Image from ArXiv research paper titled ‘[FAN: Fourier Analysis Networks](<https://arxiv.org/abs/2410.02675>)’)

A FAN Layer is described using the following equation:

Press enter or click to view image in full size

where:

* `X` is the input
* `W(p)` and `W(p̄)`are learnable projection matrices
* `B(p̄)`​​ is the bias term
* `σ` represents a non-linear activation function
* `||` denotes concatenation

Compared to an MLP layer that applies a simple linear transformation followed by a non-linear activation, the FAN layer explicitly integrates periodic transformations (sine and cosine) with the linear transformation and non-linear activation.

Press enter or click to view image in full size

An MLP layer performs linear transformation followed by non-linear activation on input X

This helps a FAN layer capture periodic patterns in the input data alongside its general-purpose modelling capabilities.

Here’s a visual and mathematical comparison between MLP and FAN layers.

Press enter or click to view image in full size

Architectural differences between a MLP and FAN layer (Image from ArXiv research paper titled ‘[FAN: Fourier Analysis Networks](<https://arxiv.org/abs/2410.02675>)’)

Press enter or click to view image in full size

Mathematical differences between a MLP and FAN layer (Image from ArXiv research paper titled ‘[FAN: Fourier Analysis Networks](<https://arxiv.org/abs/2410.02675>)’)

_If you’d like to learn about FANs in more depth, here’s one of my lessons on how they work and how to code one from scratch._

## [Fourier Analysis Networks (FANs) Are Here To Break Barriers In AIA deep dive into Fourier Analysis Networks (FANs), a novel neural network architecture and learning to build one from…levelup.gitconnected.com](</fourier-analysis-networks-fans-are-here-to-break-barriers-in-ai-1c521c6656bc?source=post_page-----d56999fab7f2--------------------------------------->)

## Moving Forward To Building The Attention Mechanism Of A FANformer

Most popular LLMs today have a [decoder-only Transformer architecture](<https://arxiv.org/abs/2005.14165>).

A FANformer borrows the periodicity-capturing principles from FAN and applies them to the Attention mechanism of this Transformer architecture.

This revised Attention mechanism is called the **ATtention-Fourier (ATF) module.**

Given an input sequence `s` of length `l`, represented by `s = { s(1)​, s(2)​, …, s(l)​ }`, it is first mapped to an input embedding `X(0)` where `X(0) = { x(1)​, x(2)​, …, x(l)​ }`.

This embedding passes through the layers of a model, obtaining the final output `X(N)`, where `N` is the total number of layers in the model.

Let’s learn how each layer processes the embedding.

Given an input embedding `X`, its Fourier-transformed representation is first computed as:

Press enter or click to view image in full size

As you will notice, this transformation uses a slightly modified `FANLayer’` where the activation function `σ` in the original `FANLayer` equation is simply replaced by an identity function or `σ(x) = x`.

Next, linear transformations are applied to the output `X(F)` to compute the query (`Q`), key (`K`), and value (`V`) as shown below:

Press enter or click to view image in full size

where `W(Q)`​, `W(K)​`, and `W(V)`​ are learnable weight matrices used to compute the query (`Q`), key (`K`), and value (`V`), respectively.

Following this, the scaled dot-product attention is calculated using the Fourier-transformed `Q`, `K`, and `V` as follows:

Press enter or click to view image in full size

where `d(h)` is the model’s hidden dimension.

Note that `ATF(X)` is mathematically equivalent to `Attention(FANLayer′(X))`, because the Fourier transformations do not alter the attention mechanism itself but only how input representations are computed.

This makes it possible to use advanced architectures like [FlashAttention](<https://arxiv.org/abs/2205.14135>) with the `FANLayer'`, and therefore, with the FANFormer.

## Building Up To Multi-Head ATF

The attention module is further extended to multiple heads, similar to [traditional Multi-head Attention](<https://intoai.pub/i/157243999/moving-towards-multi-head-attention>).

For a given input `X`, it is first projected into `k` independent heads using the previously described ATF module as follows:

Press enter or click to view image in full size

where for the `i`-th head:

* `W(Q)(i)`, `W(K)(i)`, `W(V)(i)` are the learnable weight matrices for each head’s (`Q(i)`), key (`K(i)`), and value (`V(i)`), respectively, calculated as follows:

Press enter or click to view image in full size

* `d(k)` is the dimension per head when using `k` attention heads, calculated as `​= d(h) ​/ k` where `d(h)` is the model’s hidden dimension.

Then, the outputs of all the heads are concatenated and linearly transformed using an output weight matrix (`W(O)`).

Press enter or click to view image in full size

The FANformer architecture is shown in the illustration below.

Press enter or click to view image in full size

Compare it with the conventional Multi-head Attention shown below, where `Q`, `K` and `V` for each head are computed directly from the input embedding without any Fourier transformation.

Press enter or click to view image in full size

Conventional Multi-head Attention with Q, K, V calculated from input embedding X using learnable weight matrices for each head (Image obtained from the research paper titled ‘[Attention Is All You Need](<https://arxiv.org/pdf/1706.03762>)’ )

The pseudocode for the Multi-head ATF is shown below:

Press enter or click to view image in full size

Note that in the above, `p` is the hyperparameter that controls how much of the input `X` is processed through the periodic (`X_p`) vs. non-periodic components (`X_p̄`) following the `FANLayer’` equation.

`p` is set to `0.25` by default in the experiments.

## Stacking Up To A FANformer

A FANformer is built by stacking `N` FAN-former layers where each layer consists of:

* a Multi-head ATF (Attention-Fourier) module
* a Feedforward Network (FFN) module

The Multi-head ATF output is calculated based on the previous equation:

Press enter or click to view image in full size

But the input for each layer (`X(n)`) is modified using [Pre-Normalization (Pre-Norm)](<https://arxiv.org/abs/1910.07467>) and then adding the original input back to the computed output from the `MultiHeadATF`.

Press enter or click to view image in full size

`Y(n)` is then transformed using the Feedforward Network (FFN) module as follows:

Press enter or click to view image in full size

where `FFN` uses the [SwiGLU activation](<https://arxiv.org/abs/2002.05202>) as follows:

Press enter or click to view image in full size

where `W(1)`, `W(2)`, and `W(3)` are learnable weight matrices and ⊗ denotes element-wise multiplication.

_Reading these equations with the visual representation of the FANformer side by side is highly encouraged to understand them better._

## How Good Is The FANFormer?

Researchers construct a FANformer by integrating the ATF module into the open-source LLM, [OLMo](<https://arxiv.org/abs/2402.00838>), using it as the baseline Transformer.

Tokens are sampled from OLMo’s training data, called [Dolma](<https://openreview.net/forum?id=LcARAz6Fp0>), and used to pre-train FANformers of different sizes.

### Scaling Experiments

On scaling experiments, the FANformer consistently outperforms the standard Transformer across all model sizes and achieves comparable performance while using only 69.2% of its parameters!

The scaling curve for a variant of FANformer called `Transformer + ATM`, which uses MLP layers instead of FAN layers, is very similar to that of a standard Transformer.

This shows that the revised attention mechanism with MLP layers is not as good, and instead, the periodicity capturing architectural changes is what gives the FANformer real performance boost.

Press enter or click to view image in full size

Language modeling loss for different architectures when scaling up parameters

Further experiments show that the FANformer requires 20.3% fewer training tokens to match the performance of the standard Transformer.

Press enter or click to view image in full size

Language modeling loss for different architectures when scaling up training tokens

### Performance On Downstream Tasks

FANformer’s zero-shot performance is compared with 7 open-source LLMs (of similar size/ training tokens) on a set of 8 downstream tasks using the following benchmarks:

* [**ARC-C** & **ARC-E**](<https://arxiv.org/abs/1803.05457>)**(** Advanced reasoning)
* [**BoolQ**](<https://arxiv.org/abs/1905.10044>)**(** Boolean question answering)
* [**HellaSwag**](<https://arxiv.org/abs/1905.07830>)**(** Commonsense completion)
* [**OBQA**](<https://arxiv.org/abs/1809.02789>)****(Open book question answering)
* [**PIQA**](<https://arxiv.org/abs/1911.11641>)**(** Physical reasoning)
* [**SCIQ**](<https://arxiv.org/abs/1707.06209>) (Science question answering)
* [**WinoGrande**](<https://arxiv.org/abs/1907.10641>) (Co-reference resolution)

Experiments show that FANformer-1B consistently outperforms other LLMs with similar parameter counts while requiring significantly less training data.

Notably, FANformer-1B's performance is comparable to [Qwen2.5–1.5B](<https://huggingface.co/Qwen/Qwen2.5-1.5B>), the current state-of-the-art LLM around the 1 billion parameter mark.

Also, [R1-Distill-Qwen1.5B](<https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B>), a model distilled from [DeepSeek-R1](<https://arxiv.org/abs/2501.12948>) with strong reasoning capabilities, cannot outperform the FANformer on most non-reasoning commonsense tasks.

**This shows how important pre-training is and that**[**distillation**](<https://arxiv.org/abs/1503.02531>)**alone is not enough for strong model performance on downstream tasks.**

Press enter or click to view image in full size

Zero-shot performance of FANformer-1B vs. other comparable open-source LLMs on downstream tasks

### Training Dynamics

In the early stages of training, the FANformer’s loss decreases more slowly than that of the standard Transformer’s.

This could be because the model has not learned to recognize the periodic patterns in the data in its early stages.

But as the training progresses, the FANformer converges faster than the Transformer.

Press enter or click to view image in full size

Training loss of FANformer and Transformer in the early training steps

### Instruction Following Performance with Supervised Fine-Tuning (SFT)

The pretrained FANformer-1B model is further supervised fine-tuned on the [tulu-3-sft-olmo-2-mixture](<https://huggingface.co/datasets/allenai/tulu-3-sft-olmo-2-mixture>) dataset (following OLMo), leading to FANformer-1B-SFT.

Similarly, OLMo-1B-SFT, the 1 billion parameter version of OLMo is supervised fine-tuned on the same dataset.

These models are evaluated using four benchmarks as follows:

* [**MMLU**](<https://arxiv.org/abs/2009.03300>) (General knowledge and reasoning)
* [**TruthfulQA**](<https://arxiv.org/abs/2109.07958>) (Truthfulness & informativeness)
* [**AlpacaEval**](<https://github.com/tatsu-lab/alpaca_eval>) (Instruction-following quality)
* [**ToxiGen**](<https://arxiv.org/abs/2203.09509>) (Toxicity filtering capability)

Results again show the superior performance of FANformer-1B-SFT on MMLU, AlpacaEval, and TruthfulQA compared to OLMo-1B-SFT.

Press enter or click to view image in full size

Evaluation results for FANformer-1B and OLMo-1B. Higher values are better for MMLU, AlpacaEval, and TruthfulQA, while lower values are better for ToxiGen.

### Filling A “Hole” In Mathematical Reasoning

[A 2024 research paper](<https://arxiv.org/abs/2402.17709>) described how Transformer-based LLMs use **Case-based reasoning** to solve mathematical problems.

This means that they memorize specific examples from training data and then try to generalize by finding similar cases during inference.

This differs from **Rule-based reasoning** , which involves learning underlying mathematical rules and applying them systematically for problem-solving.

Press enter or click to view image in full size

Case-based vs Rule-based reasoning (Image from ArXiv research paper titled ‘[Case-Based or Rule-Based: How Do Transformers Do the Math?](<https://arxiv.org/abs/2402.17709>)’)

_But do FANformers solve maths this way as well?_

To test this, OLMo-1B and FANformer1B, are evaluated on two mathematical problems:

* **Modular Addition** : Solve `c = (a + b) mod 113` with `a, b ∈ [0, 112]`
* **Linear Regression** : Solve `c = a + 2b + 3` with `a, b ∈ [0, 99]`

They are fine-tuned on each task dataset, and their performance is measured via the**Leave-Square-Out method**.

This is where a square region of data points is removed from the training set, and the model is trained on the remaining data to ensure that it is not exposed to the left-out square region.

The model’s performance on these left-out data points is then evaluated during testing.

In experiments, both architectures achieve near-perfect accuracy on the training dataset. However, Transformers fall short on the test dataset.

Press enter or click to view image in full size

Transformer shows a _“black hole”_ pattern in Leave-Square-Out testing, where its accuracy drops to nearly zero on unseen data, confirming that it might not be using rule-based reasoning for mathematical problem-solving.

However, tests on FANformer tell something different.

No obvious “ _black hole_ ” is seen in the test figures, which tells that they learn the underlying mathematical rules for problem-solving and, thus, perform better.

Press enter or click to view image in full size

Performance of FANformer and Transformer on Modular Addition and Linear Regression tasks

_It’s surprising how explicitly encoding periodicity-capturing capabilities in the deep neural network/ Transformer architecture can make it so powerful._

_Although many further experiments on FANformers are required, it would be exciting to see them used in the powerful LLMs of the future._

## Further Reading

* [Research paper titled ‘FANformer: Improving Large Language Models Through Effective Periodicity Modeling’ published in ArXiv](<https://www.arxiv.org/abs/2502.21309>)
* [Research paper titled ‘FAN: Fourier Analysis Networks’ published in ArXiv](<https://arxiv.org/abs/2410.02675>)
* [Research paper titled ‘OLMo: Accelerating the Science of Language Models’ published in ArXiv](<https://arxiv.org/abs/2402.00838v1>)
* [Author’s article titled ‘Fourier Analysis Networks (FANs) Are Here To Break Barriers In AI’ published in ‘Into AI’](<https://intoai.pub/p/fourier-analysis-networks-fans-are>)

## Source Of Images

All images are obtained from the [original research paper](<https://www.arxiv.org/abs/2502.21309>) unless stated otherwise.

[**_Subscribe to ‘Into AI’ — my weekly newsletter where I help you explore Artificial Intelligence from the ground up by dissecting the original research papers._**](<https://intoai.pub/>)

Press enter or click to view image in full size

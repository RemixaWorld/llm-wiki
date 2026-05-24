---
domain: blog.stackademic.com
fetch_date: '2026-05-18T12:46:05.104466'
status: ok
url: https://blog.stackademic.com/galore-memory-efficient-pre-training-for-llms-9f4c0427b1b7
---

# GaLore: Memory-Efficient Pre-training for LLMs

# **GaLore: Memory-Efficient Pre-training for LLMs**

## It also works for fine-tuning

[ ![Benjamin Marie](https://miro.medium.com/v2/resize:fill:64:64/1*sifLT7ybERpQ7SnaPwBDBQ.png) ](<https://medium.com/@bnjmn_marie?source=post_page---byline--9f4c0427b1b7--------------------------------------->)

[Benjamin Marie](<https://medium.com/@bnjmn_marie?source=post_page---byline--9f4c0427b1b7--------------------------------------->)

2 min read

·

Mar 12, 2024

\--

Listen

Share

More

For fine-tuning, LoRA has not achieved the performance levels of full-rank fine-tuning. It can, but often LoRA won’t be as good as full fine-tuning. For pre-training from scratch with LoRA, previous work, e.g., ReLoRA, has shown that LoRA necessitates initial full-rank model training, which serves as a warm-up before transitioning to optimization within a low-rank subspace. This limitation could be because optimal weight matrices may inherently not be low-rank or that reparameterization alters the gradient training dynamics.

## [ReLoRa: Pre-train a Large Language Model on Your GPULoRa but with multiple resets in a rowkaitchup.substack.com](<https://kaitchup.substack.com/p/relora-pre-train-a-large-language?source=post_page-----9f4c0427b1b7--------------------------------------->)

To overcome these challenges, a new work introduces Gradient Low-rank Projection (GaLore), a new approach enabling full-parameter learning while being more memory-efficient than traditional low-rank adaptation methods, like LoRA:

[**GaLore: Memory-Efficient LLM Training by Gradient Low-Rank Projection**](<https://arxiv.org/abs/2403.03507>)

GaLore focuses on exploiting the inherently low-rank structure of weight matrix gradients over time. It achieves this by applying two projection matrices to transform the gradient matrix into a low-rank form, thus significantly reducing memory usage associated with optimizer states. This method allows for occasional, computationally inexpensive updates to the projection matrices, offering up to 30% memory savings during pre-training compared to LoRA.

[source](<https://arxiv.org/abs/2403.03507>) (CC-BY)

GaLore seems to be effective in both pre-training and fine-tuning. For example, pre-training a LLaMA-style 7B model on the C4 dataset with GaLore, alongside 8-bit optimization techniques, matches the performance of full-rank methods with substantially less memory — enabling such training on a single 24GB GPU without external memory offloading.

Additionally, when applied to fine-tune models on tasks like the GLUE benchmarks, GaLore outperforms other low-rank methods, including LoRA, in terms of average score.

As a gradient projection strategy, GaLore is compatible with a variety of optimizers and requires minimal code to integrate.

The official implementation of this “work in progress” is available here:

* GitHub: [jiaweizzhao/GaLore](<https://github.com/jiaweizzhao/GaLore>)

This article is a short paper review from The Salt. For weekly reviews of recent advances in AI, consider subscribing to The Salt:

## [The Salt - Curated AI | Benjamin Marie | SubstackThe Salt offers weekly reviews and in-depth analyses of the latest AI papers. If you want to stay informed of recent…thesalt.substack.com](<https://thesalt.substack.com/?source=post_page-----9f4c0427b1b7--------------------------------------->)

## Stackademic 🎓

Thank you for reading until the end. Before you go:

* Please consider **clapping** and **following** the writer! 👏
* Follow us [**X**](<https://twitter.com/stackademichq>)**|**[**LinkedIn**](<https://www.linkedin.com/company/stackademic>)**|**[**YouTube**](<https://www.youtube.com/c/stackademic>)**|**[**Discord**](<https://discord.gg/in-plain-english-709094664682340443>)
* Visit our other platforms: [**In Plain English**](<https://plainenglish.io>)**|**[**CoFeed**](<https://cofeed.app/>)**|**[**Venture**](<https://venturemagazine.net/>)**|**[**Cubed**](<https://blog.cubed.run>)
* More content at [**Stackademic.com**](<https://stackademic.com>)

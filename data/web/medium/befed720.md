---
domain: medium.com
fetch_date: '2026-05-18T12:49:57.349683'
status: ok
url: https://medium.com/@florian_algo/ai-innovations-and-trends-02-visrag-graphrag-raglab-and-more-84598513d947
---

# AI Innovations and Trends 02: VisRAG, GraphRAG, RAGLAB, and More

[ ![Florian June](https://miro.medium.com/v2/resize:fill:64:64/1*DmQ3DH2JeAJquvhT_tjVCw.jpeg) ](<https://medium.com/@florian_algo?source=post_page---byline--84598513d947--------------------------------------->)

[Florian June](<https://medium.com/@florian_algo?source=post_page---byline--84598513d947--------------------------------------->)

6 min read

·

Nov 11, 2024

\--

\--

Listen

Share

More

![image](https://miro.medium.com/v2/resize:fit:700/1*Hlx0RliTqaZJN6EK-mn3pw.jpeg)

This article is the second in this series. Today we will look at five advancements in AI, which are:

* VisRAG: Farewell to Document Parsing
* Graph RAG: A Survey
* RAGLAB: A Modular and Research-Oriented Unified Framework for RAG
* rerankers: A Lightweight Python Library to Unify Ranking Methods
* Quantized Llama 3.2 Models (1B and 3B)

## VisRAG: Farewell to Document Parsing

> ** _Open source code_** _:_[_https://github.com/openbmb/visrag_](<https://github.com/openbmb/visrag>)

As shown in Figure 1, traditional text-based RAG (TextRAG) relies on parsed texts for retrieval and generation, losing visual information in multimodal documents. In contrast, [Vision-based RAG (VisRAG)](<https://arxiv.org/pdf/2410.10594v1>) uses a VLM-based retriever and generator to directly process the document page’s image. This approach preserves all information from the original page.

![Figure 1: TextRAG (left) vs. VisRAG (right). Source: VisRAG.](https://miro.medium.com/v2/resize:fit:700/0*KKJsk3npeM6h-qbp.png)

### Retrieval Stage

* **Task** : To retrieve relevant pages from a corpus based on a user query, enabling accurate information augmentation for generation.
* **Dual-Encoder Paradigm** : Uses a VLM rather than an LLM to map the query and document page images into the same embedding space for similarity calculation.
* **Vision-Language Model (VLM)** : Encodes document pages as images directly, preserving visual and textual information without text parsing.
* **Similarity Scoring** : Computes cosine similarity between the query and page embeddings to select the most relevant pages.

### Generation Stage

* **Task** : To generate an accurate and contextually enriched response based on the user query and retrieved pages.
* **Single-Image and Multi-Image Handling** : For VLMs accepting single images, VisRAG applies **page concatenation** or **weighted selection** methods to combine information from multiple retrieved pages. For VLMs supporting multi-image input, VisRAG leverages these models directly to process all retrieved pages together.
* **Weighted Selection** : Calculates the answer confidence across multiple pages, selecting the response with the highest weighted probability.

### Comments and Insights

VisRAG is a multi-modal RAG approach that eliminates the document parsing stage, thereby preserving comprehensive information for retrieval and generation.

While VisRAG demonstrates many advantages, it also presents challenges, particularly regarding computational resource requirements. Directly processing images requires powerful VLMs and significant computational support. Additionally, the approach’s dependency on model and data scale may require further adjustments for wider adoption in other domains.

## Graph RAG: A Survey

This survey provides a systematic introduction to Graph RAG and its key components.

While RAG improves on LLMs by retrieving relevant text, it still falls short in capturing deep relational knowledge, leading to incomplete answers.

As shown in Figure 2, GraphRAG addresses this issue by leveraging the structural information inherent in graphs, enabling more precise and contextually aware responses.

![Figure 2. Comparision between Direct LLM, RAG, and GraphRAG. Given a user query, direct answering by LLMs may suffer from shallow responses or lack of specificity. RAG addresses this by retrieving relevant textual information, somewhat alleviating the issue. However, due to the text’s length and flexible natural language expressions of entity relationships, RAG struggles to emphasize “influence” relations, which is the core of the question. While, GraphRAG methods leverage explicit entity and relationship representations in graph data, enabling precise answers by retrieving relevant structured information. Source: Graph Retrieval-Augmented Generation: A Survey.](https://miro.medium.com/v2/resize:fit:700/0*EQAO6fGAsMZOxQOF.png)

GraphRAG is a novel approach that combines the strengths of RAG with the robustness of graph-based data structures. By retrieving graph elements such as nodes, triples, paths, and subgraphs, GraphRAG enriches LLM outputs with relational knowledge, ensuring more accurate and comprehensive answers.

![Figure 3. The overview of the GraphRAG framework for question answering task. Source: Graph Retrieval-Augmented Generation: A Survey.](https://miro.medium.com/v2/resize:fit:700/0*HyVMhyp3d71fYiOJ.png)

The workflow of GraphRAG, as depicted in **Figure 3** , is divided into three key stages:

* **Graph-Based Indexing (G-Indexing):** This stage involves constructing or selecting a graph database relevant to the downstream tasks, indexing it for efficient retrieval.
* **Graph-Guided Retrieval (G-Retrieval):** Here, the system retrieves the most pertinent graph elements based on a given query.
* **Graph-Enhanced Generation (G-Generation):** Finally, the retrieved graph data is used to generate responses that are both accurate and contextually rich.

## RAGLAB: A Modular and Research-Oriented Unified Framework for RAG

> ** _Open source code_** _:_[_https://github.com/fate-ubw/RAGLab_](<https://github.com/fate-ubw/RAGLab>)

Two key issues have hindered the development of RAG. First, there’s a growing lack of comprehensive and fair comparisons among novel RAG algorithms. Second, open-source tools like LlamaIndex and LangChain use high-level abstractions, resulting in reduced transparency and limiting the ability to develop new algorithms and evaluation metrics.

[RAGLAB](<https://arxiv.org/pdf/2408.11381v2>) is a modular, research-oriented open-source library designed to close this gap.

![Figure 4: Architecture and Components of the RAGLAB Framework. Source: RAGLAB.](https://miro.medium.com/v2/resize:fit:700/0*ZBFUvng86W6Y-sWi.png)

Figure 5 is a comparison between RAGLAB and some existing RAG frameworks.

![Figure 5: Comparison of Different RAG Libraries and Frameworks. Fair Comparison refers to aligning all fundamental components during evaluation, including random seeds, generator, retriever, and instructions. Data Collector refers to the ability to gather or generate training and test data, either by sampling from existing raw datasets or by constructing labeled data using LLMs. Source: RAGLAB.](https://miro.medium.com/v2/resize:fit:700/0*wnOnauj-Dp9hAS4y.png)

### Comments and Insights

RAGLAB has some limitations:

1. Limited Number of Algorithms and Datasets
2. Lack of Diversity in Knowledge Bases
3. Lack of a User-Friendly Graphical Interface

These limitations can be gradually addressed in future versions by expanding algorithms, increasing datasets, and optimizing resource efficiency to meet broader research and application needs.

## rerankers: A Lightweight Python Library to Unify Ranking Methods

> ** _Open source code_** _:_[_https://github.com/answerdotai/rerankers_](<https://github.com/answerdotai/rerankers>)

We know that reranking is a crucial component in information retrieval and RAG, typically employed after the initial retrieval of candidate documents. It uses stronger models — often neural networks — to reorder these documents, thereby enhancing retrieval quality.

The [rerankers library](<https://arxiv.org/pdf/2408.17344v2>) is a lightweight Python tool that unifies various reranking methods. It offers a standardized interface for loading and using different reranking techniques, allowing users to switch between methods by changing just one line of Python code.

```python from rerankers import Reranker# Cross-encoder default. You can specify a 'lang' parameter to load a multilingual version!ranker = Reranker('cross-encoder')# Specific cross-encoderranker = Reranker('mixedbread-ai/mxbai-rerank-large-v1', model_type='cross-encoder')# FlashRank default. You can specify a 'lang' parameter to load a multilingual version!ranker = Reranker('flashrank')# Specific flashrank model.ranker = Reranker('ce-esci-MiniLM-L12-v2', model_type='flashrank')# Default T5 Seq2Seq rerankerranker = Reranker("t5")# Specific T5 Seq2Seq rerankerranker = Reranker("unicamp-dl/InRanker-base", model_type = "t5")# API (Cohere)ranker = Reranker("cohere", lang='en' (or 'other'), api_key = API_KEY)# Custom Cohere model? No problem!ranker = Reranker("my_model_name", api_provider = "cohere", api_key = API_KEY)...... ```

## Quantized Llama 3.2 Models (1B and 3B)

Meta AI released its first lightweight [quantized Llama models](<https://ai.meta.com/blog/meta-llama-quantized-lightweight-models/>) that are small and performant enough to run on many popular mobile devices.

They primarily used two techniques for quantizing Llama 3.2 1B and 3B models: Quantization-Aware Training with LoRA adaptors, which prioritizes accuracy, and SpinQuant, a state-of-the-art post-training quantization method that prioritizes portability.

![Figure 6: Comparison of quantization methods. Source: Quantized Llama models.](https://miro.medium.com/v2/resize:fit:700/0*k2Gle0wH6i3LWVpG.png)

As the first quantized models in this Llama category, these instruction-tuned models maintain the same quality and safety standards as the original 1B and 3B models while achieving a 2–4x speedup. Additionally, compared to the original BF16 format, they achieve an average 56% reduction in model size and a 41% reduction in memory usage.

## In Plain English 🚀

_Thank you for being a part of the_[** _In Plain English_**](<https://plainenglish.io/>) _community! Before you go:_

* Be sure to **clap** and **follow** the writer ️👏**️️**
* Follow us: [**X**](<https://x.com/inPlainEngHQ>) | [**LinkedIn**](<https://www.linkedin.com/company/inplainenglish/>) | [**YouTube**](<https://www.youtube.com/channel/UCtipWUghju290NWcn8jhyAw>) | [**Discord**](<https://discord.gg/in-plain-english-709094664682340443>) | [**Newsletter**](<https://newsletter.plainenglish.io/>) | [**Podcast**](<https://open.spotify.com/show/7qxylRWKhvZwMz2WuEoua0>)
* [**Create a free AI-powered blog on Differ.**](<https://differ.blog/>)
* More content at [**PlainEnglish.io**](<https://plainenglish.io/>)

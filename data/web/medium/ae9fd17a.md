---
domain: ai.gopubby.com
fetch_date: '2026-05-18T12:48:18.074736'
status: ok
url: https://ai.gopubby.com/ai-search-engine-finding-ariadnes-thread-or-losing-the-way-ab8d446d0715
---

# AI Search Engine: Finding Ariadne’s Thread or Losing the Way

## |AI|LLM|WEB SEARCH|AI SEARCH ENGINE|

# AI Search Engine: Finding Ariadne’s Thread or Losing the Way

## Exploring the Pathways and Pitfalls of Multimodal AI Search with Large Language Models

[ ![Salvatore Raieli](https://miro.medium.com/v2/resize:fill:64:64/1*cs7O1sBNbybTazY4AtBwig.jpeg) ](<https://salvatore-raieli.medium.com/?source=post_page---byline--ab8d446d0715--------------------------------------->)

[Salvatore Raieli](<https://salvatore-raieli.medium.com/?source=post_page---byline--ab8d446d0715--------------------------------------->)

8 min read

·

Sep 24, 2024

\--

Listen

Share

More

Press enter or click to view image in full size

image created by the author using AI

> If you do not expect the unexpected you will not find it, for it is not to be reached by search or trail. — Heraclitus

[Search engines](<https://en.wikipedia.org/wiki/Search_engine>) are the most effective means of navigating the endless resources on the Internet, and [every day billions of people](<https://www.statista.com/topics/1710/search-engine-usage/>) use at least one. Over the past two decades, the algorithms used for search engines have not changed much. Recently, however, [Large Language Models (LLMs)](<https://github.com/SalvatoreRa/tutorial/blob/main/artificial%20intelligence/FAQ.md#:~:text=What%20is%20a%20Large%20Language%20Model%20\(LLM\)%3F>) have shown incredible capabilities even for tasks for which they are not trained. Therefore, it has been thought that they could be used for the next generation of search engines or even completely change our interactions with the Internet itself.

## [A Requiem for the Transformer?Will be the transformer the model leading us to artificial general intelligence? Or will be replaced?towardsdatascience.com](<https://towardsdatascience.com/a-requiem-for-the-transformer-297e6f14e189?source=post_page-----ab8d446d0715--------------------------------------->)

AI search engines would have the advantage of better understanding user intent and search context. They could at the same time summarize the information found and allow for much more interactive use. At the same time, LLMs have a limitation: they can only answer textual questions and interpret only textual content. Today, however, the Internet is also populated with so many other modalities (images, audio, video, and so on) so this is a serious limitation. [Multimodal](<https://en.wikipedia.org/wiki/Multimodality>) searches are more common than one thinks: we search for videos, images, and songs.

## [BLIP-2: when ChatGPT meets imagesBLIP-2, a new visual language model capable to dialogue about imageslevelup.gitconnected.com](<https://levelup.gitconnected.com/blip-2-when-chatgpt-meets-images-463582b541e0?source=post_page-----ab8d446d0715--------------------------------------->)

Although this is a limitation of [LLMs](<https://en.wikipedia.org/wiki/Large_language_model>), recent research has been concerned with extending these patterns. Indeed, there are models that are multimodal and can therefore answer queries on images or other modalities. Although we have these multimodal models they have not yet been applied to Internet search.

> **Can we use LLM for internet searches? also for multimodal search?**

There are already companies that offer internet searches using LLM. For example, Perplexity, but also [OpenAI is testing the possibility of conducting the search](<https://www.theverge.com/2024/7/25/24205701/openai-searchgpt-ai-search-engine-google-perplexity-rival>) with ChatGPT (currently [SearchGPT is a prototype](<https://openai.com/index/searchgpt-prototype/>)). In addition, it is possible to add Internet search to an LLM as a tool. For the second question, a recently published paper presents how you can conduct the multimodal search.

## [MMSearch: Benchmarking the Potential of Large Models as Multi-modal Search EnginesThe advent of Large Language Models (LLMs) has paved the way for AI search engines, e.g., SearchGPT, showcasing a new…arxiv.org](<https://arxiv.org/abs/2409.12959?source=post_page-----ab8d446d0715--------------------------------------->)

At the heart of the pipeline is an LLM that interacts with conventional search engines (multiple times until the task is solved). The authors in this case also include [Google Lens](<https://it.wikipedia.org/wiki/Google_Lens>) to search for information for images. Also, the system can take screenshots of found sites to preserve the original format. The process consists of three steps:

* **Requery**. The user can search with an image and/or add information. The query is reformulated to be clearer, less ambiguous, and more efficient. The [rewritten text query](<https://en.wikipedia.org/wiki/Query_rewriting>) is searched in a search engine, and if there is an image this is searched on Google Lens.
* **Rerank**. The top K relevant sites are found, then LLM is used to select the most useful sites to conduct a synthetic response. To avoid filling the context length of the model it is given only some information and a screenshot of the site (to allow the model to analyze the reliability and credibility of the site).
* **Summarization**. authors conduct crawling of the sites that are chosen, and information and screenshots of the website are recuperated. Since the content is too long and full of irrelevant information, they add a text embedding model to find a maximum of 2K. After that, they give the information to the LLM and generate a response

Press enter or click to view image in full size

image source: [here](<https://arxiv.org/pdf/2409.12959>)

At this point, the authors also create a benchmark in order to conduct multimodal search capabilities. This benchmark consists of two parts: News and Knowledge. In this way, authors can test for both breaking news (information that is not known by the LLM and that the model should search online) and rare knowledge (information that is in particular domains and that the model should not know without a search). So the authors want to test the models’ capabilities on search capabilities. In fact, the models have a parametric memory and this can be used by the model to respond when the answer is not provided in context.

Press enter or click to view image in full size

image source: [here](<https://arxiv.org/pdf/2409.12959>)

The authors also decide to evaluate the search throughout the process, that is, they create a metric for each of the steps. In fact, the model may respond incorrectly because it does not find the information or hallucinates during the process:

* end-to-end score (Se2e).
* Requery score (Sreq).
* Rerank score.
* Summarization score (Ssum).

Press enter or click to view image in full size

image source: [here](<https://arxiv.org/pdf/2409.12959>)

Plus they add an end-to-end score that takes all these various components into account.

The authors at this point decide to make a comparison between different models and settings:

* Commercial AI Search Engines. compare their approach with [Perplexity](<https://en.wikipedia.org/wiki/Perplexity_AI>).
* Closed-source LMMs. they use both GPT4 and Claude.
* Open-source LMMs. use a number of different open-source models of different sizes.

The authors use the models as-is without conducting fine-tuning or additional training.

This is an example of a query:

Press enter or click to view image in full size

image source: [here](<https://arxiv.org/pdf/2409.12959>)

The authors note some interesting results:

* Current LMMs still have significant shortcomings in requery and rerank.
* Current models need improvements especially for rerank and requery step. While they perform better for summarization. Closed-source LLMs are more capable than open sources. In fact these models show better zero-shot multimodal search capabilities.
* The use of LLMs outperforms commercial AI search engines. Although Perplexity actually uses GPT-4o and Claude 3.5 Sonnet, the pipeline is superior in multimodal search. The problem seems to stem from how it handles image searches.

Press enter or click to view image in full size

image source: [here](<https://arxiv.org/pdf/2409.12959>)

The authors then analyze the errors that have happened:

* GPT4 fails mostly in reranking and integrating modalities. Open-source models also fail during website summarization.
* Errors can still occur throughout the entire pipeline. For example, the model may create queries that are not specific, ignore information in images, fail to extract information from context, and so on.

Press enter or click to view image in full size

image source: [here](<https://arxiv.org/pdf/2409.12959>)

> In this paper, we investigate the potential of LMMs as multimodal AI search engines. We first design MMSEARCH-ENGINE, a streamlined pipeline, enabling zero-shot LMMs to perform multimodal searches. To comprehensively assess the search capabilities, we introduce MMSEARCH, a benchmark comprising 300 queries across 14 subfields. — [source](<https://arxiv.org/pdf/2409.12959>)

Clearly there are still limits to the capabilities of an LLM and to use it for Internet research. Especially with [multimodal models](<https://www.kdnuggets.com/2023/03/multimodal-models-explained.html>), there are still problems in efficiently integrating the various modalities. It can be clearly seen from the error analysis that the models are unable to efficiently rewrite queries, ignore images, or fail to extract information from images. So there are still problems in handling irrelevant information. Hallucinations are still a problem for LLMs, and there still needs to be research on the topic. The analysis also shows that the models are not very capable in either rerequery or reranking. Experience with [RAG](<https://github.com/SalvatoreRa/tutorial/blob/main/artificial%20intelligence/FAQ.md#:~:text=Retrieval%20Augmented%20Generation%20\(RAG\),-What%20is%20Retrieval>) teaches us that small, specialized models can be used for these tasks. This could solve the problem.

## [RAG is Dead, Long Live RAGIs it really true that long-context LLMs are killing the RAG?levelup.gitconnected.com](<https://levelup.gitconnected.com/rag-is-dead-long-live-rag-c607e1799199?source=post_page-----ab8d446d0715--------------------------------------->)

## [Sometimes Noise is Music: How Beneficial Noise Can Improve Your RAGUnveiling the Dual Nature of Noise in Retrieval-Augmented Generationlevelup.gitconnected.com](<https://levelup.gitconnected.com/sometimes-noise-is-music-how-beneficial-noise-can-improve-your-rag-b9d67253500f?source=post_page-----ab8d446d0715--------------------------------------->)

Also, while the gap between closed-source and open-source LLMs has almost closed for text capabilities, closed-source LLMs are still superior for multimodal capabilities.

One interesting result is that with a purpose-built pipeline, one can beat commercially available services. The code for those interested is [**here**](<https://github.com/CaraJ7/MMSearch>).

### What are your thoughts on this? Curious to try it out? Let me know in the comments.

## If you have found this interesting:

_You can look for my other articles, and you can also connect or reach me on_** __**[**_LinkedIn_**](<https://www.linkedin.com/in/salvatore-raieli/>)** _._**_Check_[** _this repository_**](<https://github.com/SalvatoreRa/ML-news-of-the-week>) _containing weekly updated ML & AI news. _**_I am open to collaborations and projects_** _and you can reach me on LinkedIn. You can also_[ _subscribe for free_](<https://salvatore-raieli.medium.com/subscribe>) _to get notified when I publish a new story._

## [Get an email whenever Salvatore Raieli publishes.Get an email whenever Salvatore Raieli publishes. By signing up, you will create a Medium account if you don’t already…salvatore-raieli.medium.com](<https://salvatore-raieli.medium.com/subscribe?source=post_page-----ab8d446d0715--------------------------------------->)

_Here is the link to my GitHub repository, where I am collecting code and many resources related to machine learning, artificial intelligence, and more._

## [GitHub — SalvatoreRa/tutorial: Tutorials on machine learning, artificial intelligence, data science…Tutorials on machine learning, artificial intelligence, data science with math explanation and reusable code (in python…github.com](<https://github.com/SalvatoreRa/tutorial?source=post_page-----ab8d446d0715--------------------------------------->)

_or you may be interested in one of my recent articles:_

## [Through the Uncanny Mirror: Do LLMs Remember Like the Human Mind?Exploring the Eerie Parallels and Profound Differences Between AI and Human Memorytowardsdatascience.com](<https://towardsdatascience.com/through-the-uncanny-mirror-do-llms-remember-like-the-human-mind-cc9c63677610?source=post_page-----ab8d446d0715--------------------------------------->)

## [To CoT or Not to CoT: Do LLMs Really Need Chain-of-Thought?Looking for Reasoning in LLMs: Is Chain-of-Thought Really the Key to Smarter AI?levelup.gitconnected.com](<https://levelup.gitconnected.com/to-cot-or-not-to-cot-do-llms-really-need-chain-of-thought-5a59698c90bb?source=post_page-----ab8d446d0715--------------------------------------->)

## [OpenAI’s New ‘Reasoning’ AI Models Arrived: Will They Survive the Hype?Will the Captain Catch the Whale of Reasoning or Sink in the Pursuitlevelup.gitconnected.com](<https://levelup.gitconnected.com/openais-new-reasoning-ai-models-arrived-will-they-survive-the-hype-a55c582363b9?source=post_page-----ab8d446d0715--------------------------------------->)

## [AI Won’t Steal Your Job — But Get Ready for the World’s Most Annoying CoworkerHow AI Assistants Are Boosting Productivity While Becoming the Overachievers of the Officeai.gopubby.com](</ai-wont-steal-your-job-but-get-ready-for-the-world-s-most-annoying-coworker-6a2efb39cf5f?source=post_page-----ab8d446d0715--------------------------------------->)

## Reference

Here is the list of the principal references I consulted to write this article, only the first name for an article is cited.

1. Jiang, 2024, MMSearch: Benchmarking the Potential of Large Models as Multi-modal Search Engines, [link](<https://arxiv.org/abs/2409.12959>)
2. Barbany, 2024, Leveraging large language models for multimodal search, [link](<https://arxiv.org/abs/2404.15790>)
3. Bechard, 2024, Reducing hallucination in structured outputs via ´ retrieval-augmented generation, [link](<https://arxiv.org/abs/2404.08189>)
4. Brin, 1998, The anatomy of a large-scale hypertextual web search engine, [link](<https://snap.stanford.edu/class/cs224w-readings/Brin98Anatomy.pdf>)
5. Chen, 2024, How far are we to gpt-4v? closing the gap to commercial multimodal models with open-source suites, [link](<https://arxiv.org/abs/2404.16821>)

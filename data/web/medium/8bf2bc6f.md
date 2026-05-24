---
domain: levelup.gitconnected.com
fetch_date: '2026-05-18T12:47:31.634184'
status: ok
url: https://levelup.gitconnected.com/the-convergence-of-graph-and-vector-rags-a-new-era-in-information-retrieval-b5773a723615
---

# The Convergence of Graph and Vector RAGs: A New Era in Information Retrieval

## |LLM|RAG|GRAPH| PERSPECTIVE|

# The Convergence of Graph and Vector RAGs: A New Era in Information Retrieval

## Harnessing the Power of Hybrid Models to Transform AI-Driven Knowledge Systems

[ ![Salvatore Raieli](https://miro.medium.com/v2/resize:fill:64:64/1*cs7O1sBNbybTazY4AtBwig.jpeg) ](<https://salvatore-raieli.medium.com/?source=post_page---byline--b5773a723615--------------------------------------->)

[Salvatore Raieli](<https://salvatore-raieli.medium.com/?source=post_page---byline--b5773a723615--------------------------------------->)

9 min read

·

Sep 2, 2024

\--

Listen

Share

More

Press enter or click to view image in full size

image created by the author using AI

> What the caterpillar calls the end of the world the master calls a butterfly. — Richard Bach

[Large Language Models (LLMs)](<https://github.com/SalvatoreRa/tutorial/blob/main/artificial%20intelligence/FAQ.md#:~:text=What%20is%20a%20Large%20Language%20Model%20\(LLM\)%3F>) have been a new spark for interest in artificial intelligence, especially natural language processing. On the other hand, though, LLMs are not without their limitations. This is especially because LLMs do not reason and can easily generate hallucinations. Precisely because LLMs can hallucinate easily new paradigms have evolved that can limit this unintended behavior. [Retrieval-Augmented Generation (RAG)](<https://github.com/SalvatoreRa/tutorial/blob/main/artificial%20intelligence/FAQ.md#:~:text=What%20is%20Retrieval%20Augmented%20Generation%20\(RAG\)%3F>) is the one ch has been most successful. In this case, LLMs are provided with an external memory that allows them to retrieve a context and then be able to use it for generation

## [A Requiem for the Transformer?Will be the transformer the model leading us to artificial general intelligence? Or will be replaced?towardsdatascience.com](<https://towardsdatascience.com/a-requiem-for-the-transformer-297e6f14e189?source=post_page-----b5773a723615--------------------------------------->)

## [RAG is Dead, Long Live RAGIs it really true that long-context LLMs are killing the RAG?levelup.gitconnected.com](</rag-is-dead-long-live-rag-c607e1799199?source=post_page-----b5773a723615--------------------------------------->)

Of course, RAG is not without its flaws either, especially in real-world case scenarios:

* **Neglecting relationships**. RAG fails to capture knowledge relationships that cannot be represented through semantic similarity alone.
* **Redundant information**. LLMs have a problem when there is too much noise in the context and the RAG can find different irrelevant contexts which then hurts the generation.
* **Lacking global information**. The RAG finds a subset of documents but fails to report global information.

Press enter or click to view image in full size

image source: [4]

[Knowledge graphs](<https://en.wikipedia.org/wiki/Knowledge_graph>) (KGs) can instead bring a different point of view. A document in a [KG](<https://www.ibm.com/topics/knowledge-graph>) is a set of relationships among its entities, and these entities can then be interconnected to those in other documents. In other words, we extract only the relationships between various entities and thus have a global approach.

image source: [3]

> The primary advantage of KGs lies in their ability to offer a structured representation, which facilitates efficient querying and reasoning. — [source](<https://arxiv.org/pdf/2408.04948>)

KGs are not without problems:

> However, building and maintaining KGs and integrating data from different sources, such as documents, news articles, and other external sources, into a coherent knowledge graph poses significant challenges. — [source](<https://arxiv.org/pdf/2408.04948>)

In recent times this has been simplified thanks to LLMs. In fact, [LLMs can extract information from text](<https://neo4j.com/developer-blog/knowledge-graphs-llms-multi-hop-question-answering/>) and render it in a desired format. Therefore, several works have focused on using an LLM to populate a knowledge graph. This KG is then used for various analyses to extract entities and relationships that can be used for downstream tasks.

image source: [2]

Once more and more complete KGs were created, people began to think about being able to use these KGs to provide context to LLMs. [Graph Retrieval-Augmented Generation](<https://www.deeplearning.ai/short-courses/knowledge-graphs-rag/>) (GraphRAG) is an innovative solution that has begun to take hold in recent months. In this article, we will discuss what it is, how it works, and look in a little more detail at two particular cases.

Press enter or click to view image in full size

image source: [1]

> GraphRAG is a framework that leverages external structured knowledge graphs to improve contextual understanding of LMs and generate more informed responses — [source](<https://arxiv.org/pdf/2408.08921>)

KG can be used throughout the RAG pipeline:

* **Graph-Based Indexing (G-Indexing).** Typically, the goal is to constitute indexing that is tailored to the downstream tasks (retrieval and generation).
* **Graph-Guided Retrieval (G-Retrieval).** In response to a query, we need to be able to extract entities and relationships to answer a user’s query.
* **Graph-Enhanced Generation (G-Generation).** In this phase, triplets are used by the LLM to generate an answer, and the goal is to optimize the use of these triplets to generate an accurate answer.

Typically, many organizations today have a proprietary KG, and this can be the basis for creating a graphRAG pipeline. Alternatively as mentioned, you can use an LLM to extract entities and relationships from text. These entities and relationships are then used to build the KG.

GraphRAG has several applications, especially in those domains that are rich in entities. For example, E-commerce where we have historical information about the behavior of users and the products they buy. This information can be easily modeled in graph (and thus KG) form. In any case, KGs are used in biomedical, literature, academia, and legal fields.

In a previous article, we discussed [GraphRAG](<https://github.com/microsoft/graphrag>) (by Microsoft). This approach uses an LLM to build the KGs and then generate summaries. This system has sparked community interest but is inherently expensive (many LLM calls).

## [GraphRAG: Combining Retrieval and SummarizationEnhancing Large Language Models for Complex Question Answering over Extensive Text Corporalevelup.gitconnected.com](</graphrag-combining-retrieval-and-summarization-9262ff312d98?source=post_page-----b5773a723615--------------------------------------->)

Instead, in this article we will discuss two different approaches that are more focused and have a specific domain interest. At the same time, the systems of the future will be more like these proposals than the model proposed by Microsoft.

In the specialized domains (finance, law, and medicine) there are three main challenges for LLMs: long context, the excessive cost of [fine-tuning](<https://github.com/SalvatoreRa/tutorial/blob/main/artificial%20intelligence/FAQ.md#:~:text=What%20is%20transfer%20learning%3F>), and hallucinations. RAG in theory solves all three. In reality, when handling sensitive medical data it is of utter importance that the response generated is reliable and evidence-based. LLMs and RAG continue to generate hallucinations that lead to safety concerns.

Medical Graph RAG seeks to address the limitations of RAG with a Graph RAG approach (improving citation finding, interpretation of medical terms, interpretability, and transparency). To do this, the authors use a three-tier hierarchical graph:

> Initially, we use documents provided by users as our top-level source to extract entities. These entities are then linked to a second level consisting of more basic entities previously abstracted from credible medical books and papers. Subsequently, these entities are connected to a third level — the fundamental medical dictionary graph — that provides detailed explanations of each medical term and their semantic relationships. — [source](<https://arxiv.org/pdf/2408.04187>)

Press enter or click to view image in full size

image source: [5]

The authors use a hybrid static-semantic approach for chunking (to make sure they can conduct a detecting the topic change in the document). They then use a prompt to extract the entities in the document (which they then assign a unique ID for tracking). They then begin connecting the various entities across levels (this is to be sure that the system uses specific terminology such as disease symptoms or side effects). At this point, they begin to link the various entities together (horizontal edges in the level). They then join various subgraphs generated per document, adding tags to keep the origin and search better successively. The tag is a kind of summary that is then utilized to provide a better overview of the model

To conduct retrieval they use U-retrieve, finding the most relevant subgraphs. They then find the entities and related ones and provide them to the LLM to generate the response. In this context, the tag is added. This hybrid static-semantic approach. It is also superior to the effect of fine-tuning and according to the authors, surpasses the accuracy of human experts. This shows potential use in clinical workflows.

image source: [5]

Classical RAG is also called vector RAG, and now we have seen how graph RAG can be a potential substitute.

> But do they have to be antagonistic? Can’t they work in synergy?

In this study, they propose HybridRAG in which both vector RAG and graph RAG are used. Again, this is a solution for a specialized domain where heterogeneous data sources are used. KG is useful to be able to store them and use them for predictive models, thus creating a comprehensive view of financial entities and their relationships. On the other hand, KG is a reductivist view that loses many of the nuances of relationships.

> GraphRAG enables more accurate and context-aware generation of responses based on the structured information extracted from financial documents. But GraphRAG generally underperforms in abstractive Q&A tasks or when there is not explicit entity mentioned in the question — [source](<https://arxiv.org/pdf/2408.04948>)

Combining these two systems is possible, and they can be seen as two complementary components:

> The VectorRAG component provides a broad, similarity-based retrieval of relevant information, while the GraphRAG element contributes structured, relationship-rich contextual data — [source](<https://arxiv.org/pdf/2408.04948>)

The authors then divide the documents into chunks and use a language model to extract the information of interest and their relationships (companies, financial metrics and indicators, corporate executives, products, geographical executives, and even regulations). In this way, they create their financial KG. As they point out in the article, the process then requires additional steps to improve consistency, disambiguate entities, and so on. At the same time, they create a vector RAG and conduct chunking and embedding.

At query time they search both the KG and the vector database, then concatenate the results of the two models and provide them to an LLM for generation.

> HybridRAG’s superior performance in faithfulness, answer relevancy, and context recall underscores its effectiveness. — [source](<https://arxiv.org/pdf/2408.04948>)

The system thus shows that it takes the best of both worlds. Future systems will probably use a hybrid approach. In this work, they combined the two frameworks in a brute-force way. But in the future, there will surely be more elegant alternatives for combining graph Rag and vector RAG.

At the same time, MedRAG shows us how KG can be used in a refined way and how it is flexible (building various layers, extracting subgraphs, adding tags, and so on). Probably the systems of the future will be hybrid, but RAGs for specialized systems will have extremely specialized and multi-level KG to control the information and breath of the context taken.

### What do you think? curious to try these systems? let me know in the comments

## If you have found this interesting:

_You can look for my other articles, and you can also connect or reach me on_** __**[**_LinkedIn_**](<https://www.linkedin.com/in/salvatore-raieli/>)** _._**_Check_[** _this repository_**](<https://github.com/SalvatoreRa/ML-news-of-the-week>) _containing weekly updated ML & AI news. _**_I am open to collaborations and projects_** _and you can reach me on LinkedIn. You can also_[ _subscribe for free_](<https://salvatore-raieli.medium.com/subscribe>) _to get notified when I publish a new story._

## [Get an email whenever Salvatore Raieli publishes.Get an email whenever Salvatore Raieli publishes. By signing up, you will create a Medium account if you don’t already…salvatore-raieli.medium.com](<https://salvatore-raieli.medium.com/subscribe?source=post_page-----b5773a723615--------------------------------------->)

_Here is the link to my GitHub repository, where I am collecting code and many resources related to machine learning, artificial intelligence, and more._

## [GitHub — SalvatoreRa/tutorial: Tutorials on machine learning, artificial intelligence, data science…Tutorials on machine learning, artificial intelligence, data science with math explanation and reusable code (in python…github.com](<https://github.com/SalvatoreRa/tutorial?source=post_page-----b5773a723615--------------------------------------->)

_or you may be interested in one of my recent articles:_

## [From Syntax to Semantics: How Code Turns LLMs into Better ModelsExploring the Transformative Impact of Code Data on LLM Performance Across Diverse Taskslevelup.gitconnected.com](</from-syntax-to-semantics-how-code-turns-llms-into-better-models-1fc04fcda722?source=post_page-----b5773a723615--------------------------------------->)

## [Can AI Replace Human ResearchersThe AI Scientist: Does Sakana New Method Mean Fully Automated Research?levelup.gitconnected.com](</can-ai-replace-human-researchers-50fcc43ea587?source=post_page-----b5773a723615--------------------------------------->)

## [Safekeep Science’s Future: Can LLMs Transform Peer Review?Peer review is today’s science core, but is flawed with bias and burdening researchers. Can we improve it?levelup.gitconnected.com](</safekeep-sciences-future-can-llms-transform-peer-review-e1f323caef08?source=post_page-----b5773a723615--------------------------------------->)

## [Knowledge is Nothing Without Reasoning: Unlocking the Full Potential of RAG through Self-ReasoningEnhancing Reliability and Traceability in Retrieval-Augmented Generative Modelslevelup.gitconnected.com](</knowledge-is-nothing-without-reasoning-unlocking-the-full-potential-of-rag-through-self-reasoning-7ec213516a56?source=post_page-----b5773a723615--------------------------------------->)

## Reference

Here is the list of the principal references I consulted to write this article, only the first name for an article is cited.

1. Peng, 2024, Graph Retrieval-Augmented Generation: A Survey, [link](<https://arxiv.org/abs/2408.08921>)
2. Sarmah, 2024, HybridRAG: Integrating Knowledge Graphs and Vector Retrieval Augmented Generation for Efficient Information Extraction, [link](<https://arxiv.org/abs/2408.04948>)
3. Peng, 2024, Knowledge Graphs: Opportunities and Challenges, [link](<https://arxiv.org/abs/2303.13948>)
4. Fan, 2024, A Survey on RAG Meeting LLMs: Towards Retrieval-Augmented Large Language Models, [link](<https://arxiv.org/pdf/2405.06211>)
5. Wu, 2024, Medical Graph RAG: Towards Safe Medical Large Language Model via Graph Retrieval-Augmented Generation, [link](<https://arxiv.org/abs/2408.04187>)

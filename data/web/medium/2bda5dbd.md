---
domain: medium.com
fetch_date: '2026-05-18T12:47:36.913786'
status: ok
url: https://medium.com/@florian_algo/a-new-approach-to-optimizing-query-generation-in-rag-33c32d68f4e6
---

# A New Approach to Optimizing Query Generation in RAG

[ ![Florian June](https://miro.medium.com/v2/resize:fill:64:64/1*DmQ3DH2JeAJquvhT_tjVCw.jpeg) ](</@florian_algo?source=post_page---byline--33c32d68f4e6--------------------------------------->)

[Florian June](</@florian_algo?source=post_page---byline--33c32d68f4e6--------------------------------------->)

4 min read

·

Sep 9, 2024

\--

Listen

Share

More

_Recently, I have introduced some new advancements in Retrieval-Augmented Generation (RAG). Today, we’ll look at a study that improves the quality of RAG retrieval by optimizing queries. This method is fairly straightforward and direct_.

To address the hallucinations of large language models (LLMs), Retrieval-Augmented Generation (RAG) systems leverage document retrieval to provide more accurate answers. Despite their promise, existing RAG systems still face challenges due to vague queries.

This article introduces a new study titled “[Optimizing Query Generation for Enhanced Document Retrieval in RAG](<https://arxiv.org/pdf/2407.12325v1>)”. This study aimes to enhance document retrieval in RAG by optimizing query generation.

## Solution

QOQA (Query Optimization using Query Expansion) is illustrated in Figure 1.

Figure 1: Concept figure of QOQA. Given expansion query with top-k docs, we add top-3 rephrased queries and scores to LLM. We optimize the query based on the scores and generate the rephrased query. Source: [QOQA](<https://arxiv.org/pdf/2407.12325v1>).

The corresponding prompt is shown in Figure 2.

Figure 2: Prompt template used in QOQA. The black texts describe instructions of the optimizing task. The blue texts are original query with top-N retrieved documents with the original query. The purple texts are revised queries by LLM optimizer and scores. Source: [QOQA](<https://arxiv.org/pdf/2407.12325v1>).

The QOQA method optimizes query generation through the following steps, thereby improving the document retrieval accuracy in RAG systems.

### Query Expansion and Reconstruction

The core idea of QOQA is to utilize large language models (LLMs) to rephrase queries. First, the system retrieves the top N relevant documents using the original query. These retrieved documents, together with the original query, form an expanded query. Then, LLMs generate rephrased queries based on these expanded queries.

### Query-Document Alignment Score

To evaluate and optimize the generated queries, QOQA introduced a query-document alignment score. This scoring system includes three evaluation criteria: BM25 score, dense score, and hybrid score.

* **BM25 Score** : Based on a sparse retrieval model, it evaluates the frequency and weight of query terms in the document.
* **Dense Score** : Using a dense retrieval model, it evaluates the alignment between queries and documents through similarity in the embedding vector space.
* **Hybrid Score** : Combines both BM25 and dense scores, optimizing the final score by adjusting the parameter α.

### Optimization Process

During the optimization process, the QOQA method updates the query template, including the original query, retrieved documents, and the top K rephrased queries. In each iteration, LLMs generate new rephrased queries based on these scores and add them to the query bucket. Through multiple iterations, the system continuously optimizes the queries to ensure they outperform the original query.

## Evaluation

The experimental results showed that the QOQA method significantly improved document retrieval performance compared to baseline models. The performance of various document retrieval models across these datasets is summarized in Figure 3.

Press enter or click to view image in full size

Figure 3: Results of document retrieval task. All scores denote nDCG@10. Bold indicates the best result across all models, and the second best is underlined. Source: [QOQA](<https://arxiv.org/pdf/2407.12325v1>).

## Case Study: How QOQA Improves Query Precision

To better understand the real-world impact of the QOQA method, let’s look at a concrete example from the **SciFact** and **FiQA** datasets, which were used to validate this approach. These datasets focus on scientific fact-checking and financial question answering, respectively, offering ideal test cases for evaluating the precision of document retrieval.

Press enter or click to view image in full size

Figure 4: Examples from SciFact, and FiQA dataset. Blue texts are overlapping keywords between answer document and rephrased query. Source: [QOQA](<https://arxiv.org/pdf/2407.12325v1>).

### Example 1: SciFact Dataset

* **Original Query** : _“0-dimensional biomaterials show inductive properties.”_
* **QOQA-Rephrased Query** : _“Do nano-sized biomaterials possess unique properties that can trigger specific reactions in biological systems?”_

By rephrasing the original query, QOQA introduces more specific terms like “nano-sized biomaterials” and “specific reactions in biological systems.” This precise language ensures that the system retrieves more relevant documents. In this case, the retrieved document discussed nanotechnologies used for manipulating stem cells, which closely aligned with the rephrased query and provided a much more accurate answer compared to the original vague query.

### Example 2: FiQA Dataset

* **Original Query** : _“What is the origin of COVID-19?”_
* **QOQA-Rephrased Query** : _“What molecular evidence supports bats and pangolins as the likely origin hosts of the COVID-19 virus?”_

In this example, the QOQA method refined the query by specifying “molecular evidence” and “bats and pangolins” as the focal points. This level of detail helped retrieve more scientifically accurate documents, such as studies examining the genomic analysis of bat coronaviruses and their link to the COVID-19 virus.

## Conclusion and Insights

This article introduces a novel method to mitigate hallucinations, particularly addressing the issue of vague queries in Retrieval-Augmented Generation (RAG) systems, by optimizing query generation. The method combines the strengths of both traditional sparse retrieval and modern dense retrieval while leveraging the powerful generative capabilities of large language models (LLMs).

In my opinion, if validated in more diverse fields and larger-scale tasks in the future, and if the issue of resource consumption in query generation is addressed, this work could offer broader applications for RAG systems and the information retrieval domain.

If you’re interested in RAG technologies, feel free to check out my other articles.

[ ![Florian June](https://miro.medium.com/v2/resize:fill:40:40/1*DmQ3DH2JeAJquvhT_tjVCw.jpeg) ](</@florian_algo?source=post_page-----33c32d68f4e6--------------------------------------->)

[Florian June](</@florian_algo?source=post_page-----33c32d68f4e6--------------------------------------->)

## RAG

[View list](</@florian_algo/list/rag-1b65363c06db?source=post_page-----33c32d68f4e6--------------------------------------->)

106 stories

![](https://miro.medium.com/v2/resize:fill:388:388/0*0qcWMcyxgAEksKxH.png)

![](https://miro.medium.com/v2/resize:fill:388:388/0*d5IGGHnoIIWBcRtu.png)

![](https://miro.medium.com/v2/resize:fill:388:388/0*KzyYE7oQLMS889mV.png)

**And the latest article or video can be found in**[**my newsletter**](<https://florianjune.substack.com/>)**or on**[**YouTube**](<https://www.youtube.com/@ai_exploration_journey>)**.**

Finally, if there are any errors or omissions in this article, or if you have any questions, please point them out in the comment section.

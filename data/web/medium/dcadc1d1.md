---
domain: generativeai.pub
fetch_date: '2026-05-18T12:49:02.403683'
status: ok
url: https://generativeai.pub/unleashing-llms-self-awareness-how-seakr-enhances-knowledge-retrieval-in-ra-7a0d6603c8ee
---

# Unleashing LLM’s Self-Awareness: How SEAKR Enhances Knowledge Retrieval in RAG

[ ![Florian June](https://miro.medium.com/v2/resize:fill:64:64/1*DmQ3DH2JeAJquvhT_tjVCw.jpeg) ](<https://medium.com/@florian_algo?source=post_page---byline--7a0d6603c8ee--------------------------------------->)

[Florian June](<https://medium.com/@florian_algo?source=post_page---byline--7a0d6603c8ee--------------------------------------->)

7 min read

·

Oct 14, 2024

\--

Listen

Share

More

Today, let’s look at an improvement in RAG (Retrieval-Augmented Generation) that leverages LLM’s self-awareness.

The growing prevalence of large language models (LLMs) has exposed a critical limitation: hallucination, where models generate plausible-sounding but factually incorrect content. This is particularly problematic when the model’s internal knowledge is insufficient, leading to incorrect outputs despite high confidence.

Traditional RAG methods attempt to alleviate this by integrating external knowledge for every query. However, this approach can be inefficient and even counterproductive, **especially when the retrieved knowledge is noisy or irrelevant.**

Figure 1: Adaptive RAG mainly concerns 1) when to retrieve and 2) how to integrate retrieved knowledge. Source: [SEAKR](<https://arxiv.org/pdf/2406.19215v1>).

**This article introduces a new study called “**[**SEAKR**](<https://arxiv.org/pdf/2406.19215v1>)**”.** This study introduces a novel concept:**leveraging the model’s self-awareness of uncertainty to decide** when and how to retrieve and integrate external knowledge, optimizing both efficiency and accuracy , as shown in Figure 1.

## Solution

### Overview

Press enter or click to view image in full size

Figure 2: The overall framework of SEAKR. Source: [SEAKR](<https://arxiv.org/pdf/2406.19215v1>).

Unlike existing adaptive RAG methods that rely solely on the model’s output to judge the need for retrieval, SEAKR leverages the model’s self-aware uncertainty — a measure extracted directly from the internal states of the LLM. This allows SEAKR to more accurately assess whether the model has sufficient knowledge to answer a query or if external information is required.

SEAKR is built upon three core components:

* A search engine that retrieves and ranks relevant knowledge snippets
* An LLM that processes input contexts and generates continuations
* A self-aware uncertainty estimator that quantifies the LLM’s confidence in its output.

SEAKR employs an iterative Chain-of-Thought (CoT) reasoning strategy, where it dynamically decides whether to retrieve external knowledge based on the LLM’s internal uncertainty.

If retrieval is necessary, SEAKR re-ranks the knowledge to select the most relevant snippet. The model then integrates this knowledge with its generated rationales to produce the final answer. Throughout this process, SEAKR continuously evaluates the uncertainty of the LLM, ensuring that the generated content is both accurate and reliable.

### Self-aware Retrieval

The self-aware retrieval process in SEAKR involves three key steps: organizing the input context, generating the query, and producing the rationale.

**1\. Input Context Organization:** Before generating a rationale, SEAKR first organizes the input context, prompting the LLM to generate a rationale step without retrieval. The input context includes the current question and previously generated rationales. These are organized using a predefined prompt template as follows:

``` [In-Context Learning Examples]Rationale [r1] Rationale [r2]...For question: [q] Next Rationale: ```

In this setup, if the LLM exhibits high uncertainty in generating the rationale (measured against a predefined threshold `δ`), SEAKR triggers the retrieval step.

**2\. Query Generation:** Once the decision to retrieve has been made, the LLM performs a “pseudo-generation” to construct a retrieval query. This means that the LLM generates a temporary rationale, and any content that indicates high uncertainty (such as low-probability tokens) is identified and removed, forming the search query. The goal here is to retrieve knowledge that directly addresses these uncertainties.

**3\. Rationale Generation:** After retrieval, SEAKR integrates the knowledge snippets (if retrieval was triggered) into the current input context, and the LLM generates the final rationale based on the updated context. If retrieval is not triggered, the input context remains unchanged, and the rationale is generated as is. The generated rationale is then added to the rationale buffer for use in subsequent steps.

### Self-aware Re-ranking

After multiple knowledge snippets are retrieved, traditional RAG methods typically rank them based on their relevance to the query. However, this approach may overlook how well the retrieved knowledge aligns with the LLM’s internal knowledge, potentially leading to the integration of misleading information.

SEAKR’s self-aware re-ranking mechanism prioritizes the knowledge snippets that most effectively reduce the LLM’s uncertainty, thereby improving the accuracy of the generation process.

**1\. Multiple Knowledge Snippet Retrieval:** SEAKR allows the search engine to return multiple knowledge snippets, retaining the top N results. These snippets are then organized with the previously generated rationales into new input contexts. A sample prompt template is as follows:

``` [In-Context Learning Examples]Rationale [r1] Rationale [r2]...Knowledge Evidence: [k]For question: [q] Next Rationale: ```

**2\. Self-aware Uncertainty Evaluation:** For each retrieved knowledge snippet, SEAKR creates N different input contexts and evaluates the corresponding self-aware uncertainty of the LLM. By comparing these uncertainties, SEAKR selects the knowledge snippet that minimizes uncertainty. This re-ranking mechanism ensures that the LLM selects not only relevant but also the most accurate knowledge snippet for the generation process.

### Self-aware Reasoning

In the SEAKR system, the retrieval process halts under two conditions:

* When the LLM signals the end of generation with a statement like “So the final answer is,”
* When the maximum retrieval limit is reached.

SEAKR then employs two distinct reasoning strategies to synthesize the retrieved knowledge and generate the final answer.

1. **Reasoning with Generated Rationales:** This strategy prompts the LLM to generate the final answer directly after the last generated rationale, by appending the instruction “So the final answer is” to the rationale buffer, leading the LLM to provide an answer based on the previous rationales.
2. **Reasoning with Retrieved Knowledge:** This strategy concatenates all re-ranked retrieved knowledge with the question to form an augmented context, prompting the LLM to engage in chain-of-thought (CoT) reasoning based on this enriched context. SEAKR then compares the uncertainty of the answers generated by these two strategies and selects the one with the lowest uncertainty as the final output.

### Self-aware Uncertainty Estimator

At the core of SEAKR lies its self-aware uncertainty estimator. This estimator evaluates the credibility of generated content based on the LLM’s internal states rather than its final output.

Specifically, for each input context, the LLM generates multiple samples and retains the hidden representation of the final token. The Gram matrix of these hidden representations is then computed, and the determinant of this matrix serves as the uncertainty score.

By using this regularized Gram determinant, SEAKR ensures that the generation process is based on the most robust integration of knowledge, thereby enhancing the accuracy and reliability of the generated content.

## Evaluation

The effectiveness of SEAKR is demonstrated through experiments on both complex and simple QA datasets. SEAKR outperforms all baseline methods, achieving a 36.0% F1 score on the 2WikiMultiHopQA dataset, 39.7% on HotpotQA, and 23.5% on IIRC, surpassing the best-performing baseline by significant margins, as shown in Figure 3.

Press enter or click to view image in full size

Figure 3: Experiment results on complex QA datasets. All the results are shown in percentage (%). Source: [SEAKR](<https://arxiv.org/pdf/2406.19215v1>).

These results underscore the benefits of integrating self-awareness into adaptive RAG, particularly in handling complex questions requiring multi-hop reasoning and the synthesis of multiple knowledge sources.

## Case Study

In a case study from the HotpotQA dataset, SEAKR was tasked with determining who lived longer between Alejandro Jodorowsky and Philip Saville, as shown in Figure 4.

Press enter or click to view image in full size

Figure 4: Case study. Source: [SEAKR](<https://arxiv.org/pdf/2406.19215v1>).

`#Search` denotes the knowledge rank given by the search engine. `#U(c)` is the ranking according to self-aware uncertainty.

In the second iteration, SEAKR detected high uncertainty (`U(c) = -4.4`) during pseudo-generation, triggering a retrieval process. The first retrieved result was relevant but did not directly answer the question. The second result significantly reduced uncertainty and contained the critical information needed. The third result had overlapping information with the second, leading to a similarly low uncertainty score.

This example illustrates SEAKR’s ability to navigate complex reasoning processes with high accuracy.

## Conclusion and Insights

This article delves into SEAKR, a groundbreaking framework that enhances the reliability of LLMs by introducing self-aware knowledge retrieval.

Comparison with Traditional RAG methods, like IRCoT, retrieve knowledge at every step, often leading to unnecessary or even conflicting information being integrated into the model’s output. Other adaptive methods such as FLARE rely on output probabilities to decide when to retrieve, but these methods can be misled by the model’s overconfidence. **SEAKR’s approach, by contrast,** bases its decisions on a deeper analysis of the model’s internal states, resulting in a more accurate and reliable generation process.

However, the reliance on internal states for uncertainty estimation restricts SEAKR’s applicability to open-source LLMs, and its computational demands may pose challenges for broader adoption.

Future developments could focus on refining the uncertainty estimation process to be less resource-intensive and expanding SEAKR’s capabilities to cover a wider range of tasks beyond QA.

Additionally, if you’re interested in RAG technologies, feel free to check out my other articles.

[ ![Florian June](https://miro.medium.com/v2/resize:fill:40:40/1*DmQ3DH2JeAJquvhT_tjVCw.jpeg) ](<https://medium.com/@florian_algo?source=post_page-----7a0d6603c8ee--------------------------------------->)

[Florian June](<https://medium.com/@florian_algo?source=post_page-----7a0d6603c8ee--------------------------------------->)

## RAG

[View list](<https://medium.com/@florian_algo/list/rag-1b65363c06db?source=post_page-----7a0d6603c8ee--------------------------------------->)

106 stories

![](https://miro.medium.com/v2/resize:fill:388:388/0*0qcWMcyxgAEksKxH.png)

![](https://miro.medium.com/v2/resize:fill:388:388/0*d5IGGHnoIIWBcRtu.png)

![](https://miro.medium.com/v2/resize:fill:388:388/0*KzyYE7oQLMS889mV.png)

**And the latest article or video can be found in**[**my newsletter**](<https://florianjune.substack.com/>)**or on**[**YouTube**](<https://www.youtube.com/@ai_exploration_journey>).

Finally, if there are any errors or omissions in this article, or if you have any questions, please point them out in the comment section.

This story is published on [Generative AI](<https://generativeai.pub/>). Connect with us on [LinkedIn](<https://www.linkedin.com/company/generative-ai-publication>) and follow [Zeniteq](<https://www.zeniteq.com/>) to stay in the loop with the latest AI stories.

Subscribe to our [newsletter](<https://www.generativeaipub.com/>) and [YouTube](<https://www.youtube.com/@generativeaipub>) channel to stay updated with the latest news and updates on generative AI. Let’s shape the future of AI together!

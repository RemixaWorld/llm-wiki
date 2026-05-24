---
domain: cobusgreyling.medium.com
fetch_date: '2026-05-18T12:57:00.260022'
status: ok
url: https://cobusgreyling.medium.com/dr-rag-applying-dynamic-document-relevance-to-question-answering-rag-a15cde1055f5
---

![](https://miro.medium.com/v2/resize:fit:700/1*w_7KEW8rhE2j3Y0T6N_SEQ.png)

# DR-RAG: Applying Dynamic Document Relevance To Question-Answering RAG

## DR-RAG is a two-stage retrieval process which is focussed on calling the LLM only once by performing a multi-hop process on QA datasets. This approach shows that significant improvements can be made to the accuracy of the answers.

## Introduction

The study found the need during retrieval, to select documents that are highly relevant and decisive for the generation of answers. These are called static-relevant documents.

But also documents that are low in relevance but forms a crucial part of the answer generation process. These are referred to as dynamic-relevant documents.

## The Problem DR-RAG Solves

As illustrated in the image below, consider the example query *Who is the spouse of the child of Peter Andreas Heiberg?*

![](https://miro.medium.com/v2/resize:fit:1000/1*P48K6Thzb__30QS__rSqQQ.png)

This query necessitates retrieving the two most relevant documents to provide accurate answers. Static-relevant documents are relatively easy to retrieve due to their direct relevance to the query, such as ‘Peter Andreas Heiberg’ and ‘child/son’.

However, retrieving dynamic-relevant documents poses challenges as they are only *tangentially* related to the query, such as *spouse/wife*.

Additionally, the vast amount of information on *spouse* in the knowledge base may cause dynamic-relevant documents to be ranked lower in the retrieval process.

Notably, there is a high relevance between static and dynamic relevant documents, such as *Johan Ludvig Heiberg* and *wife*. Considering ‘spouse/wife’ along with the query can facilitate the retrieval of dynamic-relevant documents, thus enabling the extraction of accurate answers.

## Synergising Context Between Multiple Documents

The study identifies the need to create synergies between multiple documents and establish contextual relevance not only from one document, but from all relevant and applicable documents.

DR-RAG is described as multi-hop question answering framework. This framework does remind much of previous research done on this approach.

The differentiating factor of DR-RAG might be the classifier which the researches designed to determines whether the retrieved documents contribute to the current query by setting a predefined threshold.

The mechanism is aimed at reducing redundant documents and ensures that the retrieved documents are concise and efficient.

Considering the image below, which is an overview of DR-RAG:

**Step 1:** Retrieve static-relevant documents (SR-Documents) based on their high relevance with the query.

**Step 2:** Concatenate SR-Documents with the query to retrieve multiple dynamic-relevant documents (DR-Documents).

## Get Cobus Greyling’s stories in your inbox

Join Medium for free to get updates from this writer.

**Step 3: **Select each DR-Document individually and combine it with the query and SR-Documents. Feed these combinations into a classifier to determine the most relevant DR-Document.

![](https://miro.medium.com/v2/resize:fit:1000/1*6AxZC5EGj5LUbEi3a4uITQ.png)

## A Few Observations

The study does recognises two basic requirements emerging as RAG implementations are becoming more popular:

- There is a requirement to optimise the interactions to the LLM to some degree from a latency and cost perspective.
- We have moved past the point of a single chunk of text holding the contextual reference for all data. And multiple documents needs to be synthesised it some instances to reach a satisfactory answer. This is achieved via process called agentic RAG.

### However,

In general RAG is becoming more agent-like, or as LlamaIndex refer to it, *Agentic*. This is where RAG implementations become agent-like in its ability to reason and explore multiple reasoning paths, while traversing multiple documents in a RAG setup.

Matched answers user questions might span over multiple documents. Where a single document does not hold the answer, but multiple documents need to be referenced.

Hence it is not a situation of a main and supporting document. But rather synthesising multiple documents to reach an answer. Again LlamaIndex has a number of good examples on this approach.

For instance, there might be multiple documents each covering one month of financial data. Imagine the user asks, *how does January compare to February in terms of revenue and opportunities for saving.*

This type of question demands a high level of relevant data extraction and reasoning capabilities.

Following an agentic approach, LlamaIndex recently implemented a Language Agent Tree Search with advanced tree of thought reasoning capabilities.

Consider the RAG Agent (Agentic RAG) output below, notice how the RAG Agent goes through a routine of observation, thought, action, action input, etc.

![](https://miro.medium.com/v2/resize:fit:1000/1*f1X2jOW7YK6DA1tXv10gsw.png)

*⭐️ Follow me on **LinkedIn** for updates on Large Language Models ⭐️*

![](https://miro.medium.com/v2/resize:fit:700/0*uf0cwjtIKGOANhO-.png)

*I’m currently the **Chief Evangelist** @ **Kore AI**. I explore & write about all things at the intersection of AI & language; ranging from **LLMs**, **Chatbots**, **Voicebots**, **Development Frameworks**, **Data-Centric latent spaces** & more.*

![](https://miro.medium.com/v2/resize:fit:700/0*5Yufm3OkreB3mAfp.png)

![](https://miro.medium.com/v2/resize:fit:370/0*crWxEPhD4CymedfG.jpeg)

![](https://miro.medium.com/v2/resize:fit:700/0*iNyGqfNerlHNbQtV.png)

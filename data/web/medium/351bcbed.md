---
domain: generativeai.pub
fetch_date: '2026-05-18T12:49:59.723657'
status: ok
url: https://generativeai.pub/nano-graphrag-with-ollama-a-leaner-faster-and-more-efficient-approach-to-graphrag-local-936ce7a2b67c
---

# Nano GraphRAG with Ollama: A Leaner, Faster, and More Efficient Approach to GraphRAG — Local Installation Guide

## How to set up Nano GraphRAG with Ollama Llama for streamlined retrieval-augmented generation (RAG). This guide covers installation, configuration, and practical use cases to maximize local LLM performance with smaller, faster, and cleaner graph-based RAG techniques.

[ ![Md Monsur ali](https://miro.medium.com/v2/resize:fill:64:64/1*_hX0pNzd-T2-iPjAYXDJTg.jpeg) ](<https://medium.com/@monsuralirana?source=post_page---byline--936ce7a2b67c--------------------------------------->)

[Md Monsur ali](<https://medium.com/@monsuralirana?source=post_page---byline--936ce7a2b67c--------------------------------------->)

6 min read

·

Nov 11, 2024

\--

Listen

Share

More

👨🏾‍💻 [GitHub](<https://github.com/mdmonsurali>) ⭐️ | 👔 [LinkedIn ](<https://www.linkedin.com/in/mdmonsurali/>)| 📝 [Medium ](<https://medium.com/@monsuralirana>)| ☕️ [Ko-fi](<https://ko-fi.com/monsurali>)

Press enter or click to view image in full size

Photo by [nano-graphrag](<https://github.com/gusye1234/nano-graphrag>)

**Introduction**

The surge in the popularity of Large Language Models (LLMs) like OpenAI’s GPT, Anthropic’s Claude, and others has created a massive demand for tools that extend their capabilities beyond their pre-trained data. One such promising technique is **Retrieval-Augmented Generation (RAG)** , which allows users to leverage private datasets to enhance the context provided to LLMs. This is where **Nano GraphRAG** comes into play, providing a compact, efficient, and hackable solution to implement graph-based RAG systems.

In this blog post, we will explore what makes Nano GraphRAG stand out, how it differs from traditional RAG approaches, and its practical applications with the OLAMA framework.

## Understanding Retrieval-Augmented Generation (RAG)

Traditional LLMs are pre-trained on extensive datasets and can answer a wide range of questions. However, they lack access to data specific to your organization or domain, especially if that data is proprietary or not part of the model’s pre-training corpus. This is where RAG comes in.

**RAG** combines LLMs with external knowledge sources by breaking down private data into smaller chunks, converting them into numerical embeddings, and storing them in a **vector database**. Whenever a user asks a query, the system retrieves relevant data chunks based on vector similarity and feeds them into the LLM, enriching the prompt with domain-specific context. This helps the model generate more grounded and accurate responses.

## The Limitations of Vanilla RAG

While RAG is great for retrieving specific information, it struggles with complex, entity-centric queries that require understanding relationships between data points. This is because vanilla RAG is focused on a straightforward search-retrieve-respond process, making it inefficient for questions requiring a deeper semantic understanding of relationships.

## Enter GraphRAG: A New Paradigm

To address the limitations of traditional RAG, **Microsoft introduced GraphRAG** — a technique that leverages graph-based indexing to capture not only entities but also their relationships within a dataset. It breaks down the process into two stages:

1. **Entity Extraction** : It identifies entities and their relationships within a document, building an entity knowledge graph.
2. **Contextual Summarization** : It generates summaries for groups of related entities, providing context-rich responses.

By leveraging this graph structure, GraphRAG enables models to answer more complex, entity-focused questions by understanding the connections between different data points.

## What is Nano GraphRAG?

**Nano GraphRAG** is a lightweight, simplified version of GraphRAG, developed to make the graph-based RAG approach more accessible and efficient. Unlike the full-fledged GraphRAG implementations, Nano GraphRAG aims to be minimalistic, with only about 1,100 lines of code, focusing on speed, efficiency, and ease of use.

The project is designed to be **easy to integrate** with various LLM backends, including both local (e.g., OLAMA) and API-based models (e.g., OpenAI, Anthropic). This allows users to leverage graph-based knowledge augmentation without heavy infrastructure requirements.

## Why Choose Nano GraphRAG?

Here’s why Nano GraphRAG stands out:

* **Compact and Efficient** : With just 1,100 lines of code, it’s easy to understand and modify.
* **Asynchronous Processing** : Supports async operations, allowing for faster indexing and querying.
* **Versatile Backend Support** : Works seamlessly with both local LLMs via OLAMA and cloud-based API models.
* **Incremental Indexing** : Allows for real-time updates to your knowledge base, which is essential for dynamic data environments.

## Before we start! 🦸🏻‍♀️

If you like this topic and you want to support me:

1. **Clap** my article 50 times; that will help me out.👏
2. [**Follow**](<https://medium.com/@monsuralirana>) me on Medium and subscribe to get my latest article for Free🫶

## How Nano GraphRAG Works

### Setting Up Nano GraphRAG Locally: A Complete Walkthrough

Here’s a step-by-step update on how to set up and use **Nano GraphRAG** with **Ollama Llama 3.2** for both querying and indexing.

### Step 1: Clone the Repository and Install Dependencies

```python git clone https://github.com/gusye1234/nano-graphrag.gitcd nano-graphragpip install -e . ```

### Step 2: Modify the Example Script

Navigate to:

``` nano-graphrag/examples/using_ollama_as_llm_and_embedding.py ```

Update the parameters:

``` # Update these variablesMODEL = "llama3.2"EMBEDDING_MODEL = "nomic-embed-text"WORKING_DIR = "/mnt/e/Virtual Agent/Doc" ```

### Step 3: Define the Query Function

The `query()` function is used to retrieve answers using your indexed data.

```python def query(): rag = GraphRAG( working_dir=WORKING_DIR, best_model_func=ollama_model_if_cache, cheap_model_func=ollama_model_if_cache, embedding_func=ollama_embedding, ) print( rag.query("What is the inside of a cricket ball made of?", param=QueryParam(mode="global")) ) ```

### Step 4: Define the Insert Function

This function reads a text file and indexes the content.

```python def insert(): from time import time with open(f"{WORKING_DIR}/The-Game-of-Cricket.txt", encoding="utf-8-sig") as f: FAKE_TEXT = f.read() # Remove existing index files if any remove_if_exist(f"{WORKING_DIR}/vdb_entities.json") remove_if_exist(f"{WORKING_DIR}/kv_store_full_docs.json") remove_if_exist(f"{WORKING_DIR}/kv_store_text_chunks.json") remove_if_exist(f"{WORKING_DIR}/graph_chunk_entity_relation.graphml") rag = GraphRAG( working_dir=WORKING_DIR, enable_llm_cache=True, best_model_func=ollama_model_if_cache, cheap_model_func=ollama_model_if_cache, embedding_func=ollama_embedding, ) start = time() rag.insert(FAKE_TEXT) print("Indexing completed in:", time() - start) ```

### Step 5: Embedding Function

To generate embeddings using **Ollama** :

```python @wrap_embedding_func_with_attrs( embedding_dim=768, max_token_size=8192,)async def ollama_embedding(texts: list[str]) -> np.ndarray: embed_text = [] for text in texts: data = ollama.embeddings(model=EMBEDDING_MODEL, prompt=text) embed_text.append(data["embedding"]) return embed_text ```

### Step 6: Run the Script

Open your terminal and execute:

``` python3 examples/using_ollama_as_llm_and_embedding.py ```

Output:

``` The inside of a cricket ball is made of cork, while the outside is made of leather. ```

This script will first index your data using the `insert()` function and then run the `query()` function to demonstrate a retrieval.

### Explanation

* The **GraphRAG** instance handles both the retrieval and the insertion of data.
* The use of **Ollama Llama 3.2** ensures high-quality responses with cached results to optimize speed.
* You can adjust the question in the `query()` function to test different queries against your indexed dataset.

This setup efficiently leverages both graph-based RAG and LLM capabilities, allowing you to deploy a robust AI assistant using your own private data sources.

> **More details: Github:**

## [GitHub - gusye1234/nano-graphrag: A simple, easy-to-hack GraphRAG implementationA simple, easy-to-hack GraphRAG implementation. Contribute to gusye1234/nano-graphrag development by creating an…github.com](<https://github.com/gusye1234/nano-graphrag?source=post_page-----936ce7a2b67c--------------------------------------->)

> **Leave your feedback, comments, and 👏 Clap for the story**
>
> **If you enjoyed this article and would like to support my work, consider buying me a coffee here:** [**Ko-fi**](<https://ko-fi.com/monsurali>)☕

## Conclusion

In a world where businesses and researchers are increasingly looking to harness the power of LLMs for private data, Nano GraphRAG provides a lightweight yet powerful solution. Its graph-based approach bridges the gap between simple retrieval and deep semantic understanding, making it ideal for complex data environments.

Happy coding! 🎉

👨🏾‍💻 [GitHub](<https://github.com/mdmonsurali>) ⭐️ | 👔 [LinkedIn ](<https://www.linkedin.com/in/mdmonsurali/>)| 📝 [Medium ](<https://medium.com/@monsuralirana>)| ☕️ [Ko-fi](<https://ko-fi.com/monsurali>)

Thank you for your time in reading this post!

Make sure to leave your feedback and comments. 👏 Clap for the story and follow for stories. See you in the next blog; stay tuned 📢

## Enjoyed this article? Check out more of my work:

* **Building a Custom Documents Agent with Elasticsearch, Ollama, LLaMA 3.1, and LangChain:** Explore how to set up a personalized document retrieval agent using LLaMA 3.1 and Ollama for seamless information retrieval. [Read the full tutorial here](<https://medium.com/gitconnected/building-a-custom-documents-agent-with-elasticsearch-ollama-llama-3-1-and-langchain-926b28047e1d>).
* **Building Your Personal AI Assistant with Memory Using Ollama’s LLaMA3.1, LLaMA3.2 Models, Streamlit UI, and Locally:** Discover how to develop an AI assistant that remembers past interactions using the latest LLaMA models and a user-friendly Streamlit interface. [Read the full tutorial here.](<https://medium.com/gitconnected/building-porter-your-personal-ai-assistant-with-memory-using-ollamas-llama3-1-efb32b80c129>)
* **OpenAI Swarm: A Lightweight Framework for Multi-Agent Orchestration:** Dive into a new framework designed for managing multiple AI agents efficiently, enhancing your AI project management. [Read the full tutorial here.](<https://medium.com/gitconnected/openai-swarm-a-lightweight-framework-for-multi-agent-orchestration-b4a83a1a1e37>)
* **How to Use Molmo-7B for Multimodal AI: Extract Text and Images with an Open-Source Vision-Language Model:** Learn how to harness the power of the Molmo-7B model for extracting both text and images, revolutionizing your approach to multimodal AI. [Read the full tutorial here.](<https://medium.com/@monsuralirana/how-to-use-molmo-7b-for-multimodal-ai-extract-text-and-images-with-an-open-source-vision-language-8a31939a2960>)
* **Meta Spirit LM: A Complete Guide to Multimodal AI for Text and Speech Generation:** Explore the capabilities of Meta Spirit LM in generating text and speech, and how it can be applied in various AI applications. [Read the full tutorial here.](<https://medium.com/ai-advances/meta-spirit-lm-a-complete-guide-to-multimodal-ai-for-text-and-speech-generation-ed0af74bc950>)
* **Supercharge Text-to-Speech with Piper TTS:** Find out how to achieve 10x faster, real-time, offline voice synthesis with human-like accuracy in this hands-on _Google Colab tutorial_. [Transform your text into lifelike speech here.](<https://medium.com/@monsuralirana/unleashing-the-power-of-piper-tts-transforming-text-to-speech-10x-faster-with-ai-human-like-voice-eadf2065d66d>)

This story is published on [Generative AI](<https://generativeai.pub/>). Connect with us on [LinkedIn](<https://www.linkedin.com/company/generative-ai-publication>) and follow [Zeniteq](<https://www.zeniteq.com/>) to stay in the loop with the latest AI stories.

Subscribe to our [newsletter](<https://www.generativeaipub.com/>) and [YouTube](<https://www.youtube.com/@generativeaipub>) channel to stay updated with the latest news and updates on generative AI. Let’s shape the future of AI together!

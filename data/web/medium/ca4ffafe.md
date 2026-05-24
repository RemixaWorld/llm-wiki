---
domain: pub.towardsai.net
fetch_date: '2026-05-18T12:50:42.071793'
status: ok
url: https://pub.towardsai.net/llama-ocr-multimodal-rag-local-llm-python-project-easy-ai-chat-for-your-docs-058c0dd3b59f
---

# Llama-OCR + Multimodal RAG + Local LLM Python Project: Easy AI/Chat for your Docs

# **Llama-OCR +** Multimodal RAG + Local LLM Python Project: Easy AI/Chat for your Docs

[ ![Gao Dalie (高達烈)](https://miro.medium.com/v2/resize:fill:64:64/1*drBiQzO68eWvJ_Mot-m1oQ.png) ](<https://medium.com/@GaoDalie_AI?source=post_page---byline--058c0dd3b59f--------------------------------------->)

[Gao Dalie (高達烈)](<https://medium.com/@GaoDalie_AI?source=post_page---byline--058c0dd3b59f--------------------------------------->)

8 min read

·

Nov 28, 2024

\--

Listen

Share

More

Press enter or click to view image in full size

In this story, I have a super quick tutorial showing you how to create a fully local chatbot with Llama-OCR, Multimodal RAG and Local LLM to make a powerful Agent Chatbot for your business or personal use.

I was scrolling through Twitter when I came across an interesting project called **Llama-OCR**. It’s an open-source Optical Character Recognition tool powered by the **Llama 3.2 Vision model**. This tool is designed to convert images of documents into Markdown format, making it especially useful for developers and tech enthusiasts who often work with complex document layouts, such as tables, receipts, or mixed-format files.

In a standard Retrieval-Augmented Generation setup, input documents usually consist of plain text data. Llama-OCR steps up by enabling seamless interaction with visual data. It allows the LLM to leverage in-context learning, retrieving chunks of relevant text from documents that match the context of your query.

**What should you do if the document contains pictures, tables, charts, and text data?**

Each format has its structure and challenges, but the real difficulty comes from the sheer variety within these formats. For example, a PDF can be single-column or multi-column, contain tables or charts, and have headers, footers, images, or diagrams. This wide range of possibilities makes it impractical to create a one-size-fits-all solution.

So, Let me give you a quick demo of a live chatbot to show you what I mean.

I asked the chatbot: _What is approximately 85% of FY22 revenue in Canada?_ The chatbot uses Multimodal RAG to interact with PDFs and generate an output. This process combines text, visuals, tables, and charts for a comprehensive response.

We also integrated **ColPali** , a cutting-edge multimodal retrieval system, to seamlessly retrieve images. Instead of relying on traditional OCR or image captioning, ColPali directly encodes image patches, simplifying text extraction from PDFs. For embedding and retrieving images, we used **ColQwen2** , which enhances the efficiency of this workflow.

Once the relevant pages are retrieved, they are fed into the **Llama-3.2 90B Vision model** via Ollama. This powerful model processes the content and provides a clear, accurate answer. It’s an impressive example of how advanced AI systems can streamline data analysis and retrieval!

In this step-by-step guide, we will cover why OCR is still struggling to retrieve complex information, what ColPali is, how ColPali works and how to implement all these techniques together.

## Before we start! 🦸🏻‍♀️

If you like this topic and you want to support me:

1. **Clap** my article 50 times; that will really help me out.👏
2. [**Follow**](<https://medium.com/@mr.tarik098>) me on Medium and subscribe to get my latest article for Free🫶
3. Join the family — Subscribe to [**YouTube channel**](<https://www.youtube.com/channel/UC6P5WCWjqhhXVFBqbJHNxyw>)

## Traditional OCR

Standard LLM ignores this additional information. RAG systems must rely on OCR tools to extract information from tables, images, etc. Although OCR technology has greatly improved recently, it is commonly used to extract text from scanned images.

However, it still produces errors, especially in cases of poor scan quality, and also struggles when dealing with complex layouts such as multi-column PDFs or mixed documents containing text and images. This will result in irrelevant or incorrectly informed text blocks being indexed, which will negatively affect the quality of the LLM synthesized answer when these text blocks are retrieved and added to the context of the LLM

We will use the multimodal LLM ColPali to infer information from complex PDF documents.

## What is ColPali

ColPali is a model with a novel model architecture and training strategy based on a visual language model (VLM) that efficiently indexes documents based on their visual features. It is an extension [of PaliGemma-3B](<https://huggingface.co/google/paligemma-3b-mix-448>) that generates [ColBERT-](<https://arxiv.org/abs/2004.12832>) style multi-vector representations of text and images. It is introduced in the paper [ColPali: Efficient Document Retrieval with Visual Language Models](<https://arxiv.org/abs/2407.01449>)

## How ColPali works

_ColPali_ 2 offers a novel approach to dealing with complex document formats ColPali directly converts screenshots of PDF pages (including images, charts, and tables) into vector representations for retrieval (and sorting), without the need for OCR, layout analysis or any other complex pre-processing steps, and without the need for text segmentation. **All that is required is a screenshot image of the page.**

_The Col_ in ColPali is inspired by ColBERT, where text is represented as multiple vectors instead of a single vector representation. _Pali_ is derived from [PaliGemma](<https://huggingface.co/blog/paligemma>), a powerful visual language model.

ColPali is based on two observations:

* Multi-vector representation and late interaction scoring can improve retrieval performance.
* Visual language models excel in understanding visual content[.](<https://blog.vespa.ai/retrieval-with-vision-language-models-colpali/#fn:3>)

Understanding documents with rich layouts and multimodal components has always been an important and practical task. Recent Large Vision-Language Models (LVLMs) have achieved remarkable progress in various tasks, especially in single-page document understanding (DU).

## Install Llama 3.2 Vision

Ollama now officially supports the Llama 3.2 Vision model.

You can recognize the picture by dragging it in like this.

Press enter or click to view image in full size

You can see that the model has an 11B parameter version and a 90B parameter version. When choosing the 90B parameter version, the file size is about 55GB. Of course, there are also some quantized versions.

Press enter or click to view image in full size

Llama 3.2 Vision 11B requires at least 8GB VRAM, while the 90B model requires at least 64GB VRAM.

The biggest update is the support for the **Llama 3.2 Vision** visual model! The version of ollama has also been `v0.3.14`directly upgraded from `v0.4.0`.

After upgrading ollama, run the following command to experience

``` ollama run llama3.2-vision ```

## Let’s start coding

I used **Multimodal RAG** to interact with last year's Accenture investor slide deck. The slide deck spans 17 pages and includes text, visuals, tables, charts, and annotations. Each page has a unique structure and template, making it challenging to process using traditional RAG methods.

Multimodal RAG is perfect for handling such complex documents, as it combines various data types seamlessly, ensuring accurate and meaningful interactions.

Press enter or click to view image in full size

## Install relevant libraries

We will use byaldi, a library from [AnswerAI](<https://www.answer.ai/>) that makes it easier to work with an upgraded version of ColPali, called ColQwen2, to embed and retrieve images of our PDF documents. We use pdf2image to convert PDF files into PIL objects, and with Popper, you can read, modify and change PDF files.

```python !pip install byaldi ollama pdf2image ```

We also need to install`poppler-utils`, an essential package for manipulating PDF files and converting them to other formats.

```bash sudo apt install poppler-utils ```

## Initialize the ColPali Model

We load ColPali from byaldi using RAGMultiModal

```python import osfrom pathlib import Pathfrom byaldi import RAGMultiModalModel# Initialize RAGMultiModalModelmodel = RAGMultiModalModel.from_pretrained("vidore/colqwen2-v0.1") ```

## Document

Then we retrieve from the 17-page Accenture investor presentation and use the `mv` command to rename it to `accenture_presentation.pdf`.

``` # Dowload and rename the last presentation from Accenture to investors!wget https://investor.accenture.com/~/media/Files/A/Accenture-IR-V3/events-and-presentations/accenture-investor-and-analyst-conference-cfo-slides.pdf!mv accenture-investor-and-analyst-conference-cfo-slides.pdf accenture_presentation.pdf ```

Indexing

We use the ColQwen2 model to index the content of the `accenture_presentation.pdf` file. It assigns the index `"accenture_index"`, stores both vector representations and base64 images for retrieval, and allows overwriting any existing index with the same name.

``` # Use ColQwen2 to index and store the presentationindex_name = "accenture_index"model.index(input_path=Path("/content/accenture_presentation.pdf"), index_name=index_name, store_collection_with_index=True, # Stores base64 images along with the vectors overwrite=True) ```

## Let’s query our indexed document.

let’s query an indexed presentation using the question, **“What is approximately 85% of FY22 revenue in Canada?”**. The top 5 most similar results are retrieved using the `model.search()` method, which ranks pages based on similarity scores. The results are printed with document IDs, page numbers, and similarity scores for review. Finally, a message confirms that the search process was successful.

``` # Lets query our index and retrieve the page that has content with the highest similarity to the query# The Data Centre revenue results are on page 25 - for context!query = "What is approximately 85% of FY22 revenue in Canada?"results = model.search(query, k=5)print(f"Search results for '{query}':")for result in results: print(f"Doc ID: {result.doc_id}, Page: {result.page_num}, Score: {result.score}")print("Test completed successfully!") ```

The retrieval step takes about 185 ms.

``` %%timeitmodel.search(query, k=5) ```

## Llama-3.2 90B Vision Model.

Since we stored the collection along with the index, we also have the base64-encoded images of all PDF pages. This allows the system to retrieve the base64 image of the top result, enabling the matching page to be displayed visually.

The retrieved page or its base64-encoded version is then passed as **returned_page** for further use

``` # Since we stored the collection along with the index we have the base64 images of all PDF pages aswell!model.search(query, k=1) ``` ``` returned_page = model.search(query, k=1)[0].base64 ```

### Ollama

We use the Llama 3.2 Vision model, which simplifies the process by allowing us to pass in an image and either extract text or ask questions about the image. The Llama 3.2 Vision model is a 9-billion-parameter model that performs well on most OCR tasks. I run the Llama 3.2 Vision model locally on my MacBook using Ollama. To use the Llama 3.3 Vision model, you need Ollama 0.40, currently available as a pre-release.

```python import ollamaresponse = ollama.chat( model="x/llama3.2-vision", messages=[{ "role": "user", "content": query, "images": [returned_page] }],)# Extract cleaned textcleaned_text = response['message']['content'].strip()print(cleaned_text) ```

## Conclusion:

ColPali is a significant advancement in multimodal document retrieval, combining the strengths of VLM with innovative architectural choices. It efficiently processes and retrieves information from complex documents, positioning itself as a valuable tool in evolving AI-driven data analysis and retrieval systems.

Llama-OCR is an excellent assistant for developers and content creators. With the help of advanced AI models, it easily meets the OCR processing needs of complex documents. Direct output in Markdown format adds even more convenience and efficiency!

> **_🧙‍♂️ I am an AI Generative expert! If you want to collaborate on a project, drop an_**[** _inquiry here_**](<https://docs.google.com/forms/d/e/1FAIpQLSelxGSNOdTXULOG0HbhM21lIW_mTgq7NsDbUTbx4qw-xLEkMQ/viewform>)** _or Book a_**[** _1-on-1 Consulting_**](<https://calendly.com/gao-dalie/ai-consulting-call>)** _Call With Me._**

_📚Feel free to check out my other articles:_

## [Hybrid RAG + Fine-Tuning Your Dataset Python Project: Easy AI/Chat for your DocsWhen we find that AI cannot answer our questions correctly, the way we thought of earlier is to use retrieval to make…pub.towardsai.net](</hybrid-rag-fine-tuning-your-dataset-python-project-easy-ai-chat-for-your-docs-6270dfa559f2?source=post_page-----058c0dd3b59f--------------------------------------->)

## [LangGraph + Corrective RAG + RAG Fusion Python Project: Easy AI/Chat for your DocsIn this video, I have a super quick tutorial for you showing how to create a fully local chatbot with LangGraph…levelup.gitconnected.com](<https://levelup.gitconnected.com/langgraph-corrective-rag-rag-fusion-python-project-easy-ai-chat-for-your-docs-852a4248c0bc?source=post_page-----058c0dd3b59f--------------------------------------->)

## [Browser-use + LightRAG Agent That Can Scrape 99% websites with LLM!!In this story, I have a quick tutorial showing how to create a powerful chatbot using Browser-use, LightRAG, and a…pub.towardsai.net](</browser-use-lightrag-ollama-agent-that-can-scrape-any-website-e5694789efa0?source=post_page-----058c0dd3b59f--------------------------------------->)

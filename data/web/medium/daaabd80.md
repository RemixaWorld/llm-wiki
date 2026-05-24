---
domain: levelup.gitconnected.com
fetch_date: '2026-05-18T12:48:41.314776'
status: ok
url: https://levelup.gitconnected.com/exploring-multimodal-rag-with-llamaindex-and-gpt-4-or-the-new-anthropic-sonnet-model-96705c877dbb
---

# Exploring Multimodal RAG with LlamaIndex and GPT-4 or the New Anthropic Sonnet Model

[ ![Marco Bertelli](https://miro.medium.com/v2/resize:fill:64:64/1*9rlc-i8umqRTVqC1lZLngQ.jpeg) ](<https://medium.com/@marco.bertelli?source=post_page---byline--96705c877dbb--------------------------------------->)

[Marco Bertelli](<https://medium.com/@marco.bertelli?source=post_page---byline--96705c877dbb--------------------------------------->)

15 min read

·

Sep 1, 2024

\--

Listen

Share

More

Press enter or click to view image in full size

Multi-modal Rag’s Workflow

Today, we’ll explore how to build a Multimodal Retrieval-Augmented Generation (RAG) system using LlamaIndex in combination with GPT-4 or the new Anthropic Sonnet model. But first, what exactly is a Multimodal RAG?

Multimodal Retrieval-Augmented Generation (RAG) is an advanced AI framework that integrates multiple data modalities — such as text, images, or audio — with retrieval-augmented generation. This approach enhances the generation of responses by incorporating relevant information retrieved from external sources or databases, like a vector database in our case.

## In a Multimodal RAG system:

1. **Retrieval** : The model retrieves pertinent information from external databases or knowledge sources based on a given query. This retrieval process can involve various types of data, such as images, text, or other formats.
2. **Augmented Generation** : The model then uses this retrieved information to enrich and improve the generation of responses. It synthesizes the information to produce coherent and contextually relevant outputs across multiple modalities.

For instance, a multimodal RAG model might respond to a text query by pulling relevant images or audio clips from a database and integrating them into the final output. This approach results in richer, more informative responses that leverage different data types.

**New to the World of RAG?**

If you’re new to RAG, I recommend starting with the basics before diving into this advanced topic. Check out the article “[**RAG: From Theory to Production**](<https://medium.com/gitconnected/frontend-rag-mastery-deploying-with-aws-github-and-legacy-integration-3cdd875f5c5e>)” where you’ll find comprehensive resources, from the theoretical foundations of RAG to deploying a fully functional RAG server in production.

**Implementing the RAG System with LlamaIndex**

So, how do we go about implementing this RAG system? We’ll be using LlamaIndex. I found a foundational example from Jerry Liu, which I’ve adapted and expanded for this tutorial. Here’s what we will cover:

1. **Retrieving the Page and Document Name** : We’ll start by setting up the system to identify where the LLM (Large Language Model) will locate the information necessary to answer our queries. Essentially, we’ll pinpoint that the response was found on page X of document Y.
2. **Building a Multimodal Query Engine** : From scratch, we’ll construct a Multimodal Query Engine that analyzes and processes queries involving both images and text. This engine will utilize a multimodal model to generate more complex and nuanced responses.
3. **Creating an Agent with Reranking Capabilities** : Using our Multimodal Query Engine, we’ll build an agent that incorporates reranking. Reranking refers to refining and enhancing the quality of documents or passages retrieved from a knowledge source (such as a database or large corpus) before the model generates the final response.

Now that we’ve outlined the key points we’ll explore today, it’s time to dive into the code. As we go through each step, I’ll also provide a theoretical explanation of the underlying concepts. The following code is presented in a Medium notebook, and I’ll share a link later so you can interact with it directly.

```python %pip install llama-index llama-parse llama-index-multi-modal-llms-openai git+https://github.com/openai/CLIP.git llama_index.postprocessor.cohere_rerank ```

First of all we need to install some dependencies for our notebook.

```bash !wget https://github.com/user-attachments/files/16461058/data.zip -O data.zip!unzip -o data.zip!rm data.zip!mkdir files!cp ./data/fredde.pdf ./files ```

Next, we need to download the files we want to parse. For our example, we’ve chosen an IKEA product manual. This is an excellent multimodal example because these manuals typically contain little to no text but are rich in images, making it a challenging dataset to process and respond to. Here’s a sample page:

Press enter or click to view image in full size

Sample Page That Show A Complex Layout To Parse ```python import osos.environ["OPENAI_API_KEY"] = "xxx"os.environ["LLAMA_CLOUD_API_KEY"] = "xxx"os.environ["COHERE_API_KEY"] = "xxx" ```

For our sample before start make sure to have those api key’s.

```python from llama_parse import LlamaParseparser = LlamaParse( result_type="markdown", parsing_instruction="You are given IKEA assembly instruction manuals", use_vendor_multimodal_model=True, vendor_multimodal_model_name="openai-gpt4o", show_progress=True, verbose=True, invalidate_cache=True, do_not_cache=True, num_workers=8, # Setting language language="en") ```

Now it’s time to start parsing the files. To do this, we’ll use the **LlamaParse** library. Why choose this library? Because it offers a range of prebuilt features that are perfect for our needs. Here’s how it helps in our example:

* **Prompt Instruction for Parsing** : We can instruct the parser that we’re working with an IKEA manual, allowing it to optimize the parsing process accordingly.
* **OCR Support** : Since we’re building a Multimodal Query Engine, we need both text and images. LlamaParse makes this easy by providing prebuilt tools for extracting images from the pages and the text within those images.
* **Language Support** : If your files are in different languages, you can specify the language to improve the parser’s performance and accuracy.

```python DATA_DIR = "files"def get_data_files(data_dir=DATA_DIR) -> list[str]: files = [] for f in os.listdir(data_dir): fname = os.path.join(data_dir, f) if os.path.isfile(fname): files.append(fname) return filesfiles = get_data_files()print(files[0]) ```

This is a small helper to get all the files list.

``` md_json_objs = parser.get_json_result(files)image_dicts = parser.get_images(md_json_objs, download_path="data_images") ```

Now it’s time to use our previously instantiated parser to extract both JSON results and images from the document. We’ll also specify the path where the extracted images should be saved. To extract text from images, LlamaParse utilizes OCR technology under the hood:

**OCR** stands for **Optical Character Recognition**. It is a technology that enables the conversion of different types of documents, such as scanned paper documents, PDFs, or images captured by a camera, into machine-readable and editable text.

Press enter or click to view image in full size

OCR Workflow

## How OCR Works:

1. **Image Acquisition** : OCR begins with acquiring an image that contains text. This could be from a scanner, a photograph, or any other image source.
2. **Preprocessing** : The image may undergo preprocessing to enhance its quality for better recognition. This can include steps like noise reduction, binarization (converting the image to black and white), deskewing (correcting any tilt), and other image enhancement techniques.
3. **Text Detection** : The OCR system detects and locates the regions in the image where text is present. In some cases, it also involves segmenting the text into characters, words, or lines.
4. **Character Recognition** : The core of OCR involves recognizing the individual characters within the detected text regions. This is typically done by comparing the detected shapes of characters to a library of character shapes, or by using machine learning models trained on large datasets of text images.
5. **Post-processing** : After recognizing the characters, OCR software often applies post-processing techniques to improve accuracy. This might include spell-checking, context analysis, and formatting restoration.
6. **Output** : The final step is to convert the recognized text into a machine-readable format, such as a plain text file, PDF, Word document, or other editable formats.

```python import refrom pathlib import Pathimport typing as tfrom llama_index.core.schema import TextNodedef get_page_number(file_name): """Gets page number of images using regex on file names""" match = re.search(r"-page-(\d+)\\.jpg$", str(file_name)) if match: return int(match.group(1)) return 0def _get_sorted_image_files(image_dir): """Get image files sorted by page.""" raw_files = [f for f in list(Path(image_dir).iterdir()) if f.is_file()] sorted_files = sorted(raw_files, key=get_page_number) return sorted_filesdef get_text_nodes(md_json_objs, image_dir) -> t.List[TextNode]: """Creates nodes from json + images""" nodes = [] for result in md_json_objs: json_dicts = result["pages"] document_name = result["file_path"].split('/')[-1] print(json_dicts) docs = [doc["md"] for doc in json_dicts] # extract text image_files = _get_sorted_image_files(image_dir) # extract images for idx, doc in enumerate(docs): # adds both a text node and the corresponding image node (jpg of the page) for each page node = TextNode( text=doc, metadata={"image_path": str(image_files[idx]), "page_num": idx + 1, "document_name": document_name}, ) nodes.append(node) return nodestext_nodes = get_text_nodes(md_json_objs, "data_images") ```

Next, we define a series of functions to create nodes from our JSON object and images folder. For each result, a node is created, and each node contains useful metadata that will be utilized later. Here’s a breakdown of the key elements:

1. **Image Path** : This metadata indicates the location of the actual image file. It allows us to retrieve and reference the image when needed.
2. **Page Number** : This metadata stores the page number from which the image was extracted. This information will be crucial for referencing and constructing results later in our process.
3. **Image Information** : Two additional helper fields are included to capture specific details about the images, such as their dimensions or format.

To provide visibility into the structure of our nodes, we also include a print statement. This will allow you to see how each node is composed, including the metadata and any other relevant details.

This setup ensures that each node is well-defined and contains all the necessary information for subsequent processing and querying.

```python from llama_index.core import ( VectorStoreIndex, StorageContext, load_index_from_storage, Settings,)from llama_index.embeddings.openai import OpenAIEmbeddingfrom llama_index.llms.openai import OpenAIembed_model = OpenAIEmbedding(model="text-embedding-3-large")llm = OpenAI("gpt-4o")Settings.llm = llmSettings.embed_model = embed_modelif not os.path.exists("storage_manuals"): index = VectorStoreIndex(text_nodes, embed_model=embed_model) index.storage_context.persist(persist_dir="./storage_manuals")else: ctx = StorageContext.from_defaults(persist_dir="./storage_manuals") index = load_index_from_storage(ctx)retriever = index.as_retriever() ```

Now that we have our parsed nodes with all the necessary metadata, the next step is to create an index. For our multimodal model, we’re using **GPT-4o** for the generative capabilities and the latest OpenAI `text-embedding-3-large` for embeddings. These choices ensure high-quality performance in both understanding and generating responses. For detailed guidance on selecting models and embeddings, refer to the earlier articles mentioned in the introduction.

Once the index is created, we need to instantiate a retriever from it. Typically, you would directly instantiate the query engine. However, in this case, we’re building the query engine from scratch, which requires setting up a lower-level retriever instance. This approach allows for more granular control and customization of the retrieval process, tailored specifically to our needs.

In summary:

1. **Create the Index** : Use the chosen model (GPT-4o) and embeddings (text-embedding-3-large) to build the index from our parsed nodes.
2. **Instantiate the Retriever** : Develop a retriever instance from the index, which will be used to facilitate detailed querying and retrieval in our custom-built query engine.

This setup ensures that we have both a robust indexing system and a flexible retrieval mechanism to support our multimodal RAG system.

```python from llama_index.core.query_engine import CustomQueryEnginefrom llama_index.core.retrievers import BaseRetrieverfrom llama_index.multi_modal_llms.openai import OpenAIMultiModalfrom llama_index.core.schema import NodeWithScore, MetadataMode, QueryBundlefrom llama_index.core.base.response.schema import Responsefrom llama_index.core.prompts import PromptTemplatefrom llama_index.core.schema import ImageNodefrom typing import Any, List, Optional, Tuplefrom llama_index.core.postprocessor.types import BaseNodePostprocessorQA_PROMPT_TMPL = """\You are a chatbot that will help users to get technical responses about and ikea product manual.Below we give parsed text from slides in two different formats, as well as the image.We parse the text in both 'markdown' mode as well as 'raw text' mode. Markdown mode attempts \to convert relevant diagrams into tables, whereas raw text tries to maintain the rough spatial \layout of the text.Use the image information first and foremost. ONLY use the text/markdown information if you can't understand the image.When you reply dosen't send images links, but only text explaination of that.Context:---------------------{context_str}---------------------Given the context information and not prior knowledge, answer the query using ONLY Context informations, if you dosen't find the answer in the Context NOT try to answer, reply that you dosen't know and give a page and document name where the user can find similar response.Give the page's number and the document name where you find the response based on the Context.Query: {query_str}Answer: """QA_PROMPT = PromptTemplate(QA_PROMPT_TMPL)gpt_4o_mm = OpenAIMultiModal(model="gpt-4o")class MultimodalQueryEngine(CustomQueryEngine): qa_prompt: PromptTemplate retriever: BaseRetriever multi_modal_llm: OpenAIMultiModal node_postprocessors: Optional[List[BaseNodePostprocessor]] def __init__( self, qa_prompt: PromptTemplate, retriever: BaseRetriever, multi_modal_llm: OpenAIMultiModal, node_postprocessors: Optional[List[BaseNodePostprocessor]] = [], ): super().__init__( qa_prompt=qa_prompt, retriever=retriever, multi_modal_llm=multi_modal_llm, node_postprocessors=node_postprocessors ) def custom_query(self, query_str: str): # retrieve most relevant nodes nodes = self.retriever.retrieve(query_str) for postprocessor in self.node_postprocessors: nodes = postprocessor.postprocess_nodes( nodes, query_bundle=QueryBundle(query_str) ) # create image nodes from the image associated with those nodes image_nodes = [ NodeWithScore(node=ImageNode(image_path=n.node.metadata["image_path"])) for n in nodes ] # create context string from parsed markdown text ctx_str = "

".join( [r.node.get_content(metadata_mode=MetadataMode.LLM).strip() for r in nodes] ) # prompt for the LLM fmt_prompt = self.qa_prompt.format(context_str=ctx_str, query_str=query_str) # use the multimodal LLM to interpret images and generate a response to the prompt llm_repsonse = self.multi_modal_llm.complete( prompt=fmt_prompt, image_documents=[image_node.node for image_node in image_nodes], ) return Response( response=str(llm_repsonse), source_nodes=nodes, metadata={"text_nodes": text_nodes, "image_nodes": image_nodes}, ) ```

This is the core of our implementation: building the **MultiModalQuery Engine**. Let’s break down its components and functionality:

## Core Components:

**Prompt** : At the heart of our reasoning system is the prompt. In this prompt, we instruct the model to prioritize images as the primary source of information and to avoid responding with URLs. We also specify that the query engine should focus solely on the context of the query, meaning it won’t handle unrelated questions. This approach is particularly useful for QA systems. Additionally, we direct the model to include information about the page number in its responses.

**CustomQueryEngine** : We use a LlamaIndex class called `CustomQueryEngine` for our query engine. This class requires several arguments:

* **Prompt** : The one we defined earlier, which guides the model’s responses.
* **Retriever** : The storage system we’ve set up to handle our indexed data.
* **Multimodal Model** : The model used for processing both text and images.
* **Node Postprocessors** : These are used to refine the retrieved nodes. A detailed list of available node postprocessors can be found on the LlamaIndex website. For this tutorial, we’ll focus on the reranking node postprocessor, which we’ll discuss in detail later.

**Custom Query Function** : After setting up the `CustomQueryEngine`, we define a `custom_query` function. This function performs the following steps:

* **Retrieve Nodes** : It uses our retriever to fetch a list of nodes based on the query.
* **Apply Node Postprocessors** : If any node postprocessors are defined, they are applied to the retrieved nodes to enhance their quality.
* **Create Image Nodes and Context String** : We separate the images into `image_nodes` and compile all text information into a `context_string`.
* **Construct Prompt** : We build the prompt for the LLM by combining our pre-defined prompt with the retrieved nodes.
* **Invoke Multimodal LLM** : Finally, we make a call to the multimodal LLM, providing both text and images, and obtain a response.

This setup ensures that our MultiModalQuery Engine is well-equipped to handle complex queries involving both text and images, delivering precise and contextually relevant responses.

Press enter or click to view image in full size

Reraning Workflow For Undestand Better

Reranking in the context of **Retrieval-Augmented Generation (RAG)** is an advanced technique used to improve the relevance of the documents or passages that are retrieved before they are passed to the generation model. Here’s how it fits into the RAG workflow:

## RAG Overview:

1. **Query or Input** : The process starts with a query or input prompt.
2. **Document Retrieval** : The system retrieves a set of potentially relevant documents or passages from a large corpus using a retrieval model (e.g., BM25, Dense Passage Retriever).
3. **(Optional) Reranking** : The retrieved documents are reranked to better prioritize the most relevant ones.
4. **Generation** : The top-ranked documents are then used by the generation model (usually a transformer-based model) to produce a final response.

## Reranking Process in RAG:

1. **Initial Retrieval** : When a query is issued, the retriever model identifies a list of documents or passages that are most likely relevant to the query based on some scoring mechanism (like cosine similarity in vector space models).
2. **Reranking Model** : After the initial retrieval, a reranking model is applied. This model takes the top-N documents (where N might be 10, 20, etc.) and reorders them based on a more nuanced evaluation of their relevance. The reranking model might use additional features, such as:

* Deeper contextual understanding (e.g., semantic relationships).
* Query-document relevance computed with a more sophisticated model, like a cross-encoder that evaluates the query and document together.
* Other signals like metadata, document length, or recency.

**Selection for Generation** : After reranking, the most relevant documents are selected to be fed into the generator model. This helps ensure that the generation model has access to the most pertinent information, leading to better, more accurate responses.

## Why Reranking is Important in RAG:

* **Improves Response Quality** : By reranking, the system can ensure that the most contextually relevant information is prioritized, which directly impacts the quality of the generated response.
* **Handles Ambiguity Better** : Reranking helps in cases where the initial retriever might return documents that are only tangentially related to the query, ensuring that truly relevant documents are used.
* **Efficient Use of Resources** : Since generation models can be computationally expensive, reranking ensures that only the best candidates are used, optimizing resource use.

```python from llama_index.postprocessor.cohere_rerank import CohereRerankapi_key = os.environ["COHERE_API_KEY"]cohere_rerank = CohereRerank(api_key=api_key, top_n=3, model="rerank-multilingual-v3.0")# Insert reranking here only if after some test it increase the accuracyquery_engine = MultimodalQueryEngine( qa_prompt=QA_PROMPT, retriever=index.as_retriever(similarity_top_k=9), multi_modal_llm=gpt_4o_mm, node_postprocessors=[]) ```

Now it’s time to instantiate our **MultimodalQueryEngine** and prepare the node postprocessor for reranking. Although we won’t be using the reranker for our initial tests, it’s important to understand its role and configuration.

## Setting Up the MultimodalQueryEngine:

1. **Instantiate MultimodalQueryEngine** : Create an instance of the `MultimodalQueryEngine` using the previously defined components: the prompt, retriever, multimodal model, and any necessary node postprocessors.
2. **Prepare Node Postprocessor for Reranking** : Even though we won’t utilize the reranker in our test, it’s useful to configure it for future use. If you decide to implement a reranker, remember to increase the `similarity_top_k` number. This parameter controls how many of the top nodes are considered by the reranker. As previously discussed, the reranker will ultimately use only a subset of the nodes passed to it, so adjusting this number can impact the quality of your results.

## Final Step: Testing

With the `MultimodalQueryEngine` and reranking configuration in place, it's time to perform some tests. This will help you verify that the engine is functioning correctly and producing the desired results. Testing will also give you insights into how well the engine handles queries and integrates text with images.

```python from IPython.display import display, Markdownresponse = query_engine.query("What parts are included in the Uppspel?")display(Markdown(str(response))) ```

Response: I don’t have information about the parts included in the Uppspel. However, you can refer to the document “fredde.pdf” on page 2 for tools required and general assembly instructions, and other pages for specific steps and parts used in the assembly process.

Amazing, it dosen’t know the info but guide us to the page

``` response = query_engine.query("What does the FREDDE look like?")display(Markdown(str(response))) ```

Response: The FREDDE desk is a multi-functional desk with a modern design. It features a main desk surface with additional shelves and brackets for extra storage and organization. The desk has a sturdy frame with multiple levels, including a top shelf and side shelves. The design allows for efficient use of space, making it suitable for various activities such as working on a computer, studying, or gaming.

For more detailed visual instructions on assembling the FREDDE desk, you can refer to the following pages in the “fredde.pdf” document:

* Page 1
* Page 23
* Page 24
* Page 29
* Page 30
* Page 31
* Page 32

Amazing again, it was able to describe a page and also give us pages where to find more info of a “complete” product.

``` response = query_engine.query("What should I do if I'm confused with reading the manual?")display(Markdown(str(response))) ```

Response: If you are confused with reading the manual, you should contact IKEA for assistance. This information can be found on page 2 of the document “fredde.pdf”.

### Perfect for QA

Our system effectively answers queries by providing the exact solution, including the page number and document location for the IKEA contact information.

## Creating an Agent with Our Query Engine

Now, let’s move on to the final part of our article: constructing an **Agent** using our query engine.

An **RAG Agent** is an advanced AI system that integrates Retrieval-Augmented Generation (RAG) techniques with agent-based frameworks. This combination allows the agent to:

1. **Retrieve Relevant Information** : The agent can access and extract pertinent information from a large dataset using retrieval techniques. This ensures that the information is accurate and relevant to the query.
2. **Generate Contextually Accurate Responses** : Based on the retrieved information, the agent can generate responses or take actions that are contextually appropriate. This makes the system highly effective for applications requiring detailed and accurate answers, such as customer support or complex information retrieval tasks.

By leveraging our custom `MultimodalQueryEngine`, the RAG Agent can handle both text and image data, providing rich, contextually informed responses.

```python from llama_index.core.agent import FunctionCallingAgentWorkerfrom llama_index.core.tools import QueryEngineToolquery_engine_tool = QueryEngineTool.from_defaults( query_engine=query_engine, name="query_engine_tool", description="Useful for retrieving specific context from the data. Do NOT select if question asks for a summary of the data.",)agent = FunctionCallingAgentWorker.from_tools( [query_engine_tool], llm=llm, verbose=True).as_agent() ```

As you can see, using LlamaIndex simplifies the process significantly. With just a few steps, we can transform our query engine into a powerful tool for real-world applications. Here’s how it works:

### Building the Query Engine Tool

1. **Create**`**query_engine_tool**`: Using the previously defined `query_engine`, we build a `query_engine_tool`. This tool encapsulates the query engine's functionality, allowing us to easily integrate it into various applications.
2. **Instantiate**`**FunctionCallingAgentWorker**`: With the `query_engine_tool` in place, we can create a `FunctionCallingAgentWorker`. This agent utilizes the tool to perform complex tasks, such as executing function calls and generating responses based on queries.

### Real-World Test

Let’s see this setup in action with a real-world test. By applying the `FunctionCallingAgentWorker` to a practical scenario, we can observe how effectively it handles queries and generates contextually relevant responses using the multimodal capabilities of our query engine.

``` response = agent.chat( "How do I assemble the Fredde, the first 3 steps?")display(Markdown(str(response))) ```

Reponse:

### Step 1

1. Insert the screw (100181) into the hole of the metal frame.
2. Tighten the screw.
3. Ensure the screw is properly secured and not loose.

### Step 2

1. Align the metal rod with the frame.
2. Insert the rod into the frame.
3. Rotate the rod to secure it in place.

### Step 3

1. Insert 2x part 108430 into the designated slots.

For more detailed instructions and visual aids, refer to pages 5 and 15 of the document “fredde.pdf”.

## Conclusion

Once again, the results are impressive. While the information may not be 100% accurate, it’s important to remember that much of it is derived from images — an inherently challenging data type to process.

> That wraps up our exploration for today! If you found this article helpful and want to support me, please leave some claps, a comment, and subscribe to boost the article’s visibility on Medium. Your feedback and support are greatly appreciated!

If you have any questions or need further assistance, feel free to ask in the comments. I’m here to help and hope you found this article useful. For those interested in diving deeper, you can access the full article code here: [Full Article Code](<https://colab.research.google.com/drive/1PcuVqUQjacMt18p8LwODnjbsXOFMurwa?usp=sharing>).

Thank you for your time!

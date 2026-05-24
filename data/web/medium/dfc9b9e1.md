---
domain: levelup.gitconnected.com
fetch_date: '2026-05-18T12:45:01.795932'
status: ok
url: https://levelup.gitconnected.com/a-guide-to-processing-tables-in-rag-pipelines-with-llamaindex-and-unstructuredio-3500c8f917a7
---

# A Guide to Processing Tables in RAG Pipelines with LlamaIndex and UnstructuredIO

[ ![Ryan Nguyen](https://miro.medium.com/v2/resize:fill:64:64/1*Me7djoCkDU1iDjo3VCqTnw@2x.jpeg) ](<https://medium.com/@ryanntk?source=post_page---byline--3500c8f917a7--------------------------------------->)

[Ryan Nguyen](<https://medium.com/@ryanntk?source=post_page---byline--3500c8f917a7--------------------------------------->)

10 min read

·

Dec 17, 2023

\--

Listen

Share

More

From PDF to HTML: Streamlining Table Extraction for Robust RAG Implementations. A better way (yet)?

Press enter or click to view image in full size

By Author

One common challenge with RAG (Retrieval-Augmented Generation) involves handling PDFs that contain tables. Parsing tables in various formats can be quite complex.

In my previous article

## [RAG Pipeline Pitfalls: The Untold Challenges of Embedding TableA typical journey of building the RAG pipeline from Zero to Something and a guide on handling tables of RAG with…pub.towardsai.net](<https://pub.towardsai.net/rag-pipeline-pitfalls-the-untold-challenges-of-embedding-table-5296b2d8230a?source=post_page-----3500c8f917a7--------------------------------------->)

I’ve already discussed a few methods for dealing with complicated PDFs that contain a lot of tables, including 10k financial reports, insurance documents, court records, medical bills, etc.

Since I get into further detail about tactics and their application, I strongly advise you to read the aforementioned paper. If you’re feeling particularly lazy, though, here’s a brief rundown of how complicated PDFs with tables are approached.

* Normal Python libraries and OCR approach: Extract tables and the text around the tables to get more context
* Cloud Platform: AWS with AWS Textract, Adobe’s API, Apryse SDK, etc
* New kid in the block: [**UnstructuredIO**](<https://github.com/Unstructured-IO/unstructured>)**.**

Ever since the post came out, the landscape surrounding large language models (LLMs) has evolved significantly. A noteworthy stride in this domain is the emergence of GPT-4V, a formidable iteration with enhanced capabilities encompassing both textual and visual processing. This combination of text and image understanding represents a significant breakthrough that broadens the scope of what LLMs are capable of. **_Microsoft has also entered the market with Table Transformer_** , a product that strengthens document retrieval by extracting and enhancing tables from photos. This creative innovation highlights the industry’s dedication to expanding the capabilities of these models in the fields of text and picture manipulation, as well as the vitality of LLM advances.

The general ideas around this approach fall into 1 of the 4 bellow options:

1. Retrieving relevant images (PDF pages) and sending them to GPT4-V to respond to queries.
2. Regarding every PDF page as an image, let GPT4-V do the image reasoning for each page. Build Text Vector Store index for the image reasonings. Query the answer against the `Image Reasoning Vectore Store`.
3. Using `Table Transformer` to crop the table information from the retrieved images and then send these cropped images to GPT4-V for query responses
4. Applying OCR on cropped table images and send the data to GPT4/ GPT-3.5 to answer the query.

You can find more of the experiment in this [**post**](<https://docs.llamaindex.ai/en/stable/examples/multi_modal/multi_modal_pdf_tables.html>) from [**LlamaIndex**](<https://docs.llamaindex.ai/en/stable/index.html>)**.**

The problem with this, though, is that it relies on GPT4-V and pre-trains Microsort’s model to identify tables in the PDF. This approach treats each table as an image and requests that GPT4-V provide a summary or other details, leaving Microsort’s model unable to fully comprehend what the table actually represents.

I have tried the GPT4-V and table transformer approach on the simple document “The World Billionaires 2023” and the result is rather disappointing compared to the approach I have with **UnstructuredIO**.

In this post, I will dig into the details of building blocks to get RAG to work on complex PDFs.

> Though each sort of PDF may call for a different strategy, this is a decent general technique that may be used as a starting point. Please note that this approach may not work for all complex PDFs, and this guide serves as a starting point.

I’ll assume that the reader is already acquainted with RAG pipelines and LlamaIndex. If not, feel free to peruse every one of my earlier postings in my substack, beginning with

## [Zero to One: A Guide to Building a First PDF Chatbot with LangChain & LlamaIndex — Part 1Welcome to Part 1 of our engineering series on building a PDF chatbot with LangChain and LlamaIndex. Don’t worry, you…medium.com](<https://medium.com/how-ai-built-this/zero-to-one-a-guide-to-building-a-first-pdf-chatbot-with-langchain-llamaindex-part-1-7d0e9c0d62f?source=post_page-----3500c8f917a7--------------------------------------->)

then [how to use Llama’s index](<https://medium.com/better-programming/llamaindex-how-to-use-index-correctly-6f928b8944c6>), [how to use storage with LlamaIndex](<https://medium.com/@ryanntk/llamaindex-comprehensive-guide-on-storage-99ca9851be9c>), [choose the right embedding model](<https://medium.com/@ryanntk/choosing-the-right-embedding-model-a-guide-for-llm-applications-7a60180d28e3>) and finally [deploy in production](<https://medium.com/@ryanntk/deploying-hugging-face-embedding-models-on-aws-sagemaker-a-comprehensive-tutorial-with-langchain-af8e0b405b51>)

If you need a quick guide on how to improve your RAG pipeline, please refer to my previous post

## [So, You Want To Improve Your RAG PipelineWays to go from prototype to production with LlamaIndexpub.towardsai.net](<https://pub.towardsai.net/so-you-want-to-improve-your-rag-pipeline-28b0cfadbfd7?source=post_page-----3500c8f917a7--------------------------------------->)

And if you need to evaluate your RAG performance, then this long-form post will help:

## [LlamaIndex: How To Evaluate Your RAG (Retrieval Augmented Generation) ApplicationsClassic 10k reports with Australian real estate market reports to demonstrate the end-to-end evaluation processbetterprogramming.pub](<https://betterprogramming.pub/llamaindex-how-to-evaluate-your-rag-retrieval-augmented-generation-applications-2c83490f489?source=post_page-----3500c8f917a7--------------------------------------->)

Back to our main story, here is how to implement the UnstructuredIO with complex PDFs.

> You **MUST** use either Linux or Ubuntu on the Windows subsystem or Google Colab to install the necessary libraries. I’m saving you time and energy, so don’t try to do it in a normal Windows environment.

## Convert PDF into HTML

Why?

First, let’s clear this up immediately: This problem cannot be solved easily or conventionally! As previously stated, industry professionals and open-source communities are actively working to overcome the challenges of developing a productive way to parse PDFs. The state of the art indicates that using open-source technologies like [UnstructredIO](<https://github.com/Unstructured-IO/unstructured>) or cloud-based solutions like AWS or Adobe has drawbacks of its own. These methods can have unreasonably high costs, and their processing speeds frequently verge on being unworkable and sluggish. It highlights the difficulty and necessity of the continuous search for a quicker and easier method to decipher the complexities woven within PDF files.

> We’ll use a file conversion today to enable the implementation’s least frictional version in order to solve the problem.

One way we can do this is to convert PDF files into HTM/HTML file format. Many open-source frameworks can do this, but I found pdf2htmlEX is particularly notable for its ease of use and efficiency. We will then use [UnstructuredIO](<https://github.com/Unstructured-IO/unstructured>) with [LlamaIndex ](<https://www.llamaindex.ai/>)to process the HTML file

### Install libraries

* Install pdf2htmlEX

```bash !wget https://github.com/pdf2htmlEX/pdf2htmlEX/releases/download/v0.18.8.rc1/pdf2htmlEX-0.18.8.rc1-master-20200630-Ubuntu-bionic-x86_64.deb!sudo apt install "./pdf2htmlEX-0.18.8.rc1-master-20200630-Ubuntu-bionic-x86_64.deb" -y!sudo apt update ```
* Install Python libraries

```python !pip install llama-index unstructured['all-docs'] ```

### Utilities function/command to convert PDF to HTML

* With Python

```python import subprocessdef convert_pdf_to_html(pdf_path): command = f"pdf2htmlEX {pdf_path}" subprocess.call(command, shell=True)input_pdf = "The_Worlds_Billionaires.pdf"convert_pdf_to_html(input_pdf) ```
* With Linux command

``` !pdf2htmlEX The_Worlds_Billionaires.pdf ```

With the right tools and the HTML file ready, we will now go to the main part. **RAG on HTML file.**

## Data Retrieval with LlamaIndex and UnstructuredIO

If you are familiar with LlamaIndex, you already know this framework offers a variety of tools and techniques to improve data retrieval. **_The central heart of this framework is the Index_**. The flexibility of LlamaIndex allows users to customize their selection of index according to the particular details of the document in question, which is what makes it so beautiful. Every index type has distinct features that offer a tailored strategy to accommodate different document structures. For a brief overview of the available index possibilities, detailed instructions can be found [here](<https://medium.com/better-programming/llamaindex-how-to-use-index-correctly-6f928b8944c6>) and [here](<https://docs.llamaindex.ai/en/stable/module_guides/indexing/indexing.html>), providing an understanding of the wide range of options available to you. These resources are helpful manuals for understanding the vast array of tools that LlamaIndex reveals to optimize data retrieval.

For PDFs with a lot of tables, I usually go with [**RecursiveRetriever**](<https://docs.llamaindex.ai/en/stable/examples/query_engine/recursive_retriever_agents.html>)**** as it is recommended by LlamaIndex. The concept of recursive retrieval is that we not only explore the directly most relevant nodes, but also explore node relationships to additional retrievers/query engines and execute them. For instance, a node may represent a concise summary of a structured table, and link to a SQL/Pandas query engine over that structured table. Then if the node is retrieved, we want to also query the underlying query engine for the answer.

You can read more about [Recursive Retriever here](<https://docs.llamaindex.ai/en/stable/examples/query_engine/recursive_retriever_agents.html>) and [here](<https://docs.llamaindex.ai/en/stable/examples/query_engine/pdf_tables/recursive_retriever.html>)

By UnstructuredIO + LlamaIndex

Planning Strategy to implement this approach:

* Convert PDF to HTML (already covered)
* Read HTML with UnstructuredIO
* For each element that UnstructuredIO can read from HTML, we store text and table into LlamaIndex’s node.
* Now, we will have a list of nodes that either contain text or a table.
* **Optional** : loop through the list of node that contains the table only and send the table to LLM to get a summary of the table
* An LLM agent with the help of LlamaIndex recursively retrieves similar information with the question
* Send the retrieval data to LLM to get the response.

Does it seem complex enough? Yes. But with the help of LlamaIndex, there is a nicely wrapped function to help us implement those steps more easily.

### Read and process the Data

```python from llama_index.readers.file.flat_reader import FlatReaderfrom llama_index.node_parser import UnstructuredElementNodeParserimport osimport picklefrom pathlib import Pathos.environ["OPENAI_API_KEY"] = "<your openai api key>"# read the datareader = FlatReader()data = reader.load_data(Path('./The_Worlds_Billionaires.html'))# init NodeParsernode_parser = UnstructuredElementNodeParser()# in case you want to re-use it later.if not os.path.exists("qr_2023_nodes.pkl"): raw_nodes = node_parser.get_nodes_from_documents(data) pickle.dump(raw_nodes, open("the_world_billionaires_raw_nodes.pkl", "wb"))# base nodes and node mappingbase_nodes, node_mappings = node_parser.get_base_nodes_and_mappings( raw_nodes) ```

### Build Index

```python from llama_index.retrievers import RecursiveRetrieverfrom llama_index.query_engine import RetrieverQueryEnginefrom llama_index import VectorStoreIndexvector_index = VectorStoreIndex(base_nodes_qr_2023)vector_retriever = vector_index.as_retriever(similarity_top_k=3)vector_query_engine = vector_index.as_query_engine(similarity_top_k=3)recursive_retriever = RecursiveRetriever( "vector", retriever_dict={"vector": vector_retriever}, node_dict=node_mappings_qr_2023,)query_engine = RetrieverQueryEngine.from_args(recursive_retriever)query_engine.query("Who is the richest billionaire in 2020?") ```

### Other types of query index

The prior example demonstrates how well UnstructuredElementNodeParser integrates, demonstrating the effectiveness and convenience that LlamaIndex + UnstructuredIO offer in the field of data processing. It captures a simplified methodology, making the complexities of data extraction easier to understand.

Considering the wide range of index kinds and retrieval methods available in LlamaIndex, it’s worthwhile to investigate several options in order to determine the best course of action for your particular use case.

> Try experimenting with methods such as Auto Merging Retriever, Reranking, and Hybrid Search.

Every one of these strategies has special advantages, and the results can change based on the complexity of your data. Through this empirical investigation, you may optimize your retrieval procedure and make sure you’re using the best approach to draw out important insights from your dataset.

## How to extract tables from PDF/HTML

Since it covers lower API to enable table extraction from PDF/HTML, this part is optional. For your needs, it might be useful. The aforementioned method works well in most situations, but you will need to perform some data processing in between, such as passing data to LLM for a summary, if you need to access a lower API to have complete control over it. You might want to take a look at this section.

### Extracting table from PDFs

There are a lot of ORC techniques/libraries to help you with this as well as the Cloud option (which is a bit expensive). UnstructuredIO provides a **partition_pdf** with multiple parameters that allow you to control and balance between speed and accuracy as well as specific the deep learning model to help with better table extraction.

```python from unstructured.partition.pdf import partition_pdffrom unstructured.staging.base import elements_to_jsonimport json file_path = 'The_Worlds_Billionaires.pdf'raw_pdf_elements = partition_pdf( filename=file_path, extract_images_in_pdf=False, infer_table_structure=True, chunking_strategy='by_title', # Chunking params to aggregate text blocks # Attempt to create a new chunk 3800 chars # Attempt to keep chunks > 2000 chars max_characters=4000, new_after_n_chars=3800, combine_text_under_n_chars=2000, strategy = "hi_res")# Store results in jsonelements_to_json(raw_pdf_elements, filename=f"./The_Worlds_Billionaires_Converted.json")no_tables = 0def process_json_file(input_filename): # Read the JSON file with open(f'./{input_filename}.json', 'r') as file: data = json.load(file) # Iterate over the JSON data and extract required table elements extracted_elements = [] for entry in data: if entry['type'] == 'CompositeElement': extracted_elements.append(entry['text']) if entry["type"] == "Table": no_tables +=1 extracted_elements.append(entry["metadata"]["text_as_html"]) # Write the extracted elements to the output file with open(f"{input_filename}.txt", 'w') as output_file: for element in extracted_elements: output_file.write(element + "

") # Adding two newlines for separationprocess_json_file(f"The_Worlds_Billionaires_Converted") ## with new_file_name is a JSON file above print(f"Number of tables: {no_tables}")# ## load data# documents = SimpleDirectoryReader("./<folder_name>", # input_files=['./<new_file_name.txt>']).load_data() ```

This method will read a PDF file and output the **element** of the PDF such as text element or table element. The table element will be saved as “text_as_html” in a JSON format. You can read and process every individual element from a JSON file and store the processed data as a **txt** file for RAG to read later.

> The thing that needs to be considered here is performance. The performance is kinda bad when parsing PDFs directly. At the time of writing, UnstructredIO provides multiple models such as YOLOx to help you parse PDF into elements. However, these are deep neural network models so it does not perform well on lower-spec computer like mine. You can try it on a bigger machine with a fancy GPU. The only question here is how it performs on a scale with a thousand documents at the same time.

I will leave the link to the notebook at the end of the post.

## Summary

* Open-source projects and cloud providers alike clearly demonstrate the industry’s coordinated efforts to address the complexities of PDF processing.
* There’s no one-size-fits-all approach to managing complex PDFs in this ever-changing environment. Thus far, my research has led me to conclude that the utilization of LlamaIndex in conjunction with UnstructuredIO and PDF to HTML conversion is a very simple and efficient method that produces excellent outcomes.

Moreover, one important tactic to improve RAG accuracy is to carefully combine different indexes with different retrievers. This multifaceted approach recognizes that there is no one-size-fits-all set of indexing rules and emphasizes the need to tailor strategies to the particulars of each type of document and the subtleties of processing them. You may create a more accurate and sophisticated retrieval system that works with the complexities of your data by embracing this flexibility and using a customized mix of indexes and retrievers.

❤ If you found this post helpful, I’d greatly appreciate your support by giving it a clap. It means a lot to me and demonstrates the value of my work. Additionally, you can [subscribe to my substack](<https://howaibuildthis.substack.com/>) as I will cover more in-depth LLM development in that channel

``` Want to Connect?If you need to reach out, don't hesitate to drop me a message via my Twitter or LinkedIn and subscribe to my Substack, as I will covermore learning practices, especially the path of developing LLM in depth in my Substack channel. ```

## References

**Notebook** : [Google Colab](<https://colab.research.google.com/github/nguyenkien1402/llamaindex-practices/blob/main/table_unstructureio_processing/pdf_with_tables.ipynb>)

**UnstructuredIO** : <https://unstructured-io.github.io/unstructured/introduction.html#tables>

**LlamaIndex**

* [Auto Merging](<https://docs.llamaindex.ai/en/stable/examples/retrievers/auto_merging_retriever.html>)
* [Custom Retrievers](<https://docs.llamaindex.ai/en/stable/examples/query_engine/CustomRetrievers.html>)
* [Recursive Retriever + Document Agent](<https://docs.llamaindex.ai/en/stable/examples/query_engine/recursive_retriever_agents.html>)

**pdf2htmlLEX** : <https://github.com/pdf2htmlEX/pdf2htmlEX>

---
domain: medium.com
fetch_date: '2026-05-18T12:47:13.214258'
status: ok
url: https://medium.com/kx-systems/high-precision-rag-for-table-heavy-documents-using-langchain-unstructured-io-kdb-ai-22f7830eac9a
---

# High-Precision RAG for Table Heavy Documents… (Using LangChain, Unstructured.io, & KDB.AI)

[ ![Ryan Siegler](https://miro.medium.com/v2/resize:fill:64:64/1*pLl4RRdRDU5gC_E0xf1FZg.jpeg) ](</@ryan.siegler8?source=post_page---byline--22f7830eac9a--------------------------------------->)

[Ryan Siegler](</@ryan.siegler8?source=post_page---byline--22f7830eac9a--------------------------------------->)

13 min read

·

Aug 21, 2024

\--

\--

Listen

Share

More

Why does RAG on table rich documents suck?

![image](https://miro.medium.com/v2/resize:fit:700/1*bRljX4vUvqeGUOmkhbgMTA.png)

The Retrieval-Augmented Generation (RAG) revolution has been charging ahead for quite some time now, but it’s not without its bumps in the road — especially when it comes to handling non-text elements like images and tables. One challenge that’s been bugging me is the accuracy drop whenever I ask a RAG workflow to pull specific values from tables. It’s even worse when the document is packed with multiple tables on related topics, like in an earnings report. So, I set out on a mission to improve table retrieval within my RAG pipelines…

## Key Challenges:

1. Retrieval Inconsistency: Vector search algorithms often struggle to pinpoint the correct tables, especially in documents with multiple, similar-looking tables.
2. Generation Inaccuracy: Large Language Models (LLMs) frequently misinterpret or misidentify values within tables, particularly in complex tables with nested columns. My hypothesis was this could be due to formatting inconsistencies.

## The Solution:

I approached this with four key concepts:

1. Precise Extraction: Cleanly extract all tables from the document.
2. Contextual Enrichment: Leverage an LLM to generate a robust, contextual description of each table by analyzing both the extracted table and its surrounding document content.
3. Format Standardization: Employ an LLM to convert tables into a uniform markdown format, enhancing both embedding efficiency and LLM comprehension.
4. Unified Embedding: Create a ‘table chunk’ by combining the contextual description with the markdown-formatted table, optimizing it for vector database storage and retrieval.

![What a table chunk/element will consist of after contextualization and format standardization](https://miro.medium.com/v2/resize:fit:700/1*Mw-GrXOl32EdQugrBB5gtQ.png)

## Implementation

**Objective:** Build a RAG pipeline for [Meta’s earnings report data](<https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Second-Quarter-2024-Results-2024.pdf>), designed to retrieve and answer questions from the document’s text and multiple tables.

![Implementation Architecture](https://miro.medium.com/v2/resize:fit:700/1*y_Y-XDccxe6BReFgeAewYg.png)

See the [full notebook in Google Colab](<https://colab.research.google.com/github/KxSystems/kdbai-samples/blob/main/unstructured_io_RAG/Table_RAG_Unstructured_KDBAI_LangChain_RAG.ipynb>), or fork the code on [GitHub](<https://github.com/KxSystems/kdbai-samples/blob/main/unstructured_io_RAG/Table_RAG_Unstructured_KDBAI_LangChain_RAG.ipynb>)— this article covers how to create a RAG pipeline with contextualized table chunks, the full notebook includes a comparison to using non-contextualized table chunks.

## **Step 1: Precise Extraction**

To begin, we need to extract text and tables from the document, to do this we will use [Unstructured.io](<https://unstructured.io/>).

Let’s install and import all dependencies:

```python !apt-get -qq install poppler-utils tesseract-ocr%pip install -q --user --upgrade pillow%pip install -q --upgrade unstructured["all-docs"]%pip install kdbai_client%pip install langchain-openai%pip install langchainimport os!git clone -b KDBAI_v1.4 https://github.com/KxSystems/langchain.gitos.chdir('langchain/libs/community')!pip install .%pip install pymupdf%pip install --upgrade nltkimport osfrom getpass import getpassimport openaifrom openai import OpenAIfrom unstructured.partition.pdf import partition_pdffrom unstructured.partition.auto import partitionfrom langchain_openai import OpenAIEmbeddingsimport kdbai_client as kdbaifrom langchain_community.vectorstores import KDBAIfrom langchain.chains import RetrievalQAfrom langchain_openai import ChatOpenAIimport fitznltk.download('punkt') ```

Set OpenAI API key:

``` # Set OpenAI APIif "OPENAI_API_KEY" in os.environ: KDBAI_API_KEY = os.environ["OPENAI_API_KEY"]else: # Prompt the user to enter the API key OPENAI_API_KEY = getpass("OPENAI API KEY: ") # Save the API key as an environment variable for the current session os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY ```

Download Meta’s second quarter 2024 results [PDF](<https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Second-Quarter-2024-Results-2024.pdf>) (lots of tables!):

``` !wget 'https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Second-Quarter-2024-Results-2024.pdf' -O './doc1.pdf' ```

We will use Unstructured’s ‘[partition_pdf](<https://docs.unstructured.io/open-source/core-functionality/partitioning#partition-pdf>)’ implementing the ‘hi_res’ partitioning strategy to extract text and table elements from the PDF earnings report.

There are a few parameters we can set during partitioning to ensure we extract tables accurately from the PDF.

* **strategy = “hi_res”** : Identifies the layout of the document, recommended for use-cases sensitive to correct element classification, for example table elements.
* **chunking_strategy = “by_title”:** The ‘by_title’ chunking strategy preserves section boundaries by starting a new chunk when a ‘Title’ element is encountered, even if the current chunk has space, ensuring that text from different sections doesn’t appear in the same chunk.

``` elements = partition_pdf('./doc1.pdf', strategy="hi_res", chunking_strategy="by_title", ) ```

Let’s see what elements have been extracted:

```python from collections import Counterdisplay(Counter(type(element) for element in elements)) ``` ``` >>> Counter({unstructured.documents.elements.CompositeElement: 17, unstructured.documents.elements.Table: 10}) ```

There are 17 CompositeElement elements extracted, which are basically text chunks. There are 10 Table elements, which are the extracted tables.

At this point, we have extracted text chunks and tables from the document.

## **Step 2 & 3: Table Contextual Enrichment and Format Standardization**

Let’s take a look at a Table element to see if we can understand why there might be issues with this in a RAG pipeline. The second to last element is a Table element:

``` print(elements[-2])>>>Foreign exchange effect on 2024 revenue using 2023 rates Revenue excluding foreign exchange effect GAAP revenue year-over-year change % Revenue excluding foreign exchange effect year-over-year change % GAAP advertising revenue Foreign exchange effect on 2024 advertising revenue using 2023 rates Advertising revenue excluding foreign exchange effect 2024 $ 39,071 371 $ 39,442 22 % 23 % $ 38,329 367 $ 38,696 22 % 2023 $ 31,999 $ 31,498 2024 $ 75,527 265 $ 75,792 25 % 25 % $ 73,965 261 $ 74,226 24 % 2023 GAAP advertising revenue year-over-year change % Advertising revenue excluding foreign exchange effect year-over-year change % 23 % 25 % Net cash provided by operating activities Purchases of property and equipment, net Principal payments on finance leases $ 19,370 (8,173) (299) $ 10,898 $ 17,309 (6,134) (220) $ 10,955 $ 38,616 (14,573) (614) $ 23,429 ```

We see that the table is represented as a long string with a mix of natural language and numbers. If we just used this as our table chunk to be ingested to the RAG pipeline, it is easy to see how it would be difficult to decipher if this table should be retrieved or not.

We need to enrich each table with context, and then format the table into markdown.

To do this we will first extract the entire text from the pdf document to be used as context:

```python def extract_text_from_pdf(pdf_path): text = "" with fitz.open(pdf_path) as doc: for page in doc: text += page.get_text() return textpdf_path = './doc1.pdf'document_content = extract_text_from_pdf(pdf_path) ```

Next, create a function that will take in the entire context of the document (from the above code), along with the extracted text of a specific table, and output a new description containing a comprehensive description of the table, and the table itself transformed into markdown format:

```python # Initialize the OpenAI clientclient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))def get_table_description(table_content, document_context): prompt = f""" Given the following table and its context from the original document, provide a detailed description of the table. Then, include the table in markdown format. Original Document Context: {document_context} Table Content: {table_content} Please provide: 1. A comprehensive description of the table. 2. The table in markdown format. """ response = client.chat.completions.create( model="gpt-4o", messages=[ {"role": "system", "content": "You are a helpful assistant that describes tables and formats them in markdown."}, {"role": "user", "content": prompt} ] ) return response.choices[0].message.content ```

Now put it all together by applying the above function to all Table elements, and replacing each original Table element’s text with the new description (consisting of the contextual description of the table and markdown formatted table):

``` # Process each table in the directoryfor element in elements: if element.to_dict()['type'] == 'Table': table_content = element.to_dict()['text'] # Get description and markdown table from GPT-4o result = get_table_description(table_content, document_content) # Replace each Table elements text with the new description element.text = resultprint("Processing complete.") ```

Example of a enriched Table chunk/element (in markdown format for easy reading):

``` This markdown table provides a concise presentation of the financial data, making it easy to read and comprehend in a digital format.### Detailed Description of the TableThe table presents segment information from Meta Platforms, Inc. for both revenue and income (loss) from operations. The data is organized into two main sections: 1. **Revenue**: This section is subdivided into two categories: "Advertising" and "Other revenue". The total revenue generated from these subcategories is then summed up for two segments: "Family of Apps" and "Reality Labs". The table provides the revenue figures for three months and six months ended June 30, for the years 2024 and 2023.2. **Income (loss) from operations**: This section shows the income or loss from operations for the "Family of Apps" and "Reality Labs" segments, again for the same time periods.The table allows for a comparison between the two segments of Meta's business over time, illustrating the performance of each segment in terms of revenue and operational income or loss. ### The Table in Markdown Format```markdown### Segment Information (In millions, Unaudited)| | Three Months Ended June 30, 2024 | Three Months Ended June 30, 2023 | Six Months Ended June 30, 2024 | Six Months Ended June 30, 2023 ||----------------------------|----------------------------------|----------------------------------|------------------------------- |-------------------------------|| **Revenue:** | | | | || Advertising | $38,329 | $31,498 | $73,965 | $59,599 || Other revenue | $389 | $225 | $769 | $430 || **Family of Apps** | $38,718 | $31,723 | $74,734 | $60,029 || Reality Labs | $353 | $276 | $793 | $616 || **Total revenue** | $39,071 | $31,999 | $75,527 | $60,645 || | | | | || **Income (loss) from operations:** | | | | || Family of Apps | $19,335 | $13,131 | $36,999 | $24,351 || Reality Labs | $(4,488) | $(3,739) | $(8,334) | $(7,732) || **Total income from operations** | $14,847 | $9,392 | $28,665 | $16,619 | ```

As you can see, this provides much more context than the Table element’s original text which should significantly improve the performance of our RAG pipeline. We now have fully contextualized Table chunks that can be prepared for retrieval by embedding and storing them in our vector database.

## Step 4: Unified Embeddings… Prepare for RAG

Now that all of the elements have the necessary context for high quality retrieval and generation, we will take our elements, embed them, and store them in the [KDB.AI](<http://kdb.ai>) vector database.

First, we will create embeddings for each element, embeddings are just a numerical representation of the semantic meaning of each element:

```python from unstructured.embed.openai import OpenAIEmbeddingConfig, OpenAIEmbeddingEncoderembedding_encoder = OpenAIEmbeddingEncoder( config=OpenAIEmbeddingConfig( api_key=os.getenv("OPENAI_API_KEY"), model_name="text-embedding-3-small", ))elements = embedding_encoder.embed_documents( elements=elements) ```

Next, create a Pandas DataFrame to store our elements within. The DataFrame will contain columns based on the attributes of each element extracted with Unstructured. For example, Unstructured creates an ID, text (which we manipulated for the Table elements), metadata, and embedding (created above) for each element. We store this data in a DataFrame as this format is easily ingestible into the KDB.AI vector database.

```python import pandas as pddata = []for c in elements: row = {} row['id'] = c.id row['text'] = c.text row['metadata'] = c.metadata.to_dict() row['embedding'] = c.embeddings data.append(row)df = pd.DataFrame(data) ```

**Setup KDB.AI Server:**

Sign-up for KDB.AI server for free here: [KDB.AI](<http://kdb.ai>)

``` ## start session with KDB.AI Serversession = kdbai.Session(endpoint="http://localhost:8082") ```

You are now connected to the vector database instance — the next step is to define the schema for the table you will create within KDB.AI:

``` schema = [ {'name': 'id', 'type': 'str'}, {'name': 'text', 'type': 'bytes'}, {'name': 'metadata', 'type': 'general'}, {'name': 'embedding', 'type': 'float32s'}] ```

We create a column in the schema for each column in the DataFrame created earlier. (id, text, metadata embedding). The embedding column is where the vector search for retrieval will be executed.

Next, we define the index. Several parameters are defined here:

* _name_ : the user defined name of this index.
* _column_ : the column within the above schema that this index will be applied to. In this case, the ‘embedding’ column.
* _type_ : the type of index, here simply using a flat index, but could also use qFlat(on-disk flat index), HNSW, IVF, IVFPQ.
* _params_ : the _dims_ and vector search _metric_ used. _dims_ is the number of dimensions of each embedding — determined by which embedding model is used. In this case OpenAI’s ‘text-embedding-3-small’ outputs 1536 dimension embeddings. The _metric_ , L2, is Euclidean distance, other options include cosine similarity and dot product.

``` indexes = [ {'name': 'flat_index', 'column': 'embedding', 'type': 'flat', 'params': {'dims': 1536, 'metric': 'L2'}}] ```

Table creation based on the above schema:

``` # Connect to the default database in KDB.AIdatabase = session.database('default')KDBAI_TABLE_NAME = "Table_RAG"# First ensure the table does not already existif KDBAI_TABLE_NAME in database.tables: database.table(KDBAI_TABLE_NAME).drop()#Create the table using the table name, schema, and indexes defined abovetable = db.create_table(table=KDBAI_TABLE_NAME, schema=schema, indexes=indexes) ```

Insert the DataFrame into the KDB.AI table:

```sql # Insert Elements into the KDB.AI Tabletable.insert(df) ```

All elements are now stored in the vector database which is ready to be queried for retrieval.

## Use LangChain and KDB.AI to Perform RAG!

Basic setup for using [LangChain](<https://www.langchain.com/>):

``` # Define OpenAI embedding model for LangChain to embed the queryembeddings = OpenAIEmbeddings(model="text-embedding-3-small")# use KDBAI as vector storevecdb_kdbai = KDBAI(table, embeddings) ```

Define a RAG chain using KDB.AI as the retriever and gpt-4o as the LLM for generation:

``` # Define a Question/Answer LangChain chainqabot = RetrievalQA.from_chain_type( chain_type="stuff", llm=ChatOpenAI(model="gpt-4o"), retriever=vecdb_kdbai.as_retriever(search_kwargs=dict(k=5, index='flat_index')), return_source_documents=True,) ```

Helper function to perform RAG:

```python # Helper function to perform RAGdef RAG(query): print(query) print("-----") return qabot.invoke(dict(query=query))["result"] ```

## Results

**Example 1:**

``` # Query the RAG chain!RAG("what is the 2024 GAAP advertising Revenue in the three months ended June 30th? What about net cash by operating activies") ```

Result:_
For the three months ended June 30, 2024:_

* _The GAAP advertising revenue was $38,329 million._
* _The net cash provided by operating activities was $19,370 million._

![The original table that the results were retrieved from](https://miro.medium.com/v2/resize:fit:700/1*QEla-_796C7s61pycz48XQ.png)

**Example 2:**

``` # Query the RAG chain!RAG("what is the three month costs and expensis for 2023?") ```

Result:
_The three-month costs and expenses for Meta Platforms, Inc. in the second quarter of 2023 were $22.607 billion._

![The original table that the results were retrieved from](https://miro.medium.com/v2/resize:fit:700/1*g_V6GbLHfj_yBsFggvLXAA.png)

**Example 3:**

``` # Query the RAG chain!RAG("At the end of 2023, what was the value of Meta's Goodwill assets?") ```

Result:
_At the end of 2023, the value of Meta’s Goodwill assets was $20,654 million._

![The original table that the results were retrieved from](https://miro.medium.com/v2/resize:fit:700/1*cDltW6WbyAgSk0xMk4RhRw.png)

**Example 4:**

``` # Query the RAG chain!RAG("What is the research and development costs for six months ended in June 2024") ```

Result:

_The research and development costs for the six months ended in June 2024 were $20,515 million._

![The original table that the results were retrieved from](https://miro.medium.com/v2/resize:fit:700/1*6BideGqRZnD6py7sM810_w.png)

**!!Note** : This is an example where if you used non-contextualized table chunks, it gets it wrong. This means that the more complex the table, the more helpful adding additional context and formatting is.

**Example 5:**

``` # Query the RAG chain!RAG("Given a sentiment score between 1 and 10 for the outlook? Explain your reasoning") ```

Result:

``` I would give the sentiment score for Meta Platforms, Inc.'s outlook an **8 out of 10**. Here's the reasoning behind this score:### Positive Indicators:1. **Significant Increase in Earnings Per Share (EPS)**: - **Basic EPS** has risen from $3.03 in Q2 2023 to $5.31 in Q2 2024, and from $5.24 in H1 2023 to $10.17 in H1 2024. - **Diluted EPS** has also shown substantial growth, from $2.98 in Q2 2023 to $5.16 in Q2 2024, and from $5.18 in H1 2023 to $9.86 in H1 2024. 2. **Revenue Growth**: - Revenue increased by 22% from $31.999 billion in Q2 2023 to $39.071 billion in Q2 2024.3. **Improved Income from Operations**: - Income from operations rose by 58%, from $9.392 billion in Q2 2023 to $14.847 billion in Q2 2024. - Operating margin improved from 29% in Q2 2023 to 38% in Q2 2024.4. **Net Income Growth**: - Net income for Q2 2024 was $13.465 billion, marking a 73% increase from $7.788 billion in Q2 2023.5. **Effective Tax Rate**: - The effective tax rate decreased from 16% in Q2 2023 to 11% in Q2 2024, benefiting overall profitability.### Negative or Neutral Indicators:1. **Increase in Costs and Expenses**: - Total costs and expenses increased by 7%, from $22.607 billion in Q2 2023 to $24.224 billion in Q2 2024.2. **Decrease in Retained Earnings**: - Retained earnings slightly decreased from $82,070 million at the end of 2023 to $81,188 million by June 30, 2024.### Conclusion:The significant improvements in EPS, revenue, income from operations, and net income indicate strong financial performance and a positive outlook for Meta Platforms, Inc. The increase in costs and expenses and a slight decrease in retained earnings are areas to watch, but they don't outweigh the overall positive momentum. Hence, the sentiment score of 8 reflects a strong outlook with some room for careful monitoring of expenses. ```

We see that the LLM is able to use numbers from the embedded tables to create a reasoning for the sentiment score it generates.

## Considerations

While adding additional context will likely improve the results of your table heavy RAG pipeline, it is a more expensive method as there are additional calls to the LLM to gather and create this context. Also, for datasets with a few simple tables, it might not be necessary. My experimentation showed that using non-contextualized table chunks works fairly well for simple tables, however as the tables gain complexity, for example with nested columns as we see in ‘Example 4’, non-contextualized table chunks fall short.

## Wrapping Up

The challenge of accurate Retrieval-Augmented Generation (RAG) for table-heavy documents requires a methodical approach that addresses both retrieval inconsistency and generation inaccuracy. By implementing a strategy that includes precise extraction, contextual enrichment, format standardization, and unified embedding, we can significantly enhance the performance of RAG pipelines when dealing with complex tables.

The results from our Meta earnings report example highlight the quality of generated responses when these enriched table chunks are used. As RAG continues to evolve, incorporating these techniques could prove to be a great tool for ensuring reliable and precise outcomes, particularly in table-heavy datasets.

Try some other great sample notebooks:
\- [Multimodal RAG](<https://kdb.ai/learning-hub/samples/multimodal-retrieval-augmented-generation-rag/>)
\- [Metadata Filtering](<https://kdb.ai/learning-hub/samples/metadata-filtering/>)
\- [Temporal Similarity Search](<https://kdb.ai/learning-hub/samples/transformed-temporal-similarity-search-sample/>)
\- [Hybrid Search](<https://kdb.ai/learning-hub/samples/hybrid-search-sample/>)

Connect with me on [LinkedIn](<https://www.linkedin.com/in/ryan-siegler-816207102/>)

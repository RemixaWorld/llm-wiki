---
domain: medium.com
fetch_date: '2026-05-18T12:47:15.115273'
status: ok
url: https://medium.com/@irina.karkkanen/rag-on-graph-db-using-fixed-entity-architecture-make-you-retrieval-work-for-you-f4bfcac5277f
---

# RAG on Graph using Fixed Entity Architecture: make you retrieval work for you

[ ![Irina Adamchic](https://miro.medium.com/v2/resize:fill:64:64/1*bfO101i8-ormQrP4B1GqAQ.jpeg) ](</@irina.karkkanen?source=post_page---byline--f4bfcac5277f--------------------------------------->)

[Irina Adamchic](</@irina.karkkanen?source=post_page---byline--f4bfcac5277f--------------------------------------->)

17 min read

·

Aug 24, 2024

\--

Listen

Share

More

**Applications of Graph approaches in RAG — current state**

Retrieval-Augmented Generation (RAG) combines the LLM natural language generation power with the strength of the information retrieval, enabling more context-aware, accurate, relevant and nuances response. By incorporating retrieval into the generative process, RAG systems maintain high relevance and factual accuracy, making them indispensable for applications like knowledge management, customer support, and research, where precise and contextually appropriate information is critical.

Traditional Retrieval Augmented Generation (RAG) techniques, while effective in certain scenarios, often struggle to capture the intricate relationships and contextual nuances present in real-world data. Knowledge graphs, on the other hand, provide a structured representation of information, enabling more efficient retrieval and reasoning. However, effectively integrating knowledge graphs with LLMs to improve RAG performance remains a challenging task.

Using knowledge graphs in RAG systems is increasingly recognized for improving data organization and retrieval precision. Graph-based approaches are now commonly associated with usage of Large Language Models (LLMs) to extract and build complex relationships from text corpora, firstly introduced by Microsoft earlier this yaer [1]. However, building and maintaining accurate knowledge graphs using LLM remains resource-intensive, with challenges such as data sparsity, duplication, and the need for continuous updates. To address these, there is a trend towards using modular and hierarchical graph structures, which can manage large datasets effectively. Techniques like community detection and summarization are being employed to improve scalability and efficiency in graph-based RAG systems.

In this paper I am going to put a focus on the new approach I have called Fixed Entity Architecture (FEA). Both approaches, Microsoft’s GraphRAG and FEA address common issues in knowledge graph construction and utilization, such as scalability, complexity, and precision. These methods represent the latest advancements in integrating knowledge graphs with RAG, utilizing LLMs and efficient graph structuring techniques. They are two contrasting methods, that depend on the given use case and the given data. These two approaches cater to different types of data and queries, making them broadly applicable across various industries and research areas.

### Focus of this article

This article presents a novel methodology for constructing knowledge graphs that can serve as more effective knowledge bases for RAG applications for many use cases. Departing from traditional LLM-based graph construction methods, FEA approach aims to address the following limitations of existing techniques:

* Excessive usage on LLMs during the graph creation step
* Avoidance of entity duplication and elimination of the need for entity resolution
* Graph sparsity

This article is structured as follows:

· Analysis of the GraphRAG and Fixed Entity Architecture

· GraphRAG — Existing Microsoft Approach Overview

· Fixed Entity Architecture: Introduction and Comparison Overview

· The Ontological Fishbone

· Adding knowledge

· Retrieval Process

I will illustrate these concepts using a simple example of a famous Albert Einstein quote, demonstrating how to build a knowledge base and perform advanced retrievals. This approach aims to open new horizons for your RAG systems and showcase the vast potential for further exploration and development.

### Analysis of the GraphRAG and Fixed Entity Architecture

**GraphRAG — Existing Microsoft Approach Overview**

In April 2024, Microsoft published their first paper on GraphRAG, introducing an intriguing approach to extract entities and relationships from text corpora using large language models (LLMs) and build a knowledge graph based on these entities. They aggregated entities into communities, which then became summaries of their content. The actual Retrieval Augmented Generation (RAG) was performed on these summaries, showcasing a method with significant potential for information retrieval.

Like any approach, GraphRAG has its pros and cons. Table 1 below highlights the benefits and challenges of the Microsoft GraphRAG approach from my perspective. It’s important to note that in some use cases, especially those dealing with vast amounts of text data, knowing the relationships between entities in advance may not always apply.

In my case, I was working on a proof of concept (POC) with a known, or at least partially known, ontology, and there was an urgent need for a RAG implementation. The task was to build a highly effective knowledge base on very unstructured data.

I initially tried Microsoft’s approach to build a graph on my data, spending a considerable amount of time writing and refining queries to extract entities and relationships from text chunks. After creating my first and even second variant of an LLM-generated graph database, I encountered a significant problem. The information retrieval was unsuitable for the GenAI-powered application. The databases were cluttered with duplicates, and the entity resolution was insufficiently accurate, leading to a time-consuming and costly process. In summary, it was too expensive, too cluttered, too complex, and too uncontrollable for my specific use case.

I realized that for the well-defined domain I was working on, I needed a different approach to implementing RAG on a knowledge graph — one that was fast, mostly automatic, and did not rely heavily on expensive LLM calls. Additionally, I wanted it to be very controllable and flexible. The vast number of often duplicated entities created by LLMs led me to the idea that I wanted to have these entities fixed, fewer in number, and known with high precision how they were connected.

This article describes FEA approach to building RAG on a graph using a Fixed Entity Architecture. The knowledge graph was created using Neo4J.

### Fixed Entity Architecture

**Fixed Entity Architecture — New Approach Introduction**

The Fixed Entity Architecture proposed in this article is based on predefined entities and relationships that form the ontological “fishbone” of your use case domain. Determining what to include in this structure can often be a deeply philosophical question, requiring extensive domain knowledge to develop a robust Fixed Entity Architecture. Alternatively, you might consider what you need your knowledge base for and identify key or template documents to serve as the foundation for your ontological fishbone.

Unlike Microsoft’s approach, the Fixed Entity Architecture does not rely on large language models (LLMs) for building the graph. Instead, it leverages proprietary domain knowledge specific to the use case, combined with straightforward mathematical techniques. This approach offers a highly effective way to address many of the drawbacks associated with the LLM-based method.

### Comparison Overview

Table 1 offers a comparison overview of two approaches Microsoft’s GraphRAG and Fixed Entity Architecture.

Press enter or click to view image in full size

Table 1. Comparison overview of two approaches.

In summary, **Fixed Entity Architecture** is ideal for well-defined, narrow domains where high precision and control are needed. It offers lower complexity, reduced computational costs, and minimizes reliance on LLMs. However, it lacks flexibility, struggles with scalability in large datasets, and requires prior domain knowledge.

**Microsoft’s GraphRAG** excels with large, diverse datasets and complex queries, providing scalability and adaptability across various domains. It supports both local and global queries but comes with higher complexity, resource costs, and a strong dependency on LLMs. It’s less suitable when simplicity, low maintenance, or fixed entities are prioritized.

The recommendation here, choose based on dataset nature, control needs, and available resources. Combining elements from both approaches could optimize performance.

### The Ontological Fishbone

What are ontologies? Have you ever considered the ontology of your own micro-world? Every day at work, you perform tasks without consciously understanding how your brain recognizes these “things” and how it builds connections between them. Try this exercise: attempt to create a metamodel of the “things” you do or use daily, and then map out the connections between them. While this may sound challenging, I have good news — it’s entirely possible because YOU know what you do!

Ontologies are powerful tools that help us make sense of the world around us. The “fishbone” metaphor encourages us to delve into the fundamental building blocks and connections that define our conceptual domains. Creating an ontology involves careful consideration of what to include, how elements are related, and what is most important. The fishbone structure helps us identify core elements while acknowledging the intricate web of connections that bring our ideas to life.

Now, imagine you work within a narrow domain and have a clear understanding of the “fishbone” of entities that make up your work. How could you easily take all this information, connect it, and build a knowledge base for any RAG application? Keep reading — I have the answer to those questions.

### Creating a basic “fishbone” structure: Einstein example

In many organizations, subject matter experts can easily identify critical entities and relationships within well-defined domains. This foundational knowledge is essential for building effective knowledge graphs. By leveraging this expertise, a basic “fishbone” of key entities and their relationships can be established within days, providing a strong foundation that can be further enriched with detailed information.

When creating your fishbone, remember to include descriptions for your entities wherever possible. Let’s consider a famous example to illustrate how a knowledge graph is constructed: the sentence “Albert Einstein developed the theory of relativity, which revolutionized theoretical physics and astronomy.” This well-known sentence demonstrates how entities and relationships are extracted. Figure 1 below shows the graph built from this sentence.

Press enter or click to view image in full size

Figure 1. Graphical representation of the sentence “Albert Einstein developed the theory of relativity, which revolutionized theoretical physics and astronomy” — a “fishbone” ontology for the fixed entity architecture graph.

Cypher is a declarative query language used for interacting with graph databases, particularly Neo4j. It allows users to express complex graph patterns and relationships in an intuitive, SQL-like syntax. Cypher is designed to be human-readable and offers powerful capabilities for querying, updating, and managing graph data. It supports pattern matching, filtering, and manipulation of nodes and relationships, making it ideal for tasks involving social networks, recommendation engines, and other graph-based data models. For more detailed information, you can visit the official Neo4j Cypher documentation [2].

Here, I assume the reader is familiar with terms like embeddings, cosine similarity, dot product, and vector indexes. If not, please refer to additional literature, such as [3–5].

In our Einstein example, we have four entities (Albert Einstein, Theory of Relativity, Theoretical Physics, and Astronomy) and three edges with two types (Developed and Revolutionized). We can add brief descriptions to each entity, such as: “Albert Einstein was a great physicist of the 20th century,” etc. Translating this into Cypher code, the creation of your graph would look like this:

``` CREATE (a:Entity {label: 'Person' , name: 'Albert Einstein', embeddings: $person_emb}),(b:Entity {label:'Theory' ,name: 'Theory of relativity', embeddings: $theory_emb}),(c:Entity {label:'Field', name: 'Theoretical physics', embeddings: $field1_emb }),(d:Entity {label:'Field', name: 'Astronomy', embeddings: $field2_emb })// Create edgesCREATE (a)-[:DEVELOPED]->(b),(b)-[:REVOLUTIONIZED]->(c),(b)-[:REVOLUTIONIZED]->(d) ```

Note that I create the nodes with only one associated label called “Entity,” but I include different labels as a property for each node. This is done to maintain clarity during searches later on. All nodes, referred to internally as entities, form the fixed fishbone structure for subsequent operations. I will be adding differently labeled nodes later, but they will serve different functions — so keep reading! 😉

Another reason for this approach is that I haven’t found a way to build unified indexes for two or more node labels simultaneously (if you know of one, I’d be happy to hear your thoughts in the comments section later).

The `embeddings` parameter here only contains the “label: name” value, but in practice, I suggest including a detailed description of your entity and adding it to your embeddings vector as well.

## Adding knowledge

Now, we have the “fishbone” of our Graph on which we will build our knowledge base for retrieval in a RAG application (Figure 2). To create this knowledge base, we need documents. For Albert Einstein, I used a Wikipedia article [6]. I copied the text using the Wikipedia API and split it into 59 chunks, each with a size of 2000. Note that in this demo, I am not optimizing chunk sizes; the chosen size is arbitrary.

Press enter or click to view image in full size

Figure 2. Fixed Entity Fishbone representation in Neo4J

### Adding documents to the graph

Let’s add the document chunks to the graph in the following manner:

``` prev_node_id = None # Initialize prev_node_id before the loopfor i, chunk in enumerate(chunks): # Create the chunk node query = f''' CREATE (d:Document {{ chunkID: "{f"chunk_{i}"}", url: "{url}", docID: "{document_name}", full_text: '{escaped_chunk}', embeddings: {embeddings.embed_documents(chunk).tolist()}}} ) RETURN ID(d) ''' run_query(driver, query) chunk_node_id = result[0]['ID(d)'] # If this is not the first chunk, create a NEXT relationship to the previous chunk if prev_node_id is not None: query = f''' MATCH (c1:Document), (c2:Document) WHERE ID(c1) = {prev_node_id} AND ID(c2) = {chunk_node_id} CREATE (c1)-[:NEXT]->(c2) CREATE (c2)-[:PREV]->(c1) ''' run_query(driver, query) prev_node_id = chunk_node_id ```

This code results in chunks being added as nodes labeled “Document” (see Figure 3).

Figure 3. The first 25 chunks of the Albert Einstein Wikipedia article.

Connecting document chunks to each other provides a significant advantage in later retrieval. You can define, using a Cypher query, that if a similar chunk is found, you can also retrieve the previous and next chunks. It’s that simple!

### Connecting documents with the fixed entities

Next, let’s connect the text chunks to our fixed entity “fishbone.” Note that this approach does not use any costly LLM technology and avoids creating duplicates in the knowledge base. Additionally, it takes only milliseconds to execute. We use a simple mathematical formula called the dot product, which provides a cosine similarity value between each chunk and our Fixed Entity Architecture. The following Cypher code will accomplish this:

``` MATCH (e:Entity), (d:Document)WHERE e.embeddings IS NOT NULL AND d.embeddings IS NOT NULL AND size(e.embeddings) = size(d.embeddings)WITH e, d, reduce(numerator = 0.0, i in range(0, size(e.embeddings)-1) | numerator + toFloat(e.embeddings[i])*toFloat(d.embeddings[i])) as dotProduct, sqrt(reduce(eSum = 0.0, i in range(0, size(e.embeddings)-1) | eSum + toFloat(e.embeddings[i])^2)) as eNorm, sqrt(reduce(dSum = 0.0, i in range(0, size(d.embeddings)-1) | dSum + toFloat(d.embeddings[i])^2)) as dNormWITH e, d, dotProduct / (eNorm * dNorm) as cosineSimilarityWHERE cosineSimilarity > 0.8MERGE (e)-[r:RELATES_TO]->(d)ON CREATE SET r.cosineSimilarity = cosineSimilarityRETURN ID(e), e.name, ID(d), d.full_text, r.cosineSimilarityORDER BY cosineSimilarity DESC ```

In this example, we instruct the database to take all entity nodes and compare them with each chunk of text by calculating the angle between their vectors. If the cosine similarity exceeds the given threshold, which is 0.8 in this case, the database will create an edge named `RELATES_TO` between the entity node and the document. Since the chunks are not optimized, and the fixed entities lack detailed descriptions, the match might not be very high. This example is intended to illustrate the technique.

Press enter or click to view image in full size

Table 2. Result of the previous query attaching the document nodes to the fixed entities.

Press enter or click to view image in full size

Figure 3. The self-attached document nodes by cosine similarity property.

Figure 4 shows the result of this query. Some of the chunks were automatically linked to the fixed entities with a cosine similarity higher than the defined threshold of 0.8. You can adjust this threshold as needed. This approach allows for further filtering during retrieval, enabling you to select only the best-matching chunks.

Not only was the entity “Albert Einstein” connected to relevant text chunks, but so was the “Theory of Relativity.” As more documents are added, the “fishbone” entities will increasingly act as connectors between elements. This is one of the strengths of using a graph — almost everything is interconnected. There is no issue of sparsity that requires clustering. You could explore this further, but that would be a different topic. For now, let’s proceed with adding more documents.

Refer to Table 3 for an example of how text from the Wikipedia article on theoretical physics is connected to various fixed entities.

Press enter or click to view image in full size

Table 3. Returned result of matched entities to the added documents from the Wikipedia article on theoretical physics.

The result of attaching documents [6–9] to the fixed entities from our Einstein sentence is shown in Figure 5. The chunks are seamlessly linked to the related entities.

This technique for attaching documents is versatile and can be applied to various types of documents. By vectorizing your data, you can easily integrate and connect all your information.

Press enter or click to view image in full size

## Build different types of indexes for a hybrid search

The beauty of Neo4j lies in its ability to create various types of indexes on your graph, and even better, you can perform hybrid searches using just a single Cypher query. Let’s prepare the indexes for our retrieval.

### Create Vector Indexes

First, we create the vector indexes:

``` queries = ["DROP INDEX test_index_document IF EXISTS;","DROP INDEX test_index_entity IF EXISTS;"]for query in queries: run_query(driver, query)# create vector index on document embeddingsquery = '''CREATE VECTOR INDEX test_index_documentIF NOT EXISTSFOR (d:Document)ON (d.embeddings)OPTIONS {indexConfig: {`vector.dimensions`: 768,`vector.similarity_function`: 'cosine'}}'''run_query(driver, query)# create vector index on entity embeddingsquery = '''CREATE VECTOR INDEX test_index_entity IF NOT EXISTSFOR (n:Entity)ON (n.embeddings)OPTIONS {indexConfig: {`vector.dimensions`: 768,`vector.similarity_function`: 'cosine'}}'''run_query(driver, query) ```

Once the vector indexes on nodes are created, you can also create vector indexes on edges if you have descriptions for them. Since I don’t have any text for the relationships at this stage, I will skip this step.

### Create Text Indexes

Next, I will create a text index, which will also be added to the search as a standard keyword index.

``` queries = [ "DROP INDEX text_index_entity IF EXISTS;", "DROP INDEX text_index_document IF EXISTS;",]for query in queries: run_query(driver, query)# create full-text index on Entity descriptionquery = '''CREATE FULLTEXT INDEX text_index_entity FOR (n:Entity) ON EACH [n.name]'''run_query(driver, query)# create full-text index on Document full_textquery = '''CREATE FULLTEXT INDEX text_index_document FOR (d:Document) ON EACH [d.full_text]'''run_query(driver, query) ```

## Retrieval

Now that our knowledge base is ready for retrieval and to build our RAG application, we can start querying the graph database.

Let’s begin with a simple query. We’ll ask the database to find the best matching answers to a given query. For example, we’ll use the query: “Research fields of Albert Einstein”

To start, I’ll use the entity-based vector index. The query involves embedding the original user query for the vector indexes and/or using it as text for keyword-based indexing. I will begin with a straightforward query (Query 1):

``` CALL db.index.vector.queryNodes('test_index_entity', 10, $user_query)YIELD node AS vectorNode, score as vectorScoreWITH vectorNode, vectorScoreORDER BY vectorScore DESCRETURN vectorNode.name AS label, vectorScore AS score ```

Here, I query only the fixed entities, specifically using the vector index built on them. The result is shown below (Table 4).

Press enter or click to view image in full size

Since we have only four entities, the result is somewhat predictable. Extracting just the entities, especially without descriptions at this stage, provides limited value for the RAG application. To enhance our results, we need to extract relevant documents related to the question. Let’s take it a step further and identify the most relevant documents for the entities found (Query 2):

``` CALL db.index.vector.queryNodes('test_index_entity', 10, $user_query)YIELD node AS vectorNode, score as vectorScoreWITH vectorNode, vectorScoreMATCH (vectorNode)-[r]->(d:Document)WITH vectorNode.name AS label, vectorScore as score, d.docID as closest_document_name, d.full_text as closest_document_text, r.cosineSimilarity as similarityORDER BY similarity DESCRETURN label, closest_document_name, closest_document_text, similarityLIMIT 10 ```

The results, as shown in Table 5, differ slightly from the initial query. Here, “Astronomy” is returned first. However, rather than seeing “Theory of Relativity” as expected, “Albert Einstein” appears next. The advantage of using GraphRAG with this methodology is its flexibility: you can adjust your search to better fit your application’s needs. Let’s refine our query to prioritize “Astronomy” and “Theory of Relativity” as the top results for this question.

Press enter or click to view image in full size

To enhance the results further, we could implement a cross-encoder re-ranking step. Although I typically perform re-ranking on descriptions, in this case, we’ll apply it to labels due to the lack of descriptions. I will use the `cross-encoder/ms-marco-MiniLM-L-6-v2` model from the `sentence_transformers` library for this purpose. Table 6 displays the re-ranked results from Query 2.

Press enter or click to view image in full size

Table 6. Retrieved information using Query 2 including re-ranking.

As you can see, the re-ranking in combination with the query did not yield the desired results. To improve the outcomes, we can incorporate a full-text or keyword search (Query 3):

``` CALL db.index.vector.queryNodes('test_index_entity', 10, $my_query_emb_list)YIELD node AS vectorNode, score as vectorScoreWITH vectorNode, vectorScoreMATCH (vectorNode)-[r]->(d:Document)WITH vectorNode.name AS label, vectorScore as score, d.docID as closest_document_name, d.full_text as closest_document_text, r.cosineSimilarity as similarityORDER BY similarity DESCRETURN label, closest_document_name, closest_document_text, similarityLIMIT 10UNIONCALL db.index.fulltext.queryNodes('text_index_entity', $my_query)YIELD node AS textNode, score as textScoreWITH textNode, textScoreMATCH (textNode)-[r]->(d:Document)WITH textNode.name AS label, textScore as score, d.docID as closest_document_name, d.full_text as closest_document_text, r.cosineSimilarity as similarityORDER BY similarity DESCRETURN label, closest_document_name, closest_document_text, similarityLIMIT 10 ```

And the result of this query is shown on the Table 7.

Press enter or click to view image in full size

Table 7. Retrieved information using Query 3 including a hybrid vector-keyword search.

The previous attempts, including the re-ranking, did not yield the desired results. Now, I’m going to demonstrate the true power of retrieval in a Graph. To avoid issues with APOC libraries and compatibility problems with Python tools, I focus on a clear, transparent approach. I’ll use pure mathematical methods to illustrate the effectiveness of Graph’s search capabilities. The next query showcases what I refer to as a “smart search” in my work (Query 4).

``` CALL db.index.vector.queryNodes('test_index_entity', 10, $user_query_emb)YIELD node AS vectorNode, score as vectorScoreWITH vectorNode, vectorScoreMATCH (vectorNode)-[r]->(d:Document)WITH DISTINCT vectorNode as e, d, r, r.cosineSimilarity as cosineSimilarityORDER BY cosineSimilarity DESCWITH ID(e) as id, e.label as title, cosineSimilarity, e.description as description, head(collect(d.docID)) as document_id, head(collect(d.chunkID)) as chunkID, head(collect(d.full_text)) as document_text, reduce(mDot = 0.0, i IN range(0, size($user_query_emb) - 1) | mDot + $user_query_emb[i] * e.embeddings[i]) / (sqrt(reduce(mSq = 0.0, x IN $user_query_emb | mSq + x^2)) * sqrt(reduce(eSq = 0.0, y IN e.embeddings | eSq + y^2))) AS entity_similarity, reduce(mDot = 0.0, i IN range(0, size($user_query_emb) - 1) | mDot + $user_query_emb[i] * d.embeddings[i]) / (sqrt(reduce(mSq = 0.0, x IN $user_query_emb | mSq + x^2)) * sqrt(reduce(dSq = 0.0, y IN d.embeddings | dSq + y^2))) AS document_similarityWITH id, title, description, document_id, document_text, entity_similarity, document_similarity, chunkID, (entity_similarity + document_similarity) / 2 AS similarity, cosineSimilarityWHERE similarity > 0.8RETURN id, title, document_id, document_text, similarity, chunkIDORDER BY cosineSimilarity DESC, similarity DESC ```

With this query, I first extract the fixed entities using the vector index, then identify the best-matching documents. Next, I compute the dot product between the extracted entities and the user query, as well as between the found documents and the user query. I then combine these results and filter by a 0.8 threshold. This approach, combined with re-ranking, yields the following results (Table 8):

Press enter or click to view image in full size

Table 8. Retrieved information using Query 4 including re-ranking.

With this experiment, I aimed to demonstrate the power of retrieval in Graph. By having full control over the fixed entities and the process of adding documents, and with the flexibility to construct nearly any retrieval Cypher query, the potential is immense. The freedom to tailor the retrieval process to your specific use case is virtually limitless. In this experiment, we worked with a limited fixed entity architecture, lacking extensive descriptions and relationships between elements. However, by incorporating more information and connections, one could achieve remarkable results.

## Summary

This article explores the use of Graph for building and querying a knowledge base, with a focus on the Fixed Entity Architecture and its application in Retrieval Augmented Generation (RAG) systems. The Fixed Entity Architecture relies on predefined entities and relationships to construct a knowledge graph, offering benefits such as lower complexity, high precision, and reduced computational costs. However, it may face limitations in flexibility and scalability.

The article demonstrates the process of building a knowledge graph using a “fishbone” ontology and integrating documents into the graph. By leveraging vector indexes and Cypher queries, documents are connected to entities based on cosine similarity. This method enhances retrieval capabilities but may require optimization for better results.

A series of queries is performed to evaluate the effectiveness of the graph-based retrieval approach. Initial queries use vector indexes and keyword searches to find matching entities and documents. Despite some challenges, such as suboptimal re-ranking results, the article showcases the potential of Graph for powerful, flexible retrieval. A final smart search query, combining vector similarity and dot product calculations, illustrates the approach’s effectiveness in refining search results.

**Future Directions and Innovations**

* **Opportunities for Improvement** : Enhancing LLM-based extraction methods and expanding predefined ontologies could further refine the knowledge graph’s capabilities.
* **Emerging Trends** : New technologies and advancements in knowledge graph development may enhance RAG systems, offering even more robust solutions for complex retrieval tasks.

Overall, the article highlights the advantages of Graph’s flexible search capabilities and the importance of optimizing entity connections and document integrations to achieve high-quality retrieval results. Future developments in extraction techniques and emerging technologies hold promise for further advancing knowledge graph capabilities in RAG applications.

## References

1\. “From Local to Global: A Graph RAG Approach to Query-Focused Summarization”, Darren Edge et. al., 24 Apr 2024, Computer Science

2\. [Introduction — Cypher Manual (neo4j.com)](<https://neo4j.com/docs/cypher-manual/current/introduction/>)

3\. [Word embedding — Wikipedia](<https://en.wikipedia.org/wiki/Word_embedding>)

4\. [Cosine similarity — Wikipedia](<https://en.wikipedia.org/wiki/Cosine_similarity>)

5\. [What is a Vector Index? An Introduction to Vector Indexing (datastax.com)](<https://www.datastax.com/guides/what-is-a-vector-index>)

6\. [Albert Einstein — Wikipedia](<https://en.wikipedia.org/wiki/Albert_Einstein>)

7\. [Theory of relativity — Wikipedia](<https://en.wikipedia.org/wiki/Theory_of_relativity>)

8\. [Theoretical physics — Wikipedia](<https://en.wikipedia.org/wiki/Theoretical_physics>)

9\. [Astronomy — Wikipedia](<https://en.wikipedia.org/wiki/Astronomy>)

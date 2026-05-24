---
domain: medium.com
fetch_date: '2026-05-18T12:48:24.981521'
status: ok
url: https://medium.com/@infiniflowai/ai-native-database-infinity-0-1-0-is-released-31a51e4ecc83
---

# AI-native database Infinity 0.1.0 is released

[ ![InfiniFlow](https://miro.medium.com/v2/resize:fill:64:64/1*VIOVinD7tDsinrVyUvlV9w.png) ](</@infiniflowai?source=post_page---byline--31a51e4ecc83--------------------------------------->)

[InfiniFlow](</@infiniflowai?source=post_page---byline--31a51e4ecc83--------------------------------------->)

6 min read

·

May 7, 2024

\--

\--

Listen

Share

More

On April 30, four months after announcing its official open-source release, the AI-native database Infinity launched its first version, v0.1.0. This four-month effort focuses on the following four areas:

1. A comprehensive columnar storage engine supporting real-time data insertion and deletion, asynchonous background garbage collection (GC), enhanced metadata and WAL replay management, extended data types, and Zonemap and Bloomfilter indexes for rapid filtering.
2. Brand new full-text search enabling Infinity to support multiple recall essential for RAG scenarios, providing both precise and semantic recall.
3. A fully functional secondary index, primarily offering high-performance point queries and range filtering for numeric fields.
4. A brand new index maintenance framework, where primary indexes in Infinity support parallel and incremental builds, with vector indexes, full-text indexes, and secondary indexes supporting asynchronous and real-time builds.
5. More structured query operators and richer APIs. Besides the native Python API, Infinity also offers an HTTP API to facilitate development in other programming languages.

Infinity v0.1.0 is the first database that embodies the notion of “AI-native database,” and is capable of executing any arbitrary combination of the following queries or searches:

1. Structured data query
2. Vector search
3. Full-text search

Infinity’s design originates from our redefinition of the RAG architecture and will set the pattern for future LLM applications in B2B scenarios.

![image](https://miro.medium.com/v2/resize:fit:700/1*HThX2Z5NGQbqOqsH1yGq0w.png)

Therefore, Infinity is not a “vector store” but a fully fledged database. It is a comprehensive database based on columnar storage engine to ensure ACID compliance (Atomicity Consistency Isolation Durability). Additionally, Infinity supports building indexes corresponding to the types of the fields, such as secondary indexes for numeric fields, vector indexes for embedding fields, and full-text indexes for text fields.

![image](https://miro.medium.com/v2/resize:fit:700/1*togx4KFa-r5ekHt825sz7A.png)

## Index design details

Now, let’s explore the design specifics of Infinity’s three index types:

Secondary indexes primarily offer high-performance filtering for numeric columns. Implementing secondary indexing in a traditional database is never an easy task:

Secondary indexes in OLTP databases usually rely on general key-value storage, efficient for point filtering (small filtering range). Yet, ensuring high performance for large filtering ranges is often challenging, primarily due to the complexity of maintaining **a traversable or iterative structure** in key-value storage engines, especially with most Key-Value storages using LSM Tree structures. This complexity exacerbates the performance degradation for large ranging filtering.

On the other hand, OLAP databases typically do not offer secondary indexes and instead utilize auxiliary structures like ZoneMap or BloomFilter. This is because OLAP databases cater to offline scenarios, prioritizing high-throughput writes and reads, involving frequent scanning of large column data ranges for filtered aggregation results. Therefore, maintaining secondary indexes in such scenarios is deemed unnecessary. However, Infinity, as a database tailored for online applications, differs from both OLTP and OLAP databases. It operates in scenarios with low writes but substantial reads, requiring high concurrency for both point filtering and wide-range filtering tasks. Hence, Infinity adopts an innovative approach: sorting columns with secondary indexes, adding row numbers as a new data column, and employs a novel in-memory index structure called Piecewise Geometric Model (PGM). PGM, a form of learned index and a prime example of AI4DB, utilizes machine learning-based data structures to produce summary information in memory based on the sorted results, occupying minimal memory space, only about 1/100th of the original data size. Though PGM excels in range filtering queries, it cannot guarantee precise query results. PGM provides approximate ranges and necessitates scanning the original data for precision results. By combining PGM with sorted data structures, Infinity ensures high concurrency capabilities for both point filtering and range filtering tasks.

![image](https://miro.medium.com/v2/resize:fit:662/1*UV37ClRfsvkG7zzO1FZfcw.png)

Vector indexing is essential for RAG and is one of Infinity’s core features. The current version of Infinity offers two types of vector indexes: the IVF index, an inverted index known for its low memory consumption but slightly lower performance, and a graph index based on HNSW. Instead of using existing open-source HNSW implementations, Infinity further optimized its graph index by introducing quantization. This involves locally adaptive quantization for each vector needing indexing, with dynamically computed upper and lower bounds. Infinity’s quantization invovles two stages: the first stage for fast approximate searches and the second for enhanced search accuracy when necessary. The second stage quantizes the residual vectors from the first stage. Additionally, Infinity extensively uses SIMD instructions to accelerate calculations. These design choices enable Infinity to outperform all vector databases in vector search performance.

Full-text index is a well-established structure, with similar products like Lucene (Elasticsearch) and Tantivy offering comprehensive, high-performance full-text indexing capabilities. Infinity’s decision not to integrate these existing indexes is due to its emphasis on better integrating full-text indexing into the database system. This is mainly reflected in the following aspects:

1. Full-text indexing usually involves inverted indexing and forward indexing, and databases with full-text search capabilities must build on top of a full-text indexing library. For instance, data inserted into Elasticsearch is virtually written to its Lucene index. Since databases often possess some forward indexing capabilities, roughly combining such capabilities with databases can result in data redundancies. This also partly explains why Lucene-based Elasticsearch lacks immediate structured data query capabilities.
2. The primary purpose of enabling full-text search is to provide precise recall capabilities and vector search essential for RAG. Full-text search must collaborate with vector search for fused ranking, making it vital to offer customizable search and ranking capabilities in a unified database storage and execution engine framework, rather than the other way around.

Infinity achieves comprehensive full-text indexing with the following features:

1. Offers two index building modes: real-time and offline.
2. Employs a configurable index compression format, the default being SIMD-Bitpacking, for efficient compression and fast decompression.
3. Utilizes the FST (Finite State Transducer) data structure as the index dictionary, ensuring high performance and prefix matching essential for ordered traversal.
4. Implements the Block-Max Maxscore scoring strategy, enabling full-text indexes in Infinity to support OR-based semantic queries and ensuring query performance and effective recall.

## Benchmark report

The following chart compares Infinity v0.1.0 with Elasticsearch v8.13.0 and Qdrant v1.8.2 in vector search on the SIFT1M dataset:

![image](https://miro.medium.com/v2/resize:fit:700/1*DSMHGT9HIDG1oma8aQq2hQ.png)

The following chart compares Infinity v0.1.0 with Elasticsearch v8.13.0 and Qdrant v1.8.2 in vector search on the GIST1M dataset:

![image](https://miro.medium.com/v2/resize:fit:700/1*CYBIMUNUkJC4sOVGca5brQ.png)

The following chart compares Infinity v0.1.0 with Elasticsearch v8.13.0 in full-text search on the DBPedia 4.6M dataset:

![image](https://miro.medium.com/v2/resize:fit:700/1*a5w6hd98_QhifQJ53hRc-g.png)

The following chart compares Infinity v0.1.0 with Elasticsearch v8.13.0 in full-text search on the EnWiki 33M dataset:

![image](https://miro.medium.com/v2/resize:fit:700/1*_05XBgM3ZvbhiYN-n2jIYQ.png)

See [here](<https://github.com/infiniflow/infinity/blob/main/docs/references/benchmark.md>) for a detailed benchmark report.

## Future roadmap

Now, Infinity can be considered to have the essential features of an AI-native database and deliver the highest multiple recall. Future versions of Infinity will focus on:

* Enhancing query performance
* Introducing features to support more sophisticated RAG scenarios
* Developing distributed capabilities

Stay tuned for Infinity’s updates, and you are welcome to visit its GitHub repository at: <https://github.com/infiniflow/infinity>

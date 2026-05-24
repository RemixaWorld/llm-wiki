---
domain: mychen76.medium.com
fetch_date: '2026-05-18T12:57:10.104142'
status: ok
url: https://mychen76.medium.com/deep-dive-loading-unstructured-text-into-a-knowledge-graph-using-large-language-models-llms-bfc013f7dc17
---

Member-only story

# Deep Dive: Transforming Text into Knowledge Graphs with LLM

Benefits of Knowledge graphs is put data in context via linking and semantic metadata *which express relationships between data*. Knowledge Graphs can combine disparate silos of data into an overview of all of your knowledge. In this writing, let’s explore steps involve on extracting text information into Knowledge Graph using LLM manually.

### Motivation

What is the quickest way to reading lot’s of text information and provide a abstract summary without losing key information, without spending too much time with easy-to-digest result?

One way is extracting information into a knowledge graph to provide a quick visual view of key parties and important relationships. This is because knowledge graphs are designed to organize structured knowledge in a way that integrates information from multiple data sources, making it easier to visualize and understand complex relationships.

### Processing Steps

For this experimental the plan get text information from Wikipedia, condense it by performing a summation, then extract entities and relations using LLM, convert result into **entities** and **relationship** cypher query, insert query into Neo4J graph database.

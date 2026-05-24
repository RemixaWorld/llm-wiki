---
domain: medium.com
fetch_date: '2026-05-18T12:47:08.138554'
status: ok
url: https://medium.com/@kelvin.lu.au/disadvantages-of-rag-5024692f2c53
---

# Disadvantages of RAG

[ ![Kelvin Lu](https://miro.medium.com/v2/resize:fill:64:64/1*FrL61XBGRKjEzvM7O1Lxtg.jpeg) ](</@kelvin.lu.au?source=post_page---byline--5024692f2c53--------------------------------------->)

[Kelvin Lu](</@kelvin.lu.au?source=post_page---byline--5024692f2c53--------------------------------------->)

9 min read

·

Aug 25, 2023

\--

\--

Listen

Share

More

This is the first part of the RAG analysis:

* part 1: Disadvantages of RAG
* part 2: [Practical Considerations in RAG Application Design](<https://pub.towardsai.net/practical-considerations-in-rag-application-design-b5d5f0b2d19b>)

Recently, the rise of large language models (LLMs) has sparked a lot of interest in RAG systems. Many practitioners are eager to learn how RAG can benefit their own organisations, and some businesses have already released RAG-based services. In my previous posts, I addressed my research on how to host and fine-tune a project-specific embedding model[1, [4](</@kelvin.lu.au/fine-tuning-embedding-model-with-peft-and-lora-3b6f08987c24>)] and some of the considerations for developing a vector database, which is the cornerstone of the RAG system[[1](</@kelvin.lu.au/what-we-need-to-know-before-adopting-a-vector-database-85e137570fbb>)]. In this article, I will explore some of the limitations of RAG systems.

If you are unfamiliar with RAG and would like to quickly get an idea of how it works in a case study, please check out[[2](</@kelvin.lu.au/compare-pdf-question-answering-with-openai-and-google-vertexai-46638d62327b>)].

![Photo by Michael Fenton on Unsplash](https://miro.medium.com/v2/resize:fit:700/0*NZOyB8jbYVnVu8Ch)

**Table of Contents**

· It Starts With Semantic Search
· The Chunk Size and Top-k
· World Knowledge
· Multi-hop Q&A
· Information Loss
· Conclusion
· References

## It Starts With Semantic Search

Before we go any further, let's do an experiment. The following code piece compares the cosine similarity score of a query against a series of statements. It uses GCP VertexAI’s textembedding-gecko001 model to produce 768-dimensional embedding vectors.

```python from vertexai.language_models import TextEmbeddingModelimport numpy as npfrom numpy.linalg import normmodel = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")def text_embedding(texts: list[str]) -> list: batch_size = 5 embeddings = [] for batch in range (0, len(texts), batch_size): embeddings.extend(model.get_embeddings(texts[batch: batch + batch_size])) return [emb.values for emb in embeddings]def ranking_by_similarity (query, statements): query_embedding = text_embedding ([query]) [0] statements_embeddings = text_embedding(statements) for stm,emb in zip(statements,statements_embeddings): print(np.dot(query_embedding, emb) / (norm(query_embedding)*norm(emb)), '-', stm[:80]) ```

And if we use the above code pieces to try the following data:

``` query = "When not to use the support vector machine"statements = [ """Support vector machines (SVMs) are a set of supervised learning methods used for classification, regression, and outlier detection. """, """The advantages of support vector machines are:effective in high-dimensional spacesstill effective in cases where the number of dimensions is greater than the number of samples.uses a subset of training points in the decision function (called support vectors), so it is also memory efficient.Versatile: different Kernel functions can be specified for the decision function. Common kernels are provided, but it is also possible to specify custom kernels. """, """The disadvantages of support vector machines include:If the number of features is much greater than the number of samples, avoid over-fitting when choosing Kernel functions and regularisation terms.SVMs do not directly provide probability estimates; these are calculated using an expensive five-fold cross-validation (see Scores and Probabilities, below). ""","""The support vector machines in scikit-learn support both dense (numpy.ndarray and convertible to that by numpy.asarray) and sparse (any scipy.sparse) sample vectors as input. However, to use an SVM to make predictions for sparse data, it must have been fitted to such data. For optimal performance, use C-ordered numpy.ndarray (dense) or scipy.sparse.csr_matrix (sparse) with dtype=float64. """, """Support vector machines (SVMs) are a set of supervised learning methods used for classification, regression, and outlier detection.The advantages of support vector machines are:effective in high-dimensional spacesstill effective in cases where the number of dimensions is greater than the number of samples.uses a subset of training points in the decision function (called support vectors), so it is also memory efficient.Versatile: different Kernel functions can be specified for the decision function. Common kernels are provided, but it is also possible to specify custom kernels.The disadvantages of support vector machines include:If the number of features is much greater than the number of samples, avoid over-fitting when choosing Kernel functions and regularisation terms.SVMs do not directly provide probability estimates; these are calculated using an expensive five-fold cross-validation (see Scores and Probabilities, below).The support vector machines in scikit-learn support both dense (numpy.ndarray and convertible to that by numpy.asarray) and sparse (any scipy.sparse) sample vectors as input. However, to use an SVM to make predictions for sparse data, it must have been fitted to such data. For optimal performance, use C-ordered numpy.ndarray (dense) or scipy.sparse.csr_matrix (sparse) with dtype=float64. """,]ranking_by_similarity(query, statements) ```

The output is the following:

![image](https://miro.medium.com/v2/resize:fit:700/1*A4kmNfIcqedn9tuaOUfwFQ.png)

Surprise, surprise! When we ask when not to use SVM, the semantic search returns the advantages of SVM. And let’s have another example:

![image](https://miro.medium.com/v2/resize:fit:463/1*APY7_B9u5hanocjgtlTxgA.png)

The algorithm not only disregarded the sentimental difference; it was also very sensitive to language nuances like plural vs. singular. And these experiments reveal the limitation of the RAG: semantic similarity search is not magic, as with many other machine learning technologies.

The embedding vector we got from the embedding model is the top layer weights of the LLM. One thing we need to notice is that the embedding LLM and the generative LLM are different. The embedding models were designed to predict masked segments in the input text. Therefore, they can learn the intention of the input text. And these types of LLM are called autoencoders. While the generative LLM was designed to predict the next token based on the prior input string. And these types of LLM are called autoregressors. ChatGPT, Google Palm, and Llama are all autoregressors.

The embedding models, or autoencoders, learn input data features into the weights, which we call embedding vectors. We found that the embedding vectors attract important information from the input text, and the vector similarity can be used to compare the closeness of the texts. Nevertheless, we don’t know what information has been extracted or how the information was organised in the vector, let alone how to make it more efficient or develop a more accurate similarity function.

As a consequence, please be prepared that semantic similarity searches may miss the goal from time to time. Assuming semantic search will always retrieve reasonable results is unrealistic.

## **The Chunk Size and Top-k**

A sophisticated RAG should support flexible chunking and may add a little bit of overlap to prevent information loss. Generally speaking, the chunking process disregards the content of the text, and that causes a problem. The ideal content of the chunk should be consistent around a single topic for the embedding models to work better. They should not jump from one topic to another; they should not change the scenes. As depicted in the SVM test case, the model prefers short and polarised input.

Then how about we choose all small chunks? In this case, we need to consider the impact of the parameter top_k. RAG systems use top_k to choose how many top-scored chunks to feed into the generative LLM. In most designs, top_k is a fixed number. Therefore, if the chunk size is too small or the information in the chunks is not dense enough, we may not be able to extract all the necessary information from the vector database.

To people who are familiar with machine learning model tuning, does the pair of chunk size and top_k ring a bell? They look like the machine learning model's superparameters, don’t they? To make sure the RAG systems perform at their best, the chunk-size and top_k do need to be tuned to make sure they are the best fit. The old wisdom of superparameter tuning still apply, the only difference is that they are way more expensive to tune.

## World Knowledge

Consider the scenario that we are building a Harry Potter Q&A system. We have imported all Harry Potter stories into a vector database. Now, a question arises: how many heads does a dog have?

Most likely, the system will answer three because there are mentions of a huge dog that has three heads, and the system has no idea how many heads a normal dog may have.

> “Today AI and machine learning really sucks. Humans have common sense, machines don’t,”
>
> — Yann LeCun

Therefore, don't let the idea that the LLMs already know the solution fool you when we develop RAG systems. They don’t.

## Multi-hop Q&A

Let’s consider another scenario: we built a RAG system based on social media. Then we request: Who knows Elon Musk? Then the system will iterate through the vector database to extract a list of contacts for Elon Musk. Because of the limits of the chunk size and top_k, we can expect the list to be incomplete; nevertheless, functionally, it works.

Now, if we reframe our question and ask: Who can introduce Johnny Depp to Elon Musk, except Amber Heard? A single round of information retrieval cannot answer that kind of question. This type of question is called multi-hop Q&A. One way to solve it is:

1. retrieve all contacts of Elon Musk
2. retrieve all contacts of Johnny Depp
3. check whether there’s any intersection between the two results, except Amber Heard
4. Return the result if there’s any intersection, or extend the contacts of Elon Musk and Johnny Depp to their friends’ contacts and check again.

There are several architectures to accommodate this complicated algorithm; one of them uses sophisticated prompt engineering like ReACT, and another uses an external graph database to assist the reasoning. We just need to know that this is one of the limits of RAG systems.

## Information Loss

If we look at the chain of processes in the RAG system:

1\. Chunking the text and generating embedding for the chunks

2\. Retrieving the chunks by semantic similarity search

3\. Generate response based on the text of the top_k chunks

We will see that all the processes are lossy, which means there’s no guarantee that all information will be preserved in the result. As discussed above, chunking and embedding were lossy because of the selection of the chunk size and the power of embedding models; the retrieving process couldn’t be perfect because of the top_k limit and the similarity function we used; and the response generation process was imperfect because of the content length limit and the power of the generative LLMs.

If we put all the limits together and rethink the RAG-based enterprise search some companies are going to roll out, I’m really curious how much they could be better than the traditional full-text search engine. Bear in mind that the traditional search engine is very tough to beat. Microsoft E5 was the first LLM to surpass BM25, the popular search algorithm, not long ago.

What I mean is that the marriage of search engines and LLM is doable; however, it’s too difficult for simple RAG to perform better than search engines.

## Conclusion

RAG, as a simple and powerful LLM application design pattern, has its pros and cons. We do need to know the technology inside out to be confident in our design. My personal take is that despite all the hype about LLM and the amazing breakthroughs, LLMs should be placed as important components of the enterprise AI architecture. They shouldn’t be the main framework itself.

The limited power of the LLMs is one of my concerns, and explainability is another. All LLMs work like black boxes. People have no visibility into how they store their knowledge or how they reason. This is not a major issue for no-obligation applications, but it’s critical in enterprise settings. We can see that more and more regulatory rules were released to make sure the AI was doing no harm. We just need to do our due diligence in our project work.

In future research, I’m going to explore how to hybrid LLM with other external knowledge bases like graph databases to achieve harder-to-reach goals.

## References

## [What We Need to Know Before Adopting a Vector DatabaseTo continue with our journey toward applicable Generative AI, I would like to discuss some of the challenges of…medium.com](</@kelvin.lu.au/what-we-need-to-know-before-adopting-a-vector-database-85e137570fbb?source=post_page-----5024692f2c53--------------------------------------->)

## [Compare PDF Question Answering Systems Build with OpenAI and Google VertexAIThis post showed how to build a RAG with LangChain on both OpenAI and Google LLMs, and how the two solutions perform…medium.com](</@kelvin.lu.au/compare-pdf-question-answering-with-openai-and-google-vertexai-46638d62327b?source=post_page-----5024692f2c53--------------------------------------->)

## [Hosting A Text Embedding Model That is Better, Cheaper, and Faster Than OpenAI’s SolutionWith a little bit of technical effort we can get a better text embedding model that is superior to the OpenAI solution.medium.com](</@kelvin.lu.au/hosting-a-text-embedding-model-that-is-better-cheaper-and-faster-than-openais-solution-7675d8e7cab2?source=post_page-----5024692f2c53--------------------------------------->)

## [Fine-Tuning Embedding Model with PEFT and LoRAIn our previous discussion, we explored the evaluation of embedding models and the potential benefits of hosting these…medium.com](</@kelvin.lu.au/fine-tuning-embedding-model-with-peft-and-lora-3b6f08987c24?source=post_page-----5024692f2c53--------------------------------------->)

---
domain: generativeai.pub
fetch_date: '2026-05-18T12:47:46.177736'
status: ok
url: https://generativeai.pub/graph-rag-has-awesome-potential-but-currently-has-serious-flaws-c052a8a3107e
---

# Graph RAG Has Awesome Potential, But Currently Has Serious Flaws

[ ![Troyusrex](https://miro.medium.com/v2/da:true/resize:fill:64:64/0*rt5ciBejidyf_TFm) ](<https://medium.com/@troyusrex?source=post_page---byline--c052a8a3107e--------------------------------------->)

[Troyusrex](<https://medium.com/@troyusrex?source=post_page---byline--c052a8a3107e--------------------------------------->)

9 min read

·

Jul 19, 2024

\--

Listen

Share

More

I was very excited when Llama Index came out with their new Graph RAG implementation. It has great potential to make my RAG AI platform even better, and I jumped right on it. This is a very early implementation, and no doubt things will get better quickly, but my early results show little or no increase in search accuracy. Furthermore, the numerous calls to the AI needed for the Graph RAG mean it is slow (times are in minutes, not seconds) and expensive (as much as $1 per query).

That said, I have very high hopes that Graph RAG will make searches significantly more powerful and that costs will drop rapidly. I’m working hard to be part of that evolution, and I propose a potential solution. I call it hybrid bottom-up and it will leverage the power of Graph RAG while reducing the costs.

Press enter or click to view image in full size

## What is Graph RAG?

Graph RAG is a way to have AI answer questions based on the relationship between entities instead of on the entities themselves. For example, if you were to ask an AI about the difference between beagles and boxers, a regular AI would focus on the dogs themselves. A typical graph RAG answer would focus more on the relationships of the dogs to other things: “Beagles are friendly and great family pets but can be stubborn to train, while Boxers are playful and protective, requiring consistent training.”

Another way to think about Graph RAG is if you considered the closeness of cities to each other not by their physical proximity, but by their connection via air flights. In that context, New York would be closer to Paris than to Hartford, Connecticut. Although Paris is over 30 times as far in miles, there are many more daily direct flights from New York to Paris. As such, a Graph RAG would be more likely to link Paris to New York than a regular RAG AI would.

In theory, this will make searches much more powerful as it helps us understand the connections between things.

## Basic Overview: Data Setup

When pulling together the data for a Graph RAG, the system looks at a chunk of data (you decide how large; I went with 1024 tokens, which is approximately 800 words). It then passes each of those chunks into a Large Language Model (LLM) to have it extract the main ‘entities’, or items of interest, for each line and their relationship. A typical example would be the entities “Microsoft” and “NASDAQ” with the relationship “listed on” since Microsoft’s stock is traded on the NASDAQ stock exchange.

All of the entities are then clustered into “communities” of like entities. So Beagle and Boxer would be in one community, while Microsoft and NVIDIA would be in another. A second LLM call is made for each community to summarize what it is and what is in it.

## The High Cost of Graph RAG Data Preparation

This processing takes a lot of LLM calls: 1 call per data chunk to get the entities and then 1 call per cluster. Using Llama Index’s sample dataset of 50 documents and 10 clusters, it made a total of 218 LLM calls just for the data setup. If you are using GPT-4o at current pricing, these will cost you somewhere around 5 one-thousandths of a dollar each (depending on the number of tokens per call). With mine costing $1.20 for this data processing. Most of my datasets are much larger, with between 1,000 and 1,000,000 documents. This comes out to $60 per thousand records or $60,000 for my million-record dataset!

The good news is that this is (hopefully) a one-and-done exercise. Once you have processed a piece of data, you don’t have to reprocess it again.

There are also some ways to radically drive down this cost:

1. **Use an open-source model for entity extraction:** This could reduce the cost by a factor of 1000X. However, the prompt for this factoring is quite logic-intensive, and you’d have to be sure that the open-source model gives adequate results.

* **Use a cheaper model** : GPT-3.5 is 1/10th the price of GPT-4o. My very preliminary results show it probably operates well enough to do the entity extraction. $6 per 1,000 is still quite expensive, but at that price, I can afford to experiment with my data to see what works. $6,000 per million is still prohibitive absent a large increase in search accuracy.
* **Batching:** Batching API costs are 10% of the costs of regular API calls. Since this data is not needed real-time, this could be a huge cost saver.
* **Reduce the number of calls:** 218 calls seems like a lot for 50 pages. Then again, extracting entities means every piece of data needs to go to the LLM. I’m delving deep to see if there are efficiencies to be gained. For instance, perhaps some entities can be cached.
* **Extract entities algorithmically:** If we could extract algorithmically, then there’d be no need to send to an LLM at all. In domains with a known pre-set set of entities, for instance, baseball players and teams, this is a good solution.
* **Make larger nodes:** We could halve the number of nodes needed by doubling the size of each one. Unfortunately, pricing is usually based on the number of tokens, so sending half as many nodes at twice the size won’t save us anything. If you are being charged by call as well as token, this might make sense.
* **Make Fewer Communities:** This would reduce the number of summarization calls needed. It would also improve the performance and reduce the cost on the query side. Unfortunately, the fewer communities the fewer connections. Also, the more highly summarized the summaries are.

The good news is that the time and cost of this processing is one-and-done. That means that the time to process is irrelevant as long as the processing is all done before users start to query. While there are real-world effects on development time and ease of testing from slow data preparation, once live in production, that time has no impact on user experience.

LLM calls made during the actual user queries, however, have a huge impact on user experience, and currently, this Graph RAG implementation doesn’t do well on that front either.

## What Does a Graph RAG Do?

Let’s walk through what happens with a query for a Graph RAG. Say a user inputs “What are the best dog breeds for families?”. First, the Graph RAG takes that query and vectorizes it (turns it into numbers for processing). Then the Graph RAG makes an LLM call to each and every community summary, takes those answers, and sends them along with the query to answer the question.

Instead of sending the most relevant documents, as you would in a typical RAG, this Graph RAG sends the results of the query run against ALL the summaries of the various communities.

The upside of this is that because those summaries are based on communities of related entities, they include a lot of information that you likely wouldn’t find in a regular RAG. For instance, with dog breeds, it would be better able to compare temperaments of breeds than would a RAG AI without the connected relationships.

The downside is that since you are sending summaries of multiple documents combined into one, you can lose a lot of detailed information. After all, the entire purpose of summaries is to reduce the amount of detail.

The other big current issue is that since the query must be run through the LLM for every community and then the results combined, the amount of processing time and the cost is tremendous. If each LLM call averages 2 seconds (which would be quite quick), then a standard query against 10 communities would take 20 seconds for the communities and another 2 for the RAG including those summaries to go to the LLM. 22 seconds before any data begins to show is well beyond consumer expectations.

Note also how poorly this system scales. The more communities you have, the more queries and the longer they take. Yes, you can run these asynchronously so more than one can run at once, but this is a lot of calls to the LLM for one query.

There are some ways to minimize the number of calls and the cost:

1. **Decrease the number of communities:** Since the big cost is having a query per community, reducing the number of communities directly impacts the number of LLM calls. The flip side is that fewer communities means the summaries are less specific and potentially less useful. Normally, I would suggest automating an evaluation to see how the number of communities impacts cost. But currently even that test is cost-prohibitive.

* **Selective processing:** A semantic search to pre-select only the communities likely to be related would reduce costs. Of course, this is only as good as your ability to pre-select.
* **Caching:** Even with LLMs, the queries tend to be highly repetitive. Caching queries and results can go a long way to improving performance and reducing costs.

## A Bottom-Up Hybrid Approach?

I see a lot of promise in adding these relationships revealed by Graph RAG into my searches. Since I already have a very strong RAG AI search that combines hybrids with my own special tagging (really a poor man’s Graph RAG), the results of adding Graph RAG so far are underwhelming, and the performance and cost hits are devastating.

But I have a hypothesis on how to get the best of both worlds: Use my highly effective current search to retrieve the top 5 documents as per my typical RAG. Then, pull the summaries of the areas related to those documents (or maybe just the top 1 or two related) and send just those summaries along with my hybrid RAG results and the query to the LLM. This should drastically cut down on processing time and cost while still finding me highly relevant relationships.

While getting summaries from every community would doubtless provide extra relevant data for the RAG, my hypothesis is that that only the first one or two communities add enough relevant data to be worth the processing time and expense.

Furthermore, since the goal is to improve my current search, it doesn’t really matter if it isn’t as accurate as the full Graph RAG would be as long as it improves my search without adding too much time or cost.

I am already busy implementing and evaluating this approach and will let you know the results.

## Conclusion

At present, the Graph RAG implementation from Llama Index shows significant potential, but it faces several critical challenges that limit its immediate viability:

1. **Speed:** The current implementation is too slow for real-time applications, with query response times measured in minutes rather than seconds.

* **Cost:** The high number of LLM calls required for both data preparation and querying makes Graph RAG prohibitively expensive, especially for large datasets.
* **Scalability:** The system’s performance degrades as the number of communities increases, making it challenging to scale for larger, more complex datasets.
* **Accuracy:** Despite its theoretical advantages, early tests show little to no increase in search accuracy compared to traditional RAG systems.

However, these challenges should not overshadow the promising concept behind Graph RAG. As with many emerging technologies, we can expect rapid improvements and optimizations in the near future. Some potential areas for improvement include:

1. Optimizing entity extraction and community summarization processes to reduce initial setup costs.
2. Implementing more efficient querying mechanisms that don’t require processing every community for each query.
3. Developing hybrid approaches that combine the strengths of traditional RAG systems with the relationship-focused insights of Graph RAG.
4. Exploring the use of less expensive models or open-source alternatives for certain processing steps.

The proposed bottom-up hybrid approach, which combines traditional RAG results with selectively chosen Graph RAG community summaries, could offer a practical path forward. This method could potentially harness the relationship-based insights of Graph RAG while mitigating its current performance and cost issues.

As researchers and developers continue to refine Graph RAG techniques, we can anticipate significant improvements in both efficiency and effectiveness. The fundamental idea of leveraging entity relationships to enhance search and question-answering capabilities remains compelling, and future iterations of Graph RAG may well deliver on this promise.

In short, I believe Graph RAG will be a big improvement to RAG AI. It’s just not quite there yet.

This story is published on [Generative AI](<https://generativeai.pub/>). Connect with us on [LinkedIn](<https://www.linkedin.com/company/generative-ai-publication>) and follow [Zeniteq](<https://www.zeniteq.com/>) to stay in the loop with the latest AI stories.

Subscribe to our [newsletter](<https://www.generativeaipub.com/>) to stay updated with the latest news and updates on generative AI. Let’s shape the future of AI together!

---
domain: levelup.gitconnected.com
fetch_date: '2026-05-18T12:46:49.314710'
status: ok
url: https://levelup.gitconnected.com/safekeep-sciences-future-can-llms-transform-peer-review-e1f323caef08
---

# Safekeep Science’s Future: Can LLMs Transform Peer Review?

## |SCIENCE|PEER REVIEW|LLM|AI|

# Safekeep Science’s Future: Can LLMs Transform Peer Review?

## Peer review is today’s science core, but is flawed with bias and burdening researchers. Can we improve it?

[ ![Salvatore Raieli](https://miro.medium.com/v2/resize:fill:64:64/1*cs7O1sBNbybTazY4AtBwig.jpeg) ](<https://salvatore-raieli.medium.com/?source=post_page---byline--e1f323caef08--------------------------------------->)

[Salvatore Raieli](<https://salvatore-raieli.medium.com/?source=post_page---byline--e1f323caef08--------------------------------------->)

10 min read

·

Aug 14, 2024

\--

Listen

Share

More

Press enter or click to view image in full size

image created by the author using AI

> I love science. I hate supposition, superstition, exaggeration and falsified data. Show me the research, show me the results, show me the conclusions — and then show me some qualified peer reviews of all that. — Bill Vaughan

[**Peer review**](<https://en.wikipedia.org/wiki/Peer_review>)**is the foundational pillar of science.** The scientific literature is a reliable means of information by having experts in the field review and check the work of other aspects. It is not hyperbole to say that modern science (any scientific discipline from the natural sciences to computer science) is based on peer review. The passage of an article through peer review is a kind of seal that guarantees the article’s reliability and veracity. Despite its paramount importance in the scientific process, peer review is far from perfect.

## [How AI could save a pillar of sciencePeer review is a human job, but we may need the aid of the machinetowardsdatascience.com](<https://towardsdatascience.com/how-ai-could-save-a-pillar-of-science-43d564d5564d?source=post_page-----e1f323caef08--------------------------------------->)

## [How Science Contribution Has Become a Toxic EnvironmentHow computer science has inherited the same mistakes as other disciplinestowardsdatascience.com](<https://towardsdatascience.com/how-science-contribution-has-become-a-toxic-environment-6beb382cebcd?source=post_page-----e1f323caef08--------------------------------------->)

**Usually, different papers (or scientific conferences) have a different process.** Almost always, though, the manuscript is sent to an editor who evaluates the overall message of the article and then sends it to two or three reviewers. Reviewers are scientific experts in the field who have no affiliation with the author. These experts read and evaluate the manuscript and provide feedback to both the author and the editor. Authors then have to respond to this feedback, conducting if necessary further experiments, corrections, or changing other elements of the manuscript based on the suggestions of the reviewers. Once this is done the edited manuscript is sent back to the reviewers and editors. The reviewers suggest whether to accept or reject it, and the editor makes a decision. If the reviewers think more corrections are needed the process begins again [1].

> I think peer review is hindering science. In fact, I think it has become a completely corrupt system. It’s corrupt in many ways, in that scientists and academics have handed over to the editors of these journals the ability to make judgment on science and scientists. — Sydney Brenner

This typically makes it take at least three months before an article is accepted [2]. The data do not take into account the very high percentage of articles that are rejected and thus go through this process multiple times for different journals.

Reviewers are not paid, and reviewing manuscripts takes a considerable amount of time [3]. Many researchers therefore are not interested in dedicating themselves. In recent years, there have been fewer and fewer researchers available to conduct peer reviews. At the same time, the number of articles submitted to journals is continuously growing [4].

Peer review over the years has proven to have many problems:

* the judgments are not rigorous, the decision is volatile, and often influenced by external factors. In addition, the judgment of reviewers is often in disagreement [5–6].
* A researcher’s affiliation often has a greater impact than the quality of his or her work [7].
* There is gender bias because most reviewers are men [8–9].

For these reasons, people have begun to wonder whether the process could be automated. Analyzing an article and providing feedback (the peer review process in a nutshell) can be defined as a [Natural language processing](<https://en.wikipedia.org/wiki/Natural_language_processing>) (NLP) task. More precisely we could define it as a [generative AI](<https://en.wikipedia.org/wiki/Generative_artificial_intelligence>) task, where given the context (the manuscript) we want to generate feedback.

Previously attempts have been made on narrow aspects and with limited scope for automating the process. These approaches focus on extracting materials and methods, providing article summaries, and bibliometric analysis of references. This is because the analysis of scientific articles is complicated by knowledge of specific technical language (many generalist models struggle to adapt to a scientific domain) and the need for models that have prior knowledge of the topic (and can be adapted to new developments in the field).

An overview of a literature review generation task [11]

For example, in this study [10] they combined keyphrase extraction from the article (through the use of [BERT](<https://en.wikipedia.org/wiki/BERT_\(language_model\)>)) with citation analysis of the article. The output is a review that is generated by the system:

Press enter or click to view image in full size

Overall pipeline of automatic review generation method [10].

However, these approaches have serious limitations: there is no reasoning but are based on extraction, they are often repetitive or redundant, they rely on fixed templates, and there is no integration of information.

[Large Language Models (LLMs)](<https://github.com/SalvatoreRa/tutorial/blob/main/artificial%20intelligence/FAQ.md#:~:text=Large%20Language%20Models,-What%20is%20a>) have been considered by several authors to be the solution to these problems. LLMs after all excel in zero-shot and few-shot learning, common sense, and logical reasoning, and can be used in versatile ways for NLP tasks.

On the other hand, there are some problems associated with the use of LLMs:

* The inability to continue learning and thus the possibility of learning new knowledge.
* The adaptation to the scientific domain, being generalist models trained with huge amounts of nonspecific text.
* The production of hallucinations and thus generating text that sounds absolutely plausible but is full of inaccurate information.

Obviously, these are problems that are well-known and have been dealt with by the research community. There are several systems that have been developed to try to correct these behaviors, such as [Retrieval Augmented Generation (RAG)](<https://github.com/SalvatoreRa/tutorial/blob/main/artificial%20intelligence/FAQ.md#:~:text=Retrieval%20Augmented%20Generation%20\(RAG\),-What%20is%20Retrieval>).

## [A Requiem for the Transformer?Will be the transformer the model leading us to artificial general intelligence? Or will be replaced?towardsdatascience.com](<https://towardsdatascience.com/a-requiem-for-the-transformer-297e6f14e189?source=post_page-----e1f323caef08--------------------------------------->)

## [RAG is Dead, Long Live RAGIs it really true that long-context LLMs are killing the RAG?levelup.gitconnected.com](</rag-is-dead-long-live-rag-c607e1799199?source=post_page-----e1f323caef08--------------------------------------->)

An example of how these problems can lead to spectacular failures in science is [Galactica](<https://www.linkedin.com/posts/yann-lecun_what-meta-learned-from-galactica-the-doomed-activity-7130214818862567424-tCWL/>) [12]. This LLM was created by Meta with the scientific domain in focus and the authors claimed the ability to generate automatic review. the model was later withdrawn after three days precisely because of the hallucinations it generated [13].

> A fundamental problem with Galactica is that it is not able to distinguish truth from falsehood, a basic requirement for a language model designed to generate scientific text. People found that it made up fake papers (sometimes attributing them to real authors), and generated wiki articles about the [history of bears in space](<https://twitter.com/meaningness/status/1592634519269822464>) as readily as ones about protein complexes and the speed of light — [source](<https://www.technologyreview.com/2022/11/18/1063487/meta-large-language-model-ai-only-survived-three-days-gpt-3-science/>)

Press enter or click to view image in full size

Galactica Output. image source: [12]

Despite precedents attempts have proven unsuccessful there remains particular interest in automatic review generation. This in fact would reduce the backlog of articles to be analyzed, save time for article submitters, could be used to standardize the process, reduce bias, and much more.

Press enter or click to view image in full size

image source: [14]

To summarize to have an automatic review:

* we should have a model that knows the main literature on the topic.
* The model should be able to do a critical reading of the literature.
* The model should minimize hallucinations.
* The model should be able to provide feedback on an article.

> **We will look at how to solve the first three.**

According to some researchers, what led Galactica to failure was its hubris. In fact, in that study an attempt was made to create a model applicable to all domains of science, underestimating its heterogeneity. Instead, in a recent study [14] they tried to use an LLM for automatic literature review generation, thus limiting the use of an LLM to only one science task but also to only one science domain (propane dehydrogenation (PDH) catalysts).

This much better mimics the work of a reviewer, who has to perform a limited task and has in-depth but specific knowledge of a scientific domain.

Press enter or click to view image in full size

image source: [14]

The authors started by finding all articles in a specific field from 1980 to the present (especially those from a list of quality chemistry and chemical engineering journals). They then filtered out obvious duplicates first (thanks to titles and abstracts) and then conducted an analysis with an LLM to select all articles that were relevant to the project.

> To address the challenge of hallucinations in LLMs, a high priority has been placed on the detection and prevention of such phenomena. In the entire automated review generation process, we adopted a multi-level filtering and verification quality control strategy, similar to the concept of retrieval-augmented generation (RAG) — [source](<https://arxiv.org/pdf/2407.20906v1>)

Since hallucinations are the main limitation to the use of LLMs in science, the authors paid special attention to how to reduce them as much as possible. They started from the prompt, choosing strict and clear instructions to guide LLM to produce the most scientifically accurate output. Moreover, instead of conducting a single task, they decomposed the process into several specific subtasks (reading, summarization, and so on). The idea behind this is to maintain factual consistency but at the same time flexibility. So the authors established a list of questions to help the model extract the relevant content and at the same time answer based on the content. The authors then segmented the text and proceeded as if it were a conversation with the model.

In addition, they followed up with the next steps:

* **Text format filtering**. Hallucinations also originated from text structure disruptions, so they verified that the text structure (XML in many cases) was accurate.
* **DOI verification**. The DOI is a unique identifier of each article; using it as a verification system allows them to filter out some potential hallucinations.
* **Relevance verification**. In RAG documents that are redundant or have irrelevant information impact performance. Authors analyze whether responses are off-topic.
* **Self-consistency verification**. Since hallucinations are often stochastic in nature, the correct answer should be the most frequent if there are multiple interactions. The authors therefore use aggregation to eliminate stochastic hallucinations.
* **Full data stream traceability mechanism**. once generated you can trace the path to generation, this way you can verify the system

At the end of this process, the authors check for hallucinations with a focus on two types of inaccuracies:

> false positives, which include fabricated or inconsistent information, and false negatives, referring to overlooked or partially extracted content. Our focus was primarily on reducing false positives, while adopting a relatively tolerant stance on false negatives. — [source](<https://arxiv.org/pdf/2407.20906v1>)

Results show that the process greatly reduces hallucinations.

Press enter or click to view image in full size

Effectiveness of hallucination mitigation. Aggregation is sensibly reducing hallucination. image source: [14]

So far, therefore, we have a system that manages to be aware of the previous literature and minimizes hallucinations. The next part would be to have a system that was able to conduct a critical reading of a manuscript, propose corrections, potential experiments, and provide feedback. This last step could be done with specific questions to ask the model (‘ _Was the correct statistical analysis used in the article? Did the authors consider recent literature? Are there inconsistencies in the results? and so on_ ’).

However, this step requires additional reasoning skills and is currently beyond the capabilities of an LLM today. This means that still a complete peer review by one side of an LLM is not entirely feasible. Also, very few hallucinations are still not zero hallucinations.

That doesn’t mean I can’t assist, though, by perhaps conducting a flag of potential errors or problems in an article. As it stands, the system could already identify inconsistencies with the literature, some potential errors, and provide some potential feedback. Conducting a peer review is a process that requires concentration and is labor intensive; conducting a quick first review with an LLM could be a reduction in the burden of work for researchers.

### What do you think? Do you think we will be using LLMs as assistants for this task anytime soon? Let me know in the comments

## If you have found this interesting:

_You can look for my other articles, and you can also connect or reach me on_** __**[**_LinkedIn_**](<https://www.linkedin.com/in/salvatore-raieli/>)** _._**_Check_[** _this repository_**](<https://github.com/SalvatoreRa/ML-news-of-the-week>) _containing weekly updated ML & AI news. _**_I am open to collaborations and projects_** _and you can reach me on LinkedIn. You can also_[ _subscribe for free_](<https://salvatore-raieli.medium.com/subscribe>) _to get notified when I publish a new story._

## [Get an email whenever Salvatore Raieli publishes.Get an email whenever Salvatore Raieli publishes. By signing up, you will create a Medium account if you don’t already…salvatore-raieli.medium.com](<https://salvatore-raieli.medium.com/subscribe?source=post_page-----e1f323caef08--------------------------------------->)

_Here is the link to my GitHub repository, where I am collecting code and many resources related to machine learning, artificial intelligence, and more._

## [GitHub — SalvatoreRa/tutorial: Tutorials on machine learning, artificial intelligence, data science…Tutorials on machine learning, artificial intelligence, data science with math explanation and reusable code (in python…github.com](<https://github.com/SalvatoreRa/tutorial?source=post_page-----e1f323caef08--------------------------------------->)

_or you may be interested in one of my recent articles:_

## [Knowledge is Nothing Without Reasoning: Unlocking the Full Potential of RAG through Self-ReasoningEnhancing Reliability and Traceability in Retrieval-Augmented Generative Modelslevelup.gitconnected.com](</knowledge-is-nothing-without-reasoning-unlocking-the-full-potential-of-rag-through-self-reasoning-7ec213516a56?source=post_page-----e1f323caef08--------------------------------------->)

## [Short and Sweet: Enhancing LLM Performance with Constrained Chain-of-ThoughtSometimes few words are enough: reducing output length for increasing accuracytowardsdatascience.com](<https://towardsdatascience.com/short-and-sweet-enhancing-llm-performance-with-constrained-chain-of-thought-c4479361d995?source=post_page-----e1f323caef08--------------------------------------->)

## [Graph ML: Graph Data Representationhow to represent graph data? how to store them? how to do in Python?ai.gopubby.com](<https://ai.gopubby.com/graph-ml-graph-data-representation-fc9dd17e05c?source=post_page-----e1f323caef08--------------------------------------->)

## [AI Hallucinations: Can Memory Hold the Answer?Exploring How Memory Mechanisms Can Mitigate Hallucinations in Large Language Modelstowardsdatascience.com](<https://towardsdatascience.com/ai-hallucinations-can-memory-hold-the-answer-5d19fd157356?source=post_page-----e1f323caef08--------------------------------------->)

## Reference

Here is the list of the principal references I consulted to write this article, only the first name for an article is cited.

1. Li, 2022, Peer Review in Science: the pains and problems, [link](<https://sitn.hms.harvard.edu/flash/2022/peer-review-in-science-the-pains-and-problems/>)
2. Science, Peer-Review Duration, [link](<https://academic-accelerator.com/Review-Speed/Science>)
3. Kovanis, 2016, The Global Burden of Journal Peer Review in the Biomedical Literature: Strong Imbalance in the Collective Enterprise, [link](<https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0166387>)
4. The STM Report, [link](<https://www.stm-assoc.org/2015_02_20_STM_Report_2015.pdf>)
5. Peters, Peer-review practices of psychological journals: The fate of published articles, submitted again, [link](<https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/abs/peerreview-practices-of-psychological-journals-the-fate-of-published-articles-submitted-again/AFE650EB49A6B17992493DE5E49E4431>)
6. Rothwell, 2000, Reproducibility of peer review in clinical neuroscience: Is agreement between reviewers any greater than would be expected by chance alone? [link](<https://academic.oup.com/brain/article/123/9/1964/282957?login=false>)
7. Reingewertz, 2017, Academic In-Group Bias: An Empirical Examination of the Link between Author and Journal Affiliation, [link](<https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2946811>)
8. Lerback, Gender and Age Bias in Peer Review in Earth and Space Science Journals, [link](<https://peerreviewcongress.org/abstract/gender-and-age-bias-in-peer-review-in-earth-and-space-science-journals/>)
9. Helmer, 2017, Research: Gender bias in scholarly peer review, [link](<https://elifesciences.org/articles/21718#s3>)
10. Nikiforovskaya, 2020, Automatic generation of reviews of scientific papers, [link](<https://arxiv.org/abs/2010.04147>)
11. Kasanishi, 2023, SciReviewGen: A Large-scale Dataset for Automatic Literature Review Generation, [link](<https://arxiv.org/abs/2305.15186>)
12. Taylor, 2022, Galactica: A large language model for science, [link](<https://arxiv.org/abs/2211.09085>)
13. Heaven, 2013, Why Meta’s latest large language model survived only three days online, [link](<https://www.technologyreview.com/2022/11/18/1063487/meta-large-language-model-ai-only-survived-three-days-gpt-3-science/>)
14. Wu, 2024, Automated Review Generation Method Based on Large Language Models, [link](<https://arxiv.org/abs/2407.20906v1>)

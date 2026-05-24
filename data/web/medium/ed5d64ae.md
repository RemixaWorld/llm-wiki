---
domain: medium.com
fetch_date: '2026-05-18T12:53:29.052126'
status: ok
url: https://medium.com/@gupta.aman/the-challenge-of-reinforcement-learning-in-subjective-domains-315c61263ca4
---

# The challenge of reinforcement learning in subjective domains

[ ![Aman Gupta](https://miro.medium.com/v2/resize:fill:64:64/1*reugzAo-aVFiZLe_FnBbjQ.jpeg) ](</@gupta.aman?source=post_page---byline--315c61263ca4--------------------------------------->)

[Aman Gupta](</@gupta.aman?source=post_page---byline--315c61263ca4--------------------------------------->)

35 min read

·

Mar 26, 2025

\--

\--

Listen

Share

More

## 1\. Introduction

**Reinforcement Learning**(RL) has been behind some of the biggest AI breakthroughs in recent history. I remember the razzle dazzle in the media when [AlphaGo](<https://www.alphagomovie.com/>) had its moment, when it beat the highest-ranked Go player, Lee Sedol, in a straight fight. We were reminded of that success story for RL more recently with another breakthrough — the development of reasoning models that achieve frankly unbelievable results on domains like competition math and coding. Deepseek, with its [R1 model](<https://huggingface.co/deepseek-ai/DeepSeek-R1>) and the [related research paper](<https://arxiv.org/pdf/2501.12948>), has shown that large-scale RL can be used to increase an LLM’s ability on some tasks way beyond what can be achieved through pretraining or any other previous method. [Andrej Karpathy’s video](<https://youtu.be/7xTGNNLPyMI?si=okmn3_0eHgUne5um>) covering this topic is a very intuitive explanation of this latest discovery, and I highly recommend you watch it before you read further (the link above starts at the relevant timestamp in the video). It’s little surprise that the [2025 ACM Turing award](<https://awards.acm.org/about/2024-turing>) has been given to Richard Sutton and Andrew Barto for their contributions to the field of Reinforcement Learning.

### Outline

To properly understand the challenge with subjective domains, we need to see the problem from many perspectives. Here is how this article is structured:

* **Section 2: Related Work** — we discuss existing work applying RL in both objective and subjective domains.
* **Section 3:** **Problem Statement —** we understand the fundamental problems behind building a subjective a reward model.
* **Section 4: Language Modeling —** we use the latest mechanical interpretation tools to see if language models encode the right information useful to build reward models.
* **Section 5: Patterns in Subjectivity** — in this section, we discuss if there are orderly patterns in human _population_ preferences, leveraging the results from the field of _social choice theory_.
* **Section 6: Collecting preference data —** based on what we learned in Section 5, we discuss how human preference data gathering should be structured. Specifically, we discuss a proposal for a Monte Carlo simulation that can help us evaluate different methods without incurring large costs.
* **Section 7: Reward model architecture** — we discuss the structure of the model required to learn the complex patterns in subjective preference data. We also leverage existing research from the problem of _learning to rank_ and suggest alternative loss functions _._
* **Section 8: Reward model saturation —** subjective reward models will have limits on what they can evaluate. We discuss what those are and a potential solution to mitigate the issue.
* **Section 9: Conclusion —** we summarize the main conclusions we’ve reached over the course of the article.

As a break from the pattern of my previous posts, there are no hands-on experiments or results in this article. My hope is that this article will provide the grounding to dive deeper into relevant research areas, spur your curiosity and creativity, and help you potentially contribute towards solving this challenge.

## 2\. Related Work: Is RL the universal answer to scaling LLM abilities?

![Basic flow of the RL based learning in Language Models](https://miro.medium.com/v2/resize:fit:648/1*UZS2a3KpyQLdY-5Al4V0MA.png)

No, at least not on the basis of our current understanding. In the [same video from Karpathy](<https://youtu.be/7xTGNNLPyMI?si=J5rXgO5HIad6vR4Z>), he also discusses the limitations of this latest “RL for reasoning” breakthrough. This technique requires

* an **objective verifier** to provide rewards to the RL policy,
* that continues to provide an unambiguous reward signal for any level of hardness of the problem.

This can be done for math by just matching the answer, i.e., making sure we have a supervised math problem dataset where problems have a specific answer — like a number or a True/False output — and making sure LLM formats the answer in a parseable format. For competition coding, you could have a problem set like Leetcode, and the verifier is a code interpreter that runs the predefined test cases on LLM-generated code to provide a success or failure signal (Deepseek). Using these objective signals, along with a policy optimization algorithm like [PPO](<https://arxiv.org/pdf/1707.06347>) or [GRPO](<https://arxiv.org/abs/2402.03300>), LLMs show remarkable improvements in their abilities and benchmark scores.

![The huge math benchmark improvement through RL w/ objective verifiers (Deepseek, 2025)](https://miro.medium.com/v2/resize:fit:700/1*pLfK5VkLD29jtLqekTVKZg.png)

These verifiers can provide a meaningful signal irrespective of the hardness of the problem — if there are objective correctness criteria, then evaluation is easy. This means you can keep scaling RL with harder and harder inputs, and the reward model will not be the bottleneck in providing the reward signal to the model.

But there are a ton of use cases for LLMs that can’t be objectively judged at all. Karpathy uses humor as an example and shows how ambiguous the problem of applying RL for humor is. If you’ve tried to use LLMs to create jokes yourself, I’m sure you’ve found how all over the place its responses are.

![The scale of improvement on subjective tasks through RLHF (Anthropic, 2022). Compare the y-axis scale with the previous graph from Deepseek.](https://miro.medium.com/v2/resize:fit:700/1*UQgFFj6U4xQZZDKR4ZhQ3Q.png)

Even if you could make an LLM somewhat good at recognizing subjective behaviors, like creativity in fiction writing, it will have a limit on what _level_ of creativity it can distinguish. Maybe it can distinguish something written by someone with a very analytical mind, vs someone who writes for a living, but could they distinguish writing that’s good science fiction and Dune? This is a critical factor because it limits the scale of RL — your policy can _saturate_ the reward model where it can’t distinguish among multiple responses, and the improvement plateaus.

### Primer: Reward models from human feedback

The current architecture of reward models was defined by the first paper from OpenAI describing their [RLHF training technique](<https://arxiv.org/pdf/2009.01325>). In short, this is what they did:

![Illustration of the RLHF process (OpenAI, 2020)](https://miro.medium.com/v2/resize:fit:700/1*D-U4oU7cFhYX6p0aJY0Q3Q.png)

* Collected a dataset of prompts
* Generated multiple responses for each prompt from an LLM
* Asked humans to annotate their preferences, comparing different LLM responses for the same prompts. There are some nuances to how this can be done, but for simplicity, we assume that it’s a binary label — given a pair of responses, humans select one as _chosen_ and the other as _rejected_.
* They define a reward model architecture — Language Model (that outputs an embedding) and a linear layer mapping that projects the embedding to a single logit, giving the reward value.
* They train this model on the preference dataset, with the loss function that maximizes, loosely speaking, Reward(chosen response) — Reward(rejected response).
* After this is done, the reward model should be able to take any input (prompt + response) and assign a high or low reward to give feedback to the policy during training and improve the model’s ability to generate responses that align better with what humans would rate as chosen.

There are some alternate approaches that exist, and [this paper by Nvidia](<https://arxiv.org/pdf/2410.01257>) discusses some of them. For the sake of our discussion, we will fix the model architecture as shown in the diagram below. There is a language model that outputs an embedding from an input and a reward network that computes a numerical reward from that embedding.

![An abstraction of the Reward model architecture](https://miro.medium.com/v2/resize:fit:700/1*iJZJLypVqAtduf0YXvCyeQ.png)

## 3\. Problem Statement: Is reward modeling for subjective domains even possible?

This is the question that I’ve been pondering over for the last few weeks. Real life is very subjective — my taste in music, movies, genres of fiction books, etc., is my own — so how can AI be creative? If I’m feeling down, what I need to pick myself up is very personal, so how can LLMs have therapeutic conversations? Are there patterns behind subjective behaviors?

In this section, I am going to analyze the problem from the first principles.

### Is human preference data learnable?

If you’ve read any introductory book on Machine Learning, the first diagram in such a book often looks something like this:

![Easy to learn classifier boundary](https://miro.medium.com/v2/resize:fit:462/1*5g6LFmsSbeoOkyEXD3wvLQ.png) ![Harder to learn classifier boundary](https://miro.medium.com/v2/resize:fit:460/1*S518aXsZOjXtNZezWPX0PQ.png)

Here is another example where the data is not learnable at all.

![Impossible to learn classifier boundary](https://miro.medium.com/v2/resize:fit:700/1*Gea3cTYM20nhgDUnvAi1AQ.png)

Essentially, the starting problem of machine learning is this: Given some N-dimensional data, can you learn a boundary that separates some kind of data from another? The supervised learning dataset just contains examples — the input could be an image with labels identifying if it's a cat, dog, or something else.

![ImageNet classification examples](https://miro.medium.com/v2/resize:fit:559/1*JN_9-jcR80rn-FLsgLsBkw.jpeg)

Reward modeling can be thought of as a similar problem.

* You could think of the language model embedding as D-dimensional data that represents the relevant features that are helpful in identifying a response as good or bad.
* The reward network can be the classifier that is then able to encode human preferences — is the response good or not? — based on certain relevant features of the response.

Both of these aspects are worth a deep dive, and that’s what we are going to do.

### What do humans prefer?

First, let’s talk about how we would make a judgment if one response is better than the other — with an example. One of the areas that I’ve been looking at recently is LLM-powered roleplay, and here is a test sample from that use case. In this example, there are two different answers to the same question. Read the following question and responses, and before proceeding further, try to form an opinion on which feels “better” and why.

> **Question:**
>  What’s a personal rule you live by that others might find unusual?
>
> **Response A:**
>  I’m a bit of a pack rat. I keep everything. I have boxes and boxes of notes and papers and memorabilia from my days as a young journalist, from my days as a young professor, from my days as a presidential historian. My kids are always saying, “When you die, we’re going to need a bulldozer to get rid of all this stuff.” But I think it’s interesting. I mean, I have a letter from Lyndon Johnson that he sent to me when I was 24 years old and I was selected as a White House Fellow. I have a copy of the speech that I wrote for Lyndon Johnson when I was 24 years old. I have a picture of me with Lyndon Johnson. I have a picture of me with Jackie Kennedy. I have a picture of me with Martin Luther King. I have a picture of me with Bobby Kennedy. I mean, it’s a treasure trove of memorabilia. I think it’s interesting. I think someday somebody might find it interesting.
>
> **Response B:**
>  Ah, that’s an interesting question. You know, I’ve always believed that life is a tapestry of stories, and each person’s journey is woven with unique threads. A personal rule I live by is to always seek out and cherish the untold stories of everyday people. These stories, often overlooked, hold such profound lessons and insights about our shared human experience.
>
> Some might find this unusual because in a world rapidly moving towards quick sound bites and fleeting attention spans, taking the time to listen to and appreciate the depth of individual narratives can seem slow or even quaint. But much like the city I grew up in, New York — a place teeming with hidden stories and whispered histories — there’s so much value in the richness of listening. It’s a lesson I’ve learned both in my personal interactions and throughout my career as a biographer. As I often say, whatever it is that you do, if you have that passion and desire for it, that’s the most important thing, and for me, it’s the pursuit of these varied stories.

Let’s try to analyze this. To me, **Response A** is better. Here are my reasons:

* Response A has real **information** that helps you learn about the person. Response B could be condensed to less than half of its size without losing anything meaningful.
* Response A uses **anecdotes** , like what her kids say to her, to contextualize her habit. It mentions so many **real-life events** in her life. Response B has no real-life connections except that she grew up in New York.
* **Response A** has a language style that feels personal. There are like 15 “I”s in it. She says “I think it’s interesting” a lot. There is a large variation in sentence lengths. **Response B** seems like personality has been distilled away, and it's showing what remains. Sentence lengths are very similar — uniformity is the essence of robotic behavior.

I am sure you have additional opinions, and you may disagree with some of my reasons here (which is an important point that we will discuss in considerable detail — people have different preferences). What’s important right now is to identify potential _features_ that help someone make this decision. Here are some attributes of language that could be those features.

![Response A and Response B parts of speech](https://miro.medium.com/v2/resize:fit:700/1*t4l_j9D7SUQSH86_xKAkew.png)

* **Word “type” distribution**. This includes features like part-of-speech distribution (grammatical structure), number of syllables (related to [reading ease](<https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests>)), rarity of words, and informational and emotional value of words. They do explain some of the differences — if you look at the part-of-speech distribution (diagram above), you can see that response A has more proper nouns (PROPN) and pronouns (PRON) (relates to specificity), and Response B has way more adjectives (ADJ) and adverbs (ADV) (often related to [unneeded verbosity](<https://lifehacker.com/you-re-using-too-many-adjectives-and-other-common-writ-1847874443>)).
* **Language style.** This is similar to word type distribution, but at a less granular level — this could mean the text is serious or humorous, technical or informal, etc.
* **Relevance.** Topic overlap between prompt and response. If the response satisfies “true” user intent.
* **Information.** Amount of information, sequence of facts and concepts (for example, mystery is good for storytelling), type of information, rarity of information.
* **Relatability.** Social relatability to response

We could list more features, but these are enough to get the point across. Whether or not we can build a reward model **depends on answering these questions:**

* Do the Language Modeling embeddings contain this information?
* Does the preference data contain recognizable patterns across those features?

## 4\. Language Modeling for meaningful features

![How embeddings can encode reading ease and engagement](https://miro.medium.com/v2/resize:fit:700/1*-SwDzGezvy6Xe03Fd1C0UA.png)

While training language models, one useful by-product is a mapping from text into a vector representation that encodes some **meaningful** properties of the text. These embeddings can then be used in different ways. For example, they can be used to compute the L2 distance or cosine similarity between a pair of texts, which can tell you if two texts are similar — this powers modern text search mechanisms.

What features do the embeddings of these models encode? Actually, there is significant research in this area, and here is an excerpt from a [paper by Anthropic](<https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html>)

> At a high level, the **linear representation hypothesis** suggests that neural networks represent meaningful concepts — referred to as **_features_** — as directions in their activation spaces. The **superposition hypothesis** accepts the idea of linear representations and further hypothesizes that neural networks use the existence of almost-orthogonal directions in high-dimensional spaces to represent more features than there are dimensions.

Both the **linear representation hypothesis** and the **superposition hypothesis** are extremely powerful. To understand them visually, I highly recommend this [YouTube video by 3Blue1Brown](<https://www.youtube.com/watch?v=9-Jl0dxWQs8>), where he discusses how LLMs might store facts in their weights and, in that discussion, visually illustrates both of these concepts.

Knowing that directions encode meaningful concepts, we might ask: What are these meaningful concepts? Here is the answer from another excerpt in the same paper:

> Examples of features we find include features for **famous people** , features for **countries** and **cities** , and features tracking **type signatures in code**. Many features are multilingual (responding to the same concept across languages) and multimodal (responding to the same concept in both text and images), as well as **encompassing both abstract and concrete instantiations of the same idea** (such as code with security vulnerabilities, and abstract discussion of security vulnerabilities).

They actually put together a fun demo called [**Golden Gate Claude**](<https://www.anthropic.com/news/golden-gate-claude>) for a short period of time, which exploited the understanding of features in the activation space: _They identified the direction that correlates to the Golden Gate Bridge in San Francisco and tuned the strength of that feature up_. If you asked it anything, it would make sure to mention the Golden Gate Bridge in its response. Another excerpt from them:

> If you ask this “Golden Gate Claude” how to spend $10, it will recommend using it to drive across the Golden Gate Bridge and pay the toll. If you ask it to write a love story, it’ll tell you a tale of a car who can’t wait to cross its beloved bridge on a foggy day. If you ask it what it imagines it looks like, it will likely tell you that it imagines it looks like the Golden Gate Bridge.

For reward modeling, we identified a few potential features. Can we see if LLM embeddings do indeed contain similar features? Yes! The technology that makes it possible is called [Sparse Autoencoders](<https://www.deeplearningbook.org/contents/autoencoders.html>). Google has released a set of SAE called [gemma-scope](<https://huggingface.co/google/gemma-scope>), and we can see their output in a digestible format using [this interactive demo](<https://www.neuronpedia.org/gemma-scope#playground>). Let’s put our examples in there, and look at some of the features we get:

![Features found in activations of Gemma2–9B with Response A as input](https://miro.medium.com/v2/resize:fit:560/1*gPJTJSrF7wXDQSLutpkOPw.png)

As I look at the activations at different token residual streams, here are some features that I have picked out:

* (word type) forms of the verb “have.”
* (word type) the word “as” in various contexts and forms
* (word type) personal pronouns and expressions of self-reference
* (language style) items or elements associated with humor and satire
* (relevance) activities related to personal organization and productivity
* (relevance) career aspirations and transformations in personal identity
* (information) expressions related to creative and artistic processes
* (information) references to items or components related to personal belongings or possessions
* (information) references to historical events and traditions
* (information) references to political positions and affiliations
* (relatability) references to universally relatable concepts within communities

It seems like most of the feature themes we chose are represented in actual LLM features. It even thought that the first response was humorous because it said “I’m a bit of a pack rat”.

Let’s repeat the same exercise for the other response.

![Features found in activations of Gemma2–9B with Response B as input](https://miro.medium.com/v2/resize:fit:560/1*eftdd9ZrVwBrPwd9QpbX-Q.png)

Let’s pick out a few features from here as well:

* (word type) references to the second person, specifically the pronoun “you.”
* (word type) instances of the word “each.”
* (language style) positive attributes or evaluations
* (relevance) claims and statements regarding beliefs, opinions, and assertions
* (relevance) phrases related to self-reflection and personal growth
* (relevance) phrases related to decision-making and choices in life
* (information) phrases related to life and its various aspects
* (information) references to resources and vital information related to societal and cultural elements
* (information) elements related to transformation or success stories
* (information) references to personal journeys and life paths
* (relatability) expressions of shared human experience and connection
* (relatability) references to universally relatable concepts within communities

If you think these features are obvious as you read through them, then remember you are an intelligent, experienced human. These features are literally interpreted by a machine, which encodes meaning as numbers. So, it’s a very good thing that we find this list obvious.

So far, so good.

### Limitations of Language Modeling

While we found some positive signals on the quality of language modeling, there are a bunch of problems with the features extracted, too. Some features from the same texts include:

* technical terms and components related to machinery or programming within a context
* terms related to vehicle diagnostics and technology
* references to educational and governmental institutions focused on technology and textiles
* mentions of health conditions and risk factors

These are obviously not related to our texts. These can cause issues during reward modeling (and I believe that this would affect text generation as well, potentially causing hallucinations).

Beyond that, we should also recognize that we’ve only tried a simple example. While talking to someone about this, we started discussing humor, and we tried the Gemma scope playground on a joke we found online:

![Features found in activations of Gemma2–9B with a joke as input](https://miro.medium.com/v2/resize:fit:511/1*qiOuaXUlZ1wzf2PDyTAfiw.png)

Even after indicating to the LLM that the following text is a joke, none of the features across the tokens of the actual joke had the “humor feature” (which does exist, as it shows up on the token `joke`, and in Response A previously). The features are very literal — it’s clear Gemma2–9B doesn’t get this joke.

### Creator vs Critic

There is a correlation between the ability to answer _well_ and _judge_ an answer. Typically, though, judging is easier. Math proofs are easier to check than to come up with. It’s harder to invent a new art style than to critique it. One worthwhile research activity is to measure this gap — let’s call it the **creator-critic** gap — in current LLMs, as this may inform some bounds on how much an LLM can be improved by RL.

### Ensemble of Reward Models

Since language modeling is such a key component of building a good reward model, what can we do to improve it (beyond compute scaling)? The answer could lie in _domain specialization_. It has been repeatedly shown that continual pretraining (CPT) on a [domain-specific dataset improves the quality of the model](<https://huggingface.co/datasets/HuggingFaceTB/finemath>) in that domain, often at the expense of performance in other domains (with a [little experiment by me](</@gupta.aman/wildeweb-safety-improvement-poc-using-continual-pretraining-1e7ad2b00707>) showing that as well).

![Math benchmark score improvement with continual pretraining (HuggingFace, 2025)](https://miro.medium.com/v2/resize:fit:700/0*8P5BEK01oy9SndxA.png)

While we aim to train one general model, there is no limitation on how many reward models we can have (beyond the effort required to train them). Thus, we can create an ensemble of reward models, each of which is continually pretrained on datasets curated for all the relevant domains. During RL training, we just invoke the right one based on prompt classification.

![Ensemble of Reward Models](https://miro.medium.com/v2/resize:fit:700/1*0Ykp6wfMfdk10ZfP4pbmzw.png)

## 5\. Patterns in subjectivity

We now believe we can _identify the factors_ that go into human preferences. The question that remains is: Can we learn the mental process that humans go through to rate something as good or bad?

### (Partial) Order in preference data

To discuss this more objectively, let’s define a simple scenario: There is one prompt for the AI, and we generate a set **R** of _diverse_ responses from one or more LLMs.

For a moment, let’s assume that there was an _objective_ way to judge these responses. Then there will be one response that’s correct; let’s call it `r_correct`. If we were to list this out as a preference, we have this relation:

![image](https://miro.medium.com/v2/resize:fit:360/0*oZuG6ZZ7-QPLjUq9.png)

All the other elements of **R** are not comparable to each other because there can only be one right answer. This kind of ordering relationship among elements in a set can be called a [**partial order**](<https://en.wikipedia.org/wiki/Partially_ordered_set>). Specifically, in a partial order (strict version):

* **Asymmetry:** The following is not possible:

![image](https://miro.medium.com/v2/resize:fit:74/0*zOXQuP1FaKW4Kt2_.png)
* **Transitivity:** The following must hold:

![image](https://miro.medium.com/v2/resize:fit:125/0*YAvECU5_dj5r0IFM.png)

Both of these properties _are_ true for the objective case. Asymmetry is true because only the correct response is greater than others, and conditions for transitivity don’t even arise. It also has a special property — that it has a **greatest** element:

![image](https://miro.medium.com/v2/resize:fit:312/0*tUJH41laEQ0ql6XH.png)

There can only be one greatest element in a partially ordered set. The existence of this greatest element, or said another way, the best response, makes the reward allocation very simple.

Let’s now consider subjective preferences. What would we like to see in that data? Subjectivity means that we won’t find a single greatest element in the set. But, we could find multiple **maximal** elements, which are defined as:

![image](https://miro.medium.com/v2/resize:fit:479/0*__TPzSi63FTu7o8A.png)

It is not required that a maximal element is preferred over all others, but only that nothing is preferred over it. Hence, there can be many maximal elements, and that aligns with our intuition that many responses might be good in subjective use cases.

Let’s define a _sequence_ of maximal subsets of **R** as follows:

![image](https://miro.medium.com/v2/resize:fit:700/0*agLNy1EnQe2w2EXz.png)

We define the sequence of **R** recursively by removing the previous maximal subsets of R and finding the maximal elements in the remaining set. We could order the sequence as follows:

![image](https://miro.medium.com/v2/resize:fit:260/0*aICqTA2Zk8oIcZAU.png)

This formulation of order is a **_partial order on the power set_** of **R** if we assume that no other subsets are comparable to each other. This is the structure we are hoping to find in human preference data. Intuitively, this structure makes a lot of sense — people won’t agree on one _greatest of all time_(GOAT) anything — science fiction novels, rock songs, etc. — but there could be a set of GOAT works of fiction, then a set of great but not as good as GOAT works of fiction, etc.

If the data can be structured like this, there can be a nice smooth signal to the reward model to learn. Note that, in reality, the patterns will be hidden behind some noise, and heuristics will be required to find such patterns.

### Social Choice Theory

Do real preference datasets have nice structures? Both asymmetry and transitivity are not promised (as different people may have different preferences), and in general, there can be _cycles_ in the **preference graph** , where you have:

![image](https://miro.medium.com/v2/resize:fit:254/0*AKlSbCRpKaxQfV24.png)

So what do we make of it? Without making more assumptions, this data could be pure noise and, hence, unlearnable. Some practical methods (like in the [Nvidia paper](<https://arxiv.org/pdf/2410.01257>)) filter out prompts for whom the preference data has any cycles. They are obviously undesirable, but if you’re thinking that it’s just a manifestation of lazy annotators not making thoughtful choices, you’d be wrong.

That’s because this aspect has been studied in a field of economics called [social choice theory](<https://en.wikipedia.org/wiki/Social_choice_theory>). Social choice theory deals with studying the process and outcomes of making choices as a society, usually in the context of political or other elections. In that theory, there is a concept called the **Condorcet cycle** , a construct in the [Condorcet paradox](<https://en.wikipedia.org/wiki/Condorcet_paradox>).

> **Condorcet’s voting paradox** implies that it is logically impossible for any voting system to guarantee that a winner will have support from a majority of voters, even if every voter’s individual preferences are rational and avoid self-contradiction. For example (with a ranked ballot), majority of voters will prefer A to B, B to C, and also C to A.

![Marquis de Condorcet](https://miro.medium.com/v2/resize:fit:324/0*0zeOgwF25POwtZ2T)

More generally, [**Arrow’s impossibility theorem**](<https://en.wikipedia.org/wiki/Arrow%27s_impossibility_theorem>) states that, in a nutshell, no methods exist to get preference data that have some nice, highly desirable properties. In mentioning these social choice theory results, my main goal is to emphasize that rational preferences over reasonable choices can still lead to undesirable preference structures; population group dynamics are messy that way. The details of these two results are quite rewarding to understand — I first learned about them in this online [Game Theory course by Stanford](<https://www.youtube.com/playlist?list=PLeY-lFPWgBThrUy3um4FrZh7-fsrk17Ce>).

### Spatial Voting Theory

These impossibility results form a bleak picture, and we can decide to stop here and say that, no, human preference data is not learnable. However, these results are theoretical worst-case scenarios, and in practice, we may find that these don’t affect real-world data. Here is another excerpt from the Condorcet Paradox wiki page:

> A study of three-candidate elections analyzed 12 different models of voter behavior, and found the [spatial model of voting](<https://en.wikipedia.org/wiki/Spatial_model_of_voting>) to be the most accurate to real-world [ranked-ballot](<https://en.wikipedia.org/wiki/Ranked_voting>) election data. Analyzing this spatial model, they found the likelihood of a cycle to decrease to zero as the number of voters increases, with likelihoods of 5% for 100 voters, 0.5% for 1000 voters, and 0.06% for 10,000 voters.

Given the importance of political elections, the voting process has been studied in immense detail. One of these studies attempts to understand why voters vote the way they do, and it's called **spatial voting theory**. Some excerpts from a [Cambridge University book](<https://assets.cambridge.org/97805216/62222/sample/9780521662222ws.pdf>) on the topic:

> Following Anthony Downs (l957), we may think of both **voters and candidates as points in some n-dimensional issue or policy space**. A voter’s location in the space represents the voter’s ideal point (a.k.a. bliss point), whose coordinates tell us the position espoused by that voter on each of the issues. A candidate’s location in the space is taken to be an indicator of the candidate’s platform, i.e., her statement about the policy outcomes on each issue she hopes to achieve were she to be elected. Under the basic Downsian (proximity) model, **the voter chooses the candidate closest to his own ideal point**.
>
> In any spatial model of electoral competition, both voters and candidates are located at ideal points in a multidimensional space, **each dimension of which represents a substantive issue**. For example, the issue dimension of health care might be represented by a scale that ranges from the belief that government should provide universal health care to the opinion that medical expenses should be paid by individuals and private insurance plans.

The activation space of features is very similar to this multidimensional policy space! If we can identify any person's position in the activation space, then we could predict their preferences for any response!

Actually, this is how recommender systems have been working for over a decade. The [matrix factorization method](<https://en.wikipedia.org/wiki/Matrix_factorization_\(recommender_systems\)>) creates _user_ and _item_ embeddings in a **common embedding space** so that the user's location in that space defines their preferences. Here is an example from [Google’s machine learning course](<https://developers.google.com/machine-learning/recommendation/collaborative/basics>) that shows that users and movies can have positions in the same feature embedding space. We can predict that the user would like movies that are close to each other in the embedding space.

![Human preferences and movies on two dimensions. Children may not like Memento, and arthouse movie lovers may dislike Harry Potter.](https://miro.medium.com/v2/resize:fit:700/1*KbJWlkyIk9JSOZhuO7JRgQ.png)

In our case, though, we don’t want to learn the _individual users’ unique preferences_. We want to find out if _groups of humans have shared preferences_ so that our model can learn what features are preferred by most. IMO, it is a valuable research exercise to analyze datasets that show different types of user preferences at scale and find out if there is a shared preference distribution.

One possible outcome **is a power law** : that some features are relevant for assigning preferences in the eyes of many (like humor in conversations). At the same time, there is a long tail of features that only a few consider. If such a distribution does exist, we could find that the maximal elements in our set of responses correlate with certain values of a few features that are preferred by many.

There is also a likelihood of non-linear preference. For example, let’s consider the feature related to the amount of detail and information in a text. Too little and it’s not useful, and too much and it becomes overwhelming.

![Example of power law: Film Genre popularity based on IMDB data of film releases (2021), which could be used as a proxy for population preferences (@boknowsdata)](https://miro.medium.com/v2/resize:fit:700/1*RumJRsHA2JN8RVHUB5KV1Q.png)

## 6\. Putting it into practice

Let’s recap what we’ve found:

* _Do the Language Modeling embeddings contain relevant feature information?_ Yes, but it’s not perfect, and better language modeling could lead to better reward models.
* _Does the preference data contain recognizable patterns across those features?_ We’ve discussed spatial voting theory and how its concepts can lead us to recognizable structure in user preferences, manifesting as an order among sets of responses.

Based on these findings, how can we actually build a great reward model? What are the questions that we need to answer? Here are the important ones that come to mind:

* How do we gather human preferences data?
* What’s the right architecture for reward models?

### Gathering human preferences

This dataset can be seen to have three dimensions:

* Prompts — P
* Responses per prompt— R
* Choices (preferences) over responses — C

![Preference data volume](https://miro.medium.com/v2/resize:fit:529/1*hhgknAUvKjPJIiZF6W7SMQ.png)

There are two interconnected connections that we need to answer:

* How much data do we need along each dimension?
* What is the mechanism of preference selection? In social choice theory, people have studied tons of mechanisms — [pairwise ranking](<https://en.wikipedia.org/wiki/Condorcet_method>), [ranked voting](<https://en.wikipedia.org/wiki/Ranked_voting>), [score voting](<https://en.wikipedia.org/wiki/Score_voting>), [quadratic voting](<https://blog.tally.xyz/a-simple-guide-to-quadratic-voting-327b52addde1>), etc — and each method has its pros and cons.

They are interconnected because the mechanism can define the _efficiency_ of this process — presumably, the most appropriate mechanism will lead to higher quality data, and thus, we would need fewer samples in the dataset.

Let’s understand the nuances of each dimension:

* **Prompts (P):** Diversity and size in the prompt set are positive attributes. Many organizations, like [LMSys on huggingface](<https://huggingface.co/lmsys>), share large-scale user prompt datasets.
* **Responses (R):** This is a more complex topic. The set of responses for each prompt needs to be diverse because we need different feature activations across different responses — that’s the only way to learn good from bad. These responses are typically generated by LLMs to _align the input distribution_ of reward model sensitivity with LLM’s action space. For an LLM that can write, say, only amateur-level stories, we don’t want the reward function to score them all poorly because it was trained on the most creative works of fiction of all time (like a snobby critic). This limits the long-term viability of a reward model. IRL, preference data gathering mechanisms increase diversity using temperature or using multiple model checkpoints. Another important factor is to generate responses from a pretrained model that has _not_ undergone instruction tuning, as the latter often [reduces the entropy of the model](<https://youtu.be/bZQun8Y4L2A?si=lZnVVfCmOaOEMjV6>).
* **Choices (C)** : To me, this is the most complex part of this data collection, as there are so many choice-gathering mechanisms out there. The need for volume and diversity of data is even more critical here because the underlying patterns — like the power law distribution of preferred features or non-linearity in the strength of that preference — can be complex. Since this will involve a large operational effort, any work that’s done to optimize the efficiency of the process using the mechanism has a very large cost impact.

This discussion implies that we are not hoping to get preferences from a few people. A more appropriate term for them is **population** preferences, which more directly indicates the need for many people to rate the same responses. Thus, the RL method itself may be called **Reinforcement Learning from population feedback (RLPF) —** a new term that we are introducing**.**

### Proposal: Monte Carlo Simulation

While this is some qualitative guidance, launching a real-life operational effort will require some quantitative information. Learning with real-life experiments could be too costly even for larger AI labs, and I would posit that a **Monte Carlo simulation** can provide that quantitative information. We can use prior human preference datasets (LLM-relevant and others, like movie preferences) to make some grounded assumptions for:

* Dimensionality D of the feature set underlying the preferences
* Distribution from which **human raters** are sampled as D-dimensional feature vectors indicating their preferences and their strengths
* Distribution from which **prompts** are sampled as a D-dimensional feature vector; each prompt is _related_ to only a smaller subset of features, so it’s expected to be a sparse vector
* Distribution from which **responses** are sampled as a D-dimensional feature vector indicating strengths along each feature; modeling LLM capability and diversity

Then, we can run the simulation by defining:

* A random process to sample human preferences using a specific choice-gathering mechanism.
* A Neural network architecture, like an FFN, to train the reward model on sampled data

The reward model is then tested by generating more test samples (from the underlying distribution) and comparing simulated preferences to the reward model output.

We can find correlations between data volume, feature dimension, rater diversity, etc., with reward model accuracy, which helps us choose the right specifics for a real-life preference-gathering project.

## 7\. Reward model architecture

The reward model architecture that’s commonly used adds a linear layer projecting the output hidden states of an LLM down to a single logit. This gives us unique reward values for each token in the input, but only the reward attached to the last token in the input sequence is often considered the final reward. To me, this architecture has a few problems:

![Typical implementation of reward model](https://miro.medium.com/v2/resize:fit:700/1*eGbKGFR9JEHtnZ0Ap2_GjA.png)

* In our analysis with Gemma Scope, we found that feature activations are _highly localized_ to specific tokens’ residual streams. In Response A, the feature for humor was found only in one token’s stream (**rat** in _I’m a bit of a pack rat_). While reward model training will likely alter this distribution, the scale of reward model training is many orders of magnitude smaller than pretaining, so I’m doubtful how much impact it has on the feature activation space.
* A linear model seems woefully underpowered to learn the complexity of population preferences, especially due to the diversity of feature preferences across humans. In current reward models, it's possible that through the training process, the decoder stack learns to classify like humans as well, not just act as a language model.

There is some potential for creativity and experimentation in the architecture here. The minimum complexity version probably looks like this:

![Proposed reward model architecture to deal with the complexity of language model features and population preferences](https://miro.medium.com/v2/resize:fit:700/1*z4wXEGUCRncdeR5xb7iM_w.png)

* Pool the embeddings across the token streams into a single vector (by using mean pooling or other methods).
* Feed that as an input to an FFN. This allows for modeling non-linear patterns.
* Then, finally, add the linear layer projecting the FFN output down to a single logit.

### Reward Model Loss

The standard loss function used for training reward models attempts to maximize the difference in the chosen response’s reward and rejected response’s reward. Here is what the function looks like in [OpenAI’s RLHF paper](<https://arxiv.org/pdf/2009.01325>):

![Reward model training loss function, where r(x, y) is the scalar output of the reward model (OpenAI, 2020)](https://miro.medium.com/v2/resize:fit:674/1*AL0flBrELRuwumst1BE3iA.png)

This is often called the **RankNet** loss, named after the [RankNet model](<https://icml.cc/2015/wp-content/uploads/2015/06/icml_ranking.pdf>) that introduced a pairwise comparison-based loss function for document retrieval ranking and is based on the Bradley-Terry model for computing probabilities from pairwise comparisons. You might be familiar with Elo rankings in chess and other arenas, which are used to rank players; those scores are computed using this model. Ranking through learned models has been researched extensively and gives us a volume of research work to which we can refer.

The main challenge with this loss function is that it attempts to maximize the “reward distance” between every (chosen, rejected) pair of responses. And if many response pairs belong to the same prompt (or very similar prompts), we might have similar responses appear as both chosen and rejected in the dataset.

This is something that the community has realized, and the common fix is to use a wider scale for preference selection (Likert-7) and filter out samples where the preference was very close — as [Meta describes in its Llama3 paper](<https://arxiv.org/pdf/2407.21783>). This reduces the chances for this issue to occur because if the rejected response is strongly disliked, then it’s unlikely to be strongly liked as well.

(As an aside, the [DPO loss function](<https://arxiv.org/pdf/2305.18290>) mirrors the pairwise approach. If curating a dataset for DPO, the same practices should be applied.)

Previously, we defined an order among the responses that is essentially a ranked list. We can use that with a **_listwise_ loss function**. It’s here where we can lean on some “learning to rank” research. The listwise loss function computes loss using _all values in a ranked lis_ t instead of just a pair sampled from that list.

Specifically, there is [research](<https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-2007-40.pdf>) that directly compares pairwise and listwise approaches to ranking. In the introduction, they mention their reasons why the pairwise approach may not be ideal:

> There are advantages with taking the pairwise approach. First, existing methodologies on classification can be directly applied. Second, the training instances of document pairs can be easily obtained in certain scenarios (Joachims, 2002). However, there are alsao problems with the approach. **First, the objective of learning is formalized as minimizing errors in classification of document pairs, rather than minimizing errors in ranking of documents.** Second, the training process is computationally costly, as the number of document pairs is very large. Third, the assumption of that the document pairs are generated i.i.d. is also too strong. Fourth, the number of generated document pairs varies largely from query to query, which will result in training a model biased toward queries with more document pairs.

The first negative listed above (in bold) is effectively the one that we highlighted. The research paper continues to define a loss function for listwise comparisons, that is, the cross entropy loss with **n** terms for a ranked list of size **n**. Here is what it will look like if we assume that the partial order on the power set of responses

![image](https://miro.medium.com/v2/resize:fit:260/0*aICqTA2Zk8oIcZAU.png)

is treated as a ranked list:

![Listwise loss function for reward model training when we have a ranked list of responses](https://miro.medium.com/v2/resize:fit:462/0*_ypp3HKWZXKm6f7D.png) ![Predicted probability distribution can be computed using softmax on predicted reward values](https://miro.medium.com/v2/resize:fit:324/0*EDJPV9qVqxjzZvZn.png) ![Ground-truth probability distribution can be computed from from “score” function s, computed heuristically from preference data](https://miro.medium.com/v2/resize:fit:260/0*Pcj75iXk_Sji9S1R.png)

This means that we need to compute scores for each of the responses in the training data — but if we have data to order them, we can use the same heuristic process to compute the score function as well.

Their research finds that **ListNet** , a model trained with listwise loss function, performs better than pairwise approaches.

## 8\. Reward model saturation

![robot shooting hoops (Google Imagen 3)](https://miro.medium.com/v2/resize:fit:512/1*v906-__cEK4tlUAWfnW0vA.png)

For tasks with objective reward signals, it doesn’t matter how difficult the task is. For example, if you’re teaching a robot to shoot a basketball through the hoop — whether it's standing a few feet away or beyond the half-line — the reward mechanism remains identical.

With a subjective task, consistency of reward allocation across task difficulty no longer holds. For example, if we consider the domain of law, some cases never go beyond the district courts, whereas others are always destined for the Supreme Court. If the reward model is only trained on district court cases (say, to rate an analysis of the case), it will not do well for the Supreme Court cases. If a reward model dataset doesn’t have diversity over task complexity, the RL training process will _saturate_ the reward model. Beyond a certain level of complexity, the reward model won’t be able to tell good from bad.

If our preference data only annotates responses generated by LLM, these bounds on reward model abilities will always exist. “Expert” human answers are not the solution, either. The best work humanity has done isn’t done in an hour or even a day. A book written and refined over multiple years will have more quality than any practical method we can enact to answer prompts with the highest-quality responses.

### Data curation for Prompt Response datasets

This is the area where the scope for innovation may lie. One may believe that for most real-life prompts, the response to it already exists somewhere in the recorded works of humanity. Not only that, but _many_ responses exist at varying levels of _quality_. For example, if I want to know more about sleep training a baby, there exists a plethora of information — from low-effort blog posts to well-researched books with proven methods. LLMs are not good enough to create responses that cover the diversity of information (both in content and quality) out there in real life.

![Diversity of “all” relevant responses vs what we can easily generate](https://miro.medium.com/v2/resize:fit:666/1*39No6lDrmfDUvLFFYctXNA.png)

We could search the content dataset and use the retrieved information to aid the generation of LLM responses. This shifts the focus on search quality, and one can argue that similar constraints (of lack of diversity) apply to _methods of search_ as well. Intuitively, though, we may believe that search may cover a larger portion of real-life content diversity.

Data curation can be considered a method of search. Computationally, it sits at the opposite end of online search mechanisms, taking 1000s of GPU hrs to complete a pass through the dataset as opposed to mere milliseconds for online search (which, _theoretically_ , is a pass through all internet data). Thus, it can afford more complex methods to find the content we may be looking for.

Is it possible to curate a (prompt, responses) dataset using curation? Let’s think it through — what are the steps?

* Let’s assume we already have a prompt set of size P (assumed to be in millions).
* The content dataset has size T, which is assumed to be in billions.
* We need two _functions:_`score(prompt, content)` and `response(prompt, content)`. The first one matches relevant content, and the other one extracts the relevant portion and generates a response (like in RAG).
* Typically, data curation involves linearly looping through the content dataset, executing a function `score(content)`. This has complexity O(T).
* In our case, since `score` needs to run once for each prompt, the complexity is O(P*T). If current curation processes take 1000s of GPU hours, this means billions of GPU hours! Over a year for a data center with 10,000 GPUs!
* We can optimize it — we could partition it based on various criteria, like the subject or theme. We could do the same for prompts. Let’s assume there are k partitions, and we get the time complexity as O(k * P/k * T/k) = O(P*T/k) (assuming equal-sized partitions). Depending on the value of k, this can enter the realm of feasibility for large labs.
* Finally, we need to generate responses using an LLM. Let’s assume we generate R responses per prompt, using R different items of content that are sampled based on their scores. Then, this has the complexity of O(P*R), which is much smaller because it’s not proportional to T, only P and R.

We skipped over the nuance of how to implement `score` and `response` methods, and sampling top R content items per prompt. These are nontrivial problems.

Overall, it is a computationally intensive process but not outside the realm of real-life workstreams. Combining this with an ensemble approach to reward modeling and population scale preference data, we could build a reward model that withstands RL training for enough steps to see a large quality jump, similar to the recent reasoning models.

## **9\. Conclusion**

In this article, we have discussed the problem of RL training in subjective domains from many perspectives, leaning on AI research like interpretability analysis and theories from outside the ML domain, like social choice theory. More than a few ideas are sprinkled throughout the article on how we might get closer to building a reward model that powers this learning process.

Despite the breadth of coverage, there are many areas we’ve only lightly touched. One that comes to mind is the policy optimization process itself (like PPO or GRPO). Understanding the limits of the current policy optimization processes might help us invent new ones.

As I write this, having written the rest of the article, the biggest takeaway for me is that _it’s going to take quite a monumental effort_ to perform large-scale RL in subjective domains. That said, that kind of effort is not dissimilar to the methods (extreme scale pretraining) that have led to the leaps the industry has taken over the last decade.

The question worth pondering is whether we need RL to make language models super capable in subjective domains. As of now, pre-training scale and dataset improvements are really the only known methods for making meaningful improvements in subjective domains. And I’m not sure about you, but I don’t expect those methods to lead to a breakthrough level of improvement anytime soon. Time will tell what actually ends up working.

## Citation Information

``` @article{gupta2025subjectiverl, author = { Gupta, Aman }, title = { The challenge of reinforcement learning in subjective domains }, year = 2025, month = mar url = { https://medium.com/@gupta.aman/wildeweb-safety-improvement-poc-using-continual-pretraining-1e7ad2b00707 }, } ```

## References

1. Kohs, Greg (Director). (2017). _AlphaGo_ [Film]. Moxie Pictures. <https://www.alphagomovie.com/>
2. Guo, D., Yang, D., Zhang, H., Song, J., Zhang, R., Xu, R., et al (2025). _Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning_. [arXiv preprint arXiv:2501.12948](<https://arxiv.org/pdf/2501.12948>)
3. Andrej Karpathy. (2025, February 5). _Deep Dive into LLMs like ChatGPT_ [Video]. [YouTube](<https://www.youtube.com/watch?v=7xTGNNLPyMI>)
4. Association for Computing Machinery (2025, March 5). _ACM A.M. Turing Award Honors Two Researchers Who Led the Development of Cornerstone AI Technology_. <https://awards.acm.org/about/2024-turing>
5. Schulman, J., Wolski, F., Dhariwal, P., Radford, A., & Klimov, O. (2017). _Proximal policy optimization algorithms_. [arXiv preprint arXiv:1707.06347](<https://arxiv.org/abs/1707.06347>)
6. Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X., et al (2024). _Deepseekmath: Pushing the limits of mathematical reasoning in open language models_. [arXiv preprint arXiv:2402.03300](<https://arxiv.org/pdf/2402.03300>)
7. Bai, Y., Jones, A., Ndousse, K., Askell, A., Chen, A., DasSarma, N., eta al (2022). _Training a helpful and harmless assistant with reinforcement learning from human feedback_. [arXiv preprint arXiv:2204.05862](<https://arxiv.org/pdf/2204.05862>).
8. Stiennon, N., Ouyang, L., Wu, J., Ziegler, D., Lowe, R., Voss, C., et al (2020). _Learning to summarize with human feedback_. [Advances in neural information processing systems, 33, 3008–3021](<https://arxiv.org/pdf/2009.01325>).
9. Wang, Z., Bukharin, A., Delalleau, O., Egert, D., Shen, G., Zeng, J., et al (2024). _Helpsteer2-preference: Complementing ratings with preferences_. [arXiv preprint arXiv:2410.01257](<https://arxiv.org/pdf/2410.01257>)
10. Russakovsky, O., Deng, J., Su, H., Krause, J., Satheesh, S., Ma, S., et al (2015). _Imagenet large scale visual recognition challenge._ [International journal of computer vision, 115, 211–252](<https://arxiv.org/pdf/1409.0575>)
11. Flesch R. (1948). _A new readability yardstick_. [The Journal of applied psychology, 32(3), 221–233](<https://comp311.wordpress.com/wp-content/uploads/2010/11/flesch_rudolph.pdf>)
12. Sarah Showfety (2021, October 18). _You’re Using Too Many Adjectives (and Other Common Writing Mistakes to Avoid)_. [LifeHacker](<https://lifehacker.com/you-re-using-too-many-adjectives-and-other-common-writ-1847874443>)
13. Adly Templeton, Tom Conerly, Jonathan Marcus, Jack Lindsey, Trenton Bricken, Brian Chen, et al (2024). _Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet._ [Antrophic](<https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html>)
14. Grant Sanderson (3Blue1Brown). (2024, August 31). _How might LLMs store facts | DL7_ [Video]. [YouTube](<https://www.youtube.com/watch?v=9-Jl0dxWQs8>)
15. Anthropic Product team (2024, May 23). _Golden Gate Claude_. [Anthropic](<https://www.anthropic.com/news/golden-gate-claude>)
16. Lieberum, T., Rajamanoharan, S., Conmy, A., Smith, L., Sonnerat, N., Varma, V., et al (2024). _Gemma scope: Open sparse autoencoders everywhere all at once on gemma 2_. [arXiv preprint arXiv:2408.05147](<https://arxiv.org/pdf/2408.05147>)
17. Ian Goodfellow, Yoshua Bengio, and Aaron Courville (2016). _Deep Learning_[Book]. [MIT Press](<http://www.deeplearningbook.org>)
18. Lin, Johnny (2023). _Neuronpedia: Interactive Reference and Tooling for Analyzing Neural Networks_. [Neuronpedia](<https://www.neuronpedia.org>)
19. Lozhkov, Anton and Ben Allal, Loubna and Bakouch, Elie and von Werra, Leandro and Wolf, Thomas (2024). _FineMath: the Finest Collection of Mathematical Content._ [HuggingFace](<https://huggingface.co/datasets/HuggingFaceTB/finemath>)
20. Gupta, Aman (2025). _WildeWeb: Safety Improvement PoC using Continual Pretraining._[Medium](</@gupta.aman/wildeweb-safety-improvement-poc-using-continual-pretraining-1e7ad2b00707>)
21. Partially ordered set. (2025, February 25). [Wikipedia](<https://en.wikipedia.org/wiki/Partially_ordered_set>)
22. Social choice theory. (2025, February 15). [Wikipedia](<https://en.wikipedia.org/wiki/Social_choice_theory>)
23. Condorcet paradox. (2025, March 12). [Wikipedia](<https://en.wikipedia.org/wiki/Condorcet_paradox>)
24. Arrow’s impossibility theorem. (2025, February 19). [Wikipedia](<https://en.wikipedia.org/wiki/Arrow%27s_impossibility_theorem>)
25. Matt Jackson, Yoav Shoham, and Kevin Leyton-Brown (Game Theory Online). (2014). _Game Theory II — Week 1 (Social Choice)_ [Video Playlist]. [YouTube](<https://www.youtube.com/playlist?list=PLeY-lFPWgBThrUy3um4FrZh7-fsrk17Ce>)
26. Merrill, III, S., & Grofman, B. (1999). _A Unified Theory of Voting: Directional and Proximity Spatial Models_. [Cambridge: Cambridge University Press](<https://www.cambridge.org/core/books/unified-theory-of-voting/3AF7BC5F28148C947D61EF0DDE3F8B77>).
27. Matrix factorization (recommender systems). (2024, August 23). [Wikipedia](<https://en.wikipedia.org/wiki/Matrix_factorization_\(recommender_systems\)>)
28. Google for Developers (2025). _Recommendation Systems._[Google Developers](<https://developers.google.com/machine-learning/recommendation/collaborative/basics>)
29. Condorcet method. (2025, February 14). [Wikipedia](<https://en.wikipedia.org/wiki/Condorcet_method>)
30. Score voting. (2025, February 24). [Wikipedia](<https://en.wikipedia.org/wiki/Score_voting>)
31. Ranked voting. (2025, March 19). [Wikipedia](<https://en.wikipedia.org/wiki/Ranked_voting>)
32. Austin Robey (2022). _A Simple Guide to Quadratic Voting_. [Medium](<https://blog.tally.xyz/a-simple-guide-to-quadratic-voting-327b52addde1>)
33. Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Tianle Li et al (2023). _LMSYS-Chat-1M: A Large-Scale Real-World LLM Conversation Dataset_ [HuggingFace](<https://huggingface.co/datasets/lmsys/lmsys-chat-1m>).
34. Andrej Karpathy (Microsoft Developer). (2023, May 25). State of GPT | BRK216HFS [Video]. [YouTube](<https://youtu.be/bZQun8Y4L2A?si=JsO3pfqArPrMbCBA>)
35. Burges, C., Shaked, T., Renshaw, E., Lazier, A., Deeds, M., Hamilton, N., and Hullender, G. (2005). _Learning to rank using gradient descent_. [Proceedings of the 22nd International Conference on Machine Learning — ICML ’05](<https://icml.cc/2015/wp-content/uploads/2015/06/icml_ranking.pdf>)
36. Zhe Cao, Tao Qin, Tie-Yan Liu, Ming-Feng Tsai and Hang Li (2007). _Learning to rank: from pairwise approach to listwise approach_. [Proceedings of the 24th International Conference on Machine Learning — ICML ’07](<https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-2007-40.pdf>)
37. Grattafiori, A., Dubey, A., Jauhri, A., Pandey, A., Kadian, A., Al-Dahle, A., et al. (2024). _The llama 3 herd of models_. [arXiv preprint arXiv:2407.21783](<https://arxiv.org/pdf/2407.21783>)
38. Rafailov, R., Sharma, A., Mitchell, E., Manning, C. D., Ermon, S., & Finn, C. (2023). _Direct preference optimization: Your language model is secretly a reward model_. [Advances in Neural Information Processing Systems, 36, 53728–53741](<https://arxiv.org/pdf/2305.18290>)

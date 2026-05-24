---
domain: ai.gopubby.com
fetch_date: '2026-05-18T12:51:20.807478'
status: ok
url: https://ai.gopubby.com/making-llms-more-truthful-with-dola-a-contrastive-decoding-approach-part-i-1c2f90c91996
---

# Making LLMs more Truthful with DoLa: A Contrastive Decoding Approach (Part I)

[ ![Nikhil Anand](https://miro.medium.com/v2/resize:fill:64:64/1*WUi3_JE6nFyvnhbWnBxYKg.jpeg) ](<https://medium.com/@nikhilanandnj?source=post_page---byline--1c2f90c91996--------------------------------------->)

[Nikhil Anand](<https://medium.com/@nikhilanandnj?source=post_page---byline--1c2f90c91996--------------------------------------->)

5 min read

·

Nov 14, 2024

\--

Listen

Share

More

All my articles are free to read. [**_Non-members can read for free by clicking this link._**](</making-llms-more-truthful-with-dola-a-contrastive-decoding-approach-part-i-1c2f90c91996?sk=9dd1e9e43d18a8bbdb5678dfb0d6f274>)

Press enter or click to view image in full size

A Summary of the DoLa method

LLMs hallucinate a lot.

Some studies show that hallucinations are inevitable, and nothing we do could change that. Using LLMs for situations like medical consultations and legal issues without a human expert ensuring the trustworthiness of outputs might never be possible.

But has no one been able to eradicate hallucinations, at least to some extent?

Some people have tried to remove hallucinations and make LLMs more truthful in various ways. This blog discusses an exciting method called “[DoLa: Decoding by Contrasting Layers](<https://arxiv.org/abs/2309.03883>)”, which improved LLM truthfulness through a simple technique called contrastive decoding.

> **Note** : I would recommend going through [this blog](<https://medium.com/ai-in-plain-english/decoding-an-llms-thoughts-logit-lens-in-just-25-lines-of-code-100c1dbf2ac0>) if you don’t know how LLM decoding works before checking out this one. In summary though, through decoding, the activations at the output layer are passed through an unembedding layer and converted to logits, which are then passed through a softmax function to convert to probabilities. The token with the maximum probability becomes the next token output.

## The Method

The principle for the DoLa method is summarised in the diagram below:

Press enter or click to view image in full size

Step 1: Extract probability distributions from all layers

When we ask the LLM, “What is the capital of Washington?”, it outputs “Seattle”, probably because “Seattle” is the most famous city in Washington, and it inherently has a high token probability. However, the actual capital of Washington is “Olympia”.

> Note that in an “[early exit](<https://medium.com/ai-in-plain-english/decoding-an-llms-thoughts-logit-lens-in-just-25-lines-of-code-100c1dbf2ac0>)”, we take the activations at an intermediate layer and pass them through the unembedding and softmax layers directly to get output probabilities. It’s an “early exit” because we do this at intermediate layer activations rather than the final layer activations.

The DoLa method hypothesises that:

* **If a token is factually incorrect or doesn’t represent a fact, its probability remains constant across layers.** So if “Seattle” is 40% likely in the 16th layer, it remains around 40% likely even after the final 32nd layer. Additionally, a token like “was”, which doesn’t represent a fact, should remain constant across layers.
* **However, when a token is factually correct, it is brought out only in later layers.** While “Olympia” might have a probability of 2% at layer 16, its probability could grow to 30% by the time it reaches layer 32. The later layers seem to have “brought out” the fact by increasing that token’s probability.

Could outputting tokens with a **larger contrast in probability** across layers be smarter than outputting tokens with a **larger final layer probability**?

### How would this look in reality? Here’s an example.

To test the hypothesis, we ask the LLM questions, such as “Who was the first Nigerian to win the Nobel Prize, in which year?”. We then check the outputs at intermediate and final layers across token positions.

Press enter or click to view image in full size

Words pulled from the question and stopwords are predicted even at earlier layers, but words that required retrieval from some factual database were only finalised at later layers.

There are two key observations:

* Tokens like “Wole Soyinka” and “1986”, which needed to be retrieved from some factual database, were only predicted at the later layers.
* Tokens that are stopwords (“was”, “the”, etc.) and tokens that were copied directly from the question (“Nigerian”, “Nobel”, etc.) were predicted at much earlier layers, and the prediction did not change up to the final layer.

You’re hopefully getting the idea now.

Factual tokens have a **much larger contrast** across the layers, and boosting their probabilities according to this contrast could help ensure the LLM stays more truthful to the context.

### How do we implement this?

We are changing the “decoding” approach, which means that while we aren’t changing any of the activations to make our LLM more truthful, we are changing how the activations are decoded.

In standard decoding, we would convert the last layer’s hidden states to a probability distribution and use that to deduce the output token.

Now, we utilise the last layer along with some intermediate layers and take the difference of the probability distributions as our final probability distribution. The hope is that the truthful tokens’ probabilities get boosted further before we find the token with maximum probability and output _“Olympia”_.

Press enter or click to view image in full size

We subtract the “bad” distribution from the “good” distribution, so that “Olympia” gets boosted

Here, we subtract layer 16’s distribution from layer 32’s, so tokens high in both get penalised, while tokens smaller in layer 16 but more significant in layer 32 get boosted.

That’s the idea behind contrastive decoding — tokens that show _more considerable contrast_ are given _larger probabilities_.

By performing contrastive decoding, we find the token that shows the most significant change across layers, the “truthful token”.

> In this specific case, the method is called “Decoding by Contrasting Layers”, since we are literally contrasting layers to generate the net probability distribution for decoding.

Press enter or click to view image in full size

A Summary of the DoLa method

## Conclusions

This blog discussed the overall hypothesis and idea behind what was implemented in DoLa. I’ll write a “Part II” of this blog sometime soon to more precisely explain the steps involved in the method. But for now, it’s enough to understand how it fundamentally works.

This method shows how LLMs can be made more truthful by utilising information already present in the LLM through a modified decoding approach.

## Limitations

* **While the method works to some extent, it’s not clear why it works mechanistically.** Some might hypothesise that later layers “store the facts”, but it’s difficult to pinpoint a very specific mechanism in LLMs, which are generally hard to interpret.
* **The method might only sometimes be reliable or universal.** This is especially true since we don’t know “why” the technique works, and it might depend on the dataset they tested on.
* **The method only incrementally affects accuracy.** This is quite common in techniques like these since the LLM mechanisms are often quite complex. While the method started with a hypothesis, we hardly see a “100% true” hypothesis in LLMs.

## Acknowledgements

The contents of this blog are from the paper “[Dola: Decoding by Contrasting Layers](<https://arxiv.org/abs/2309.03883>)”. All diagrams were made using Canva.

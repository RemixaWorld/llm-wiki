---
domain: medium.com
fetch_date: '2026-05-18T12:52:58.308762'
status: ok
url: https://medium.com/data-science-in-your-pocket/what-is-chain-of-drafts-bye-bye-chain-of-thoughts-76658d913169
---

# What is Chain of Drafts? Bye Bye Chain of Thoughts

## faster, more efficient version of CoT

[ ![Mehul Gupta](https://miro.medium.com/v2/resize:fill:64:64/1*vyvhK_h4zA05mg_Y-n2qBA.jpeg) ](</@mehulgupta_7991?source=post_page---byline--76658d913169--------------------------------------->)

[Mehul Gupta](</@mehulgupta_7991?source=post_page---byline--76658d913169--------------------------------------->)

4 min read

·

Mar 2, 2025

\--

\--

Listen

Share

More

![Photo by Maria Lysenko on Unsplash](https://miro.medium.com/v2/resize:fit:700/0*lKL1De1OLal6IICa)

For quite a few months, Chain of Thoughts has been the go-to prompting technique for any guy who is using LLM or ChatGPT. One issue that I always found with the Chain of Thoughts (CoT) was its verbosity.

## [Subscribe to datasciencepocket on GumroadOn a Mission to teach AI to everyone !datasciencepocket.gumroad.com](<https://datasciencepocket.gumroad.com/?source=post_page-----76658d913169--------------------------------------->)

> It generates just too many tokens.

You ask ChatGPT a simple question and receive an essay in return? That’s where **Chain of Drafts (CoD)** comes in — a prompting technique designed to streamline reasoning without sacrificing accuracy. Think of it as the **“get to the point”** version of the more detailed Chain of Thought (CoT) approach. Let’s break it down!

## What is Chain of Drafts (CoD)?

CoD is a prompting method that **prioritizes concise reasoning steps** to improve efficiency. Unlike Chain of Thought (CoT), which walks through every single step in excruciating detail, CoD focuses on delivering only the **essential information** needed to solve a problem. This means:

* **Less verbosity** — No excessive explanations.
* **Fewer tokens** — Lower computational cost.
* **Faster responses** — Ideal for real-time applications.

## A Simple Example

![sample prompt](https://miro.medium.com/v2/resize:fit:700/1*nZ7eelvmYIcgTZonKQI4tw.png)

Let’s compare different prompting techniques using a basic math problem:

**Problem:** _Jason had 20 lollipops. He gave Denny some. Now he has 12 left. How many did Jason give to Denny?_

### Standard Prompting (Direct Answer)

* **Response:** _8_

### Chain of Thought (CoT) Prompting (Step-by-Step Explanation)

* **Response:**

> Jason started with 20 lollipops.
>
> After giving some away, he had 12 left.
>
> To find out how many he gave away, we subtract: 20–12.
>
> That gives us **8**.

### Chain of Drafts (CoD) Prompting (Concise Reasoning)

* **Response:** _20–12 = 8 → Final Answer: 8._

> See the difference? CoT is comprehensive but can be overkill. CoD trims the fat, retaining clarity while saving time.

## Metrics and benchmark

![image](https://miro.medium.com/v2/resize:fit:823/1*OmChNTPAYkWSmT88hN2u7Q.png) ![image](https://miro.medium.com/v2/resize:fit:394/1*0a_J-CeoFKHUYwxy7i_slA.png)

As you must be able to see, CoD appears to be the real-world problem solver, being in the middle of standard and CoT prompting.

## Why is CoD Better than CoT?

* **Same accuracy, fewer tokens** : CoD achieves nearly the same accuracy as CoT but with far fewer tokens, making it computationally cheaper and faster.
* **More efficiency** : Reducing token count means faster response times and lower costs in real-world applications.
* **Best of both worlds** : Unlike Standard Prompting, which sacrifices accuracy for brevity, and CoT, which is too verbose, CoD **strikes a balance** — concise yet accurate.

## Advantages and Disadvantages

### Advantages of CoD over CoT

> **Faster inference:** CoD generates responses quicker due to reduced token usage.
>
> **Lower computational cost:** Using fewer tokens translates to lower operational expenses.
>
> **More concise outputs:** Ideal for real-time applications where brevity is key.
>
> **Easier to integrate in production systems:** Less verbose reasoning makes responses more user-friendly.

### Disadvantages of CoD compared to CoT

* **Less transparency:** CoT provides a clear, step-by-step breakdown, which is useful for debugging and explaining reasoning.
* **Higher risk of errors in complex reasoning:** Some problems require detailed intermediate steps to ensure logical correctness, which CoD might skip.
* **Not ideal for educational purposes:** When learning a new concept, detailed explanations (as in CoT) can be more beneficial.

## Where CoD Works Best

* **Real-time AI applications** — Customer support, personal assistants, and chatbots.
* **Resource-constrained environments** — Running LLMs on edge devices or limited compute resources.
* **Summarization tasks** — Quickly distilling key points from text-heavy sources.
* Cost is priority

One last thing …

## Why is it called Chain of Drafts?

The name **“Chain of Drafts” (CoD)** comes from the idea that instead of fully elaborating each reasoning step (like in **Chain of Thought (CoT)**), the model generates **concise “drafts” of reasoning steps** — just enough to keep the logic intact without unnecessary verbosity.

> Think of it like **writing a rough draft instead of a full essay**. Instead of carefully spelling out every thought process in detail, CoD takes a **minimalist approach** , stripping reasoning down to its most essential components. This makes responses **faster, more efficient, and token-economical** , while still retaining accuracy.

The “chain” aspect still applies because there’s a **logical progression of thoughts** , just expressed in a more streamlined way.

## Wrapping Up

Chain of Drafts is a simple yet powerful tweak that enhances LLM efficiency without compromising correctness. If you want responses that are **faster, cheaper, and just as accurate** , COD is for you.

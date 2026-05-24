---
domain: thewhitebox.beehiiv.com
fetch_date: '2026-05-18T12:38:24.154266'
status: ok
url: https://thewhitebox.beehiiv.com/p/we-ve-hit-ai-hardware-2-0
---

![](https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,quality=80,format=auto,onerror=redirect/uploads/asset/file/f3b30d64-0c96-4851-8a63-3c5907e5a84f/image.png)

**THEWHITEBOX**

We’ve Hit AI Hardware 2.0

*Is heterogeneous hardware the new norm? *I profound believe so, but that isn’t good news for neither of us.

Over the last few days, something has changed in the AI industry: hardware. For years, **hardware dictated how AI software was built.**

Now,** it’s the other way around**.

This leads us to hardware 2.0, heterogeneous hardware built purposefully not only for AI, **but for AI inference in particular**. After reading this article in full, you will:

Intuitively understand how AI workloads work to a level of depth even most so-called experts don’t reach

Deeply understand ‘where AI hardware is going’ by understanding NVIDIA’s new product, the POD,

**the most powerful AI server the world has ever seen,**in striking detail most miss.The coveted inference technique that heterogeneous hardware finally unlocks,

And winners and losers of all this, which is particularly relevant,

**considering most stock market action in AI is hardware-based**, as AI software companies are mostly private.

This is a little bit longer content than usual. If the AI industry feels alien to you, it won’t be as much after this read. And if you are already an expert, you’ll be an even bigger one.

*This week is my personal agent week; ***I’m going to go deep into the trenches to test the limits of what can be done with agents***, and I’ll share my updated AI stack, or how I use AI in my daily routine, next weekend. Stay tuned!*

## Inference is taking over the world

Inference, the act of serving AI models to users, is the most important single word in the industry today.

However, **it’s also AI’s biggest concern**.

#### GPUs were not built for it

When a handful of AI researchers at Google presented the Transformer architecture back in 2017, the algorithm that has underpinned almost every inch of progress over what is now nearing a decade, **they built it to the image and likeness of NVIDIA GPUs**.

As researchers realized that AIs were going to get bigger and require more computations per second, they turned to the hardware that could deliver the highest compute per second: the GPU, and created an algorithm built to leverage GPUs' strengths.

**That ‘strength’ is parallelization**, being capable of doing a lot of computations in parallel so as to increase the number of computations one can do per second. Data is stored in memory, then fed to the processors, which perform many parallel computations and return the results to memory.

*Simply put, ***the more parallel a workload is, the better suited for GPUs.*** Conversely, if a workload is highly sequential, you’re leaving out a lot of ‘GPU potential’, just like buying a Ferrari that can reach 190 miles per hour to ride through the city at 30.*

Okay, I think we all knew GPUs were important in AI. Nevertheless, today, **we spend more than $500 billion per year on this hardware**, making the efficient use of it of utmost importance.

*But how do we measure this?*

### The most important metric in AI: arithmetic intensity

There’s a way to measure how well we’re using GPUs. **This “potential” is known as arithmetic intensity (AR)**.

**AR is a GPU’s main productivity metric**. It measures how much “work” the GPU performs per byte of data moved, which is what “all” engineers care about when optimizing AI infrastructure.

*But why is AR so important?* Well, because it tells you the degree of parallelization. **It’s a measure of work efficiency**. I’ve explained this before in greater detail, but to understand AR, we can think of it with a pretty intuitive example: **package delivery**.

Say you have a truck that can hold 50 packages, which is the number of packages to be delivered today.

If your warehouse is efficient, the truck will leave with either 50 packages or close to that to execute the delivery route. In that scenario, the delivery truck can deliver a large number of packages per route, potentially all at once. This is efficient; your truck was designed for this. You’ve parallelized the delivery to fifty households very effectively.

![](https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,quality=80,format=auto,onerror=redirect/uploads/asset/file/a4dc9792-1406-4fbf-8467-b409f854aae7/image.png)

Here, the truck (GPU) is filled to the brim, so every delivery route is super efficient, as we can do a lot of stops per route

Crucially, here, **you’re limited by how many packages your truck can hold in one route**. If you had to deliver 60 packages, the only reason you couldn’t deliver them in one go is that your truck is too small.

Hence, you’re ‘truck-bound’, because how much work you can deliver is limited by your truck’s size.

Instead, if that same truck with capacity for 50 packages leaves with only 10 from the warehouse because the forklift workers couldn’t supply enough packages on time,** the truck’s route will be shorter and will need to come back to the warehouse multiple times**, all the while having more than enough capacity to load larger amounts of packages and make fewer warehouse loadings.

That is, **despite having the opportunity to “do more” per delivery mile, the truck is heavily underutilized**.

![](https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,quality=80,format=auto,onerror=redirect/uploads/asset/file/79545fba-4e10-4ca4-9e25-656fd9584254/Generated_Image_March_23__2026_-_6_23PM.jpg)

This driver is going to have a long day going back to the warehouse many times to get the job finished.

Now think of the GPU’s potential parallelization capability, as the truck’s maximum package capacity. GPUs are the delivery trucks; it’s what gets you paid. But just like trucks need packages to deliver, **GPUs need data to process in order to generate the response to your cake recipe request**.

Thus, the warehouse and forklift are the memory and memory bandwidth, respectively; the warehouse might be massive, but if the forklift is painfully slow, not enough packages are loaded up in time.

So AR basically tells us “how many packages we are delivering per route”, a measure of how much of the GPU’s “work potential” we are using. If every byte of data provided by memory yields a lot of work, GPUs are well utilized.

**AR goes up**.If memory provides insufficient data, the GPU is basically idle; if the truck could deliver 50 packages in one route but instead has to do so in five because it leaves the warehouse almost empty every time, you are underutilizing your truck.

**AR goes down**.

But at the time when the Transformer was invented, **everyone was thinking of compute as the bottleneck**; how fast you could feed the processors that did the compute was secondary.

*Why?* We can’t blame them, as in that day and age, **the primary AI workload was model training**, a workload type you could design to do a lot of ‘work’ for every byte of data you sent to be processed.

*But why is that the case? And why is inference the exact opposite? *If we understand this, we understand **a lot** of what is happening in AI today.

### Understanding a training workload

AI training is considered extremely parallel (called ‘embarrassingly parallel’) for two reasons:

We know what each prediction should be

We don’t care about latency, as there isn’t a user waiting for the answer, unlike in inference


Let me explain. For example, say we want the AI to learn Gandhi’s famous quote, *“Be the change you wish to see in the world.”* You could have the model learn the quote by predicting each word one after the other. Instead, **we give the model the entire sequence to predict. **

In other words, instead of predicting the sequence in 11 consecutive steps, we do them all at once (see below for a visualization of what I mean).

As you can see, **the model returns a prediction for all 11 words simultaneously.** This is possible because modern LLMs are autoregressive, meaning each newly predicted word is conditioned on previous words, not future ones.

Put another way, instead of asking the model * “what word comes after ‘be the change’”* and next ask what word comes after

*“be the change that you…”*, You ask both questions at once because your GPU allows it.

![](https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,quality=80,format=auto,onerror=redirect/uploads/asset/file/e52807b8-9ec4-4f2b-9d49-9807340ec09b/Screen_Recording_2026-03-23_at_10.55.49.gif)

All eleven predictions are done in parallel. Source: Generated by author using ChatGPT animations

And why is this important? Think of our track analogy: Instead of doing 11 delivery routes to deliver 11 packages, we deliver all 11 in a single route because our truck (the GPU) can deliver them in parallel.

Therefore,* in training we make much better use of our GPU!* Less energy consumed (the truck’s fuel), much faster response (delivery timelines are faster).

Again, the crucial enabler of this is that we know what the sequence looks like. In turn, doing this requires more work from the GPU, so it will take longer to return results. Think of our truck analogy again, if we did 11 deliveries, a person would get their package faster than if they were the last in the 11-package route.

*Wouldn’t this still be slower, as the truck has to go back to the warehouse each time?* Yes, but in practice, we deploy several “trucks” in parallel (several GPUs working on different users).

If we do, each user gets their package super fast (since they are the only recipient on that route),** but we are doing an extremely poor use of each truck**; *we are using 11 trucks for something one could!*

It’s crucial that you understand this. Just like delivery routes, some workloads, like inference as we’re about to see, are inherently sequential.

So, yeah, we can deploy 11 trucks to fight this sequential nature, **but it’s an absolute waste of money**. Instead, the goal is to make use of the least amount of “hardware” possible per task.

Think about it this way:

Training is like low-priority package delivery: the users aren’t that time-sensitive; they just want the package relatively soon, but not

**now**.Inference, on the other hand, is like Amazon’s Prime delivery: being fast is all the user cares about; they want the package not today, but yesterday. In AI terms, inference is highly latency-sensitive.


And to make matters worse… **we don’t know what the rest of the sequence will look like**. Thus, in order to predict the next word, we need to predict the previous word first. This, as mentioned, makes inference inherently sequential.

Therefore, in inference, **we cannot predict the entire sequence simultaneously**, as we did during training. Instead, every word requires the previous word to have been predicted earlier to be predicted.

The way GPUs execute AI inference is something you are already highly aware of now, even if you don’t realize it (you see it every time you interact with ChatGPT), but it’s nonetheless represented below:

There are two stages:

**Prefill**is the initial part where the model takes in your input and produces the first word. As the entire input is processed simultaneously, it’s a highly parallelizable workload, and GPUs are just fine**Decode**is the sequential “one after the previous” process that generates the remaining words in the response, one after the previous.**This is an extremely sequential phase GPUs are not built for**. This distinction will become important later on.

![](https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,quality=80,format=auto,onerror=redirect/uploads/asset/file/e8af0e7e-3d80-40a6-ad4f-3432a44a61dd/Screen_Recording_2026-03-23_at_10.45.18.gif)

In inference, predictions are sequential. Source: Generated by author using ChatGPT animations

There’s no way to sugarcoat this: AI inference is, by nature, sequential. And sequential is the opposite of parallel. Thus,** the main consequence is that AR drops significantly below your ideal threshold**, sending us directly into memory-bottleneck territory.

Suddenly, it’s tremendously hard for our GPUs to run at full throttle; in inference, the “truck” is always leaving the warehouse half-empty.

**It’s important that we understand that this can’t be solved, only mitigated**. AI inference for autoregressive LLMs is inherently sequential; it just is.

**And the issue is that every single mitigation you implement involves a latency trade-off**, like increasing the batch size (the number of users served in parallel), which increases latency and hurts the user experience.

**Latency is the main user experience metric in AI**, so Labs are forced to use small batches, or even implement ‘fast mode’ like all offer these days; the problem with fast mode is that batches are so incredibly small that, unless you increase prices considerably, you lose a lot of money in the process. **This is why Claude’s fast mode is 6 times more expensive than the normal mode**.

So, as of now, we have two things:

While inference is taking over the AI world thanks to reasoning models and agents, latency-sensitive workloads now represent the most important workload type.

Sadly,

**GPUs can be considerably inefficient for inference**. We can serve inference very fast with them, but at the expense of very high prices.

So,* is there a better way?* Luckily, there is, even if once again, many companies have been taken completely off guard.

## Toward Hardware 2.0

If you look at most incumbent roadmaps, they are all building inference ASICs. That is, **they are building AI hardware that is optimized for inference**.

GPUs are basically unbeatable for training and inference prefill, but as the balance of compute shifts massively toward inference, **the temptation to avoid using GPUs for inference decoding is strong, at least in terms of performance**.

So, with the dawn of the inference era upon us, hardware companies are doing one of three things:

Building an HBM-heavy inference ASIC (we’ll see later what HBM actually is), with examples like Meta’s MTIA 400/500 series, to colocate with standard, GPU-like chips.

**These are basically GPU-like hardware, too, but tailored to inference by having much more memory and memory bandwidth.****Building a heterogeneous server**, with examples like NVIDIA’s POD,Reaching deals with

**external SRAM-only suppliers**to build heterogeneous servers, with examples like the Amazon and Cerebras partnership.

The point in common? All are heterogeneous builds.

*But what is a heterogeneous AI server?*

Let’s explain what it is and why it’s the future of AI hardware by looking at the three options and the players in each.

By the end, we’ll turn to software to explain a technique that is soon going to be table stakes for any inference provider that is remotely serious about winning the AI race: **SpecDec**, along with **several key metrics to watch for** that reveal the future of AI hardware over the next several years.

## Subscribe to Full Premium package to read the rest.

Become a paying subscriber of Full Premium package to get access to this post and other subscriber-only content.

Upgrade#### A subscription gets you:

- NO ADS
- An additional insights email on Tuesdays
- Gain access to TheWhiteBox's knowledge base to access four times more content than the free version on markets, cutting-edge research, company deep dives, AI engineering tips, & more

---
domain: medium.com
fetch_date: '2026-05-18T12:56:05.919027'
status: ok
url: https://medium.com/data-science-collective/building-research-agents-for-tech-insights-f175e3a5bcba
---

# Build Research Agents for Tech Insights

## Using a controlled workflow, unique data & prompt chaining

[ ![Ida Silfverskiöld](https://miro.medium.com/v2/resize:fill:64:64/1*-PJYZEnMvuSpoVNkHyVeZg.png) ](</@ilsilfverskiold?source=post_page---byline--f175e3a5bcba--------------------------------------->)

[Ida Silfverskiöld](</@ilsilfverskiold?source=post_page---byline--f175e3a5bcba--------------------------------------->)

9 min read

·

Sep 10, 2025

\--

Listen

Share

More

Press enter or click to view image in full size

_If you’re not a member and you would like to read this story click_[ _here._](</data-science-collective/building-research-agents-for-tech-insights-f175e3a5bcba?sk=19f4ebefe230af39d782977466ab552b>)

If you’ve ever asked ChatGPT something like: “Please scout all of tech for me and summarize trends and patterns based on what you think I would be interested in.”

You know that you’d get something generic, where it searches a few websites and news sources and hands you those.

This is because ChatGPT is built for general use cases. It applies normal search methods to fetch information, often limiting itself to a few web pages.

Press enter or click to view image in full size

Simple illustration of using ChatGPT search to build a report | Image by author

This article will show you how to build a niche agent that can scout all of tech, aggregate millions of texts, filter data based on a persona, and find patterns and themes you can act on.

The point of this workflow is to avoid sitting and scrolling through forums and social media on your own. The agent should do it for you, grabbing whatever is useful.

Press enter or click to view image in full size

An example monthly report for an PM/Investor persona by the agent | Image by author

We’ll be able to pull this off using a unique data source, a controlled workflow, and some prompt chaining techniques.

Press enter or click to view image in full size

The three different processes, the API, fetching/filtering data, summarizing | Image by author

By caching data, we can keep the cost down to a few cents per report.

If you want to try the bot without booting it up yourself, you can join this [Discord ](<https://discord.gg/v6BV49DCpp>)channel. You’ll find the repository [here](<https://github.com/ilsilfverskiold/ai-personalized-tech-reports-discord>) if you want to build it on your own.

This article focuses on the general architecture and how to build it, not the smaller coding details as you can find those in [Github](<https://github.com/ilsilfverskiold/ai-personalized-tech-reports-discord>).

### Notes on building

If you’re new to building with agents, you might feel like this one isn’t groundbreaking enough.

Still, if you want to build something that works, you will need to apply quite a lot of software engineering to your AI applications. Even if LLMs can now act on their own, they still need guidance and guardrails.

For workflows like this, where there is a clear path the system should take, you should build more structured “workflow-like” systems. If you have a human in the loop, you can work with something more dynamic.

The reason this workflow works so well is because I have a very good data source behind it. Without this data moat, the workflow wouldn’t be able to do better than ChatGPT.

### Preparing and caching data

Before we can build an agent, we need to prepare a data source it can tap into.

Something I think a lot of people get wrong when they work with LLM systems is the belief that AI can process and aggregate data entirely on its own.

LLMs work a bit as a communication layer, which means they can process some data but do not replace data engineering.

Press enter or click to view image in full size

LLMs working as a communication layer (simplified illustration) | Image by author

At some point, we might be able to give them enough tools to build on their own, but we’re not there yet in terms of reliability.

So when we build systems like this, we need data pipelines to be just as clean as for any other system.

The system I’ve built here uses a data source I already had available, which means I understand how to teach the LLM to tap into it.

It ingests thousands of texts from tech forums and websites per day and uses small NLP models to break down the main keywords, categorize them, and analyze sentiment.

This lets us see which keywords are trending within different categories over a specific time period.

Press enter or click to view image in full size

Trending keywords within different categories | Image by author

To build this agent, I added another endpoint that collects “facts” for each of these keywords.

This endpoint receives a keyword and a time period, and the system sorts comments and posts by engagement. Then it process the texts in chunks with smaller models that can decide which “facts” to keep.

Press enter or click to view image in full size

The “facts” extracting process for each keyword | Image by author

We apply a last LLM to summarize which facts are most important, keeping the source citations intact.

Press enter or click to view image in full size

What the result looks like once we have extracted some facts for a keyword | Image by author

This is a kind of prompt chaining process, and I built it to mimic LlamaIndex’s citation engine.

The first time the endpoint is called for a keyword, it can take up to half a minute to complete. But since the system caches the result, any repeat request takes just a few milliseconds.

As long as the models are small enough, the cost of running this on a few hundred keywords per day is minimal. Later, we can have the system run several keywords in parallel.

You can probably imagine now that we can build a system to fetch these keywords and facts to build different reports with LLMs.

### When to work with small vs larger models

Before moving on, let’s just mention that choosing the right model size matters.

I think this is on everyone’s mind right now.

There are quite advanced models you can use for any workflow, but as we start to apply more and more LLMs to these applications, the number of calls per run adds up quickly and this can get expensive.

So, when you can, use smaller models.

You saw that I used smaller models to cite and group sources in chunks. Other tasks that are great for small models include routing and parsing natural language into structured data.

If you find that the model is faltering, you can break the task down into smaller problems and use prompt chaining, first do one thing, then use that result to do the next, and so on.

You still want to use larger LLMs when you need to find patterns in very large texts, or when you’re communicating with humans.

In this workflow, the cost is minimal because the data is cached, similar queries are cached, and the only unique LLM calls are the final ones.

### How this agent works

Let’s go through how the agent works under the hood. I built the agent to run inside Discord, but that’s not the focus here. We’ll focus on the agent architecture.

I split the process into two parts: one setup, and one news. The first process asks the user to set up their profile.

Press enter or click to view image in full size

Since I already know how to work with the data source, I’ve built a fairly extensive system prompt that helps the LLM translate those inputs into something we can fetch data with later.

```sql PROMPT_PROFILE_NOTES = """You are tasked with defining a user persona based on the user's profile summary.Your job is to:1. Pick a short personality description for the user.2. Select the most relevant categories (major and minor).3. Choose keywords the user should track, strictly following the rules below (max 6).4. Decide on time period (based only on what the user asks for).5. Decide whether the user prefers concise or detailed summaries.Step 1. Personality- Write a short description of how we should think about the user.- Examples: - CMO for non-technical product → "non-technical, skip jargon, focus on product keywords." - CEO → "only include highly relevant keywords, no technical overload, straight to the point." - Developer → "technical, interested in detailed developer conversation and technical terms."[...] ```

I’ve also defined a schema for the outputs I need:

```python class ProfileNotesResponse(BaseModel): personality: str major_categories: List[str] minor_categories: List[str] keywords: List[str] time_period: str concise_summaries: bool ```

Without having domain knowledge of the API and how it works, it’s unlikely that an LLM would figure out how to do this on its own.

_You could try building a more extensive system where the LLM first tries to learn the API or the systems it is supposed to use, but that would make the workflow more unpredictable and costly._

For tasks like this, I try to always use structured outputs in JSON format. That way we can validate the result, and if validation fails, we re-run it.

This is the easiest way to work with LLMs in a system, especially when there’s no human in the loop to check what the model returns.

Once the LLM has translated the user profile into the properties we defined in the schema, we store the profile somewhere. I used MongoDB, but that’s optional.

Storing the personality isn’t strictly required, but you do need to translate what the user says into a form that lets you generate data.

### Generating the reports

Let’s look at what happens in the second step when the user triggers the report.

When the user hits the `/news` command, with or without a time period set, we first fetch the user profile data we’ve stored.

This gives the system the context it needs to fetch relevant data, using both categories and keywords tied to the profile. The default time period is weekly.

From this, we get a list of top and trending keywords for the selected time period that may be interesting to the user.

Press enter or click to view image in full size

Example of trending keywords that can come up from the system in two different categories | Image by author

Without this data source, building something like this would have been difficult. The data needs to be prepared in advance for the LLM to work with it properly.

After fetching keywords, it could make sense to add an LLM step that filters out keywords irrelevant to the user. I didn’t do that here.

> The more unnecessary information an LLM is handed, the harder it becomes for it to focus on what really matters. Your job is to make sure that whatever you feed it is relevant to the user’s actual question.

Next, we use the endpoint prepared earlier, which contains cached “facts” for each keyword. This gives us already vetted and sorted information for each one.

We run keyword calls in parallel to speed things up, but the first person to request a new keyword still has to wait a bit longer.

Once the results are in, we combine the data, remove duplicates, and parse the citations so each fact links back to a specific source via a keyword number.

We then run the data through a prompt-chaining process. The first LLM finds 5 to 7 themes and ranks them by relevance, based on the user profile. It also pulls out the key points.

Press enter or click to view image in full size

Short chain of prompting, breaking the task into smaller ones | Image by author

The second LLM pass uses both the themes and original data to generate two different summary lengths, along with a title.

We can do this to make sure to reduce cognitive load on the model.

This last step to build the report takes the most time, since I chose to use a reasoning model like GPT-5.

You could swap it for something faster, but I find advanced models are better at this last stuff.

The full process takes a few minutes, depending on how much has already been cached that day.

Check out the finished result below.

Press enter or click to view image in full size

How the tech scounting bot works in [Discord](<https://discord.gg/v6BV49DCpp>) | Image by author

If you want to look at the code and build this bot yourself, you can find it [here](<https://github.com/ilsilfverskiold/ai-personalized-tech-reports-discord>). If you just want to generate a report, you can join this [channel](<https://discord.gg/v6BV49DCpp>).

Press enter or click to view image in full size

A weekly report created for my profile | Image by author

I have some plans to improve it, but I’m happy to hear feedback if you find it useful.

And if you want a challenge, you can rebuild it into something else, like a content generator.

### Notes on building agents

Every agent you build will be different, so this is by no means a blueprint for building with LLMs. But you can see the level of software engineering this demands.

LLMs, at least for now, do not remove the need for good software and data engineers.

For this workflow, I’m mostly using LLMs to translate natural language into JSON and then move that through the system programmatically. It’s the easiest way to control the agent process, but also not what people usually imagine when they think of AI applications.

There are situations where using a more free-moving agent is ideal, especially when there is a human in the loop.

Hopefully you learned something, or got inspiration to build something on your own.

Or, you found the [Discord](<https://github.com/ilsilfverskiold/ai-personalized-tech-reports-discord>) bot useful to get some updates what’s going on in tech (I run these reports every day in a private channel but they could get better).

If you want to follow my writing, follow me here, my [website ](<https://www.ilsilfverskiold.com/>)or [LinkedIn](<https://www.linkedin.com/in/ida-silfverskiold/>).

❤

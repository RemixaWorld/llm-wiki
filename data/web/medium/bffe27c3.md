---
domain: medium.com
fetch_date: '2026-05-18T12:55:34.774405'
status: ok
url: https://medium.com/data-science-in-your-pocket/qwen-mt-the-best-ai-language-translation-model-beats-everything-5d38a3c7fcea
---

# Qwen-MT : The best AI Language Translation model, beats everything

## Beats Gemini 2.5 Pro, GPT and more

[ ![Mehul Gupta](https://miro.medium.com/v2/resize:fill:64:64/1*vyvhK_h4zA05mg_Y-n2qBA.jpeg) ](</@mehulgupta_7991?source=post_page---byline--5d38a3c7fcea--------------------------------------->)

[Mehul Gupta](</@mehulgupta_7991?source=post_page---byline--5d38a3c7fcea--------------------------------------->)

4 min read

·

Jul 24, 2025

\--

Listen

Share

More

Press enter or click to view image in full size

Photo by [Mark Rasmuson](<https://unsplash.com/@mrasmuson?utm_source=medium&utm_medium=referral>) on [Unsplash](<https://unsplash.com/?utm_source=medium&utm_medium=referral>)

While everyone is fighting for the top spot for the best AI LLM, there are problems like language translation that no one is paying attention to, and they are still stuck at the same point for along time

> Not for long, as Qwen-MT is here.

> Qwen just dropped a new update to their translation model: **Qwen-MT (Turbo)**. And yeah, the name sounds like something from a racing game, but the model’s actually solid.

**It builds on Qwen3, adds a massive pile of multilingual and translation-specific data, and uses reinforcement learning to make the output not just correct, but readable.**

## It Works Across 92 Languages

Press enter or click to view image in full size

Press enter or click to view image in full size

This thing supports 92 languages, including dialects. It’s not just Chinese, English, Spanish, they’ve thrown in Assamese, Swahili, even North Levantine Arabic. This covers over 95% of the people on the planet. And it’s not just “we added the language,” it’s actually usable.

## It’s Fast, And It’s Cheap

Qwen-MT runs on a **Mixture of Experts** setup. That means it only uses the parts of the model it needs for the job. Result: fast response, low API cost — **about $0.5 per million output tokens**. That’s useful if you’re building apps that need to translate stuff quickly and at scale.

## It Beats the Big Names

Press enter or click to view image in full size

Press enter or click to view image in full size

They tested Qwen-MT against a bunch of other models, GPT-4.1-mini, Gemini 2.5-Flash, Qwen3–8B. It beat them on standard translation benchmarks (like Chinese-English, English-German, WMT24). Even when stacked against huge models like GPT-4.1 or Gemini-Pro, it held up, while still being faster and lighter.

## Humans Liked It Too

Benchmarks are fine, but actual humans tested this too. Professional translators rated translations in 10 major languages. Qwen-MT came out ahead in both “good enough to use” and “really well done.” That’s not common.

## It Doesn’t Butcher Meaning

Press enter or click to view image in full size

Press enter or click to view image in full size

Some examples:

> Casual slang? It gets the tone right.
>
> Formal press statements? No weird phrasing.
>
> Long, cultural references? It keeps context.

Here’s a real one , a long sentence about a Chinese video game that mixes history and myth. Most models either over-explain it or flatten it. Qwen-MT nailed it. Felt like it came from a real person, not a script.

## You Can Control the Output

You can set **terminology rules,** like making sure it always translates “???” as “graphene.” You can also add **domain-specific prompts** , so it knows you’re talking about, say, IT or legal docs.

```json "terms": [ {"source": "???", "target": "graphene"}, {"source": "????", "target": "chemical elements"} ```

And it actually listens. No weird syntax. Just tell it what the sentence is about and how you want it to sound. Example: “This is from a cloud computing doc, translate like it’s for devs.” It’ll follow.

## Final Thoughts

Qwen-MT isn’t perfect. It’ll still fumble jokes and idioms like most models do. But for most real-world uses translating docs, product content, support tickets, subtitles, it’s clean, fast, and way better than expected.

> If you’re building anything that needs language translation without breaking the bank or the meaning, this one’s worth trying.

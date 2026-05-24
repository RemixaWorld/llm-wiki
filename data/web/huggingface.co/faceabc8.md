---
domain: huggingface.co
fetch_date: '2026-05-18T12:34:59.818020'
status: ok
url: https://huggingface.co/blog/wolfram/llm-comparison-test-llama-3?utm_source=ainews&utm_medium=email&utm_campaign=ainews-to-be-named-4285
---

![](https://cdn-avatars.huggingface.co/v1/production/uploads/5fd5e18a90b6dc4633f6d292/gZXHW5dd9R86AV9LMZ--y.png)

# LLM Comparison/Test: Llama 3 Instruct 70B + 8B HF/GGUF/EXL2 (20 versions tested and compared!)

Let's check out the new Llama 3 Instruct, 70B and 8B models. I'm also going to directly compare the most popular formats and quantizations available for local Llama 3 use.

Therefore, consider this post a **dual-purpose evaluation**: firstly, an in-depth assessment of Llama 3 Instruct's capabilities, and secondly, a comprehensive comparison of its HF, GGUF, and EXL2 formats across various quantization levels. In total, I have rigorously tested 20 individual model versions, working on this almost non-stop since Llama 3's release.

Read on if you want to know how Llama 3 performs in my series of tests, and to find out which format and quantization will give you the best results.

## Models (and quants) tested

- MaziyarPanahi/Meta-Llama-3-70B-Instruct-GGUF Q8_0, Q6_K, Q5_K_M, Q5_K_S, Q4_K_M, Q4_K_S, IQ4_XS, Q3_K_L, Q3_K_M, Q3_K_S, IQ3_XS, IQ2_XS, Q2_K, IQ1_M, IQ1_S
- NousResearch/Meta-Llama-3-70B-Instruct-GGUF Q5_K_M
- meta-llama/Meta-Llama-3-8B-Instruct HF (unquantized)
- turboderp/Llama-3-70B-Instruct-exl2 5.0bpw (
**UPDATE 2024-04-24!**), 4.5bpw, 4.0bpw - turboderp/Llama-3-8B-Instruct-exl2 6.0bpw
**UPDATE 2024-04-24:**casperhansen/llama-3-70b-instruct-awq AWQ (4-bit)

## Testing methodology

This is my tried and tested testing methodology:

**4 German data protection trainings:**- I run models through
**4**professional German online data protection trainings/exams - the same that our employees have to pass as well. - The test data and questions as well as all instructions are in German while the character card is in English. This
**tests translation capabilities and cross-language understanding**. - Before giving the information, I instruct the model (in German):
*I'll give you some information. Take note of this, but only answer with "OK" as confirmation of your acknowledgment, nothing else.*This**tests instruction understanding and following capabilities**. - After giving all the information about a topic, I give the model the exam question. It's a multiple choice (A/B/C) question, where the last one is the same as the first but with changed order and letters (X/Y/Z). Each test has 4-6 exam questions, for a total of
**18**multiple choice questions. - I rank models according to how many correct answers they give, primarily after being given the curriculum information beforehand, and secondarily (as a tie-breaker) after answering blind without being given the information beforehand.
- All tests are separate units, context is cleared in between, there's no memory/state kept between sessions.

- I run models through
- SillyTavern frontend
- koboldcpp backend (for GGUF models)
- oobabooga's text-generation-webui backend (for HF/EXL2 models)
**Deterministic**generation settings preset (to eliminate as many random factors as possible and allow for meaningful model comparisons)- Official Llama 3 Instruct prompt format

## Detailed Test Reports

And here are the detailed notes, the basis of my ranking, and also additional comments and observations:

**turboderp/Llama-3-70B-Instruct-exl2**EXL2 5.0bpw/4.5bpw, 8K context, Llama 3 Instruct format:- ✅ Gave correct answers to all
**18/18**multiple choice questions! Just the questions, no previous information, gave correct answers:**18/18**⭐ - ✅ Consistently acknowledged all data input with "OK".
- ✅ Followed instructions to answer with just a single letter or more than just a single letter.

- ✅ Gave correct answers to all

The 4.5bpw ~~is the largest EXL2 quant I can run on my dual 3090 GPUs, and it~~ aced all the tests, both regular and blind runs.

**UPDATE 2024-04-24:** Thanks to MeretrixDominum for pointing out that 2x 3090s can fit 5.0bpw with 8k context *using Q4 cache*! So I ran all the tests again three times with 5.0bpw and Q4 cache, and it aced all the tests as well!

Since EXL2 is not fully deterministic due to performance optimizations, I ran each test three times to ensure consistent results. The results were the same for all tests.

Llama 3 70B Instruct, when run with sufficient quantization, is clearly one of - if not the - best local models.

The only drawbacks are its limited native context (8K, which is twice as much as Llama 2, but still little compared to current state-of-the-art context sizes) and subpar German writing (compared to state-of-the-art models specifically trained on German, such as Command R+ or Mixtral). These are issues that Meta will hopefully address with their planned follow-up releases, and I'm sure the community is already working hard on finetunes that fix them as well.

**UPDATE 2023-09-17:****casperhansen/llama-3-70b-instruct-awq**AWQ (4-bit), 8K context, Llama 3 Instruct format:- ✅ Gave correct answers to all
**18/18**multiple choice questions! Just the questions, no previous information, gave correct answers:**17/18** - ✅ Consistently acknowledged all data input with "OK".
- ✅ Followed instructions to answer with just a single letter or more than just a single letter.

- ✅ Gave correct answers to all

The AWQ 4-bit quant performed equally as well as the EXL2 4.0bpw quant, i. e. it outperformed all GGUF quants, including the 8-bit. It also made exactly the same error in the blind runs as the EXL2 4-bit quant: During its first encounter with a suspicious email containing a malicious attachment, the AI decided to open the attachment, a mistake consistent across all Llama 3 Instruct versions tested.

That AWQ performs so well is great news for professional users who'll want to use vLLM or (my favorite, and recommendation) its fork aphrodite-engine for large-scale inference.

**turboderp/Llama-3-70B-Instruct-exl2**EXL2 4.0bpw, 8K context, Llama 3 Instruct format:- ✅ Gave correct answers to all
**18/18**multiple choice questions! Just the questions, no previous information, gave correct answers:**17/18** - ✅ Consistently acknowledged all data input with "OK".
- ✅ Followed instructions to answer with just a single letter or more than just a single letter.

- ✅ Gave correct answers to all

The EXL2 4-bit quants outperformed all GGUF quants, including the 8-bit. This difference, while minor, is still noteworthy.

Since EXL2 is not fully deterministic due to performance optimizations, I ran all tests three times to ensure consistent results. All results were the same throughout.

During its first encounter with a suspicious email containing a malicious attachment, the AI decided to open the attachment, a mistake consistent across all Llama 3 Instruct versions tested. However, it avoided a vishing attempt that all GGUF versions failed. I suspect that the EXL2 calibration dataset may have nudged it towards this correct decision.

In the end, it's a no brainer: If you can fully fit the EXL2 into VRAM, you should use it. This gave me the best performance, both in terms of speed and quality.

**MaziyarPanahi/Meta-Llama-3-70B-Instruct-GGUF**GGUF Q8_0/Q6_K/Q5_K_M/Q5_K_S/Q4_K_M/Q4_K_S/IQ4_XS, 8K context, Llama 3 Instruct format:- ✅ Gave correct answers to all
**18/18**multiple choice questions! Just the questions, no previous information, gave correct answers:**16/18** - ✅ Consistently acknowledged all data input with "OK".
- ✅ Followed instructions to answer with just a single letter or more than just a single letter.

- ✅ Gave correct answers to all

I tested all these quants: Q8_0, Q6_K, Q5_K_M, Q5_K_S, Q4_K_M, Q4_K_S, and (the updated) IQ4_XS. They all achieved identical scores, answered very similarly, and made exactly the same mistakes. This consistency is a positive indication that quantization hasn't significantly impacted their performance, at least not compared to Q8, the largest quant I tested (I tried the FP16 GGUF, but at 0.25T/s, it was far too slow to be practical for me). However, starting with Q4_K_M, I observed a slight drop in the quality/intelligence of responses compared to Q5_K_S and above - this didn't affect the scores, but it was noticeable.

All quants achieved a perfect score in the normal runs, but made these (exact same) two errors in the blind runs:

First, when confronted with a suspicious email containing a malicious attachment, the AI decided to open the attachment. This is a risky oversight in security awareness, assuming safety where caution is warranted.

Interestingly, the exact same question was asked again shortly afterwards in the same unit of tests, and the AI then chose the correct answer of not opening the malicious attachment but reporting the suspicious email. The chain of questions apparently steered the AI to a better place in its latent space and literally changed its mind.

Second, in a vishing (voice phishing) scenario, the AI correctly identified the attempt and hung up the phone, but failed to report the incident through proper channels. While not falling for the scam is a positive, neglecting to alert relevant parties about the vishing attempt is a missed opportunity to help prevent others from becoming victims.

Besides these issues, Llama 3 Instruct delivered flawless responses with excellent reasoning, showing a deep understanding of the tasks. Although it occasionally switched to English, it generally managed German well. Its proficiency isn't as polished as the Mistral models, suggesting it processes thoughts in English and translates to German. This is well-executed but not flawless, unlike models like Claude 3 Opus or Command R+ 103B, which appear to think natively in German, providing them a linguistic edge.

However, that's not surprising, as the Llama 3 models only support English officially. Once we get language-specific fine-tunes that maintain the base intelligence, or if Meta releases multilingual Llamas, the Llama 3 models will become significantly more versatile for use in languages other than English.

**NousResearch/Meta-Llama-3-70B-Instruct-GGUF**GGUF Q5_K_M, 8K context, Llama 3 Instruct format:- ✅ Gave correct answers to all
**18/18**multiple choice questions! Just the questions, no previous information, gave correct answers:**16/18** - ✅ Consistently acknowledged all data input with "OK".
- ✅ Followed instructions to answer with just a single letter or more than just a single letter.

- ✅ Gave correct answers to all

For comparison with MaziyarPanahi's quants, I also tested the largest quant released by NousResearch, their Q5_K_M GGUF. All results were consistently identical across the board.

Exactly as expected. I just wanted to confirm that the quants are of identical quality.

**MaziyarPanahi/Meta-Llama-3-70B-Instruct-GGUF**GGUF Q3_K_S/IQ3_XS/IQ2_XS, 8K context, Llama 3 Instruct format:- ✅ Gave correct answers to all
**18/18**multiple choice questions! Just the questions, no previous information, gave correct answers:**15/18** - ✅ Consistently acknowledged all data input with "OK".
- ✅ Followed instructions to answer with just a single letter or more than just a single letter.

- ✅ Gave correct answers to all

Surprisingly, Q3_K_S, IQ3_XS, and even IQ2_XS outperformed the larger Q3s. The scores unusually ranked from smallest to largest, contrary to expectations. Nonetheless, it's evident that the Q3 quants lag behind Q4 and above.

**MaziyarPanahi/Meta-Llama-3-70B-Instruct-GGUF**GGUF Q3_K_M, 8K context, Llama 3 Instruct format:- ✅ Gave correct answers to all
**18/18**multiple choice questions! Just the questions, no previous information, gave correct answers:**13/18** - ✅ Consistently acknowledged all data input with "OK".
- ✅ Followed instructions to answer with just a single letter or more than just a single letter.

- ✅ Gave correct answers to all

Q3_K_M showed weaker performance compared to larger quants. In addition to the two mistakes common across all quantized models, it also made three further errors by choosing two answers instead of the sole correct one.

**MaziyarPanahi/Meta-Llama-3-70B-Instruct-GGUF**GGUF Q3_K_L, 8K context, Llama 3 Instruct format:- ✅ Gave correct answers to all
**18/18**multiple choice questions! Just the questions, no previous information, gave correct answers:**11/18** - ✅ Consistently acknowledged all data input with "OK".
- ✅ Followed instructions to answer with just a single letter or more than just a single letter.

- ✅ Gave correct answers to all

Interestingly, Q3_K_L performed even poorer than Q3_K_M. It repeated the same errors as Q3_K_M by choosing two answers when only one was correct and compounded its shortcomings by incorrectly answering two questions that Q3_K_M had answered correctly.

**MaziyarPanahi/Meta-Llama-3-70B-Instruct-GGUF**GGUF Q2_K, 8K context, Llama 3 Instruct format:- ❌ Gave correct answers to only
**17/18**multiple choice questions! Just the questions, no previous information, gave correct answers:**14/18** - ✅ Consistently acknowledged all data input with "OK".
- ✅ Followed instructions to answer with just a single letter or more than just a single letter.

- ❌ Gave correct answers to only

Q2_K is the first quantization of Llama 3 70B that didn't achieve a perfect score in the regular runs. Therefore, I recommend using at least a 3-bit, or ideally a 4-bit, quantization of the 70B. However, even at Q2_K, the 70B remains a better choice than the unquantized 8B.

**meta-llama/Meta-Llama-3-8B-Instruct**HF unquantized, 8K context, Llama 3 Instruct format:- ❌ Gave correct answers to only
**17/18**multiple choice questions! Just the questions, no previous information, gave correct answers:**9/18** - ✅ Consistently acknowledged all data input with "OK".
- ❌ Did NOT follow instructions to answer with just a single letter or more than just a single letter consistently.

- ❌ Gave correct answers to only

This is the unquantized 8B model. For its size, it performed well, ranking at the upper end of that size category.

The one mistake it made during the standard runs was incorrectly categorizing the act of sending an email intended for a customer to an internal colleague, who is also your deputy, as a data breach. It made a lot more mistakes in the blind runs, but that's to be expected of smaller models.

Thus, I consider Llama 3 8B the best in its class. If you're confined to this size, the 8B or its derivatives are advisable. However, as is generally the case, larger models tend to be more effective, and I would prefer to run even a small quantization (just not 1-bit) of the 70B over the unquantized 8B.

**turboderp/Llama-3-8B-Instruct-exl2**EXL2 6.0bpw, 8K context, Llama 3 Instruct format:- ❌ Gave correct answers to only
**17/18**multiple choice questions! Just the questions, no previous information, gave correct answers:**9/18** - ✅ Consistently acknowledged all data input with "OK".
- ❌ Did NOT follow instructions to answer with just a single letter or more than just a single letter consistently.

- ❌ Gave correct answers to only

The 6.0bpw is the largest EXL2 quant of Llama 3 8B Instruct that turboderp, the creator of Exllama, has released. The results were identical to those of the GGUF.

Since EXL2 is not fully deterministic due to performance optimizations, I ran all tests three times to ensure consistency. The results were identical across all tests.

The one mistake it made during the standard runs was incorrectly categorizing the act of sending an email intended for a customer to an internal colleague, who is also your deputy, as a data breach. It made a lot more mistakes in the blind runs, but that's to be expected of smaller models.

**MaziyarPanahi/Meta-Llama-3-70B-Instruct-GGUF**GGUF IQ1_S, 8K context, Llama 3 Instruct format:- ❌ Gave correct answers to only
**16/18**multiple choice questions! Just the questions, no previous information, gave correct answers:**13/18** - ✅ Consistently acknowledged all data input with "OK".
- ❌ Did NOT follow instructions to answer with just a single letter or more than just a single letter consistently.

- ❌ Gave correct answers to only

IQ1_S, just like IQ1_M, demonstrates a significant decline in quality, both in providing correct answers and in writing coherently, which is especially noticeable in German. Currently, 1-bit quantization doesn't seem to be viable.

**MaziyarPanahi/Meta-Llama-3-70B-Instruct-GGUF**GGUF IQ1_M, 8K context, Llama 3 Instruct format:- ❌ Gave correct answers to only
**15/18**multiple choice questions! Just the questions, no previous information, gave correct answers:**12/18** - ✅ Consistently acknowledged all data input with "OK".
- ❌ Did NOT follow instructions to answer with just a single letter or more than just a single letter consistently.

- ❌ Gave correct answers to only

IQ1_M, just like IQ1_S, exhibits a significant drop in quality, both in delivering correct answers and in coherent writing, particularly noticeable in German. 1-bit quantization seems to not be viable yet.

## Quant Rankings

Today, I'm focusing exclusively on Llama 3 and its quants, so I'll only be ranking and showcasing these models. However, given the excellent performance of Llama 3 Instruct in general (and this EXL2 in particular), it has earned the **top spot in my overall ranking** (sharing first place with the other models already there).

| Rank | Model | Size | Format | Quant | 1st Score | 2nd Score | OK | +/- |
|---|---|---|---|---|---|---|---|---|
| 1 | turboderp/Llama-3-70B-Instruct-exl2 | 70B | EXL2 | 5.0bpw/4.5bpw | 18/18 ✓ | 18/18 ✓ | ✓ | ✓ |
| 2 | casperhansen/llama-3-70b-instruct-awq | 70B | AWQ | 4-bit | 18/18 ✓ | 17/18 | ✓ | ✓ |
| 2 | turboderp/Llama-3-70B-Instruct-exl2 | 70B | EXL2 | 4.0bpw | 18/18 ✓ | 17/18 | ✓ | ✓ |
| 3 | MaziyarPanahi/Meta-Llama-3-70B-Instruct-GGUF | 70B | GGUF | Q8_0/Q6_K/Q5_K_M/Q5_K_S/Q4_K_M/Q4_K_S/IQ4_XS | 18/18 ✓ | 16/18 | ✓ | ✓ |
| 3 | NousResearch/Meta-Llama-3-70B-Instruct-GGUF | 70B | GGUF | Q5_K_M | 18/18 ✓ | 16/18 | ✓ | ✓ |
| 4 | MaziyarPanahi/Meta-Llama-3-70B-Instruct-GGUF | 70B | GGUF | Q3_K_S/IQ3_XS/IQ2_XS | 18/18 ✓ | 15/18 | ✓ | ✓ |
| 5 | MaziyarPanahi/Meta-Llama-3-70B-Instruct-GGUF | 70B | GGUF | Q3_K_M | 18/18 ✓ | 13/18 | ✓ | ✓ |
| 6 | MaziyarPanahi/Meta-Llama-3-70B-Instruct-GGUF | 70B | GGUF | Q3_K_L | 18/18 ✓ | 11/18 | ✓ | ✓ |
| 7 | MaziyarPanahi/Meta-Llama-3-70B-Instruct-GGUF | 70B | GGUF | Q2_K | 17/18 | 14/18 | ✓ | ✓ |
| 8 | meta-llama/Meta-Llama-3-8B-Instruct | 8B | HF | — | 17/18 | 9/18 | ✓ | ✗ |
| 8 | turboderp/Llama-3-8B-Instruct-exl2 | 8B | EXL2 | 6.0bpw | 17/18 | 9/18 | ✓ | ✗ |
| 9 | MaziyarPanahi/Meta-Llama-3-70B-Instruct-GGUF | 70B | GGUF | IQ1_S | 16/18 | 13/18 | ✓ | ✗ |
| 10 | MaziyarPanahi/Meta-Llama-3-70B-Instruct-GGUF | 70B | GGUF | IQ1_M | 15/18 | 12/18 | ✓ | ✗ |

- 1st Score = Correct answers to multiple choice questions (after being given curriculum information)
- 2nd Score = Correct answers to multiple choice questions (without being given curriculum information beforehand)
- OK = Followed instructions to acknowledge all data input with just "OK" consistently
- +/- = Followed instructions to answer with just a single letter or more than just a single letter (not tested anymore)

## TL;DR: Observations & Conclusions

**Llama 3 rocks!**Llama 3 70B Instruct, when run with sufficient quantization (4-bit or higher), is one of the best - if not*the*best - local models currently available. The EXL2 4.5bpw achieved perfect scores in all tests, that's (18+18)*3=108 questions.- The GGUF quantizations, from 8-bit down to 4-bit, also performed exceptionally well, scoring 18/18 on the standard runs. Scores only started to drop slightly at the 3-bit and lower quantizations.
- If you can fit the EXL2 quantizations into VRAM, they provide the best overall performance in terms of both speed and quality. The GGUF quantizations are a close second.
- The unquantized Llama 3 8B model performed well for its size, making it the best choice if constrained to that model size. However, even a small quantization (just not 1-bit) of the 70B is preferable to the unquantized 8B.
- 1-bit quantizations are not yet viable, showing significant drops in quality and coherence.
- Key areas for improvement in the Llama 3 models include expanding the native context size beyond 8K, and enhancing non-English language capabilities. Language-specific fine-tunes or multilingual model releases with expanded context from Meta or the community will surely address these shortcomings.

- Here on Reddit are my previous model tests and comparisons or other related posts.
- Here on HF are my models.
- Here's my Ko-fi if you'd like to tip me. Also consider tipping your favorite model creators, quantizers, or frontend/backend devs if you can afford to do so. They deserve it!
- Here's my Twitter if you'd like to follow me.

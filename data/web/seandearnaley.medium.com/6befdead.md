---
domain: seandearnaley.medium.com
fetch_date: '2026-05-18T12:57:21.778940'
status: ok
url: https://seandearnaley.medium.com/fine-tuning-shootout-may-2024-10ef6a8ee1c9
---

# Fine Tuning Shootout (May 2024)

## Comparing Unsloth Fine Tuned Models for Sentiment Analysis

![](https://miro.medium.com/v2/resize:fit:700/1*3yZgbf06R4SHmn-AVtXl0w.png)

See Part 1 @ Elevating Sentiment Analysis

## Introduction

This article is a fast follow up to our article Elevating Sentiment Analysis, in that article we covered creating datasets (from public data and data synthesis), fine tuning models with the amazing Unsloth library and finally evaluating the results with a comprehensive Python test suite.

In the last article we fine tuned a LLaMA 3 8b model on a custom dataset of 41k records to perform sentiment analysis with predefined JSON outputs. We published our findings with guidance for interpreting the results. This is going to be a shorter article discussing our optimizations on 3 new models.

We will build on what we did before by optimizing our fine tuning to see if we can get better results, this time we will include new fine tuned models based on Microsoft’s Phi-3 tiny 3.5b model as well as the brand new Mistral 7b 0.3 base model.

## Enhanced Training and Model Precision

What are we aiming for in this phase? The last round of fine-tunes hinted at potential improvements, but our performance evaluation revealed some key observations:

- Comparable Performance: The fine-tuned LLaMA 3 8B models performed on par with other models in the same class. While there were slight speed benefits due to no longer needing specialized prompting, the overall results were underwhelming.
- Stable JSON Outputs: Reliable JSON outputs were achievable down to the Q4 quantization levels. However, the base model with specialized prompting also maintained stability.
- Reduced Sentiment Variance: There were indications that sentiment variance was reduced, which is desirable for sentiment analysis models.
- Dropped Confidence Levels: Mysteriously, confidence levels dropped. This could be due to various factors, such as the higher variance and high confidence in the base models indicating overconfidence, or potential nerfing in the fine-tuned models.

Given these observations, we decided to continue pushing performance further. It’s often beneficial to keep tweaking until hitting a performance wall. Our goals remain higher inference rates, lower variance, and increased confidence. In the next steps section of the previous article, we outlined some strategies to improve performance. In this article, we will discuss additional approaches we’ve discovered.

The open-source LLM landscape evolves rapidly. In the week since publishing part one, we’ve seen the release of new promising models: Microsoft introduced the small and medium versions of their Phi-3 model (8B and 14B), and Mistral released version 0.3 of their popular 7B base model.

In this article, we will present three models:

- An updated LLaMA 3 8B model trained for two epochs (twice as long).
- An updated Mistral model fine-tuned on the Mistral 7B v0.3 base (also for two epochs).
- A Phi-3 tiny 4K model with a shorter context length, but trained for two epochs.

These updates aim to explore whether extended training can push the boundaries of performance further, yielding higher inference rates, reduced variance, and greater confidence in the models’ outputs.

### Loading a 4bit model vs FP16/32

In this iteration , we’ve trained our models for twice as long and we’re using the full-fat base models instead of 4-bit models. In previous iterations, we observed clamping and rounding issues, so opting for higher quantized variants proved beneficial for precision. Our JSON outputs include floating point values for sentiment and confidence, making higher precision crucial. However, this approach requires more time and memory for training.

All our fine-tunes utilized the latest Unsloth models with `load_in_4bit`

set to `False`

, yet they still ran efficiently on Google Colab T4 instances with high RAM runtimes, taking approximately 7 hours to train — about twice as long as our previous runs.

We recommend using the supported Unsloth models from their Hugging Face repository. Gated models can encounter issues even with a Hugging Face key (such as loading configuration JSONs). The upside is significant performance gains from the extended 2-epoch training. While this approach is more resource-intensive, it resulted in notable improvements in variance and confidence across the models. The loss numbers significantly decreased in the second epoch. Experimentation is encouraged, but beware of overfitting; the goal is to enhance general model performance. Monitor the loss numbers within the training step of the Jupyter notebook to identify when they begin to level off, as there are diminishing returns beyond a certain point.

The Dolphin-Mistral 7B 2.8 models, along with the LLaMA 3 Instruct 8B models, performed exceptionally well in the last evaluation, even though they required specialized prompting. Fine-tuning’s essence is to bring substantial improvements; without meaningful enhancements, the effort becomes futile.

We have already demonstrated a notable speed improvement. This time, we fine-tuned Mistral 7b 0.3 models as well as a Phi-3 tiny model despite its lower 4K context length. This model, at approximately 2.5GB, performed admirably, making it an excellent choice for resource-limited environments or where super-fast performance is needed.

![](https://miro.medium.com/v2/resize:fit:700/1*myI0N7H7LKoxckF23k83cg.png)

Note for loading models in Ollama they use different templates for their model files, we’ll provide examples for each.

### LLaMA 3 8B (updated with longer training run)

In our last article, we focused on Meta’s LLaMA 3 8B, a state-of-the-art large language model featuring 8 billion parameters. Released on April 18, 2024, this model is part of a family of models that includes both pre-trained and instruction-tuned variants optimized for dialogue and various natural language generation tasks. It employs an autoregressive transformer architecture, benefiting from supervised fine-tuning (SFT) and reinforcement learning with human feedback (RLHF) to enhance alignment with human preferences for helpfulness and safety. With a context length of 8192 tokens, LLaMA 3 8B is designed for both commercial and research use, excelling in tasks that require following instructions and generating coherent, contextually appropriate text.

**LLaMA 3 Ollama Modelfile**: (remember to change to the right file name)

`FROM ./llama3-8b-sentiment-may-22-2024-2epoches-unsloth.Q4_K_M.gguf`

SYSTEM """

You are an advanced AI assistant created to perform sentiment analysis on text. Your task is to carefully read the text and analyze the sentiment it expresses towards the potential future stock value of any company mentioned. Analyze the sentiment of this text and respond with the appropriate JSON:

"""

TEMPLATE """{{ if .System }}<|start_header_id|>system<|end_header_id|>


{{ .System }}<|eot_id|>{{ end }}{{ if .Prompt }}<|start_header_id|>user<|end_header_id|>


{{ .Prompt }}<|eot_id|>{{ end }}<|start_header_id|>assistant<|end_header_id|>


{{ .Response }}<|eot_id|>"""


# A parameter that sets the temperature of the model, controlling how creative or conservative the model's responses will be

PARAMETER temperature 0.2


# Sets how far back for the model to look back to prevent repetition. (Default: 64, 0 = disabled, -1 = num_ctx)

PARAMETER repeat_last_n 256

### Mistral 7B v0.3

The latest iteration of the Mistral 7B series, developed by Mistral AI, is Mistral 7B v0.3. With 7.3 billion parameters, this large language model excels in various natural language processing (NLP) tasks. Released under the Apache 2.0 license, it is available for both commercial and non-commercial use, promoting broad adoption and innovation. Mistral 7B v0.3 stands out due to its extended vocabulary, function-calling capabilities, and improved attention mechanisms, making it a powerful tool for research, development, and real-world applications.

### Key Features and Innovations

**Extended Vocabulary and Tokenizer:**The model supports up to 32,768 tokens, enhancing its ability to handle complex language tasks. The v3 Tokenizer improves performance and compatibility, ensuring efficient text processing and understanding.**Function Calling Capability:**Mistral 7B v0.3 now supports function calling, allowing it to interact with external functions and APIs. This capability enables integration into various applications, such as retrieving weather information or performing specific calculations.**Improved Attention Mechanisms:**Innovative attention mechanisms like Grouped-Query Attention (GQA) and Sliding Window Attention (SWA) enhance the model’s performance. GQA improves inference speed for real-time applications, while SWA optimizes attention processes, allowing efficient handling of longer text sequences.

**Mistral 7b 0.3 Ollama Modelfile Example: **(remember to change to the right file name)

`FROM ./mistral-7b-03-sentiment-may-23-2024-2epoch-unsloth.Q4_K_M.gguf`

SYSTEM """

You are an advanced AI assistant created to perform sentiment analysis on text. Your task is to carefully read the text and analyze the sentiment it expresses towards the potential future stock value of any company mentioned. Analyze the sentiment of this text and respond with the appropriate JSON:

"""

TEMPLATE """{{ if .System }}### Instruction:

{{ .System }}

{{ end }}

### Input:

{{ .Prompt }}

### Response:

"""


PARAMETER num_ctx 8192


# A parameter that sets the temperature of the model, controlling how creative or conservative the model's responses will be

PARAMETER temperature 0.2


# Sets how far back for the model to look back to prevent repetition. (Default: 64, 0 = disabled, -1 = num_ctx)

PARAMETER repeat_last_n 256

### Microsoft’s Phi-3

Microsoft’s Phi-3 family represents a significant leap in small language models (SLMs), offering powerful capabilities at lower costs with reduced computational requirements. These models excel in various applications, from language understanding and reasoning to coding and math tasks. This overview covers the Phi-3-mini, Phi-3-small, and Phi-3-medium models, highlighting their unique features and available context length variants.

## Get Sean Dearnaley’s stories in your inbox

Join Medium for free to get updates from this writer.

On May 21, 2024, Microsoft introduced several new models, including small, medium, and silica variants (for use on AI Copilot+ machines). The small and medium models are available for fine-tuning, providing additional flexibility for various applications.

**Phi-3-Mini:**Released on April 23, 2024, with 3.8 billion parameters, it is the smallest in the Phi-3 family. Despite its size, it outperforms many larger models, making it ideal for efficient and cost-effective AI solutions. Available in 4K and 128K token context lengths, the 4K variant is optimized for shorter contexts, while the 128K variant handles more extensive text inputs. This model is perfect for on-device applications, offering robust performance across various benchmarks.**Phi-3-Small:**With 7 billion parameters, Phi-3-Small balances size and performance, outperforming models of similar and larger sizes, including GPT-3.5T. Available in 8K and 128K context lengths, the 8K variant suits moderate context windows, while the 128K variant is for more demanding tasks requiring extensive context handling. This model is ideal for applications needing strong reasoning capabilities and efficient performance in memory-constrained environments.**Phi-3-Medium:**The largest in the family, Phi-3-Medium has 14 billion parameters and reportedly outperforms larger models like Gemini 1.0 Pro. Available in 4K and 128K context lengths, the 4K variant suits tasks with shorter contexts, while the 128K variant excels in processing large volumes of text. It is particularly effective in applications requiring strong language understanding, coding, and logical reasoning capabilities. Quantized versions of this model are especially useful as they fit on consumer-level 80-series RTX cards and MacBooks with reasonable memory.

**Phi-3 Ollama Modelfile Example: **(remember to change to the right file name)

`FROM ./phi3-4k-sentiment-may-24-2024-2epoches-unsloth.Q4_K_M.gguf`

SYSTEM """

You are an advanced AI assistant created to perform sentiment analysis on text. Your task is to carefully read the text and analyze the sentiment it expresses towards the potential future stock value of any company mentioned. Analyze the sentiment of this text and respond with the appropriate JSON:

"""

TEMPLATE """{{ if .System }}<|system|>

{{ .System }}<|end|>

{{ end }}{{ if .Prompt }}<|user|>

{{ .Prompt }}<|end|>

{{ end }}<|assistant|>

{{ .Response }}<|end|>"""


# A parameter that sets the temperature of the model, controlling how creative or conservative the model's responses will be

PARAMETER temperature 0.2


# Sets how far back for the model to look back to prevent repetition. (Default: 64, 0 = disabled, -1 = num_ctx)

PARAMETER repeat_last_n 256

## Testing

We’re using the same testing suite from the original article (read the original article for more detail). This time we’re doing 14 iterations of the same test for each model, each test evaluates 19 articles using MSFT as the stock ticket (last time we used NVDA but NVDA have such positive sentiment lately, its not a great eval to use). This test can take a very long time, almost a whole day to run.

Important to remember that all non-tuned variants use specialized prompting, see Part 1 @ Elevating Sentiment Analysis for more details. If we don’t use prompting with 5-shot for those models the results are completely unreliable.

The fine tuned variants all use a much shorter instruction prompt so use less tokens by default and achieve consistent outputs regardless of examples.

![](https://miro.medium.com/v2/resize:fit:700/1*IOwI5Rubg7xr8_H1PAOS6A.png)

## Results

Original sentiment analysis results @ Github.

See below for heatmaps, raw CSV and interactive 3D viz:

![](https://miro.medium.com/v2/resize:fit:1000/1*7sY1NlmefweB6GiWS0_WIQ.png)

![](https://miro.medium.com/v2/resize:fit:2000/1*006BQ9v57G8nR2vntRinSQ.png)

![](https://miro.medium.com/v2/resize:fit:2000/1*mjA2C2oELh9rgSAg7hd_kQ.png)

Note: inference of 0 is a fail and that may not be clear on the graph

![](https://miro.medium.com/v2/resize:fit:2000/1*TTu3Hcb3tVnRvwCnjposFQ.png)

![](https://miro.medium.com/v2/resize:fit:2000/1*gRt2l0ZTaQWj8KXGQWwiBw.png)

![](https://miro.medium.com/v2/resize:fit:2000/1*e8s6TDW_MjW3SLkNYIhyvQ.png)

## Evaluating Results

This set of results are better than last time, not using 4bit to train and extending training time to 2 epoch's improves the performance of the LLaMA 3 8b model, and the new Mistral 7b 0.3 based tune has slightly better performance in this round of tests, these models are now better than their base counterparts, run slightly faster and the dip in confidence seems to have been resolved also.

The surprise from this set of results is the performance of the fine tuned Phi-3 models, these perform remarkably well even at Q4, that model is only 2.34gb in size, it can run on very modest hardware and at high speeds. The tradeoff is half the context length of the larger models, but if you use 3k for your input and 1k for the JSON output, that is usually enough for most articles. You could also use preprocess summaries.

Our recommendation is Mistral 7b 0.3 Q8 if you need precision, Q5 if you’re comfortable with slightly less and need 8192 context length. If you’re ok with 4k context and need speed, try the Phi-3, its remarkably good.. If your task is highly specialized and doesn’t need huge context, Phi-3 tiny is a very compelling option, as it will load fast, and run faster than any other model, useful for chaining models (less warmup time) and if you have the resources you can even run multiple at once, for example ~2.4gb goes in 16gb multiple times.

## Next Steps?

We’ve achieved significant performance improvements over the generalized base models… can we go further? Its hard to say when to stop but it there are still intuitive improvements to try:

- Improve the dataset with higher quality data, we’re only using 41k records, there is much more public data available but it will be more expensive to train
- We generated a lot of synthetic data using LLaMA 3 70b hosted on Perplexity API and Groq, we think this was a smart move as it was relatively inexpensive.
- OpenAI’s new GPT-o is 50% cheaper and there are further discounts using their Batch API, we could do a portion of our enhanced synthetic data using that, which in theory should give higher quality outputs.
- We could tweak our output format and prompting to enhance the quality of our inferences, a good rule of thumb with LLMs is to “spread out” your answers so the model gets to think for longer.
- We could enhance our reasoning response, potentially asking it to respond in a chain of thought, which has been shown to improve performance.
- There are issues interpreting articles for financial analysis as they often include mentions of multiple companies, we could consider preprocessing articles before they are evaluated, again more costly but its not uncommon to find yourself making these intuitive tweaks. When we reach the next stage of optimization we will have more ideas percolating from those results.

## Conclusion

Our fine-tuning shootout has demonstrated the substantial impact of extended training and higher precision models on sentiment analysis performance. By training for two epochs and avoiding 4-bit quantization, we’ve achieved notable improvements across several models.

### Key Highlights:

**LLaMA 3 8B and Mistral 7B v0.3:**Both models showed enhanced performance, reduced variance, and improved confidence levels.**Phi-3 Tiny:**Despite its shorter context length, the Phi-3 tiny model excelled in efficiency and speed, making it ideal for resource-constrained environments.

### Recommendations:

**For High Precision:**Use Mistral 7B v0.3 Q8 with an 8192 context length.**For Speed and Efficiency:**Opt for Phi-3 tiny, which offers excellent performance with a 4K context length.

**Future Directions: **While we’ve made significant strides, further optimization is possible by enhancing dataset quality, generating higher quality synthetic data, optimizing output formats, improving reasoning responses, and preprocessing articles for more accurate financial analysis.

In conclusion, our experiments underscore the value of meticulous fine-tuning and optimization in achieving superior performance in sentiment analysis. We look forward to further innovations and refinements that will continue to advance the capabilities of AI-driven sentiment analysis. Good luck with your fine tuning!

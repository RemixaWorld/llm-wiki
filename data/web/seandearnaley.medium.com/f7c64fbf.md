---
domain: seandearnaley.medium.com
fetch_date: '2026-05-18T12:57:21.688360'
status: ok
url: https://seandearnaley.medium.com/elevating-sentiment-analysis-ad02a316df1d
---

# Elevating Sentiment Analysis

## Fine-Tuning LLaMA 3 8B with Unsloth

![](https://miro.medium.com/v2/resize:fit:700/1*7z7NGShoxIiW2MJAhQ_03w.png)

- See the follow up with new fine tunings for LLaMA 3 8b, Mistral 7b 0.3 and Phi-3 Tiny —
**Part 2**@ Fine Tuning Shootout (May 2024)

## Introduction

Open source large language models (LLMs) like Meta’s LLaMA-3 8B, with its 8 billion parameters, are designed to tackle complex language tasks such as sentiment analysis. In this article, we explore how to fine-tune LLaMA-3 8B for financial sentiment analysis using Unsloth, a library that simplifies and accelerates the training process. This guide will help you create custom datasets, fine-tune models, and evaluate their performance.

### Learning Outcomes

**LLaMA-3 8B Overview:**Understand the standout features and benefits of the LLaMA-3 8B model, including the controversies around fine-tune quantization performance.**Custom Datasets:**Learn to build datasets by mixing publicly available data with synthetic outputs. Get hands-on with code for large-scale generation.**Fine-Tuning Workflow:**Master the process of fine-tuning models for sentiment analysis using Unsloth notebooks, from setup to execution.**GGUF Export:**Discover how exporting to the General Graph Universal Format (GGUF) boosts performance and simplifies deployment.**Ollama Deployment:**Deploy custom GGUF models in Ollama for efficient inference. Explore specialized prompting techniques to enhance performance.**Performance Insights:**Compare different fine-tuned models using provided Python scripts. Evaluate performance objectively to find the best configurations.**Evaluation:**Present and measure the differences between quantizations and models like Mistral 7b and Dolphin-Mistral 7b 2.8.**Anomalies Detection:**Learn to spot and address anomalies despite thorough evaluations, ensuring your models’ reliability.

Let’s dive in and enhance your sentiment analysis capabilities with one of the most advanced open-source language models available today.

### Understanding Fine-Tuning

Fine-tuning is a process used to adapt a pre-trained model to a specific task or dataset, enhancing its performance and relevance for particular applications. In the context of large language models (LLMs) like LLaMA-3 8B, fine-tuning involves further training the model on a smaller, task-specific dataset, allowing it to specialize in tasks such as sentiment analysis. This is achieved by adjusting the model’s parameters to better capture the nuances of the new data. Fine-tuning can significantly improve the model’s accuracy and efficiency for the desired task, leveraging the strengths of the pre-trained model while tailoring it to meet specific needs. In this article, we’ll delve into the fine-tuning process of LLaMA-3 8B using Unsloth, demonstrating how it enhances sentiment analysis performance, particularly in the financial sector.

### Applying Sentiment Analysis in Finance

Sentiment analysis in finance involves examining news articles, social media posts, and other texts to gauge market sentiment towards specific stocks or the market overall. By identifying positive, negative, or neutral tones, investors can gain insights into public perception and market trends. For example, consistently positive news about a company’s earnings and innovations might suggest a rise in its stock price, while negative sentiment could indicate declines. This technique uses natural language processing to turn qualitative data into quantitative signals, aiding in informed decision-making and strategic investment planning.

### Meta’s LLaMA-3 8B: An Overview

Meta LLaMA 3 8B developed by Meta AI, is a state-of-the-art language model with 8 billion parameters. Part of the LLaMA 3 family, it includes pre-trained and instruction-tuned versions for various natural language processing tasks. The model features an optimized transformer architecture, Grouped-Query Attention (GQA), and a new tokenizer with a larger vocabulary, enhancing its efficiency and multilingual capabilities. Designed for commercial and research use, LLaMA 3 8B excels in dialogue generation, reasoning, and code generation, and can be deployed on consumer-grade hardware.

![Llama in space suit](https://miro.medium.com/v2/resize:fit:700/1*hxtC5XwXvU9R59a9BT3-ZA.jpeg)

## Overview

This article is divided into three main sections, each representing a critical step in the fine-tuning process:

**Building Your Dataset:**We start by gathering data from public sources and transforming it into a standardized format. This involves cleaning, normalizing, and structuring the data to ensure consistency and reliability. Additionally, we leverage larger language models (LLaMA 3 70b and GPT-4 Turbo) to generate synthetic datasets, enhancing the diversity and volume of our training data.**Fine Tuning:**Using the Unsloth library, we fine-tune our selected base model with the prepared dataset. Unsloth optimizes the training process, significantly reducing memory usage and training time while maintaining high accuracy.**Testing:**Our comprehensive testing phase involves running multiple iterations to measure performance and identify any anomalies. We use statistical analyses to evaluate the results, ensuring the fine-tuned model meets our performance criteria. This step helps us understand the model’s strengths and areas for improvement, providing valuable insights into its behavior and accuracy.

## Building Your Dataset

In this section, we’ll walk you through the process of building a comprehensive sentiment analysis dataset using various scripts. Each step involves processing different types of data, combining them, and preparing them for use in machine learning models. We’ll provide an overview of each script, highlighting important features and functionality.

We have a code repo with various tools broken up by step to prepare a dataset. You can find the code @ GitHub

The finished dataset contains 41.4k records and you can download it @ HuggingFace.

We source data from three different public datasets. Step 1 processes tweets from the Airline Sentiment dataset, Step 2 handles sentiment analysis from the Financial Phrase bank, and Step 3 processes articles from newsdata.io. Each step requires a unique strategy to transform the data into the desired format. For instance, we make assumptions about confidence levels and synthesize sentiment records for news articles using larger language models. This approach enables us to gather more data, leveraging the generalization capabilities of larger models to perform sentiment analysis effectively.

### Step 1: Processing Tweets

File: `step-01-process_tweets.py`


This script processes a dataset of tweets related to airline sentiment and saves the output to a new CSV file.

**Sentiment Mapping:**Maps sentiment labels (positive, neutral, negative) to numeric values (1.0, 0.0, -1.0).**Data Processing:**Reads the input CSV, processes each tweet to extract the sentiment, and constructs a JSON object with sentiment, confidence, and reasoning.**Output:**Saves the processed data to a new CSV file with columns for the sentence and the JSON object.**Dataset Source**

### Step 2: Processing Financial PhraseBank

File: `step-02-process_financial_phrase_bank.py`


This script processes the Financial PhraseBank dataset, which contains financial news phrases, and saves the output to a CSV file.

**Confidence Scores:**Assigns different confidence scores based on the agreement level of the sentiment annotations.**Sentiment Mapping:**Similar to the tweets script, it maps sentiment labels to numeric values.**Data Processing:**Reads the dataset, processes each phrase, and constructs a JSON object.**Output:**Combines processed data from different agreement levels into a single CSV file.**Dataset Source**

### Step 3: Processing Articles

File: `step-03-process_articles.py`


This script processes a dataset of news articles, generates synthetic outputs using various language models, and saves the output to a CSV file.

**API Integration:**Uses multiple AI models (e.g., LLaMA 3 70b, OpenAI GPT-3.5, GPT-4, etc.) to generate sentiment analysis. Note Perplexity.ai and Groq offer great value fast inference for LLaMA 3 70b, although not the most powerful. We spent under $20 all in, after numerous experiments, the whole run can probably done for under $10. If you want really high accuracy you should pay for the best model you can get.**Specialized Prompting:**We use a system message and 5-shot examples to get stable results and we run the output through a pydantic validator. This is important and we’ll use the same specialized prompting for our inference tests later. This can take some tweaking to get reliable results.**Retry Mechanism:**Implements a retry mechanism to handle API call failures. It keeps track of processed records as this process can take all night, if it fails for whatever reason you can run it again.**Data Validation:**Ensures that the generated JSON responses are valid using Pydantic models.**Output:**Saves the processed articles with their sentiment analysis to a CSV file.**Dataset Source**

### Step 4: Joining Outputs

File: `step-04-join_outputs.py`


This script combines the outputs from the tweets, financial phrases, and articles datasets into a single CSV file.

**Data Sanitization:**Ensures that all data is in a consistent format and free from encoding issues.**JSON Validation:**Validates the JSON strings to ensure they meet the expected format.**Output:**Combines valid records from all processed datasets into one CSV file.

### Step 5: Building HuggingFace Dataset

File: `step-05-build_hf_dataset_sharegpt.py`


This script converts the combined dataset into a format suitable for uploading to HuggingFace for sharing and training models.

**Data Transformation:**Reads the combined CSV file, sanitizes the data, and transforms it into a JSON format.**Dataset Structure:**Organizes the data into a conversation format suitable for training models on HuggingFace.**Output:**Saves the transformed data to a JSON file ready for upload.- You can create a dataset in HuggingFace and upload the JSON to that repo.

### Utility Scripts

Files: `utils/sentiment_response.py`

, `utils/utils.py`


These utility scripts provide helper functions and classes used across the main scripts, such as:

**SentimentResponse:**A Pydantic model for validating the JSON responses.**File Utilities:**Functions for reading messages, generating record IDs, loading and saving processed records.

By following this guide, you can adapt these scripts to process and analyze your own datasets, enabling you to build comprehensive sentiment analysis datasets for various applications.

![](https://miro.medium.com/v2/resize:fit:700/1*2D9U6Q7Kqq4V9_AV3WBjTg.jpeg)

## Fine Tuning Workflow

### Introduction

We used Unsloth’s Google Colab notebooks to perform our fine tune. Unsloth is efficient, uses very low resources, notably lower memory, its possible to run it locally on consumer hardware, its also cheap to run on the Colab services. The T4 tier works fine, but is slower, we trained on 41.4k records (1 epoch) and that took around 9 hrs on a T4. Expect to some experimentation, so definitely use a lower number of steps rather than full epoches to test. There are always changes happening, so occasionally a dependency gets updated that breaks something. Unsloth has a very helpful Discord where users discuss and ask questions.

Here is a copy of the Notebook we used. There are some changes from the official notebook, it uses the ShareGPT style for formatting and templating.

https://colab.research.google.com/drive/1H40hAFkh8FnOivEEyEsMn6REN8HfKPwB?usp=drive_link

We recommend you use the official notebooks on the Unsloth Github, these will be more up to date and more supported.

### Unsloth

Unsloth is a powerful library designed to accelerate the fine-tuning of large language models (LLMs) while reducing memory usage. Created by Daniel and Michael Han, it achieves up to 30x faster training speeds and 60–80% lower memory consumption by optimizing back propagation and rewriting PyTorch modules into Triton kernels. Supporting a wide range of NVIDIA GPUs, Unsloth integrates seamlessly with the Hugging Face ecosystem, making it compatible with various LLM architectures like LLaMA and Mistral. Remarkably, it maintains 0% accuracy degradation compared to traditional methods, providing an efficient solution for fine-tuning LLMs. Learn more at HuggingFace.

### Fine-Tuning Workflow with Unsloth

The Unsloth script simplifies and accelerates the fine-tuning process of large language models (LLMs) like LLaMA-3 8B. Here’s a breakdown of what this notebook/script does:

**Installation and Setup:**The script begins by installing the necessary libraries, including Unsloth, which optimizes the training process. It supports various models like LLaMA, Mistral, and others, and uses 4-bit quantization to reduce memory usage and speed up training.**Model Preparation:**It loads a pre-trained model using Unsloth’s`FastLanguageModel`

class, specifying parameters like`max_seq_length`

and`dtype`

to optimize performance based on the hardware (e.g., Tesla T4 GPU). The script supports LoRA (Low-Rank Adaptation) adapters, which allow fine-tuning by updating only a small percentage of the model’s parameters, further reducing memory usage.**Data Preparation:**The official script uses the Alpaca dataset as an example, we use our dataset in the sentiment analysis version, both format the data into a standardized prompt structure. It ensures that each prompt includes an end-of-sequence (EOS) token to prevent infinite text generation.**Training the Model:**Using Hugging Face’s`SFTTrainer`

, the script fine-tunes the model on the prepared dataset. Key training parameters like batch size, learning rate, and number of steps are set to optimize the training process. The script monitors GPU memory usage to ensure efficient resource management.**Inference:**After training, the script demonstrates how to run the model for inference. It sets up inputs, generates outputs, and decodes them to text. The script also includes an option for continuous inference, allowing users to see generated text token by token.**Saving the Model:**The script provides methods for saving the fine-tuned model, either locally or by pushing it to Hugging Face’s hub. It supports saving the model in different formats, including 16-bit, 4-bit, and GGUF (General Graph Universal Format), making it flexible for various deployment scenarios.

We are especially interested in the GGUF outputs because they can be used easily on most deployments including local machines.

### GGUF

GGUF, or General Graph Universal Format, is a file format designed to enhance the efficiency and flexibility of deploying LLMs like LLaMA-3 8B. Introduced by the llama.cpp team, GGUF offers improvements over its predecessor, GGML, single-file deployment, extensibility, and memory mapping for faster model loading. This format is particularly good for quantized models, allowing for reduced computational resource demands without compromising performance. GGUF’s is an ideal choice for developers looking to streamline the deployment and inference of LLMs across various platforms, including CPUs and Apple devices. Learn more at HuggingFace.

![](https://miro.medium.com/v2/resize:fit:700/1*jVgv2Vb5jEnU6T0NvKLVdg.png)

## Testing and Inference

This repository, co-authored by Andreas Traczyk, is designed specifically for testing and inference against various models. You can access the code on GitHub. Use this repository to effectively compare different models and analyze their performance.

**https://github.com/seandearnaley/llama_3_8b_sentiment_analysis_tests**

This repository contains a Python project for testing and comparing the performance of various models on sentiment analysis tasks. The project utilizes the `Ollama`

library for local model inference and includes scripts for running sentiment tests, generating comparison reports, and visualizing the results.

Follow the **README.md** for install instructions.

### Specialized Prompting

This is an important step, the dataset was partially built using these prompting techniques (synthetic data), and often you can use this instead of fine tuning, we really want to evaluate whether we’re actually getting better performance in our fine tunes and whether its even worth doing. The goal is to get reliable JSON results back that pass the pydantic validation, we want JSON because it’s easy to pass into python functions (eg function calling).

Here is a special system prompt:

`You are an advanced AI assistant created to perform sentiment analysis on financial news articles. I need you to classify each article you receive and provide your analysis using the following JSON schema:`

{

"reasoning": {

"type": "string",

"description": "A brief description explaining the logic used to determine the numeric sentiment value.",

"required": true

},

"sentiment": {

"type": "number",

"description": "A floating-point representation of the sentiment of the news article, rounded to two decimal places. Scale ranges from -1.0 (negative) to 1.0 (positive), where 0.0 represents neutral sentiment.",

"required": true

},

"confidence": {

"type": "number",

"description": "A floating-point representation of how confident the analysis is, rounded to two decimal places. Scale ranges from 0.0 (not confident) to 1.0 (very confident).",

"required": true

}

}


Always respond with a valid JSON object adhering to this schema. Do not include any other text or messages in your response. Exclude markdown.

and we initialize the thread with 5 examples (known as 5-shot prompting, the fine tunes give us 0-shot, but specialized to this one specific task):

`You will be provided with a financial news article enclosed within the following XML tags:`


<article>{$ARTICLE}</article>


Your task is to carefully read the article and analyze the sentiment it expresses towards the potential future stock value of the company mentioned.


First, write out your reasoning and analysis of the article's sentiment inside the "reasoning" property. Explain the key points in the article that influence your assessment of the sentiment and how they would likely impact the stock price.


Then, output a numeric score between -1.0 and 1.0 representing the sentiment, where -1.0 is the most negative, 0 is neutral, and 1.0 is the most positive. Put this score inside the "sentiment" property.


Provide a sentiment value as a function of how positive or negative the sentiment is. If no conclusion can be drawn, provide a sentiment value of 0.0.


Provide a confidence value as a function of how confident you are in the sentiment value. If you are very confident, provide a confidence value of 1.0. If you are unsure, provide a confidence value of 0.0.


Make no alterations to the schema. This is important for our company.


Examples:


1. <article>NVDA shares rise 5% on earnings beat.</article>

Output:

{

"reasoning": "The news article reports a positive earnings beat, which is likely to increase investor confidence and, consequently, the stock value of NVDA.",

"sentiment": 0.75,

"confidence": 0.9

}



2. <article>NVDA shares may be affected by a drop in oil prices. Analysts predict a 5% drop in stock value due to NVDA's exposure to the energy sector.</article>

Output:

{

"reasoning": "The article suggests a potential negative impact on NVDA stock due to falling oil prices, which could lead to decreased investor confidence.",

"sentiment": -0.25,

"confidence": 0.8

}


3. <article>Apple's recent launch of its innovative AR glasses has not met expected sales targets.</article>

Output:

{

"reasoning": "Despite the innovative product launch, the failure to meet sales targets could lead to negative market reactions and a potential drop in Apple's stock value.",

"sentiment": -0.5,

"confidence": 0.6

}


4. <article>Boeing secures a $5 billion contract for new aircrafts from Emirates, signaling strong future revenues.</article>

Output:

{

"reasoning": "Securing a large contract suggests positive future revenue prospects for Boeing, likely boosting investor sentiment and stock value.",

"sentiment": 0.85,

"confidence": 0.9

}


5. Determine the sentiment towards the stock value of Tesla from the following article:

<article>Tesla recalls 100,000 vehicles due to safety concerns.</article>

Output:

{

"reasoning": "A significant recall due to safety issues could harm Tesla's brand reputation and negatively impact investor confidence, likely decreasing its stock value.",

"sentiment": -0.65,

"confidence": 0.7

}

### Code Overview


This script runs sentiment analysis tests on a specified company using the models defined in the **generate_model_sentiments.py:**`config.yaml`

file. It retrieves news articles related to the company, extracts relevant content, and analyzes the sentiment of each article using the specified models. The results are saved as JSON files in the `sentiments`

folder. The script performs a configurable number of iterations, ensuring that each iteration evaluates the same pre-cached articles.

## Get Sean Dearnaley’s stories in your inbox

Join Medium for free to get updates from this writer.


This script generates a comparison report based on the sentiment analysis results generated by **generate_model_comparison_report.py:**`generate_model_sentiments.py`

. It calculates various metrics for each model, including inference rate, sentiment variance, mean sentiment, and mean confidence. It also performs statistical comparisons between models using ANOVA and t-tests. The report is saved as an Excel spreadsheet and CSV files in the `reports`

folder.


This script computes various metrics for the sentiment analysis models based on their performance and stores the results in Excel and CSV formats. It processes the sentiment analysis results to generate comprehensive performance reports.**generate_model_metrics.py:**


This script generates heatmaps for different performance metrics of the sentiment analysis models and saves them as PNG images in the **generate_heatmaps.py:**`heatmaps`

folder. It visualizes metrics such as inference rate, valid JSON rate, sentiment variance, mean sentiment, and mean confidence.

### Utils

This folder contains utility modules used by the main scripts.


Provides functions for cleaning company names, filtering news articles, testing models, and analyzing content.**analysis_utils.py:**

**context.py:**** **Defines the `AnalysisContext`

dataclass, which encapsulates the context for sentiment analysis.


Provides a decorator for handling errors gracefully.**error_decorator.py:**


Provides functions for reading and writing files, including JSON and YAML files.**file_utils.py:**


Provides functions for validating JSON data and parsing numeric values.**validation_utils.py:**


Provides functions for scraping content from websites.**web_scraper.py:**

### Example Sentiment JSON

Each iteration in `generate_model_sentiments.py`

produces a JSON file for each model. These JSON files contain hashed sentiments derived from the articles, ensuring that each iteration evaluates the same pre-cached articles. The structure of the JSON files is as follows:

`{`

"average_sentiment": 0.57,

"time_taken": 53.91,

"sentiments": {

...

"91ba90ac": {

"reasoning": "The article reports that the market is holding near record highs, with several companies such as BYD, Nvidia, and Walmart flashing buy signals, indicating a positive sentiment towards these stocks.",

"sentiment": 0.6,

"confidence": 0.8,

"valid": true,

"url": "https://finance.yahoo.com/m/ae28caa6-3ead-3745-aece-9ddb64e2ea1d/dow-jones-futures%3A-walmart%2C.html?.tsrc=rss",

"published": "Thu, 16 May 2024 23:52:02 +0000",

"time_taken": 3.17

},

"bf372e87": {

"reasoning": "The article reports that Nvidia's stock finished lower on Thursday, despite being on track to set a record high due to optimism around the chip maker ahead of its earnings report next week. The marketwide rally sparked by April's inflation data and upbeat analyst estimates lifted Nvidia shares, but ultimately led to a 0.3% decline.",

"sentiment": -0.15,

"confidence": 0.8,

"valid": true,

"url": "https://finance.yahoo.com/m/6ab7d488-38e1-3ef1-beef-bf75a726d6c2/nvidia-stock-couldn%E2%80%99t-close.html?.tsrc=rss",

"published": "Thu, 16 May 2024 20:30:00 +0000",

"time_taken": 5.12

},

"d4c4ccc1": {

"reasoning": "The article discusses Wolfe Research's positive outlook on Nvidia (NVDA) and Advanced Micro Devices (AMD), with a price target increase for Nvidia to $1,200. The addition of AMD to the Wolfe Alpha List highlights its robust AI product lineup, indicating potential growth opportunities. The analyst's tactical shift in priority towards AMD suggests a more balanced approach considering both stocks' performance.",

"sentiment": 0.75,

"confidence": 0.85,

"valid": true,

"url": "https://finance.yahoo.com/video/chip-stocks-wolfe-research-bullish-201319388.html?.tsrc=rss",

"published": "Thu, 16 May 2024 20:13:19 +0000",

"time_taken": 6.24

},

...

}

}

### Methodology

We are using a Mac Pro M2 with 32gb. Ollama 0.1.38. We do 15 iterations on the same set of news articles from Yahoo Finance.

`default_temperature: 0.2`

context_window_size: 8192

num_tokens_to_predict: 1024

### Ollama

Ollama is an tool that enables users to run open LLMs locally on their machines, eliminating the need for cloud services. Its a front end for llama.cpp and can load GGUF models. Designed for ease of use, it offers a simple API, OpenAI endpoint compatibility (eg can work with anything that supports OpenAI) and a library of pre-built models. Ollama runs on macOS, Linux, and Windows, can use CPU and GPU, it integrates seamlessly with popular frameworks like LangChain, LiteLLM and more. By providing local execution, , it ensures data privacy and reduces latency, making it an ideal choice for developers and researchers looking to leverage advanced NLP capabilities efficiently.

You can download our GGUF fine tuned models @ HuggingFace

Loading GGUFs into Ollama needs a custom `Modelfile`

with the system message and template, remember to substitute the GGUF file for the quantization level you are using here we’re using `llama3-8b-sentiment-may-3-2024-unsloth.Q4_K_M.gguf`

, you can name it whatever you want when importing into Ollama:

`ollama create llama3:8b-instruct-sentiment_analysis-q4_K_M -f Modelfile`

## Results and Evaluation

In this section, we present the results of our evaluation of various sentiment analysis models, focusing on key performance metrics and statistical comparisons. We compared fine-tuned sentiment models against their base counterparts to determine their efficiency and accuracy in processing financial sentiment data. These metrics provide a comprehensive view of each model’s performance and highlight the advantages of using specialized, fine-tuned models for sentiment analysis tasks.

![](https://miro.medium.com/v2/resize:fit:1000/1*b0X-cWVScetnotysccculw.png)

![](https://miro.medium.com/v2/resize:fit:1000/1*spCkD21f4ZcdLyWR7i4hjw.png)

![](https://miro.medium.com/v2/resize:fit:1000/1*1LUnMMmm5UJj3Ja4UniC6A.png)

![](https://miro.medium.com/v2/resize:fit:1000/1*5FWFssGUdEP8kG952s6GLQ.png)

![](https://miro.medium.com/v2/resize:fit:1000/1*Z_SXx4q8bAyptpK_pkrm-g.png)

![](https://miro.medium.com/v2/resize:fit:1000/1*TRrlLUQCpsImtVSwQOzC3g.png)

## Interpreting Sentiment Analysis Model Comparison Results

When working with sentiment analysis models, understanding their performance and comparing different models is crucial. Here’s a simple guide to help you interpret the results from our analysis, which includes model details, performance metrics, and statistical comparisons.

### Model Details

**Model Name:**This indicates the specific model used (e.g.,`llama3_8b-instruct-fp16`

).**Quantization Level:**This tells you the precision level used in the model (e.g.,`q4`

,`q5`

,`fp16`

). Lower levels like`q4`

and`q5`

use less memory and can be faster but might be less accurate.

### Performance Metrics

**Rate (sec/sample):**This measures how fast the model processes each sample. Lower numbers mean faster performance.**Valid JSON Response Rate:**This is the percentage of times the model successfully returned valid results. Higher percentages indicate better reliability.**Variance:**This shows how much the sentiment scores vary. High variance means the scores are spread out widely, while low variance means they are more consistent.**Mean Sentiment Score:**This is the average sentiment score across all samples, indicating the general sentiment detected (positive, negative, or neutral).**Mean Confidence:**This is the average confidence level of the sentiment predictions. Higher values indicate the model is more certain about its predictions.**Reasoning:**This provides sample explanations from the model, showing why it predicted a certain sentiment. It helps understand the model’s decision-making process.

### How to Interpret the Results

**Inference Speed:**Faster models (lower Rate) are generally preferable, especially for real-time applications.**Reliability:**Models with higher Valid JSON Response Rates are more dependable.**Consistency:**Low Variance is often better, indicating the model’s predictions are stable.**Sentiment and Confidence:**Higher Mean Sentiment Scores and Mean Confidence Scores are desirable, showing the model detects clear sentiment and is confident about its predictions.

### Example

Imagine comparing `llama3_8b-instruct-fp16`

with `llama3_8b-instruct-sentiment_analysis-fp16`

:

**Rate:**If the sentiment analysis model is faster, it’s better for real-time needs.**Valid JSON Response Rate:**If higher, it means fewer errors.**Variance:**If lower, the model’s predictions are more consistent.**Mean Sentiment Score:**Higher score indicates a stronger overall sentiment detection.**Mean Confidence:**Higher value means the model is more certain about its predictions.

By understanding these metrics and comparisons, even beginners can make informed decisions about which sentiment analysis models to use based on their specific needs and contexts.

![Llama inspecting results with a clipboard](https://miro.medium.com/v2/resize:fit:700/1*n5rOmeMpkri-pXcX_XoMUg.png)

## Financial Sentiment Analysis Model Comparison

### Introduction

The goal of this analysis is to compare different sentiment analysis models, specifically fine-tuned models for sentiment analysis against their base models, to identify the best model for financial sentiment analysis. We have examined metrics such as inference speed, valid JSON response rate, variance in sentiment scores, mean sentiment score andmean confidence score.

### Key Metrics and Comparisons

**Inference Speed (Rate):**Fine-tuned models generally show similar or slightly improved processing times compared to their base models. For instance,`llama3_8b-instruct-sentiment_analysis-q5_K_M`

has a rate of 4.42 seconds/sample, while`llama3_8b-instruct-q5_K_M`

processes at 5.08 seconds/sample.**Valid JSON Response Rate:**Both fine-tuned and base models consistently deliver a valid JSON response rate of 100% in most cases. This indicates high reliability across models. Mistral 7b has errors for all quantization levels, it is the most unreliable.**Variance in Sentiment Scores:**Fine-tuned models exhibit comparable variance in sentiment scores in these tests. Sometimes higher, this is a disappointing result, indicates tweaks are needed to the dataset and training mechanism. Lower variance suggests more consistent predictions.**Mean Sentiment Score:**Fine-tuned models tend to have comparable mean sentiment scores. Higher mean sentiment scores indicate a stronger overall sentiment detection.**Mean Confidence Score:**Fine-tuned models generally show slightly lower mean confidence scores compared to base models, which may be due to their specialized training focusing more on accuracy of sentiment detection than on confidence.

### Explanation for Variance in Confidence Scores

The slight decrease in mean confidence scores for fine-tuned models can be attributed to their specialized training. Fine-tuned models are optimized for specific tasks, which might involve making more nuanced distinctions in sentiment that base models are not trained to handle. This increased nuance can lead to a more cautious (lower confidence) prediction approach, as the model is designed to capture subtle variations in sentiment.

### Controversy around LLaMA 3 8B quantization

Recent discussions in the AI community have highlighted significant issues with quantizing the `LLaMA 3 8B`

model, particularly to lower bit-widths like Q4. Reports suggest substantial degradation in output quality, including issues such as random insertion of dates, repeated words, and reduced coherence. These performance drops are more pronounced compared to other models like Mistral or older LLaMA versions. The extensive pre-training and high token count of LLaMA 3 models may make them more sensitive to precision loss inherent in quantization, necessitating further research to optimize quantization techniques for these advanced models.

### Implications for Sentiment Analysis Models

**Lower Precision Issues:** When the LLaMA 3 8B models are quantized to Q4, the reduction in precision might cause inaccuracies in sentiment detection. This could lead to less reliable sentiment scores and confidence levels.

### Clamping and Rounding Effects:

**Clamping:**This occurs when values are restricted within a certain range. In the context of sentiment analysis, it might mean extreme sentiment values (very positive or very negative) are less accurately represented, leading to more neutral outputs.**Rounding:**This refers to approximating numbers to the nearest representable value in the lower precision format. Rounding errors can accumulate, causing a degradation in the quality of sentiment analysis outputs.**Variance Observations:**Interestingly, some users have observed lower variance in sentiment scores at Q4 compared to higher precision levels like Q5, Q8, and FP16. This contradicts typical expectations where higher precision usually yields more stable results. This anomaly suggests that the extensive pre-training of LLaMA 3 models might make them more sensitive to precision loss, affecting the stability of sentiment scores.

### Practical Consequences

For your sentiment analysis models:

**Reduced Output Quality**: The overall quality and coherence of the sentiment analysis might decline when using quantized LLaMA 3 8B models at Q4.**Inconsistent Performance**: You might notice more inconsistencies, such as unexpected neutral sentiment scores or unusual patterns in the sentiment analysis results.**Recommendation**: Based on these observations, it might be better to use higher precision levels (e.g., Q8 or FP16) for LLaMA 3 8B models or consider other models like Mistral or Dolphin-Mistral, which handle quantization better. The steps outlined in this article show you how to fine tune but you may yet get better performance from more generalized models.

## Conclusion

- For financial sentiment analysis, using fine-tuned models such as
`llama3_8b-instruct-sentiment_analysis-q5_K_M`

could be a good choice in producing consistent and strong sentiment detections if you want it slightly faster and skip special prompting. But the dolphin-mistral models perform very well (with prompting) and there is a very low margin of improvement, more work is needed to improve the performance of the fine tuned models for practical use. The mistral sentiment fine tune performs better than the base model, but not better than the dolphin general fine tunes. - Fine tuned models can offer meaningful improvements over their base counterparts, potentially ensuring more reliable and accurate sentiment analysis. However, the controversy surrounding LLaMA 3 8B quantization, particularly at Q4, suggests caution and a need for further research and optimization in quantization techniques.
- Fine tuning using Unsloth notebooks offer a relatively cheap path to fine tuning your own data on open language models like LLaMA 3 8b and Mistral 7b.
- It is possible to get reliable JSON results that can be used in function calling, non-tuned requires special prompting but can be done.
- Fine tuned LLaMA 3 8B for sentiment analysis offers some advantages, it doesn’t require specialized prompting tricks, all of the quantities have relatively low variance and appropriate confidence as well as slight improvements in speed (less tokens required to prompt).
- There is room for improvement in the dataset and training time. Tweaking the synthetic data prompts could be help, running the set for longer than 1 epoch appears to lower loss.
- Web scraping can be complex, scraping from Yahoo Finance sometimes encounters multiple companies mentioned in the same article as well as articles that are paywalled.
- Using a specialized system prompt and 5-shot examples, the Llama 3 8B model achieves a 100% success rate in generating valid JSON with all four quantization levels when executed correctly. However, it exhibits a higher variance in sentiment scores despite maintaining high confidence, indicating potential overconfidence.
- Mistral 7b Instruct with the same system prompt and 5-shot frequently fails to output correct JSON, all the way up to the FP16 quantization level.
- Dolphin-Mistral 7b-v2.8 performs much better than the base Mistral 7b at sentiment analysis, with specialized prompting it achieves 100% success. This suggests Mistral 7b base can be fine tuned effectively.
- If you’re doing commercial work, make sure to understand the model’s license, take note for example that many models disallow training other models with their outputs/ though it seems many don’t follow this rule/ very hard to litigate but you should follow the terms of the respective license.

### Next Steps

- Fine tuning requires extensive investment in time to experiment further.
- Try fine tuning on other models, LLaMA 3 may not be the best, especially at lower quants. Try Mistral-7b or even Phi-3 and compare the results using the test repo.
- Enhance the dataset, this was largely a proof of concept, there is much more data available.
- Tweak the dataset instructions along with the special prompting to see if you can change the numbers.
- Spend more for more powerful models on the synthetic training. GPT-o was released after this set was built, its 50% cheaper and you can get even bigger discounts if you use the Batch API and can complete the job in under 24 hours.
- The fine tune we did only covered 1 epoch (a full pass through the dataset), the loss could down even further if trained for longer.

### Final Words

With the techniques covered in this article, you can confidently create fine-tuned models using custom data. Our findings show that fine-tuned variants can deliver minor performance improvements without the need for special prompts, leading to faster and more efficient outputs.

Evaluating fine-tuned models at lower quantization levels can be challenging due to high variance and overconfidence, requiring careful analysis. Future articles will explore fine-tuning other base models for further insights.

For assistance or questions, feel free to reach out, I’m also available for contracts. Best of luck with your projects and happy fine-tuning!

NOTE: we did a follow to this article **Part 2** @ Fine Tuning Shootout (May 2024)

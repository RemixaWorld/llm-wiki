---
domain: blog.gopenai.com
fetch_date: '2026-05-18T12:46:34.804956'
status: ok
url: https://blog.gopenai.com/lab-4-chat-with-10m-data-records-b2da20c4d9da
---

# Lab #4: Chat with 10M data records (ChatGPT, PandasAI and Streamlit)

[ ![Elinson](https://miro.medium.com/v2/resize:fill:64:64/1*T2LVlt9AqxAXRBZKKE1kFw@2x.jpeg) ](<https://medium.com/@elinson?source=post_page---byline--b2da20c4d9da--------------------------------------->)

[Elinson](<https://medium.com/@elinson?source=post_page---byline--b2da20c4d9da--------------------------------------->)

7 min read

·

Jul 16, 2024

\--

Listen

Share

More

Ask question about your data in natural language

> **“Chat with Data”** is an article in the[**“Chat with Everything”**](<https://github.com/S0NM/chat-with-everything>) series. This part will focus on how to ask questions about your data in natural language.
>
> For those of you who don’t know, the **“Chat with Everything”** series is a series that focuses on providing you with the tech knowledge and techniques in building LLM applications. All applications I’ve created using popular frameworks: Streamlit, Langchain & OpenAI (LLM model).
>
> You can find “Chat with Everything” series here: [My github](<https://github.com/S0NM/chat-with-everything>)

### Difficulty Level: Intermediate 🎖️

### What I’m going to cover in this article:

1. Using natural language to “talk” with your data?
2. How “Chat with Data” actually works
3. Preparing Tech stack & data for our Demo
4. Implementing the “Chat-with-Data” app
5. Show Case (For those of you who want to see the results first to be motivated.)

## 1\. Using Natural language to “talk” with your data

We are all very familiar with natural language, the language we use every day for social communication. But when it comes to interacting with computers and data, the process becomes much more complex.

**In the past,** to work with data, I had to learn SQL . This process could take several days, or even weeks, if I wanted to grasp it thoroughly. For someone with a tech background like me, it was still manageable, but for those without technical expertise, it could take months.

**Nowadays** , with the support of large language models (LLMs), this process has become significantly easier and faster. Imagine LLMs as a talented translator. Instead of learning a new programming language or query language, you can simply use your natural language. LLMs automatically translate your requests into programming language, execute complex tasks, and return the results to you. This entire process happens within minutes, providing you with the necessary information quickly and accurately.

Press enter or click to view image in full size

“Past & Present,” created by DALL-E

Using LLMs (like ChatGPT, Gemini, etc.) not only saves time but also opens up opportunities for everyone, regardless of technical proficiency, to access and leverage the power of data.

### There are two possible ways to use LLMs to work with our data:

The first solution is to use _the capabilities of ChatGPT for data analysis directly_. It is possible to access the OpenAI website and upload a data file from your computer for processing and analysis. However, this kind of approach has three significant drawbacks:

* **Your data could be leaked** to third parties (OpenAI)
* The processing of big data is**so “expensive** ,” How to calculate the token cost will be explained below
* Excessive data processing can cause your account to be**blocked for 1-2** hours because OpenAI limits computing capabilities to a user’s account

> In order to overcome these limitations, let’s come to the second solution that I’ll implement in the next section. To be more convincing, I’d use a dataset with 10 million records. With this dataset, it’s impossible to use the first solution.

## 2\. How “Chat with Data” actually works

Press enter or click to view image in full size

How “Chat with Data” works

The high-level design concept of the “Chat with Data” application is described as shown below:

* **Step 1:** Receive **Question** from users
* **Step 2:** Connect to the database (CSV, XLSX, PostgreSQL, MySQL, BigQuery, Databrick, Snowflake, etc.) to retrieve **Metadata** (information about the data tables with description of the respective data fields)
* **Step 3:** Instead of sending the entire data to the LLM, this step only sends **Metadata + Question**
* **Step 4:** Based on the metadata, the LLM will create **executable code**. Explain it in a simple way: LLM translates from natural language to query language (SQL) or programming language (Python) to work with data
* **Step 5+6:** The executable code in step 4 will be run on the database to get the final result
* **Step 7:** Form the final **Answer** and return it to you.

## 3\. Preparing Tech stack & data for our Demo

### PandasAI: A**sk questions about your data in natural language.**

To implement the above concept, I’m going to introduce you to a very interesting Python library for data analysis: **PandasAI.**

**PandasAI** uses a generative AI model to understand and interpret natural language queries and translate them into Python code and SQL queries. It then uses the code to interact with the data and return the results to the user. If you want to find out more information about PandasAI, check it out: : [https://pandas-ai.com](<https://pandas-ai.com/>). Here is a demo video:

Features of PandasAI

* Natural language querying: Ask questions to your data in natural language.
* Data visualization: Generate graphs and charts to visualize your data.
* Data cleansing: Cleanse datasets by addressing missing values.
* Feature generation: Enhance data quality through feature generation.
* Data connectors: Connect to various data sources like CSV, XLSX, PostgreSQL, MySQL, BigQuery, Databrick, Snowflake, etc.

### IDBD Datasets:

I’m going to use the data set from IMDB. For those of you who love movies, IMDB is a well-known website that provides detailed information about movies, TV shows, actors, directors, producers, and other professionals in the film and television industry. I chose the “title.basics.tsv.gz” dataset. You can download it [here](<https://developer.imdb.com/non-commercial-datasets/>). Some information about this dataset:

* Contain more than **10 million records**
* The information on each record includes: the title of the programmes (film, TV, etc.) in English and native languages. Besides, there’s a year of release, a duration...

If you process this dataset directly on ChatGPT, the cost of the input tokens is:

``` Total tokens: 322.644.846Cost: 161.322423$ ```

Can you imagine?**$161** was just for putting this information on the ChatGPT and not processing anything.

The code to calculate the number of tokens and estimate the cost is:

```python import tiktokenimport pandas as pddef calculate_cost(): encoding = tiktoken.encoding_for_model("gpt-3.5-turbo") cost_per_1M_tokens = 0.5 # 0.5$ / 1M Tokens # Load data in df dataset_file = "./dataset/title.basics.tsv" df = pd.read_csv(dataset_file, sep="\t", low_memory=False) # For each row, combine all fields into a tring data_as_strings = df.apply(lambda row: ' '.join(row.values.astype(str)), axis=1).tolist() # Count the number of tokens for each row token_counts = [len(encoding.encode(text)) for text in data_as_strings] # Print the results total_tokens = sum(token_counts) print('Total tokens:', total_tokens) print('Cost:', total_tokens * cost_per_1M_tokens / 1000000) ```

The preparation steps are complete; let’s start building the application[​](<https://docs.pandas-ai.com/intro#how-does-pandasai-work>)

## 4\. Implementing the “Chat-with-Data” app

**Step 1:** Install & import all library

```python pip install pandasaipip install tiktokenpip install streamlit ``` ```python from pandasai.helpers.openai_info import get_openai_callbackimport matplotlibfrom pandasai.responses.response_parser import ResponseParserfrom pandasai.connectors import PandasConnectorimport streamlit as stimport pandas as pdfrom pandasai import SmartDataframefrom pandasai.llm import OpenAI ```

**Step 2:** Load data into Dataframe

```python # Load into Dataframe, the size of the dataset is around 960 MB and it took 30s of loading on my laptop@st.cache_datadef load_data(): dataset_file = "./dataset/title.basics.tsv" df = pd.read_csv(dataset_file, sep="\t", low_memory=False) return df ```

**Step 3:** To help LLM understand our data easier, you can create and attach the Metadata to request. This is an example of Metadata for our data. Firstly, I’ve got the Metadata directly on IMDB site:

Press enter or click to view image in full size

Then, our main processing code is:

```python # Init llmllm = OpenAI()# Handle response messages according to type: dataframe, plot or textclass MyStResponseParser(ResponseParser): def __init__(self, context) -> None: super().__init__(context) def parse(self, result): if result['type'] == "dataframe": st.dataframe(result['value']) elif result['type'] == 'plot': st.image(result["value"]) else: st.write(result['value']) return# Tip: Adding Description for data fields to make GPT understand more easily, using in case you don't want to use GPT's automatic understanding mechanismfield_descriptions = { "tconst": "An alphanumeric unique identifier of the title", "titleType": " the type/format of the title (e.g. movie, short, tvseries, tvepisode, video, etc)", "primaryTitle": "the more popular title / the title used by the filmmakers on promotional materials at the point of release", "originalTitle": "original title, in the original language", "isAdult":"0: non-adult title; 1: adult title", "startYear": "represents the release year of a title. In the case of TV Series, it is the series start year. YYYY format", "endYear" : "TV Series end year. \\\N means null value", "runtimeMinutes": "primary runtime of the title, in minutes. \\\N means null value", "genres":"includes up to three genres associated with the title"}# Create PandasConnector to pass Metadata to ChatGPTconnector = PandasConnector( {'original_df': df}, field_descriptions=field_descriptions)agent = SmartDataframe(connector, config={ "llm": llm, "conversational": False, "response_parser": MyStResponseParser, })chat_reponse = agent.chat(prompt) ```

**Step 4:** To call ChatGPT and get the response

``` # Get the responsechat_reponse = agent.chat(prompt) ```

## 5\. Show case

**Question 1:** Plot the number of programs releases from 2010 to 2020

**Answer 1:**

Press enter or click to view image in full size

What happened behind the scenes? And now, total cost is only around $0.002 (very cheap, right) and you can easily control the generated code, save it for future use.

Press enter or click to view image in full size

**Question 2:** Count the number of programs between title types, display in table format

**Answer 2:**

Press enter or click to view image in full size

Press enter or click to view image in full size

**Question 3:** List the 5 programs with the longest runtime minutes. Show only id, original title, runtime minutes and genres fields

**Answer 3:**

Press enter or click to view image in full size

Press enter or click to view image in full size

## Before you go! 🤟

If you found value in this article and wish to show your support, **clap my article 10 times.** 👏, that will really motivate me and boost this article to others.

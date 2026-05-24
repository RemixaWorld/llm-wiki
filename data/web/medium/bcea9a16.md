---
domain: pub.towardsai.net
fetch_date: '2026-05-18T12:51:56.045696'
status: ok
url: https://pub.towardsai.net/build-your-llm-engineer-portfolio-a-3-month-roadmap-19826e39c185
---

# Build Your LLM Engineer Portfolio (Part 1): A 3-Month Roadmap

# **Build Your LLM Engineer Portfolio (Part 1): A 3-Month Roadmap**

## A step-by-step guide to designing, refining, and showcasing a portfolio that kickstarts your career.

[ ![Maxime Jabarian](https://miro.medium.com/v2/resize:fill:64:64/1*CWn_uZAK7SNa3dBJD5YrhA.jpeg) ](<https://medium.com/@maximejabarian?source=post_page---byline--19826e39c185--------------------------------------->)

[Maxime Jabarian](<https://medium.com/@maximejabarian?source=post_page---byline--19826e39c185--------------------------------------->)

14 min read

·

Dec 15, 2024

\--

Listen

Share

More

Press enter or click to view image in full size

[Source](<https://unsplash.com/fr/photos/vaisseau-spatial-gris-decollant-pendant-la-journee-OHOU-5UVIYQ>)

If you’ve just finished your degree or are looking for your first job, this article is for you. As you know, the AI job market is more competitive than ever. Simply having a degree or academic projects in AI isn’t enough to differentiate yourself from the crowd, specifically for an LLM engineer position. You need practical, hands-on projects that show your skills.

If you’re not a member, you can read it [here](</build-your-llm-engineer-portfolio-a-3-month-roadmap-19826e39c185?sk=b224a9bc030bcb5ffc1a61e718606bd3>).

For those who don’t know me, my journey started as an LLM Engineer 2 years ago with a degree in Astrophysics and Data Science. Before that, I was a data scientist doing research and development for some enterprises. Since then, I’ve crafted sophisticated GenAI applications for several clients, leveraging multimodal models for thousands of users, and have designed comprehensive architectures for end-to-end product solutions.

### **Why Your Portfolio Matters** ?

When I started as an LLM engineer, I quickly realized that having a portfolio of practical work was essential for building trust and confidence with your audience. For example, in my free time, I built a custom HR chatbot for my previous employer, designed to answer internal queries and automate repetitive tasks like onboarding FAQs for all collaborators (few hundred). Using closed and open-source LLM, I fine-tuned the LLMs on company data and integrated it into their existing systems. This project not only improved efficiency but also demonstrated my ability to combine technical skills with real-world problem-solving. Then, during interviews with my stakeholders and clients, at the beginning it became my standout example, showcasing my initiative and ability to deliver solutions using the latest tools and techniques on the market.

It also showed that I keep up with the fast-paced changes in the AI world, where new models and new methods can become outdated in less than 6 months. For example, [here is a list of all existing RAG methods](</build-your-llm-engineer-portfolio-part-2-a-3-month-roadmap-92e333c27335>), and it’s crucial to identify the one best suited for the use case. That’s why doing some benchmark before choosing a tool for any use case can be incredibly valuable. By staying current and using the latest advancements, I was able to adapt quickly and provide high-tech solutions.

### **Here’s What’s Ahead** 📋

* 📅 A comprehensive plan to guide your 3-month journey toward building an impressive LLM portfolio.
* 🛠️ Key preparation steps to establish a solid foundation for your projects.
* ✨ Seven (+1 bonus) impactful projects designed to sharpen your expertise and stand out.
* 🎨 Strategies to effectively deploy and present your portfolio for maximum visibility.

### Time to plan it out 📅✨

Press enter or click to view image in full size

Made by Author

This roadmap covers **seven (+1 bonus)** useful projects designed to equip you with the tools and experience needed to stand out in the competitive GenAI job market. From interactive LLM systems to cutting-edge fine-tuning, this guide walks you through every step. The last project it’s a bonus and not necessary because in 90% of the use cases in the real world, you don’t need to fine-tune the LLM to answer into a specific format (except if you build an assistant coder). If you’re considering training a model on your personal or enterprise database, think twice. You can’t predict all the questions users might ask, so only a small subset of queries will be handled well. Plus, depending on the model you’re using, the costs can skyrocket. That said, it might make sense if your goal is to enhance a RAG (Retrieval-Augmented Generation) application — this can sometimes improve the accuracy of the answers. So, you should consider the pros and cons if it is worth it.

* Assuming you’re in the process of exploring this domain, I’ve designed this timeline with the idea that you’ll dedicate around 8 hours per week to developing your portfolio. Of course, if you have more time or need to accommodate a busier schedule, feel free to adapt this plan to match your pace and commitments.
* The time allocated for each project assumes you have some experience in python and a basic understanding of essential LLM concepts. You should already be familiar with: Prompt Engineering, Tokenization, Transformer, and [GPU memory](<https://medium.com/p/b4a015a0174f>). Additionally, having a grasp of Retrieval-Augmented Generation (RAG) and agent-based workflows is a plus, but not necessary as you will learn about it across these projects.

## Skills Developed During the Projects

* Write effective prompts for AI models, including advanced techniques like step-by-step reasoning to solve tricky problems.
* Work with both paid AI tools (like OpenAI) and free, open-source ones (like Hugging Face) to get the best of both worlds — flexibility and cost savings.
* Got hands-on with Python, building apps, connecting to APIs, cleaning data, and automating tasks using libraries like LangChain, Selenium, and Beautiful Soup.
* Built smart systems that can look up documents and give accurate answers using RAG and tools like Chroma for fast data searches.
* Design workflows where multiple AI “agents” collaborate to automate things like debugging, testing, and coding, using tools like LangGraph.
* Make and share apps using frameworks like Streamlit or Flask and deployed them on platforms like Hugging Face Spaces.
* Gain experience in fine-tuning AI models to make them better and more efficient using methods like QLoRA.

## **Getting Started: Set Up Your Workspace 💻**

1\. **Set Up VS Code**

* Start by installing Visual Studio Code, my favourite code editor that works seamlessly with Python and Jupyter Notebooks. You can download it [here](<https://code.visualstudio.com/>).
* Once installed, add the Jupyter plugin so you can easily work with Notebooks. Open any Notebook to ensure you’re comfortable switching between environments: simply open the Command Palette (Cmd/Ctrl + Shift + P), select **Python: Select Interpreter** , and verify that all your environments appear on the list.

2\. **Set Up GitHub**

* If you don’t already have a GitHub account, now’s the time to create one. Once you’re set, create a new repository for each project (there are 8 portfolio projects — check the list below).
* In your terminal (inside VS Code or any terminal you like), navigate to a main directory where you’ll store all your projects — something like “Portfolio” works great. Clone each repository into this directory one by one.

And that’s it! Your workspace is ready, and you’re all set to embark on this 3-month journey to build your portfolio. 🚀

## Project 1: **Local LLM Chat App with Streamlit**

Press enter or click to view image in full size

[Made by Author](<https://github.com/MaximeJabarian/OpenSource_LLM_APP_Ollama/blob/main/chat-interface-app.png>)

### **🎯 Objective**

Create a real-time, user-friendly chat application using Streamlit and Ollama’s local LLMs.

**👉 Tech Stack:** Streamlit, Ollama (e.g., Llama3, Phi3…), Python, Hugging Face, FastAPI.

👉 **Tools Used:**

* [Streamlit](<https://streamlit.io/>): For building an intuitive chat interface.
* [Ollama](<https://ollama.com/>): For integrating local LLMs for query processing.
* Python: For backend development and managing dependencies.
* [FastAPI](<https://fastapi.tiangolo.com/>): For building APIs with Python
* [Hugging Face](<https://huggingface.co/>): For deploying the application.

👉 **Sources** :

* [Building Local LLMs App with Streamlit and Ollama (Llama3, Phi3…)](<https://medium.com/@maximejabarian/building-a-local-llms-app-with-streamlit-and-ollama-llama3-phi3-511d519c95fe>)
* [Deploying Your FastAPI Applications on Huggingface Via Docker](<https://huggingface.co/blog/HemanthSai7/deploy-applications-on-huggingface-spaces>)
* [Creating a Local Interactive Chat Application with Mistral’s LLM](<https://medium.com/@maximejabarian/creating-a-local-interactive-chat-application-with-mistrals-llm-daebc7597ec4>)

**👉 Steps:**

1\. **Set Up Environment:** Create a Python virtual environment to manage dependencies.

2\. **Install Dependencies:** Install required libraries, including streamlit and llama-index.

3\. **Develop User Interface:** Build a Streamlit UI for selecting models, entering queries, and displaying responses.

4\. **Integrate Local LLM:** Connect the application to Ollama for local LLM query processing.

5\. **Deployment:** Host the application on Hugging Face Spaces for easy sharing and access.

6\. **Compare Different Models** : Compare model performance (speed, accuracy) directly in the app.

> It’s crucial to work with open-source models, not just closed APIs like OpenAI or Anthropic, to stay adaptable. Open-source models let you experiment, learn deeply, and avoid being locked into one platform, ensuring the flexibility to switch as your needs evolve.

## Project 2: Document Summarization

Press enter or click to view image in full size

[Source](<https://unsplash.com/fr/photos/page-de-livre-blanche-et-noire-9Y6eZOaF4U4>)

### **🎯 Objective**

Develop a tool that allows users to upload a PDF document and generates a concise summary of its content.

**👉 Key Techniques:** Text extraction, abstractive summarization, and an interactive user interface for file upload and result display.

**👉 Tools Used:**

* **PyPDF2 or pdfplumber:** For reading and extracting text from PDF files.
* **Transformers Library:** For summarization using pre-trained models like BERT or [DistilBertModel](<https://huggingface.co/docs/transformers/model_doc/distilbert>).
* **Streamlit:** To create a user-friendly interface for uploading files and displaying summaries.

👉 **Source** : [Summarize text document using transformers and BERT](<https://theaidigest.in/summarize-text-document-using-transformers-and-bert/>)

**👉 Steps** :

1\. **PDF Reading and Text Extraction:** Ensure preprocessing steps, such as removing headers, footers, or unnecessary whitespace, to clean the extracted content.

2\. **Summarization Model Initialization:** Load a pre-trained summarization model from the Hugging Face Transformers library.

3\. **Interactive UI:** Build a Streamlit-based interface where users can upload a PDF, then view the resume in a pop-up message box.

> Picking the right model can make or break your app. Choose poorly, and you might end up with something slow, expensive, or overkill for the task. Sometimes, a smaller model with good accuracy is all you need — saving costs and keeping things efficient.

> It’s not always about using the biggest or newest model but finding the one that fits your needs best.

## **Project 3: Global News Topic Tracker**

Press enter or click to view image in full size

[Source](<https://unsplash.com/fr/photos/black-android-smartphone-on-white-table-YDDnFThf48g>)

### **🎯 Objective**

Develop a tool that scrapes the Google News page to extract and list the latest trending topics discussed around the world.

**👉 Key Techniques:** Web scraping, keyword extraction, topic clustering, and summarization using LLMs.

**👉 Tools Used:**

* **Beautiful Soup/Selenium:** For scraping headlines and article snippets from Google News.
* **Transformers Library (e.g., OpenAI or Hugging Face):** For summarizing trends and clustering similar topics.
* **Pandas:** For organizing extracted data into categories.
* **Streamlit or Flask:** For building a user-friendly interface to display global news trends.

👉 **Source** :

* [Scraping Google News Using Python](<https://www.scrapingdog.com/blog/scrape-google-news/>)
* <https://huggingface.co/meta-llama/Llama-3.1-8B>

**👉 Steps:**

1\. **Scraping Google News Content:** Use Beautiful Soup or Selenium to extract headlines, snippets, and URLs from the Google News homepage.

2\. **Keyword Extraction and Clustering:** Apply LLM with a well defined prompt system to extract key topics from headlines and group similar articles together.

3\. **Topic Summarization:** Use an LLM to generate concise summaries for each cluster of news articles.

4\. **Organizing Data:** Categorize articles by topics and structure them into an easily accessible format using Pandas or a similar library.

5\. **Interactive UI:** Create a Streamlit or Flask-based interface to display trending topics, summaries, and links to the full articles.

> With a well-crafted prompt, you can often skip the hassle of fine-tuning LLMs for specific tasks.

## **Project 4: Multi-Modal Assistant**

Press enter or click to view image in full size

[Source](<https://unsplash.com/fr/photos/ecran-de-surveillance-active-qwtCeJ5cLYs>)

### 🎯 Objective

Build a multi-modal AI assistant capable of addressing customer queries through text and images.

**👉 Key Techniques:** Function calling, multimodal interactions, and interface design.

👉 **Tools Used:**

* Python: For implementing the backend logic and function calls.
* Streamlit: For creating an interactive and user-friendly interface.
* OpenAI [GPT-4o mini](<https://platform.openai.com/docs/models#gpt-4o-mini>) Model: For handling text and image-based customer queries with precision.

👉 **Source** : [Multi-Modal LLM using OpenAI GPT-4V model for image reasoning](<https://docs.llamaindex.ai/en/stable/examples/multi_modal/openai_multi_modal/>)

**👉 Steps:**

1\. Create function calls for the LLM to address text/image-based queries.

2\. Design an interactive Streamlit UI for seamless user experience.

## **Project 5: Meeting Notes and Action Item Extractor**

Press enter or click to view image in full size

[Source](<https://unsplash.com/fr/photos/macbook-pro-displaying-group-of-people-smgTvepind4>)

### 🎯 Objective

Develop a tool to process audio recordings into comprehensive meeting summaries and task lists.

**👉 Key Techniques:** Speech-to-text conversion, summarization, and LLM-based text refinement.

👉 **Tools Used:**

* [Whisper](<https://platform.openai.com/docs/guides/speech-to-text>): For converting speech to text from audio recordings.
* [OpenAI API](<https://platform.openai.com/docs/guides/realtime>): For summarizing discussions and extracting actionable insights.
* [Streamlit](<https://streamlit.io/>)/[Flask](<https://flask.palletsprojects.com/en/stable/>): For building an intuitive user interface to manage and view meeting summaries.

👉 **Source** : [st.audio](<https://docs.streamlit.io/develop/api-reference/media/st.audio>)

**👉 Steps:**

1\. **Upload or Record Audio:** Allow users to upload pre-recorded meeting audio files or record live discussions directly within the application.

2\. **Audio-to-Text Conversion:** Use a speech-to-text model like Whisper to transcribe audio recordings into text.

3\. **Text Preprocessing:** Clean and structure the transcribed text, removing filler words and formatting it into paragraphs.

4\. **Key Point Extraction:** Use an LLM to identify and summarize key discussion points from the transcript.

**5\. Interactive UI:** Build a user interface with Streamlit or Flask where users can upload audio files or access recorded meeting summaries.

## **Project 6: Custom Chatbot Q &A (RAG)**

Press enter or click to view image in full size

[Source](<https://unsplash.com/fr/photos/macbook-pro-near-white-open-book-FHnnjk1Yj7Y>)

### 🎯 Objective

Build an AI-powered system that enables users to upload and query documents, providing accurate, context-aware answers by leveraging embeddings and RAG pipelines. This tool is ideal for corporate environments, helping teams quickly retrieve insights from large volumes of company data.

👉 **Key Techniques:** Document ingestion and preprocessing, embedding generation for semantic understanding, and Retrieval-Augmented Generation (RAG) pipelines for contextual and accurate responses.

👉 **Tools Used:**

* [LangChain](<https://python.langchain.com/v0.1/docs/get_started/introduction>): For document processing and pipeline orchestration.
* OpenAI Embeddings: For generating high-quality semantic representations.
* Ollama: For integrating open-source LLMs for query processing
* [Chroma](<https://www.trychroma.com/>): For storing and retrieving embeddings efficiently.

👉 **Source** :

* [Build a Retrieval Augmented Generation (RAG) App: Part 1](<https://python.langchain.com/docs/tutorials/rag/>)
* [rag-chroma](<https://python.langchain.com/v0.1/docs/templates/rag-chroma/>)
* [How to Find Ideal Open Source LLM for RAG-Based Chatbots?](<https://medium.com/generative-ai/how-to-find-ideal-open-source-llm-for-rag-based-chatbots-2806ebe8618e>)
* [Which RAG Method to use ?](</build-your-llm-engineer-portfolio-part-2-a-3-month-roadmap-92e333c27335>)
* [Streamline Your LLM Evaluation: A Step-by-Step Guide to RAG Metrics with Streamlit](<https://medium.com/towards-artificial-intelligence/streamline-your-llm-evaluation-a-step-by-step-guide-to-rag-metrics-with-streamlit-38ed9efbdc9a>)

**👉 Steps:**

1\. **Document Upload:** Allow users to upload various document types (PDF, Word, or text).

2\. **Document Preprocessing:** Process and clean uploaded documents, removing unnecessary formatting and segmenting them into manageable chunks using LangChain.

3\. **Embedding Generation:** Generate semantic embeddings for each document chunk using OpenAI Embeddings or similar models.

4\. **Vector Storage:** Store embeddings in a vector database like Chroma for efficient similarity-based retrieval.

5\. **Query Interface Setup:** Build a user-friendly interface where users can input natural language queries.

6\. **Retrieval Pipeline:** Implement a RAG pipeline that retrieves the most relevant document chunks from the database based on the query and passes them to an LLM for final contextual generation.

7\. **Answer Refinement:** Use the LLM to refine retrieved content and generate a concise, user-friendly response.

8\. **Performance Evaluation** : Evaluate the RAG system and the generated answer based on retrieved information (Groundness, Correctness…).

## Project 7: Multi-Agent System

Press enter or click to view image in full size

[Source](<https://unsplash.com/fr/photos/robot-blanc-pres-dun-mur-brun-2EJCSULRwC8>)

### 🎯 Objective

Build a multi-agent system using LangGraph to automate the process of software development, including coding, testing, debugging, and execution. The agents collaborate to streamline the workflow, reduce human intervention, and ensure optimized, error-free code.

👉 **Key Techniques:** Multi-agent architecture for task automation, LangGraph for orchestrating agent interactions, and Chain-of-Thought (CoT) prompting for logical execution.

**👉 Tools Used:**

* [**LangGraph**](<https://www.langchain.com/langgraph>)**:** For managing and orchestrating agents.
* **OpenAI GPT Models:** For generating and refining Python code.
* **Python:** For building and integrating agent workflows.

👉 **Source** :

* [LangGraph CoT](<https://smith.langchain.com/public/51d543f7-bdf6-4d93-9ecd-2fc09bf6d666/r>)
* [LangGraph: Multi-Agent Workflows](<https://blog.langchain.dev/langgraph-multi-agent-workflows/>)
* [Multi-agent Systems](<https://langchain-ai.github.io/langgraphjs/concepts/multi_agent/>)

**👉 Steps:**

1\. **Set Up LangGraph Workflow:**

* Define a state graph and establish nodes for agents like Programmer, Tester, Executor, and Debugger. Create edges to control the flow of information and decisions among agents.

2\. **Define Programmer Agent:**

* Task: Generate Python code based on requirements using CoT prompting. Include steps for understanding requirements, pseudocode creation, and efficient coding.

3\. **Develop Tester Agent:**

* Task: Generate test cases to validate the code. Include both basic and edge test cases for robustness and reliability.

4\. **Implement Executor Agent:**

* Task: Execute the generated code against test cases to validate functionality.

5\. **Build Debugger Agent:**

* Task: Analyze errors identified during execution and refine the code to resolve them. Leverage LLM capabilities for debugging and generating improved code.

6\. **Integrate Workflow with Example:**

* Provide an example requirement (e.g., solving a LeetCode problem).
* Pass the requirement through the entire workflow: Programmer → Tester → Executor → Debugger → Decision Edge.

7\. **Test and Optimize Agents:**

* Run multiple scenarios to validate each agent’s functionality and interaction.

## **Project 8: Fine-Tuning Open-Source Models for Price Prediction**

Press enter or click to view image in full size

[Source](<https://unsplash.com/fr/photos/gros-plan-dun-ventilateur-dordinateur-sur-un-mur-D5hXm7eIhi8>)

### 🎯 Objective

Fine-tune open-source LLMs to predict product prices based on descriptions, achieving competitive performance while optimizing costs through parameter-efficient techniques. This project is designed to demonstrate mastery of fine-tuning and evaluation methodologies.

👉 **Key Techniques:** Domain-specific dataset preparation, parameter-efficient fine-tuning with QLoRA, and comprehensive evaluation against state-of-the-art models.

**👉 Tools Used:**

* **Hugging Face:** For accessing and fine-tuning open-source LLMs.
* **QLoRA:** For efficient fine-tuning with reduced computational costs.
* **Weights & Biases (W&B):** For tracking experiments, metrics, and performance.

👉 **Source** :

* [Fine-Tuning Open-Source LLM using QLoRA with MLflow and PEFT](<https://mlflow.org/docs/latest/llms/transformers/tutorials/fine-tuning/transformers-peft.html>)
* [HuggingFace LLM Finetuning](<https://huggingface.co/docs/autotrain/llm_finetuning>)
* [Fine Tune Large Language Model (LLM) on a Custom Dataset with QLoRA](<https://dassum.medium.com/fine-tune-large-language-model-llm-on-a-custom-dataset-with-qlora-fb60abdeba07>)

**👉 Steps:**

1\. **Dataset Collection and Preparation:**

* Collect a dataset containing product descriptions and corresponding prices from public sources or synthetic generation.
* Preprocess the data to ensure clean, high-quality input, including tokenization and normalization of price values.

2\. **Model Initialization:**

* Load an open-source base model from Hugging Face, such as Llama3.1 for fine-tuning.

3\. **Fine-Tuning with QLoRA:**

* Apply QLoRA to fine-tune the base model on the prepared dataset, optimizing for cost and performance.
* Monitor training progress and loss metrics using Weights & Biases.

4\. **Hyperparameter Optimization:**

* Experiment with different learning rates, batch sizes, and prompt strategies to achieve the best results.

5\. **Model Evaluation:**

* Compare the tuned model’s performance against baseline metrics such as RMSE, MAE, and R².
* Benchmark results against frontier models like OpenAI GPT or other fine-tuned LLMs for the same task.

6\. **Model Deployment:**

* Package the fine-tuned model and deploy it via [FastAPI](<https://fastapi.tiangolo.com/>) for real-world use cases.

> Ready to take the next step in building your RAG portfolio? “[Build Your LLM Engineer Portfolio (Part 2): A 3-Month Roadmap](</build-your-llm-engineer-portfolio-part-2-a-3-month-roadmap-92e333c27335>)”, continues our roadmap covering all the RAG techniques shaping the market today.”

## **✨ Final Tips ✨**

As you wrap up your 3-month journey to build your LLM portfolio, take some time to finish strong. Make sure your tools are set up, your GitHub is organized, and your virtual environments are ready. Aim to spend about 8 hours a week, breaking projects into small, manageable steps, and plan out your tasks before tackling in. Get feedback on your code to improve and regularly update your GitHub to keep everything safe and up-to-date.

After each project, jot down what you learned, what could be better, and anything you want to revisit later — it’ll be super helpful for interviews. Stay flexible if life gets busy, and use tools like Google Drive to keep track of your progress. With steady effort and good planning, your portfolio will showcase your skills and prove you’re ready to excel in the fast-changing world of GenAI.

## Loved the Article? Here’s How to Show Some Love:

* **Clap** many times — each one truly helps! 👏
* **Follow** me here on Medium and subscribe for free to catch my latest posts. 🗞️
* Let’s connect on [**LinkedIn**](<https://www.linkedin.com/in/maxime-jabarian/>), check out my projects on [**GitHub**](<https://github.com/MaximeJabarian>), and stay in touch on [**Twitter**](<https://x.com/Max_JB_AI>)

---
domain: levelup.gitconnected.com
fetch_date: '2026-05-18T12:48:29.511660'
status: ok
url: https://levelup.gitconnected.com/transforming-voice-assistants-with-llamaindex-livekit-and-ai-agents-the-future-of-intelligent-5706bcb558a1
---

# Transforming Voice Assistants with LlamaIndex, LiveKit, and AI Agents: The Future of Intelligent Voice Interaction

# Transforming Voice Assistants with LlamaIndex, LiveKit, and AI Agents: **The Future of Intelligent Voice Interaction**

[ ![Chew Loong Nian - AI ENGINEER](https://miro.medium.com/v2/da:true/resize:fill:64:64/0*Ar6uzSBz8K2Kdbhd) ](<https://medium.com/@chewloongnian?source=post_page---byline--5706bcb558a1--------------------------------------->)

[Chew Loong Nian - AI ENGINEER](<https://medium.com/@chewloongnian?source=post_page---byline--5706bcb558a1--------------------------------------->)

9 min read

·

Sep 17, 2024

\--

Listen

Share

More

Press enter or click to view image in full size

In an increasingly connected world, voice assistants are becoming an integral part of daily life. From answering questions to controlling smart devices, they offer convenience and efficiency. But what if voice assistants could become even smarter — offering more dynamic conversations, handling complex queries, and providing contextually aware responses? This is where the power of **LiveKit** , combined with **Large Language Models (LLMs)** , comes into play.

## What is LiveKit?

LiveKit is an open-source platform designed for building scalable real-time audio and video communication applications. It allows developers to create applications that facilitate high-quality, low-latency interactions — whether through live audio, video conferencing, or real-time messaging

LiveKit provides a powerful platform for building voice assistants that deliver high-quality, real-time communication experiences. Here’s how LiveKit’s integration with LLMs brings a revolution in conversational AI:

1. **Real-Time Multimodal Experiences** : LiveKit enables sub-100ms latency for voice and video, ensuring seamless interactions between users and AI. With plugins from OpenAI, Google, and ElevenLabs, developers can quickly create advanced multimodal applications.
2. **Human-Like Conversations** : Integrated plugins for interruption handling and turn-taking cue detection make conversations feel natural, as if speaking with a person.
3. **Telephony Network Integration** : LiveKit supports connecting voice assistants to telephony networks, enabling users to dial into sessions or make outbound calls.
4. LiveKit, integrated with **AI agents** and **LLMs** , enables businesses to build advanced voice assistants tailored for real-world business contexts. These AI-driven assistants can automate complex tasks, retrieve accurate information, and offer real-time assistance, making them ideal for industries like customer support, sales, and service management.

## Business Task Automation

**LiveKit** has AI agent capabilities meaning that it can intelligently identify user intent and call **pre-built functions** to execute tasks in real-time, such as processing orders, managing appointments, or providing account support. This automation enables businesses to streamline operations, improve efficiency, and enhance customer satisfaction without human intervention.

## LlamaIndex for Accurate Business Information

With **LlamaIndex’s retrieval-augmented generation (RAG)** capabilities, AI agents can access **vector databases** to pull precise, up-to-date business information. Whether it’s retrieving customer records, product details, or business-specific documentation, the voice assistant can provide accurate, context-aware answers to even the most complex inquiries.

## Benefits for Businesses

* **Efficient Operations** : Automate routine business functions and tasks via AI agents.
* **Accurate Information** : Ensure customers and employees receive correct answers by pulling from reliable business databases.
* **Real-Time Service** : Deliver fast, context-aware responses, improving user experiences across various business interactions.

With LiveKit, businesses can build voice assistants that automate critical tasks and retrieve valuable business data, driving efficiency, accuracy, and customer satisfaction.

## Code Demonstration: Building a business-context AI Agent with LiveKit and LLamaindex

The **first step** is to create the necessary files to demonstrate how to start building a project. In this case, you will need to create the following Python files:

1. `**.env**` – This file will store environment variables, such as Openai and LiveKit API keys
2. `**api.py**` – This file will handle all API and AI agent calls
3. `**build_knowledge.py**` – This script will build the knowledge base, potentially for storing or indexing data (for instance, setting up a vector database for retrieval-augmented generation).
4. `**main.py**` – The core entry point of your application.

Press enter or click to view image in full size

### Step 2: Install Required Libraries

After creating the necessary files, the next step is to install the required libraries for the project. Open your terminal and run the following commands to install all the necessary packages:

```python pip install livekit-agents livekit-plugins-openai livekit-plugins-silero python-dotenvpip install llama_index llama-index-vector-stores-chroma chromadb ```

### Step 3: Set up the environment

To get started with LiveKit, follow these steps to retrieve your **API Key** :

1. **Sign into LiveKit** : Go to the [LiveKit website](<https://livekit.io>) and log in to your account.
2. **Navigate to Settings** :

* Click on the **Try Out LiveKit** button to access the platform features.
* Head over to the **Settings** section of your dashboard to create key

Press enter or click to view image in full size

3\. Now head to `.env` file to replace `your_livekit_api_key` and `your_livekit_api_secret` with the actual values from LiveKit. Similarly, replace `your-livekit-server-url` with the appropriate server URL provided by LiveKit.

``` LIVEKIT_URL="wss:xxxxxx"LIVEKIT_API_KEY="APIxxxxxx"LIVEKIT_API_SECRET="uEzxxxxx"OPENAI_API_KEY="sk-xxxxx" ```

### Step 5: Paste and Configure the Main Code

Once you’ve set up your environment variables, it’s time to move on to the main integration. Below is the code to build and launch your voice assistant using LiveKit and OpenAI.

**1\. Main Code Explanation**

Here’s the code you’ll need to paste into your main.py Python file:

```python import asynciofrom dotenv import load_dotenvfrom livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llmfrom livekit.agents.voice_assistant import VoiceAssistantfrom livekit.plugins import openai, silero# from api import AssistantFnc # Uncomment if you have additional assistant functionsload_dotenv() # Load environment variables from .env fileasync def entrypoint(ctx: JobContext): # Set up the initial context for the assistant initial_ctx = llm.ChatContext().append( role="system", text=( "You are a voice assistant created by LiveKit. Your interface with users will be voice. " "You should use short and concise responses, and avoid usage of unpronounceable punctuation." ), ) # Connect the assistant to the room (audio only) await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY) # Initialize the voice assistant with various modules assistant = VoiceAssistant( vad=silero.VAD.load(), # Voice activity detection using Silero stt=openai.STT(), # Speech-to-text with OpenAI llm=openai.LLM(), # Language model with OpenAI tts=openai.TTS(), # Text-to-speech with OpenAI chat_ctx=initial_ctx, # Set the initial chat context # fnc_ctx=fnc_ctx, # Uncomment if you have defined AssistantFnc ) # Start the assistant in the connected room assistant.start(ctx.room) # Voice prompt to greet the user await asyncio.sleep(1) await assistant.say("Hey, how can I help you today!", allow_interruptions=True)# Entry point for running the applicationif __name__ == "__main__": cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint)) ```

**2\. What This Code Does:**

* **Environment Loading (**`**load_dotenv**`**)** : The API keys and environment variables are loaded from your `.env` file.

**Voice Assistant Setup** :

* **Voice Activity Detection (VAD)** : The assistant uses the Silero model for detecting when a user is speaking.
* **Speech-to-Text (STT)** : The OpenAI model converts the user’s speech into text.
* **Language Model (LLM)** : The core of your assistant is the OpenAI language model, which processes user input and generates responses.
* **Text-to-Speech (TTS)** : Responses are converted back into speech using OpenAI’s TTS model.
* **Chat Context (**`**ChatContext**`**)** : The assistant is initialized with a predefined personality and behavior via the `ChatContext`. Here, it’s instructed to provide concise responses and avoid complex punctuation.
* **Interaction Flow** : The assistant is connected to a room, starts listening for user input, and responds with a greeting after initializing

3\. Run the Application
Execute your Python script to start the voice assistant. You can run it in your terminal

``` python main.py start ```

After running should see this

Press enter or click to view image in full size

## Step 6: Building a Vector Database for Storing Business Context

No go back to `**build_knowledge.py**` to create a vector database to store business knowledge using **LlamaIndex** , **OpenAI embeddings** , and **ChromaDB**. By storing context in a vectorized format, it becomes easier for Ai agent to retrieve relevant information in response to user questions

```python from llama_index.llms.openai import OpenAIfrom llama_index.embeddings.openai import OpenAIEmbeddingfrom llama_index.vector_stores.chroma import ChromaVectorStorefrom llama_index.core import download_loaderfrom llama_index.core import ( VectorStoreIndex, StorageContext, Settings)import chromadbfrom dotenv import load_dotenv# Load environment variables (e.g., API keys)load_dotenv()# Define the data loader for web contentBeautifulSoupWebReader = download_loader("BeautifulSoupWebReader")# Set up OpenAI models for LLM and embeddingSettings.llm = OpenAI(model='gpt-4')Settings.embed_model = OpenAIEmbedding( model="text-embedding-ada-002", # Use OpenAI embeddings for vectorization)# Load documents from a webpage (replace with your business URL or sources)loader = BeautifulSoupWebReader()documents = loader.load_data(urls=[ 'https://www.llamaindex.ai/'])# Initialize ChromaDB to persist vectors on diskdb = chromadb.PersistentClient(path="./query_database")# Create or get a collection for your datachroma_collection = db.get_or_create_collection("llamaindex_knowledge")# Initialize the Chroma vector storevector_store = ChromaVectorStore(chroma_collection=chroma_collection)# Set up storage context using the Chroma vector storestorage_context = StorageContext.from_defaults(vector_store=vector_store)# Build the index from your documents, using the LlamaIndex settings and storage contextindex = VectorStoreIndex.from_documents( documents, storage_context=storage_context, settings=Settings) ```

## Step 7: Building an AI Agent for LiveKit Voice Assistant

After establishing a business knowledge base, the next step is to integrate an AI agent that can retrieve relevant information during voice interactions. This agent will be utilized by LiveKit’s voice assistant to answer questions related to the business.

Here’s the process of building the AI agent, which interacts with the vector database for efficient business information retrieval.

```python from typing import Annotatedfrom livekit.agents import llmimport loggingfrom llama_index.llms.openai import OpenAIfrom llama_index.embeddings.openai import OpenAIEmbeddingfrom llama_index.core import VectorStoreIndexfrom llama_index.core.retrievers import VectorIndexRetrieverfrom llama_index.core.query_engine import RetrieverQueryEnginefrom llama_index.core import ServiceContextfrom llama_index.vector_stores.chroma import ChromaVectorStoreimport chromadbfrom llama_index.core import ( VectorStoreIndex, Settings)# Define the function class for the voice assistantclass AssistantFnc(llm.FunctionContext): def __init__(self) -> None: super().__init__() # Set the LLM and embedding model using OpenAI Settings.llm = OpenAI(model='gpt-4o') Settings.embed_model = OpenAIEmbedding( model="text-embedding-3-small" ) # Define a callable function to retrieve business information based on user queries @llm.ai_callable(description="To retrieve business information if user asks about business information related to LiveKit") def retrieve_business_information( self, query: str ): # Load the persisted ChromaDB collection from disk db2 = chromadb.PersistentClient(path="./query_database") chroma_collection = db2.get_or_create_collection("llamaindex_knowledge") # Load the vector store with the business knowledge context vector_store = ChromaVectorStore(chroma_collection=chroma_collection) # Create an index from the vector store using the settings index = VectorStoreIndex.from_vector_store( vector_store, settings=Settings ) # Use the index retriever to get relevant responses (top 3 similar) retriever = VectorIndexRetriever( index=index, similarity_top_k=3, ) # Set up the query engine using the retriever query_engine = RetrieverQueryEngine(retriever=retriever) # Process the user query and retrieve a response response = query_engine.query(query) # Return the information retrieved in a user-friendly format return f"Please find the information related to your query: {response.response}" ```

**Querying the Business Knowledge** :

* The `retrieve_business_information` function is marked with `@llm.ai_callable`, making it callable by LiveKit during voice interactions.
* When the user asks a question about LiveKit or any related business information, the agent accesses the persisted **ChromaDB** collection and retrieves the stored vectors representing business knowledge.
* It uses a **VectorStoreIndex** to search the database and fetch the top 3 most similar entries to the user’s query.

## Step 8: Experimenting with Your AI Agent

Now that you’ve successfully built the AI agent that integrates with the LiveKit voice assistant, it’s time to test it in a live environment. Before that please revise the main.py code to uncomment below ai agent function

```python from api import AssistantFncfnc_ctx = AssistantFnc() ``` ```python import asynciofrom dotenv import load_dotenvfrom livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llmfrom livekit.agents.voice_assistant import VoiceAssistantfrom livekit.plugins import openai, silerofrom api import AssistantFncload_dotenv()async def entrypoint(ctx: JobContext): initial_ctx = llm.ChatContext().append( role="system", text=( "You are a voice assistant created by LiveKit. Your interface with users will be voice. " "You should use short and concise responses, and avoiding usage of unpronouncable punctuation." ), ) await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY) fnc_ctx = AssistantFnc() assitant = VoiceAssistant( vad=silero.VAD.load(), stt=openai.STT(), llm=openai.LLM(), tts=openai.TTS(), chat_ctx=initial_ctx, fnc_ctx=fnc_ctx, ) assitant.start(ctx.room) await asyncio.sleep(1) await assitant.say("Hey, how can I help you today!", allow_interruptions=True)if __name__ == "__main__": cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint)) ```

Access the LiveKit Playground over to the [LiveKit Agents Playground](<https://agents-playground.livekit.io/>) to chat with Ai assistant.

Press enter or click to view image in full size

## Conclusion

In conclusion, integrating LiveKit with Large Language Models (LLMs) presents a groundbreaking approach to enhancing voice assistants, pushing them beyond simple task automation to handling complex, contextually aware conversations. LiveKit’s real-time capabilities, combined with advanced AI functionalities, enable businesses to build sophisticated voice assistants that streamline operations, automate tasks, and retrieve accurate, real-time information. Through seamless multimodal interactions, human-like conversations, and efficient task execution, these systems significantly improve both user experience and business productivity. As demonstrated through the combination of LiveKit with LlamaIndex and vector databases, businesses can offer precise, dynamic, and intelligent responses to customer inquiries, setting a new standard for voice assistant technology in various industries.

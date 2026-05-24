---
domain: ai.plainenglish.io
fetch_date: '2026-05-18T12:54:21.862503'
status: ok
url: https://ai.plainenglish.io/building-a-dynamic-ai-chatbot-with-graphiti-solving-rags-static-knowledge-problem-22248705d015
---

# Building a Dynamic AI Chatbot with Graphiti: Solving RAG’s Static Knowledge Problem

# **Building a Dynamic AI Chatbot with Graphiti: Solving RAG’s Static Knowledge Problem**

[ ![Samar Singh](https://miro.medium.com/v2/da:true/resize:fill:64:64/0*2cpqEgR9BJY-4CLn) ](<https://medium.com/@samarrana407?source=post_page---byline--22248705d015--------------------------------------->)

[Samar Singh](<https://medium.com/@samarrana407?source=post_page---byline--22248705d015--------------------------------------->)

9 min read

·

May 7, 2025

\--

Listen

Share

More

The rise of AI chatbots has revolutionized customer service, sales, and personalized interactions. However, traditional Retrieval-Augmented Generation (RAG) systems often struggle with a critical flaw: _static knowledge bases_. These fixed datasets limit chatbots’ ability to adapt to new information, leading to outdated or irrelevant responses. Enter **Graphiti** — a groundbreaking solution that combines dynamic knowledge graphs, long-term memory, and AI agents to create chatbots that evolve with your data.

In this article, we’ll explore how Graphiti overcomes the limitations of RAG systems, dive into its core features, and walk through a practical implementation of a multi-agent chatbot using **LangGraph** and Neo4j.

## The Problem with Traditional RAG Systems

RAG systems rely on pre-defined knowledge bases, which are frozen in time. Imagine a customer asking a shoe store chatbot about a new product line — if the knowledge base hasn’t been manually updated, the chatbot might respond with outdated inventory details or pricing. This rigidity stems from two key issues:

1. **Static Data Structures** : RAG systems struggle to map dynamic user inputs to fixed data.
2. **Memory Bottlenecks** : Large Language Models (LLMs) have limited context windows, making it hard to retain long-term conversation history or integrate real-time data.

The result? Hallucinations, irrelevant answers, and frustrated users.

## Graphiti: The Dynamic Knowledge Graph Solution

Press enter or click to view image in full size

Graphiti addresses these challenges by building **temporally aware knowledge graphs** that evolve with new interactions. Unlike static graphs, Graphiti ingests both structured (e.g., product databases) and unstructured (e.g., chat logs) data, creating a living representation of relationships between entities over time.

### Key Features of Graphiti

* **Dynamic Updates** : Automatically incorporates new user interactions, product details, or market changes.
* **Hybrid Querying** : Combines time-based, semantic, and graph algorithms to retrieve contextually relevant answers.
* **Long-Term Memory** : Tracks user preferences and past conversations, enabling personalized interactions.

For example, when a user named _Jess_ asks, _“What sizes do the Tiny Birds Wool Runners in Natural Black come in?”_ Graphiti:

1. Queries a JSON product database.
2. Links Jess’s profile to her preferences (e.g., shoe style, budget).
3. Updates the knowledge graph with this interaction for future reference.

## Graphiti vs. GraphRAG: What’s the Difference?

While both tools use knowledge graphs to enhance LLMs, they serve distinct purposes:

Press enter or click to view image in full size

Graphiti shines in environments where information changes rapidly, such as e-commerce or customer service, by maintaining historical context while adapting to new data.

## Building a Graphiti-Powered Chatbot: A ShoeBot Sales Assistant with LangGraph and Graphiti

This sample walks through creating an assistant powered by LangGraph, with Graphiti layering on personalized dialogue based on what it learns over prior chats. We also preload a catalog of footwear into the Graphiti knowledge graph so the bot can reference actual products.

Key features:

* Storing each incoming message in Graphiti and retrieving pertinent facts tied to the latest user input
* Providing a dedicated tool to fetch shoe details directly from Graphiti
* Using an in-memory MemorySaver to preserve the assistant’s conversational context between exchanges

### 1\. Dependencies & Setup

* Install dependencies

```python !pip install graphiti-core langchain-openai langgraph ipywidgets ```
* **Graphiti** : our specialized graph‑database client on top of Neo4j.
* **LangGraph** & **LangChain** : orchestrate the agent’s logic and LLM calls.
* **ipywidgets** \+ Jupyter: optional UI for interactive chat in a notebook.

```python import asyncioimport jsonimport loggingimport osimport sysimport uuidfrom contextlib import suppressfrom datetime import datetime, timezonefrom pathlib import Pathfrom typing import Annotatedimport ipywidgets as widgetsfrom dotenv import load_dotenvfrom IPython.display import Image, displayfrom typing_extensions import TypedDictload_dotenv() ```

### 2\. Logging & Neo4j Initialization

```python def setup_logging(): logger = logging.getLogger() logger.setLevel(logging.ERROR) console_handler = logging.StreamHandler(sys.stdout) console_handler.setLevel(logging.INFO) formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s') console_handler.setFormatter(formatter) logger.addHandler(console_handler) return loggerlogger = setup_logging() ```

* Configure logging to track errors and system messages.

**LangSmith integration (Optional)**

If you’d like to trace your agent using LangSmith, ensure that you have a `LANGSMITH_API_KEY` set in your environment.

Then set `os.environ['LANGCHAIN_TRACING_V2'] = 'false'` to `true`.

``` os.environ['LANGCHAIN_TRACING_V2'] = 'false'os.environ['LANGCHAIN_PROJECT'] = 'Graphiti LangGraph Tutorial' ```

Log in to [Neo4j](<https://neo4j.com/>), click on ‘Start Building,’ then create an instance and download the credentials.

Press enter or click to view image in full size

```python # Configure Graphitifrom graphiti_core import Graphitifrom graphiti_core.edges import EntityEdgefrom graphiti_core.nodes import EpisodeTypefrom graphiti_core.utils.maintenance.graph_data_operations import clear_dataneo4j_uri = os.environ.get('NEO4J_URI', 'bolt://localhost:7687')neo4j_user = os.environ.get('NEO4J_USER', 'neo4j')neo4j_password = os.environ.get('NEO4J_PASSWORD', 'password')client = Graphiti( neo4j_uri, neo4j_user, neo4j_password,) ```

* Connect to a Neo4j database to store the knowledge graph.

### 3\. Generating a database schema

The following is only required for the first run of this notebook or when you’d like to start your database over.

**IMPORTANT** : `clear_data` is destructive and will wipe your entire database.

``` await clear_data(client.driver)await client.build_indices_and_constraints() ```

### 4\. Load Shoe Data into the Graph

Load several shoe and related products into the Graphiti.

> **IMPORTANT** : This only needs to be done once. If you run `clear_data` you'll need to rerun this step.

```python async def ingest_products_data(client: Graphiti): script_dir = Path.cwd().parent json_file_path = script_dir / 'data' / 'manybirds_products.json'with open(json_file_path) as file: products = json.load(file)['products'] for i, product in enumerate(products): await client.add_episode( name=product.get('title', f'Product {i}'), episode_body=str({k: v for k, v in product.items() if k != 'images'}), source_description='ManyBirds products', source=EpisodeType.json, reference_time=datetime.now(timezone.utc), )await ingest_products_data(client) ```

### 5\. Create a user node in the Graphiti graph

In your own app, this step could be done later once the user has identified themselves and made their sales intent known. We do this here so we can configure the agent with the user’s `node_uuid`. To personalize recommendations, we represent each shopper as a node too:

```python from graphiti_core.search.search_config_recipes import NODE_HYBRID_SEARCH_EPISODE_MENTIONSuser_name = 'jess'await client.add_episode( name='User Creation', episode_body=(f'{user_name} is interested in buying a pair of shoes'), source=EpisodeType.text, reference_time=datetime.now(timezone.utc), source_description='SalesBot',)# let's get Jess's node uuidnl = await client._search(user_name, NODE_HYBRID_SEARCH_EPISODE_MENTIONS)user_node_uuid = nl.nodes[0].uuid# and the ManyBirds node uuidnl = await client._search('ManyBirds', NODE_HYBRID_SEARCH_EPISODE_MENTIONS)manybirds_node_uuid = nl.nodes[0].uuid ```

* The **episode_body** seeds Graphiti with the fact “Jess is interested…”.
* We then run a node search recipe to retrieve that newly created user node’s UUID for centering future searches.

```python def edges_to_facts_string(entities: list[EntityEdge]): return '-' + '
- '.join([edge.fact for edge in entities]) ``` ```python from langchain_core.messages import AIMessage, SystemMessagefrom langchain_core.tools import toolfrom langchain_openai import ChatOpenAIfrom langgraph.checkpoint.memory import MemorySaverfrom langgraph.graph import END, START, StateGraph, add_messagesfrom langgraph.prebuilt import ToolNode ```

### `6. `Defining the “get_shoe_data” Tool

The agent will use this to search the Graphiti graph for information about shoes. We center the search on the `manybirds_node_uuid` to ensure we rank shoe-related data over user data.

```python @toolasync def get_shoe_data(query: str) -> str: """Search the graphiti graph for information about shoes""" edge_results = await client.search( query, center_node_uuid=manybirds_node_uuid, num_results=10, ) return edges_to_facts_string(edge_results)tools = [get_shoe_data]tool_node = ToolNode(tools) ``` ``` llm = ChatOpenAI(model='gpt-4.1-mini', temperature=0).bind_tools(tools) ``` ``` # Test the tool nodeawait tool_node.ainvoke({'messages': [await llm.ainvoke('wool shoes')]}) ```

### 7\. Chatbot Function Explanation

The chatbot uses Graphiti to provide context-aware responses in a shoe sales scenario. Here’s how it works:

1. **Context Retrieval** : It searches the Graphiti graph for relevant information based on the latest message, using the user’s node as the center point. This ensures that user-related facts are ranked higher than other information in the graph.
2. **System Message** : It constructs a system message incorporating facts from Graphiti, setting the context for the AI’s response.
3. **Knowledge Persistence** : After generating a response, it asynchronously adds the interaction to the Graphiti graph, allowing future queries to reference this conversation.

This approach enables the chatbot to maintain context across interactions and provide personalized responses based on the user’s history and preferences stored in the Graphiti graph.

```python class State(TypedDict): messages: Annotated[list, add_messages] user_name: str user_node_uuid: strasync def chatbot(state: State): facts_string = None if len(state['messages']) > 0: last_message = state['messages'][-1] graphiti_query = f'{"SalesBot" if isinstance(last_message, AIMessage) else state["user_name"]}: {last_message.content}' # search graphiti using Jess's node uuid as the center node # graph edges (facts) further from the Jess node will be ranked lower edge_results = await client.search( graphiti_query, center_node_uuid=state['user_node_uuid'], num_results=5 ) facts_string = edges_to_facts_string(edge_results) system_message = SystemMessage( content=f"""You are a skillfull shoe salesperson working for ManyBirds. Review information about the user and their prior conversation below and respond accordingly. Keep responses short and concise. And remember, always be selling (and helpful!) Things you'll need to know about the user in order to close a sale: - the user's shoe size - any other shoe needs? maybe for wide feet? - the user's preferred colors and styles - their budget Ensure that you ask the user for the above if you don't already know. Facts about the user and their conversation: {facts_string or 'No facts about the user and their conversation'}""" ) messages = [system_message] + state['messages'] response = await llm.ainvoke(messages) # add the response to the graphiti graph. # this will allow us to use the graphiti search later in the conversation # we're doing async here to avoid blocking the graph execution asyncio.create_task( client.add_episode( name='Chatbot Response', episode_body=f'{state["user_name"]}: {state["messages"][-1]}
SalesBot: {response.content}', source=EpisodeType.message, reference_time=datetime.now(timezone.utc), source_description='Chatbot', ) ) return {'messages': [response]} ```

### 8\. Setting up the Agent

This section sets up the Agent’s LangGraph graph:

1. **Graph Structure** : It defines a graph with nodes for the agent (chatbot) and tools, connected in a loop.
2. **Conditional Logic** : The `should_continue` function determines whether to end the graph execution or continue to the tools node based on the presence of tool calls.
3. **Memory Management** : It uses a MemorySaver to maintain conversation state across turns. This is in addition to using Graphiti for facts.

```python graph_builder = StateGraph(State)memory = MemorySaver()# Define the function that determines whether to continue or notasync def should_continue(state, config): messages = state['messages'] last_message = messages[-1] # If there is no function call, then we finish if not last_message.tool_calls: return 'end' # Otherwise if there is, we continue else: return 'continue'graph_builder.add_node('agent', chatbot)graph_builder.add_node('tools', tool_node)graph_builder.add_edge(START, 'agent')graph_builder.add_conditional_edges('agent', should_continue, {'continue': 'tools', 'end': END})graph_builder.add_edge('tools', 'agent')graph = graph_builder.compile(checkpointer=memory) ```

We define a simple two‑node graph:

1. `**agent**` — runs `chatbot()`
2. `**tools**` — invokes `get_shoe_data` if the AI issues a tool call

Edges loop back from `**agent → (conditional) → tools → agent**`**,** with a****`**should_continue()**` function that checks whether the last message contains any tool calls. This lets the agent chain multiple tool queries seamlessly before returning to user output.

### 9\. Running the Agent

Let’s test the agent with a single call

``` await graph.ainvoke( { 'messages': [ { 'role': 'user', 'content': 'What sizes do the TinyBirds Wool Runners in Natural Black come in?', } ], 'user_name': user_name, 'user_node_uuid': user_node_uuid, }, config={'configurable': {'thread_id': uuid.uuid4().hex}},) ```

### 10\. Running the Agent interactively

The following code will run the agent in an event loop. Just enter a message into the box and click submit.

```python conversation_output = widgets.Output()config = {'configurable': {'thread_id': uuid.uuid4().hex}}user_state = {'user_name': user_name, 'user_node_uuid': user_node_uuid}async def process_input(user_state: State, user_input: str): conversation_output.append_stdout(f'
User: {user_input}
') conversation_output.append_stdout('
Assistant: ') graph_state = { 'messages': [{'role': 'user', 'content': user_input}], 'user_name': user_state['user_name'], 'user_node_uuid': user_state['user_node_uuid'], } try: async for event in graph.astream( graph_state, config=config, ): for value in event.values(): if 'messages' in value: last_message = value['messages'][-1] if isinstance(last_message, AIMessage) and isinstance( last_message.content, str ): conversation_output.append_stdout(last_message.content) except Exception as e: conversation_output.append_stdout(f'Error: {e}')def on_submit(b): user_input = input_box.value input_box.value = '' asyncio.create_task(process_input(user_state, user_input))input_box = widgets.Text(placeholder='Type your message here...')submit_button = widgets.Button(description='Send')submit_button.on_click(on_submit)conversation_output.append_stdout('Asssistant: Hello, how can I help you find shoes today?')display(widgets.VBox([input_box, submit_button, conversation_output])) ```

## Putting It All Together

By combining:

* **Graphiti** for knowledge ingestion & retrieval
* **LangGraph** for structured agent flow
* **LangChain/OpenAI** for LLM responses

you get a fully stateful, personalized ShoeBot that:

* Remembers past turns (via Graphiti episodes + MemorySaver)
* Knows your brand catalog inside‑out
* Dynamically calls tools to fetch product facts
* Persists every new fact for even richer future recommendations

Feel free to tweak search limits, change the system prompt, or swap in your own product catalog — this pattern scales to any vertical where personalized selling matters.

> Graphiti works best with LLM services that support Structured Output (such as OpenAI and Gemini). Using other services may result in incorrect output schemas and ingestion failures. This is particularly problematic when using smaller models.

## Why Graphiti Matters for Real-World Applications

Graphiti isn’t just a technical novelty — it’s a game-changer for industries like:

* **E-commerce** : Provide up-to-date product recommendations.
* **Healthcare** : Track patient histories and evolving symptoms.
* **Finance** : Adapt to market fluctuations and regulatory changes.

By solving RAG’s static data problem, Graphiti empowers AI agents to deliver accurate, context-aware responses while reducing hallucinations.

## Final Thoughts

Traditional chatbots are limited by their inability to learn from interactions. Graphiti breaks this barrier by merging dynamic knowledge graphs with long-term memory, creating AI agents that grow smarter over time. Whether you’re building a sales assistant or a customer support bot, Graphiti offers a scalable, future-proof solution.

Ready to revolutionize your chatbot? Dive into [Graphiti’s documentation](<https://github.com/getzep/graphiti>), experiment with LangGraph, and start building agents that truly understand your users.

## Thank you for being a part of the community

_Before you go:_

* Be sure to **clap** and **follow** the writer ️👏**️️**
* Follow us: [**X**](<https://x.com/inPlainEngHQ>) | [**LinkedIn**](<https://www.linkedin.com/company/inplainenglish/>) | [**YouTube**](<https://www.youtube.com/@InPlainEnglish>) | [**Newsletter**](<https://newsletter.plainenglish.io/>) | [**Podcast**](<https://open.spotify.com/show/7qxylRWKhvZwMz2WuEoua0>) | [**Differ**](<https://differ.blog/inplainenglish>) | [**Twitch**](<https://twitch.tv/inplainenglish>)
* [**Start your own free AI-powered blog on Differ**](<https://differ.blog/>) 🚀
* [**Join our content creators community on Discord**](<https://discord.gg/in-plain-english-709094664682340443>) 🧑🏻‍💻
* For more content, visit [**plainenglish.io**](<https://plainenglish.io/>) \+ [**stackademic.com**](<https://stackademic.com/>)

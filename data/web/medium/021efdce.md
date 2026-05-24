---
domain: medium.com
fetch_date: '2026-05-18T12:51:34.443422'
status: ok
url: https://medium.com/@manthapavankumar11/asknews-and-qdrant-meet-phidata-the-future-of-agentic-ai-driven-news-moderation-e68f6baf4c95
---

# AskNews and Qdrant Meet Phidata: The Future of Agentic AI-Driven News Moderation

[ ![M K Pavan Kumar](https://miro.medium.com/v2/resize:fill:64:64/1*hm4EMU6eAUOoFTldl_OzNg.jpeg) ](</@manthapavankumar11?source=post_page---byline--e68f6baf4c95--------------------------------------->)

[M K Pavan Kumar](</@manthapavankumar11?source=post_page---byline--e68f6baf4c95--------------------------------------->)

17 min read

·

Dec 14, 2024

\--

\--

Listen

Share

More

In this article we will do very deep dive of creating heavy agentic news team, that is powered by `AskNews`, `Qdrant` and `Phidata`. The main intention of this article is to show the potential of the agentic system from the planning, memory and their tool calling capabilities. The entire system as said is designed using `Phidata`. In this article we will also use `Phidata Playground,` an UI to interact with our Agentic News team and in the next article we will create our own UI for this Agentic team. without much delay let's dive into our article.

![created by author M K Pavan Kumar](https://miro.medium.com/v2/resize:fit:700/1*P9B9JG2gv7G7NqO6nJjT2g.png)

### The Story:

Imagine you are sitting with a friendly editor who knows exactly where to find the right stories for you. When you first ask a question or request some piece of news, you start by talking to this “Editor in Chief.” This editor is not just any editor. It’s the main connection point that understands what you need, considers the best place to look, and then passes on your request to just the right specialist.

From the editor’s desk, your request heads off to a variety of specialized news agents. Each agent has its own area of focus — science and technology, business, political, crime, finance, and sports. Think of them like individual reporters who are experts in their respective fields. After receiving your question, the appropriate news agent gets right to work. It takes your request, searches for the information, and then shapes the answer before handing it back to the editor.

Once a news agent begins to hunt for information, it connects to a knowledge repository and an API that runs on a platform called Qdrant. This repository acts as a massive library, filled with the most up-to-date and rich set of data. The news agent queries the repository, finds the relevant information, and returns the findings. These results then travel back through the agent to the editor, who polishes the answer into something you can easily understand and appreciate.

In this setup, you do not need to worry about who is finding what or where the information is coming from behind the scenes. You only speak with the Editor in Chief. Behind that editor, an entire team of specialized agents and a powerful knowledge engine are working together, quietly making sure you get the quality news answers you are looking for. It is a harmonious blend of human-like guidance and well-organized data retrieval that feels both efficient and personal.

### What are Agents?

![created by author, M K Pavan Kumar](https://miro.medium.com/v2/resize:fit:700/1*tG3Ztg9jYkhVSylW2LEKHA.png)

An AI agent is an autonomous software system that can sense its surroundings, process information, and take actions to accomplish defined objectives. Think of it as a digital entity that operates independently, analyzing input from its environment and making decisions without needing constant human guidance. These agents use various data sources planning and tools to understand their context and determine the most appropriate responses or actions to take.

### The Implementation

``` .├── LICENSE├── README.md├── agents│ ├── __init__.py│ ├── business_news_agent.py│ ├── climate_news_agent.py│ ├── crime_news_agent.py│ ├── financial_news_agent.py│ ├── health_news_agent.py│ ├── military_news_agent.py│ ├── political_news_agent.py│ ├── science_and_technology_news_agent.py│ └── sports_news_agent.py├── asknews_tools│ ├── __init__.py│ ├── agents.db│ └── query_tool.py├── asknews_utils│ ├── __init__.py│ └── news_encoder.py├── news_agent_team.py└── requirements.txt ```

At the top level, there is a main project directory that likely represents the entire codebase. Inside the main project, you’ll see an `agents` folder. This directory is where the core of the application’s logic is organized. Each sub-directory or file within it usually corresponds to a specific type of news agent, grouping all related code together. This makes it easier to maintain and scale different parts of the system without getting lost in a tangled codebase. Next, you’ll find a folder named `asknews_tools`, which acts like a small toolkit within the project. This is where the foundational tools and helper functionalities are placed resources that the agents rely on to perform their tasks. Similarly, `asknews_utils` is another folder dedicated to reusable components that the system depends on, whether that means functions that standardize data processing or utilities that help agents interact with external resources.

In essence, the folder structure is designed to keep everything tidy and intuitive. Each folder serves a clear purpose, whether it’s holding agents that fetch and process news, storing utilities that agents rely on, or simply helping you manage and navigate your project more effectively.

### The Agent Prompt:

Prompt technique, in the context of language models or AI assistants, refers to a method of instructing the AI on how to respond or perform a certain task. A “prompt” is the input you give to the model — essentially a set of directions, constraints, or content examples that guide the model toward producing a desired type of output. Effective prompt techniques include specifying roles, outlining steps for reasoning, setting a tone or style, and detailing the formatting or structure of the final answer. By carefully crafting prompts, you can guide the AI to produce more accurate, contextually appropriate, and useful responses.

``` """You are now the Sports News Reporter and News Agent of a major news organization, who decades of experience in fact-checking of the actual news. Always use the tools provided to fulfil request from editor in chief. Your role requires: ANALYSIS APPROACH: 1. First, break down the news piece using Chain of Thought reasoning: - What are the key claims? - Who are the primary sources? - What is the chronological sequence of events? - What supporting evidence is provided? 2. Then, apply critical analysis: - Cross-reference dates and statistics with your knowledge base - Identify potential biases or gaps in reporting - Evaluate the credibility of sources - Check for logical consistency in the narrative 3. For data verification: - Use the most recent available data (specify the year) - Flag any outdated statistics - Note any discrepancies between different data sources - Highlight where additional verification might be needed OUTPUT STRUCTURE: - Start with an executive summary - Present key findings using markdown bullet points - Include specific dates and sources for all major claims - Provide confidence levels for each verified claim (High/Medium/Low) - Add editorial recommendations for further investigation if needed CRITICAL GUIDELINES: - Always indicate source links and dates. - Always use the tools provided. - Always refer to the latest year. - Clearly separate verified facts from unverified claims. - Note any temporal gaps in the narrative. - Flag any potential misinformation or need for additional context. When responding, explicitly walk through your reasoning process before presenting conclusions.""" ```

The provided prompt is instructing the AI (in this case, an Agent) to step into a specific role and follow a well-defined process for analyzing and reporting on sports news. Here’s what it’s doing, step-by-step:

**Role Definition:**

* The assistant is told: “You are now the Sports News Reporter and News Agent of a major news organization.”
This sets the stage for the assistant to respond as if it is an experienced journalist with decades of fact-checking expertise.

**Tool Utilization:**

* The assistant is directed to “Always use the tools provided.” In a system where external tools may be available (such as web search plugins or reference databases), this means the assistant should rely on those tools to verify facts and obtain the latest data.

**Analysis Approach (Chain of Thought):**
The prompt outlines a structured method for analyzing a piece of sports news:

* **Break down the key claims:** Identify what the main pieces of information are.
* **Check sources:** Determine who is reporting the claims, such as official sports organizations, reputable journalists, or eyewitness accounts.
* **Chronological sequence of events:** Understand the timeline of when things happened.
* **Supporting evidence:** Look at what data, interviews, documents, or statistics support the claims.

After identifying the basics, the prompt asks the assistant to perform:

* **Critical analysis:** Cross-check facts, identify biases, evaluate credibility, and check logical consistency.
* **Data verification:** Ensure the data used is recent and reliable. Flag outdated or conflicting numbers and consider where more verification might be needed.

**Output Structure:**
The prompt requires the assistant to present its final report in a structured way:

* Start with an executive summary (a concise overview of the findings).
* Use markdown bullet points for key findings.
* Include specific dates, sources, and confidence levels (High/Medium/Low) for each verified claim.
* Provide editorial recommendations for further investigation.

**Critical Guidelines:**
The prompt sets rules for the assistant’s response:

* Always show source links and dates.
* Always use tools and refer to the latest year.
* Separate verified facts from unverified claims.
* Note any temporal gaps or potential misinformation.

The instructions emphasize full transparency, careful sourcing, and distinguishing between what is confirmed and what is speculative or uncertain.

**Reasoning before Conclusions:**
Finally, the prompt instructs the assistant to “explicitly walk through your reasoning process before presenting conclusions.” This means the assistant should show how it reached its final assessment, demonstrating the reasoning steps to the user before giving the polished summary and recommendations.

`business_new_agent.py`

```python from phi.agent import Agentfrom asknews_tools.query_tool import query_business_newsfrom phi.model.openai import OpenAIChatfrom phi.storage.agent.sqlite import SqlAgentStoragebusiness_news_agent = Agent( name="Business News Agent", model=OpenAIChat(id="gpt-4o-mini"), tools=[query_business_news], role="Search only for business news using the tools provided", instructions=[ """You are now the Business News Reporter and News Agent of a major news organization, who decades of experience in fact-checking of the actual news. Always use the tools provided to fulfil request from editor in chief. Your role requires: ANALYSIS APPROACH: 1. First, break down the news piece using Chain of Thought reasoning: - What are the key claims? - Who are the primary sources? - What is the chronological sequence of events? - What supporting evidence is provided? 2. Then, apply critical analysis: - Cross-reference dates and statistics with your knowledge base - Identify potential biases or gaps in reporting - Evaluate the credibility of sources - Check for logical consistency in the narrative 3. For data verification: - Use the most recent available data (specify the year) - Flag any outdated statistics - Note any discrepancies between different data sources - Highlight where additional verification might be needed OUTPUT STRUCTURE: - Start with an executive summary - Present key findings using markdown bullet points - Include specific dates and sources for all major claims - Provide confidence levels for each verified claim (High/Medium/Low) - Add editorial recommendations for further investigation if needed CRITICAL GUIDELINES: - Always indicate source links and dates. - Always use the tools provided. - Always refer to the latest year. - Clearly separate verified facts from unverified claims. - Note any temporal gaps in the narrative. - Flag any potential misinformation or need for additional context. When responding, explicitly walk through your reasoning process before presenting conclusions.""" ], storage=SqlAgentStorage(table_name="news_agent", db_file="asknews_tools/agents.db"), add_history_to_messages=True, markdown=True, reasoning=True, show_full_reasoning=True) ```

`crime_news_agent.py`

```python from phi.agent import Agentfrom asknews_tools.query_tool import query_crime_newsfrom phi.model.openai import OpenAIChatfrom phi.storage.agent.sqlite import SqlAgentStoragecrime_news_agent = Agent( name="Crime News Agent", model=OpenAIChat(id="gpt-4o-mini"), tools=[query_crime_news], role="Search only for crime news using the tools provided", instructions=[ """You are now the Crime News Reporter and News Agent of a major news organization, who decades of experience in fact-checking of the actual news. Always use the tools provided to fulfil request from editor in chief. Your role requires: ANALYSIS APPROACH: 1. First, break down the news piece using Chain of Thought reasoning: - What are the key claims? - Who are the primary sources? - What is the chronological sequence of events? - What supporting evidence is provided? 2. Then, apply critical analysis: - Cross-reference dates and statistics with your knowledge base - Identify potential biases or gaps in reporting - Evaluate the credibility of sources - Check for logical consistency in the narrative 3. For data verification: - Use the most recent available data (specify the year) - Flag any outdated statistics - Note any discrepancies between different data sources - Highlight where additional verification might be needed OUTPUT STRUCTURE: - Start with an executive summary - Present key findings using markdown bullet points - Include specific dates and sources for all major claims - Provide confidence levels for each verified claim (High/Medium/Low) - Add editorial recommendations for further investigation if needed CRITICAL GUIDELINES: - Always indicate source links and dates. - Always use the tools provided. - Always refer to the latest year. - Clearly separate verified facts from unverified claims. - Note any temporal gaps in the narrative. - Flag any potential misinformation or need for additional context. When responding, explicitly walk through your reasoning process before presenting conclusions.""" ], storage=SqlAgentStorage(table_name="news_agent", db_file="asknews_tools/agents.db"), add_history_to_messages=True, markdown=True, reasoning=True, show_full_reasoning=True) ```

`military_news_agent.py`

```python from phi.agent import Agentfrom asknews_tools.query_tool import query_military_newsfrom phi.model.openai import OpenAIChatfrom phi.storage.agent.sqlite import SqlAgentStoragemilitary_news_agent = Agent( name="Military News Agent", model=OpenAIChat(id="gpt-4o-mini"), tools=[query_military_news], role="Search only for military news using the tools provided", instructions=[ """You are now the Military News Reporter and News Agent of a major news organization, who decades of experience in fact-checking of the actual news. Always use the tools provided to fulfil request from editor in chief. Your role requires: ANALYSIS APPROACH: 1. First, break down the news piece using Chain of Thought reasoning: - What are the key claims? - Who are the primary sources? - What is the chronological sequence of events? - What supporting evidence is provided? 2. Then, apply critical analysis: - Cross-reference dates and statistics with your knowledge base - Identify potential biases or gaps in reporting - Evaluate the credibility of sources - Check for logical consistency in the narrative 3. For data verification: - Use the most recent available data (specify the year) - Flag any outdated statistics - Note any discrepancies between different data sources - Highlight where additional verification might be needed OUTPUT STRUCTURE: - Start with an executive summary - Present key findings using markdown bullet points - Include specific dates and sources for all major claims - Provide confidence levels for each verified claim (High/Medium/Low) - Add editorial recommendations for further investigation if needed CRITICAL GUIDELINES: - Always indicate source links and dates. - Always use the tools provided. - Always refer to the latest year. - Clearly separate verified facts from unverified claims. - Note any temporal gaps in the narrative. - Flag any potential misinformation or need for additional context. When responding, explicitly walk through your reasoning process before presenting conclusions.""" ], storage=SqlAgentStorage(table_name="news_agent", db_file="asknews_tools/agents.db"), add_history_to_messages=True, markdown=True, reasoning=True, show_full_reasoning=True) ```

`political_news_agent.py`

```python from phi.agent import Agentfrom asknews_tools.query_tool import query_political_newsfrom phi.model.openai import OpenAIChatfrom phi.storage.agent.sqlite import SqlAgentStoragepolitical_news_agent = Agent( name="Political News Agent", model=OpenAIChat(id="gpt-4o-mini"), tools=[query_political_news], role="Search only for political news using the tools provided", instructions=[ """You are now the Political News Reporter and News Agent of a major news organization, who decades of experience in fact-checking of the actual news. Always use the tools provided to fulfil request from editor in chief. Your role requires: ANALYSIS APPROACH: 1. First, break down the news piece using Chain of Thought reasoning: - What are the key claims? - Who are the primary sources? - What is the chronological sequence of events? - What supporting evidence is provided? 2. Then, apply critical analysis: - Cross-reference dates and statistics with your knowledge base - Identify potential biases or gaps in reporting - Evaluate the credibility of sources - Check for logical consistency in the narrative 3. For data verification: - Use the most recent available data (specify the year) - Flag any outdated statistics - Note any discrepancies between different data sources - Highlight where additional verification might be needed OUTPUT STRUCTURE: - Start with an executive summary - Present key findings using markdown bullet points - Include specific dates and sources for all major claims - Provide confidence levels for each verified claim (High/Medium/Low) - Add editorial recommendations for further investigation if needed CRITICAL GUIDELINES: - Always indicate source links and dates. - Always use the tools provided. - Always refer to the latest year. - Clearly separate verified facts from unverified claims. - Note any temporal gaps in the narrative. - Flag any potential misinformation or need for additional context. When responding, explicitly walk through your reasoning process before presenting conclusions.""" ], storage=SqlAgentStorage(table_name="news_agent", db_file="asknews_tools/agents.db"), add_history_to_messages=True, markdown=True, reasoning=True, show_full_reasoning=True) ```

With the given prompt it creates a unified behavioural framework tailored to each specific domain of reporting. Under this prompt structure, each agent adopts a role as a specialized journalist and fact-checker with decades of experience in their respective field. They meticulously break down claims, analyze events chronologically, verify data, and attribute all information to credible sources. Although each agent covers a different domain, they share the same structured process: performing chain-of-thought analysis, identifying sources, checking for logical consistency, and critically evaluating the reliability of information.

### Tools | Function Calling:

In the realm of AI agents, **tools** are external resources or functions that enhance an agent’s capabilities, enabling it to perform tasks beyond simple text generation. These tools can include APIs, databases, or other software services that provide specific functionalities, such as retrieving real-time data, performing computations, or executing actions in external systems.

**Function calling** is a mechanism that allows AI agents to invoke these external tools or functions programmatically. By defining functions with specific parameters and behaviors, developers can enable AI models to recognize when a function is needed and generate the appropriate function calls with the required arguments. This integration allows AI agents to perform complex tasks, access up-to-date information, and interact dynamically with various systems.

`create_asknews_client.py`

```python def asknews_news_client(): ask = AskNewsSDK( client_id=os.environ.get("ASK_NEWS_CLIENT_ID"), client_secret=os.environ.get("ASK_NEWS_SECRET"), scopes={"news"} ) return ask ```

`query_tools.py`

```python def query_political_news(query_str: str, continents: str, country_code: str) -> Any: """Use this function to get top news related to technology. Args: query_str (str): the user query to search for technology news. continents (str): specific news from the geographic region (continent) country_code (str): specific news in a specific country within the continents. Returns: str: JSON object of top story summaries. """ print(f"Calling political Tool with, query_str: {query_str}, continents: {continents}") response = asknews_news_client().news.search_news( query=query_str, # your keyword query n_articles=10, # control the number of articles to include in the context return_type="dicts", # you can also ask for "dicts" if you want more information method="both", # use "nl" for natural language for your search, or "kw" for keyword search continents=[continents], countries=[country_code], categories=["Politics"], strategy='latest news' ) return create_json_response(response)def query_business_news(query_str: str, continents: str, country_code: str) -> Any: """Use this function to get top news related to business Args: query_str (str): the user query to search for business news. continents (str): specific news from the geographic region (continent). country_code (str): specific news in a specific country within the continents. Returns: str: JSON object of top story summaries. """ print(f"Calling business tool with, query_str: {query_str}, continents: {continents}") response = asknews_news_client().news.search_news( query=query_str, # your keyword query n_articles=10, # control the number of articles to include in the context return_type="dicts", # you can also ask for "dicts" if you want more information method="both", # use "nl" for natural language for your search, or "kw" for keyword search, continents=[continents], countries=[country_code], categories=["Business"], strategy='latest news' ) return create_json_response(response)def query_crime_news(query_str: str, continents: str, country_code: str) -> Any: """Use this function to get top news related to Crime Args: query_str (str): the user query to search for business news. continents (str): specific news from the geographic region (continent). country_code (str): specific news in a specific country within the continents. Returns: str: JSON object of top story summaries. """ print(f"Calling crime tool with, query_str: {query_str}, continents: {continents}") response = asknews_news_client().news.search_news( query=query_str, # your keyword query n_articles=10, # control the number of articles to include in the context return_type="dicts", # you can also ask for "dicts" if you want more information method="both", # use "nl" for natural language for your search, or "kw" for keyword search, continents=[continents], countries=[country_code], categories=["Crime"], strategy='latest news' ) return create_json_response(response)def query_military_news(query_str: str, continents: str, country_code: str) -> Any: """Use this function to get top news related to Military Args: query_str (str): the user query to search for military news. continents (str): specific news from the geographic region (continent). country_code (str): specific news in a specific country within the continents. Returns: str: JSON object of top story summaries. """ print(f"Calling military tool with, query_str: {query_str}, continents: {continents}") response = asknews_news_client().news.search_news( query=query_str, # your keyword query n_articles=10, # control the number of articles to include in the context return_type="dicts", # you can also ask for "dicts" if you want more information method="both", # use "nl" for natural language for your search, or "kw" for keyword search, continents=[continents], countries=[country_code], categories=["Military"], strategy='latest news' ) return create_json_response(response) ```

**Supervisor Agent (Editor in Chief)**

The `agent_team` defined here acts as the central authority or coordinator in a multi-agent news system, designated as the "chief news editor." Its primary role is to manage and oversee a team of specialized news agents, each focusing on a particular domain such as business, crime, finance, politics, science and technology, sports, military, health, and climate. Powered by the `AskNews, Phidata and Qdrant.`the chief editor's responsibilities include synthesizing and streamlining the information provided by these domain-specific agents to fulfil user queries efficiently. The agent is configured to rely on tools for answering queries, ensuring that responses are both accurate and supported by relevant source links. It operates with clear, user-friendly communication by enabling markdown formatting and streaming responses in real-time. Additionally, it includes contextual details such as the current date and time in its responses and prioritizes transparency by displaying tool calls and reasoning processes. This design ensures the agent delivers authoritative, well-reasoned, and traceable news outputs, embodying the editorial oversight necessary for a robust, multi-agent news system.

`news_agent_team.py`

```python from phi.agent import Agentfrom agents.business_news_agent import business_news_agentfrom agents.climate_news_agent import climate_news_agentfrom agents.sports_news_agent import sports_news_agentfrom agents.health_news_agent import health_news_agentfrom agents.crime_news_agent import crime_news_agentfrom agents.military_news_agent import military_news_agentfrom agents.science_and_technology_news_agent import science_and_technology_news_agentfrom agents.political_news_agent import political_news_agentfrom agents.financial_news_agent import financial_news_agentfrom phi.playground import Playground, serve_playground_appfrom phi.model.openai import OpenAIChatagent_team = Agent( name="chief news editor", model=OpenAIChat(id="gpt-4o-mini"), team=[business_news_agent, crime_news_agent, financial_news_agent, political_news_agent, science_and_technology_news_agent, sports_news_agent, military_news_agent, health_news_agent, climate_news_agent], instructions=["Always use tools to fulfil the user query. Always give the link to sources "], show_tool_calls=True, reasoning=False, markdown=True, show_full_reasoning=True, add_datetime_to_instructions=True, stream=True)app = Playground(agents=[agent_team]).get_app()if __name__ == "__main__": serve_playground_app("news_agent_team:app", reload=True) ```

From AskNews we would receive the dtaa in the Dict forat or as a string format bt for better understanding we need to conver the Dict format to JSOn and below code is a custom framework for converting complex data types (Dict) into JSON-compatible formats and creating a structured JSON response for a search-related use case, likely for a news aggregation system. It includes a custom JSON encoder, `NewsJSONEncoder`, to handle special data types like `datetime`, `UUID`, and objects with attributes, ensuring they are serialized appropriately. The `convert_to_json` function recursively processes various Python data structures (e.g., lists, dictionaries, and custom objects) to clean and standardize their format, removing private attributes (those starting with `_`) and `None` values. The `extract_search_response_data` function extracts and processes data from a `SearchResponse` object or its string representation, including special handling for tuples and string representations of such objects. Finally, `create_json_response` combines these utilities to generate a formatted JSON response, including metadata like status, article count, and a list of serialized articles, ensuring the result is human-readable and adheres to a defined structure.

`news_encoder.py`

```python import jsonfrom datetime import datetimefrom typing import Any, Dict, Listfrom uuid import UUIDclass NewsJSONEncoder(json.JSONEncoder): """Custom JSON encoder to handle special types""" def default(self, obj): if isinstance(obj, datetime): return obj.isoformat() if isinstance(obj, UUID): return str(obj) if hasattr(obj, '__dict__'): return self._clean_dict(obj.__dict__) return str(obj) def _clean_dict(self, d): """Clean dictionary by removing None values and private attributes""" return {k: v for k, v in d.items() if not k.startswith('_') and v is not None}def convert_to_json(data: Any) -> Dict: """Convert objects to JSON-compatible dictionary""" if isinstance(data, list): return [convert_to_json(item) for item in data] if hasattr(data, '_asdict'): # Handle namedtuple-like objects data = data._asdict() if isinstance(data, dict): result = {} for key, value in data.items(): if key.startswith('_') or value is None: continue if isinstance(value, (list, tuple)): result[key] = convert_to_json(value) elif isinstance(value, (dict, object)) and hasattr(value, '__dict__'): result[key] = convert_to_json(value.__dict__) elif isinstance(value, UUID): result[key] = str(value) elif isinstance(value, datetime): result[key] = value.isoformat() else: result[key] = value return result if hasattr(data, '__dict__'): return convert_to_json(data.__dict__) return str(data)def extract_search_response_data(data): """Extract data from SearchResponse object or string representation""" if isinstance(data, str): # Handle string representation if "SearchResponseDictItem" in data: # Extract the list part from the string start = data.find("[") end = data.rfind("]") if start != -1 and end != -1: data = eval(data[start:end + 1]) # Handle SearchResponse object if hasattr(data, 'as_dicts'): return data.as_dicts elif isinstance(data, tuple): # Handle tuple representation for item in data: if isinstance(item, list): return item elif isinstance(item, str) and "SearchResponseDictItem" in item: return extract_search_response_data(item) return datadef create_json_response(data: Any) -> str: """Create a formatted JSON response""" # Extract the actual data articles_data = extract_search_response_data(data) if not articles_data: return json.dumps({ "status": "error", "message": "Could not extract articles data", "count": 0, "articles": [] }, indent=2) response = { "status": "success", "count": len(articles_data), "articles": convert_to_json(articles_data) } return json.dumps(response, indent=2, ensure_ascii=False, cls=NewsJSONEncoder) ```

### The Execution:

run the `news_agent_team.py` and click on the URL generated on your consle. The UI should lloks something as below connected to locahost:7777 and pointing to our Chief News Editor agent.

![image](https://miro.medium.com/v2/resize:fit:700/1*IjoyrUApzBZAx_Wn5uZHig.png) ![image](https://miro.medium.com/v2/resize:fit:700/1*GBWUGr2j0IBlknTquSnUTQ.png) ![image](https://miro.medium.com/v2/resize:fit:700/1*tK447TdfyeceIRRWR_0B8g.png) ![image](https://miro.medium.com/v2/resize:fit:700/1*aq8zL8sRI3-fbCY_vXU4zg.png)

Behind the scenes respective agents are called as below by passing required details as parameters.

![image](https://miro.medium.com/v2/resize:fit:700/1*TJyFca73R-KQ7hZCzgvrgQ.png)

### The Conclusion

In conclusion, the integration of advanced AI tools and frameworks into news aggregation systems represents a transformative step toward delivering personalized, accurate, and timely information to users. By leveraging the capabilities of solutions like Phidata, AskNews and Qdrant, we not only enhance the efficiency of retrieving relevant content but also set the stage for more dynamic, multi-agent collaboration in data processing. As these innovations continue to evolve, they promise to redefine how we interact with and consume information, paving the way for smarter, more intuitive systems that truly understand and cater to user needs.

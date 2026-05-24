---
domain: medium.com
fetch_date: '2026-05-18T12:55:12.192686'
status: ok
url: https://medium.com/@richardhightower/litellm-and-mcp-one-gateway-to-rule-all-ai-models-378a38ce7746
---

# LiteLLM and MCP: One Gateway to Rule All AI Models

![LiteLLM and MCP](https://miro.medium.com/v2/resize:fit:643/1*kmDiftNhwb1lQ87gHWsg3g.png)

# LiteLLM and MCP: One Gateway to Rule All AI Models

[ ![Rick Hightower](https://miro.medium.com/v2/resize:fill:64:64/1*cozwhlRkTftuwz3ugEosIA.jpeg) ](</@richardhightower?source=post_page---byline--378a38ce7746--------------------------------------->)

[Rick Hightower](</@richardhightower?source=post_page---byline--378a38ce7746--------------------------------------->)

8 min read

·

Jun 24, 2025

\--

\--

Listen

Share

More

Picture this: You’ve built a sophisticated AI tool integration, but your client suddenly wants to switch from OpenAI to Claude for cost reasons. Or maybe they need to use local models for sensitive data while leveraging cloud models for general queries. Without proper abstraction, each change means rewriting your integration code. LiteLLM combined with the Model Context Protocol (MCP) transforms this nightmare into a simple configuration change.

This article demonstrates how LiteLLM’s universal gateway integrates with MCP to create truly portable AI tool integrations. Whether using OpenAI, Anthropic, AWS Bedrock, or local models through Ollama, your MCP tools work seamlessly across all of them.

If you like this article, follow Rick on [LinkedIn](<https://www.linkedin.com/in/rickhigh/>) or [Medium](</@richardhightower>).

## About Our MCP Server: The Customer Service Assistant

Before exploring how to connect LiteLLM to MCP, it’s helpful to understand what we’re linking to. We built a full customer service MCP server using FastMCP in our complete MCP guide. This server serves as our foundation for demonstrating different client integrations.

Our MCP server exposes three powerful tools that any AI system can leverage:

**Available Tools:**

* **get_recent_customers** : This tool retrieves a list of recently active customers with their current status. It helps AI agents understand customer history and patterns.
* **create_support_ticket** : This tool creates new support tickets with customizable priority levels. It validates customer existence and generates unique ticket IDs.
* **calculate_account_value** : Analyzes purchase history to calculate total account value and average purchase amounts. This helps in customer segmentation and support prioritization.

The server also provides a **customer resource** (customer://{customer_id}) for direct customer data access and includes a **prompt template** for generating professional customer service responses.

What makes this special is that these tools work with any MCP-compatible client, whether using OpenAI, Claude, LangChain, DSPy, or any other framework. The same server, built once, serves them all. This is the power of standardization that MCP brings to AI tool integration.

In this article, we’ll explore how LiteLLM connects to this server and enables these tools to work with over 100 different LLM providers.

## Understanding LiteLLM: The Universal LLM Gateway

LiteLLM is more than just another AI library — it’s a universal translator for language models. Think of it as the Rosetta Stone of AI APIs, enabling you to write code once and run it with any supported model. Key features include:

* **100+ Model Support** : From OpenAI and Anthropic to local models and specialized providers
* **Unified Interface** : Same code works across all providers
* **Load Balancing** : Distribute requests across multiple providers
* **Cost Tracking** : Monitor usage and costs across providers
* **Fallback Support** : Automatically switch providers on failure
* **Format Translation** : Converts between different API formats seamlessly

For deeper dives into LiteLLM’s capabilities, check out my articles on building a [multi-provider chat application](</@richardhightower/multi-provider-chat-app-litellm-streamlit-ollama-gemini-claude-perplexity-and-modern-llm-afd5218c7eab>) and [enhancing it with RAG and streaming](</@richardhightower/beyond-chat-enhancing-litellm-multi-provider-app-with-rag-streaming-and-aws-bedrock-65767dd34a53>).

## The Power of LiteLLM + MCP

Combining LiteLLM with MCP creates unprecedented flexibility:

1. **Write Once, Deploy Anywhere** : Your MCP tools work with any LLM provider.
2. **Provider Agnostic** : Switch between models without changing the tool integration code
3. **Cost Optimization** : Route requests to the most cost-effective provider
4. **Compliance Friendly** : Use local models for sensitive data, cloud for general queries
5. **Future Proof** : New LLM providers automatically work with existing tools

## Building Your First LiteLLM + MCP Integration

Let’s create an integration demonstrating LiteLLM’s ability to use MCP tools across different providers.

## Step 1: Setting Up the Integration

Here’s the [core setup that connects LiteLLM ](<https://github.com/RichardHightower/mcp_article1/blob/main/src/litellm_integration.py>)to your MCP server:

```python import asyncioimport jsonimport litellmfrom litellm import experimental_mcp_clientfrom mcp import ClientSession, StdioServerParametersfrom mcp.client.stdio import stdio_clientfrom config import Configasync def setup_litellm_mcp(): """Set up LiteLLM with MCP tools.""" # Create MCP server connection server_params = StdioServerParameters( command="poetry", args=["run", "python", "src/main.py"] ) async with stdio_client(server_params) as (read, write): async with ClientSession(read, write) as session: # Initialize the MCP connection await session.initialize() # Load MCP tools in OpenAI format tools = await experimental_mcp_client.load_mcp_tools( session=session, format="openai" ) print(f"Loaded {len(tools)} MCP tools") ```

The key insight here is the `format="openai"` parameter. LiteLLM's experimental MCP client loads tools in OpenAI's function calling format, which LiteLLM can then translate to any provider's format.

## Step 2: Multi-Model Testing

One of LiteLLM’s strengths is enabling the same code to work with multiple models:

```json # Dynamically select models based on configurationmodels_to_test = []if Config.LLM_PROVIDER == "openai": models_to_test.append(Config.OPENAI_MODEL)elif Config.LLM_PROVIDER == "anthropic": models_to_test.append(Config.ANTHROPIC_MODEL)else: # Test with multiple providers models_to_test = [Config.OPENAI_MODEL, Config.ANTHROPIC_MODEL]for model in models_to_test: print(f"
Testing with {model}...") # Same code works for any model response = await litellm.acompletion( model=model, messages=messages, tools=tools, ) ```

This flexibility means you can:

* Test tools with different models to compare performance.
* Switch providers based on availability or cost.
* Use different models for different types of queries.

## Step 3: Handling Tool Execution

LiteLLM standardizes tool execution across providers:

```json # Check if the model made tool callsif hasattr(message, "tool_calls") and message.tool_calls: print(f"🔧 Tool calls made: {len(message.tool_calls)}") # Process each tool call for call in message.tool_calls: print(f" - Executing {call.function.name}") # Execute the tool through MCP arguments = json.loads(call.function.arguments) result = await session.call_tool( call.function.name, arguments ) # Add tool result to conversation messages.append({ "role": "tool", "content": str(result.content), "tool_call_id": call.id, }) # Get final response with tool results final_response = await litellm.acompletion( model=model, messages=messages, tools=tools, ) ```

This code demonstrates how LiteLLM:

1. Receives tool calls in a standardized format.
2. Executes them through MCP.
3. Formats results appropriately for each provider.
4. Handles the complete conversation flow.

## Understanding the Flow

Let’s visualize how LiteLLM orchestrates communication between different LLM providers and MCP tools:

![image](https://miro.medium.com/v2/resize:fit:700/1*Rx8Z11a_w60hICYkz7j6sQ.png)

This diagram reveals LiteLLM’s role as a universal translator, converting between different provider formats while maintaining a consistent interface for your application. It shows how it seamlessly allows many models to support MCP tooling.

## Real-World Scenarios

Here are some interesting things that you can do with LiteLLM.

## Scenario 1: Cost-Optimized Routing

``` # Route simple queries to cheaper modelsif is_simple_query(message): model = "gpt-4.1-mini" # Cheaperelse: model = "gpt-4.1" # More capableresponse = await litellm.acompletion( model=model, messages=messages, tools=tools) ```

## Scenario 2: Compliance-Based Routing

``` # Use local models for sensitive dataif contains_pii(message): model = "ollama/llama2" # Local modelelse: model = "claude-sonnet-4-0" # Cloud model ```

## Scenario 3: Fallback Handling

``` # LiteLLM can automatically handle fallbacksmodels = ["gpt-4.1", "claude-sonnet-4-0", "ollama/mixtral"]for model in models: try: response = await litellm.acompletion( model=model, messages=messages, tools=tools ) break # Success, exit loop except Exception as e: print(f"Failed with {model}, trying next...") continue ```

## Architectural Insights

The complete architecture shows how LiteLLM bridges multiple worlds:

![image](https://miro.medium.com/v2/resize:fit:700/0*iF2kkAs5M7NqZbIz)

This architecture provides several key benefits:

1. **Single Integration Point** : Your application only needs to know LiteLLM’s interface
2. **Provider Independence** : Switch or add providers without changing application code
3. **Unified Tool Access** : MCP tools work identically across all providers
4. **Centralized Monitoring** : Track usage and costs across all providers

## Advanced Patterns

## Pattern 1: Provider-Specific Optimizations

```json # Customize parameters per providerprovider_configs = { "gpt-4.1": {"temperature": 0.7, "max_tokens": 2000}, "claude-sonnet-4-0": {"temperature": 0.5, "max_tokens": 4000}, "ollama/mixtral": {"temperature": 0.8, "max_tokens": 1000}}model = select_best_model(query)config = provider_configs.get(model, {})response = await litellm.acompletion( model=model, messages=messages, tools=tools, **config # Provider-specific parameters) ```

## Pattern 2: Cost and Performance Tracking

```python # LiteLLM tracks costs automaticallyfrom litellm import completion_costresponse = await litellm.acompletion( model=model, messages=messages, tools=tools)cost = completion_cost(completion_response=response)print(f"This request cost: ${cost:.4f}") ```

## Pattern 3: Streaming with Tool Support

``` # Stream responses while maintaining tool supportasync for chunk in await litellm.acompletion( model=model, messages=messages, tools=tools, stream=True): if chunk.choices[0].delta.content: print(chunk.choices[0].delta.content, end="") # Handle streaming tool calls if hasattr(chunk.choices[0].delta, "tool_calls"): # Process tool calls in real-time pass ```

## Getting Started

**Clone the**[**example repository**](<https://github.com/RichardHightower/mcp_article1>):

``` git clone git@github.com:RichardHightower/mcp_article1.gitcd mcp_article1 ```

**Install LiteLLM and dependencies (follow instructions in**[**README.md**](<http://README.md>)**)** :

``` poetry add litellm python-mcp-sdk ```

**Configure your providers** :

``` # .env fileOPENAI_API_KEY=your-keyANTHROPIC_API_KEY=your-key# Add any other provider keys ```

**Run the integration** :

``` poetry run python src/litellm_integration.py ```

## Key Takeaways

The combination of LiteLLM and MCP represents the ultimate flexibility in AI tool integration:

* **True Portability** : Write once, run with any LLM provider
* **Cost Optimization** : Route to the most economical provider for each query
* **Risk Mitigation** : No vendor lock-in, easy provider switching
* **Compliance Ready** : Use appropriate models for different data sensitivities.
* **Future Proof** : New providers automatically work with existing tools

By abstracting the tool layer (MCP) and the model layer (LiteLLM), you create AI systems that adapt to changing requirements without code changes. This is enterprise-grade flexibility at its finest.

## References

* [Building Your First FastMCP Server: A Complete Guide](</@richardhightower/building-your-first-fastmcp-server-a-complete-guide-b2a176eaa631>)
* **GitHub Repository** : [MCP Article Examples](<https://github.com/RichardHightower/mcp_article1>) — Complete working code for all integrations.
* **Comprehensive MCP Guide** : [MCP: From Chaos to Harmony](</@richardhightower/mcp-from-chaos-to-harmony-building-ai-integrations-with-the-model-context-protocol-98123d374ac4>) — Deep dive into MCP architecture and server development
* **LiteLLM Articles** :
* [Multi-Provider Chat App](</@richardhightower/multi-provider-chat-app-litellm-streamlit-ollama-gemini-claude-perplexity-and-modern-llm-afd5218c7eab>) — Building with LiteLLM and Streamlit
* [Beyond Chat: RAG and Streaming](</@richardhightower/beyond-chat-enhancing-litellm-multi-provider-app-with-rag-streaming-and-aws-bedrock-65767dd34a53>) — Advanced LiteLLM patterns
* **Official Documentation** :
* [LiteLLM Docs](<https://docs.litellm.ai/>) — Complete API reference
* [MCP Specification](<https://modelcontextprotocol.io/>) — Protocol details

## Next Steps

Ready to build provider-agnostic AI tools? Here’s your roadmap:

1. Start here: [Building Your First FastMCP Server: A Complete Guide](</@richardhightower/building-your-first-fastmcp-server-a-complete-guide-b2a176eaa631>)
2. Explore the example code to understand the integration patterns.
3. Experiment with different providers to find the best fit for your use case.
4. Implement cost tracking and optimization strategies.
5. Build fallback chains for mission-critical applications.

The future of AI isn’t tied to a single provider — it’s about choosing the right tool for each job. With LiteLLM and MCP, you can make that choice without rewriting your code.

_Want to explore more integration patterns? Check out our articles on_[ _OpenAI + MCP_](</@richardhightower/mcp-from-chaos-to-harmony-building-ai-integrations-with-the-model-context-protocol-98123d374ac4#openai-integration>) _,_[_DSPy’s self-optimizing approach_](</@richardhightower/mcp-from-chaos-to-harmony-building-ai-integrations-with-the-model-context-protocol-98123d374ac4#dspy-integration>) _, and_[ _LangChain workflows_](</@richardhightower/mcp-from-chaos-to-harmony-building-ai-integrations-with-the-model-context-protocol-98123d374ac4#langchain-integration>) _. For the complete guide to building MCP servers, see our_[ _comprehensive guide_](</@richardhightower/mcp-from-chaos-to-harmony-building-ai-integrations-with-the-model-context-protocol-98123d374ac4>) _._

If you like this article, follow Rick on [LinkedIn](<https://www.linkedin.com/in/rickhigh/>) or [Medium](</@richardhightower>).

## About the Author

Rick Hightower brings extensive enterprise experience as a former executive and distinguished engineer at a Fortune 100 company, where he specialized in Machine Learning and AI solutions to deliver an intelligent customer experience. His expertise spans the theoretical foundations and practical applications of AI technologies.

As a [TensorFlow-certified professional a](<https://file.notion.so/f/f/65913469-18c4-46a6-9302-ae4e3f1c94aa/e76c7baa-e353-4263-ab62-30d4c7a7e7de/Coursera_U4ETPRWRADE6.pdf?table=block&id=155d6bbd-bbea-80fc-89de-e1b0e96044f4&spaceId=65913469-18c4-46a6-9302-ae4e3f1c94aa&expirationTimestamp=1747958400000&signature=QPctHaVpkVhUB7hyc9U9WEz_q8g6r4zDXZWnGUWT7SU&downloadName=Coursera+U4ETPRWRADE6.pdf>)nd graduate of [Stanford University’s comprehensive Machine Learning Specialization](<https://www.notion.so/About-133d6bbdbbea813aa509e9585e6867fe?pvs=21>), Rick combines academic rigor with real-world implementation experience. His training includes mastery of supervised learning techniques, neural networks, and advanced AI concepts, which he has successfully applied to enterprise-scale solutions.

With a deep understanding of AI implementation's business and technical aspects, Rick bridges the gap between theoretical machine learning concepts and practical business applications, helping organizations leverage AI to create tangible value.

If you like this article, follow Rick on [LinkedIn](<https://www.linkedin.com/in/rickhigh/>) or [Medium](</@richardhightower>).

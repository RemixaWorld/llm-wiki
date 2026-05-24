---
domain: blog.gopenai.com
fetch_date: '2026-05-18T12:52:01.633943'
status: ok
url: https://blog.gopenai.com/build-react-agents-using-slms-from-scratch-a0336e99ba7c
---

# Build ReAct Agents using SLMs from Scratch

[ ![Akshay Ballal](https://miro.medium.com/v2/resize:fill:64:64/1*9OyTvE-dUyJn3t_K5fsbmQ.png) ](<https://medium.com/@akshayballal95?source=post_page---byline--a0336e99ba7c--------------------------------------->)

[Akshay Ballal](<https://medium.com/@akshayballal95?source=post_page---byline--a0336e99ba7c--------------------------------------->)

6 min read

·

Sep 29, 2024

\--

Listen

Share

More

Press enter or click to view image in full size

Build a function-calling agent using a custom Unsloth model with a LoRA adapter, switching between reasoning and function execution, following ReAct-style reasoning.

In this post, I will demonstrate how to create a function-calling agent using **Small Language Models (SLMs)**. Leveraging SLMs offers a range of benefits, especially when paired with tools like LoRA adapters for efficient fine-tuning and execution. While Large Language Models (LLMs) are powerful, they can be resource-intensive and slow. On the other hand, SLMs are more lightweight, making them ideal for environments with limited hardware resources or specific use cases where lower latency is critical.

By using **SLMs** with **LoRA adapters** , we can separate reasoning and function execution tasks to optimize performance. For instance, the model can execute complex function calls using the adapter and handle reasoning or thinking tasks without it, thus conserving memory and improving speed. This flexibility is perfect for building applications like function-calling agents without needing the infrastructure required for larger models.

Moreover, SLMs can be easily scaled to run on devices with limited computational power, making them ideal for production environments where cost and efficiency are prioritized. In this example, we’ll use a custom model trained on the **Salesforce/xlam-function-calling-60k** dataset via Unsloth, demonstrating how you can utilize SLMs to create high-performance, low-resource AI applications.

Additionally, the approach discussed here can be scaled to more powerful models, such as **LLaMA 3.1–8B**, which have in-built function-calling capabilities, offering a smooth transition when larger models are necessary.

## 1\. Initiate the Model and Tokenizer with Unsloth

We’ll first set up the model and tokenizer using **Unsloth**. Here, we define a max sequence length of 2048, though this can be adjusted. We also enable **4-bit quantization** to reduce memory usage, ideal for running models on lower-memory hardware.

```python from unsloth import FastLanguageModelmax_seq_length = 2048 # Choose any! We auto support RoPE Scaling internally!dtype = None # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+load_in_4bit = True # Use 4bit quantization to reduce memory usage. Can be False.model, tokenizer = FastLanguageModel.from_pretrained( model_name = "akshayballal/phi-3.5-mini-xlam-function-calling", max_seq_length = max_seq_length, dtype = dtype, load_in_4bit = load_in_4bit,) ```

## 2\. Implement Stopping Criteria for Controlled Generation

To ensure that the agent pauses execution after function calls, we define a **stopping criteria**. This will halt the generation when the model outputs the keyword “PAUSE,” allowing the agent to fetch the result of the function call.

```python from transformers import StoppingCriteria, StoppingCriteriaListimport torchclass KeywordsStoppingCriteria(StoppingCriteria): def __init__(self, keywords_ids:list): self.keywords = keywords_ids def __call__(self, input_ids: torch.LongTensor, _: torch.FloatTensor, **kwargs) -> bool: if input_ids[0][-1] in self.keywords: return True return Falsestop_ids = [17171]stop_criteria = KeywordsStoppingCriteria(stop_ids) ```

## 3\. Define the Tools for Function Calling

Next, we define the functions the agent will use during execution. These Python functions will act as “tools” that the agent can call. The return type must be clear, and the function should include a descriptive docstring, as the agent will rely on this to choose the correct tool.

```python def add_numbers(a: int, b: int) -> int: """ This function takes two integers and returns their sum.Parameters: a (int): The first integer to add. b (int): The second integer to add. """ return a + b def square_number(a: int) -> int: """ This function takes an integer and returns its square. Parameters: a (int): The integer to be squared. """ return a * adef square_root_number(a: int) -> int: """ This function takes an integer and returns its square root. Parameters: a (int): The integer to calculate the square root of. """ return a ** 0.5 ```

## 4\. Generate Tool Descriptions for the Agent

These function descriptions will be structured into a list of dictionaries. The agent will use these to understand the available tools and their parameters.

```json tool_descriptions = []for tool in tools: spec = { "name": tool.__name__, "description": tool.__doc__.strip(), "parameters": [ { "name": param, "type": arg.__name__ if hasattr(arg, '__name__') else str(arg), } for param, arg in tool.__annotations__.items() if param != 'return' ] } tool_descriptions.append(spec)tool_descriptions ```

This is how the output looks like

``` [{'name': 'add_numbers', 'description': 'This function takes two integers and returns their sum.\\
\\
Parameters:\\
a (int): The first integer to add.\\
b (int): The second integer to add.', 'parameters': [{'name': 'a', 'type': 'int'}, {'name': 'b', 'type': 'int'}]}, {'name': 'square_number', 'description': 'This function takes an integer and returns its square.\\
\\
Parameters:\\
a (int): The integer to be squared.', 'parameters': [{'name': 'a', 'type': 'int'}]}, {'name': 'square_root_number', 'description': 'This function takes an integer and returns its square root.\\
\\
Parameters:\\
a (int): The integer to calculate the square root of.', 'parameters': [{'name': 'a', 'type': 'int'}]}] ```

## 5\. Create the Agent Class

We then create the agent class that takes the system prompt, the function calling prompt, the tools and the messages as input and returns the response from the agent.

* `__call__` is the function that is called when the agent is called with a message. It adds the message to the messages list and returns the response from the agent.
* `execute` is the function that is called to generate the response from the agent. It uses the model to generate the response.
* `function_call` is the function that is called to generate the response from the agent. It uses the function calling model to generate the response.

```python import astclass Agent: def __init__( self, system: str = "", function_calling_prompt: str = "", tools=[] ) -> None: self.system = system self.tools = tools self.function_calling_prompt = function_calling_prompt self.messages: list = [] if self.system: self.messages.append({"role": "system", "content": system}) def __call__(self, message=""): if message: self.messages.append({"role": "user", "content": message}) result = self.execute() self.messages.append({"role": "assistant", "content": result}) return result def execute(self): with model.disable_adapter(): # disable the adapter for thinking and reasoning inputs = tokenizer.apply_chat_template( self.messages, tokenize=True, add_generation_prompt=True, return_tensors="pt", ) output = model.generate( input_ids=inputs, max_new_tokens=128, stopping_criteria=StoppingCriteriaList([stop_criteria]), ) return tokenizer.decode( output[0][inputs.shape[-1] :], skip_special_tokens=True ) def function_call(self, message): inputs = tokenizer.apply_chat_template( [ { "role": "user", "content": self.function_calling_prompt.format( tool_descriptions=tool_descriptions, query=message ), } ], tokenize=True, add_generation_prompt=True, return_tensors="pt", ) output = model.generate(input_ids=inputs, max_new_tokens=128, temperature=0.0) prompt_length = inputs.shape[-1] answer = ast.literal_eval( tokenizer.decode(output[0][prompt_length:], skip_special_tokens=True) )[ 0 ] # get the output of the function call model as a dictionary print(answer) tool_output = self.run_tool(answer["name"], **answer["arguments"]) return tool_output def run_tool(self, name, *args, **kwargs): for tool in self.tools: if tool.__name__ == name: return tool(*args, **kwargs) ```

## 6\. Define System and Function-Calling Prompts

We now define two key prompts:

* **System Prompt** : The core logic for the agent's reasoning and tool use, following the **ReAct** pattern.
* **Function-Calling Prompt:** This enables function calling by passing the relevant tool descriptions and queries.

``` system_prompt = f"""You run in a loop of Thought, Action, PAUSE, Observation.At the end of the loop you output an AnswerUse Thought to describe your thoughts about the question you have been asked.Use Action to run one of the actions available to you - then return PAUSE.Observation will be the result of running those actions. Stop when you have the Answer. Your available actions are:{tools}Example session:Question: What is the mass of Earth times 2?Thought: I need to find the mass of EarthAction: get_planet_mass: EarthPAUSE Observation: 5.972e24Thought: I need to multiply this by 2Action: calculate: 5.972e24 * 2PAUSEObservation: 1,1944×10e25If you have the answer, output it as the Answer.Answer: \\\\\\\\{{1,1944×10e25\\\\\\\\}}.PAUSENow it's your turn:""".strip()function_calling_prompt = """You are a helpful assistant. Below are the tools that you have access to. \\
\\
### Tools: \\
{tool_descriptions} \\
\\
### Query: \\
{query} \\
""" ```

## 7\. Implement the ReAct Loop

Finally, we define the loop that enables the agent to interact with the user, execute the necessary function calls, and return the correct answers.

```python import redef loop_agent(agent: Agent, question, max_iterations=5): next_prompt = question i = 0 while i < max_iterations: result = agent(next_prompt) print(result) if "Answer:" in result: return result action = re.findall(r"Action: (.*)", result) if action: tool_output= agent.function_call(action) next_prompt = f"Observation: {tool_output}" print(next_prompt) else: next_prompt = "Observation: tool not found" i += 1 return resultagent = Agent( system=system_prompt, function_calling_prompt=function_calling_prompt, tools=tools)loop_agent(agent, "what is the square root of the difference between 32^2 and 54"); ```

Check out the complete notebook on Colab here:

[small-function-calling-agents.ipynb — Colab (google.com)](<https://colab.research.google.com/drive/1rpJZ-hSGG0E83xUNE5oAU2R0UmANn7Tb>)

## Conclusion

By following this step-by-step guide, you can create a function-calling agent using a custom model trained with **Unsloth** and **LoRA adapters**. This approach ensures efficient memory use while maintaining robust reasoning and function execution capabilities.

Explore further by extending this method to larger models or customizing the functions available to the agent.

``` Want to Connect?My WebsiteGitHubLinkedInTwitter ```

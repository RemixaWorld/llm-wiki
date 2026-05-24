---
domain: github.com
fetch_date: '2026-05-18T12:34:50.089784'
status: ok
url: https://github.com/MeetKai/functionary
---

Functionary is a language model that can interpret and execute functions/plugins.

The model determines when to execute functions, whether in parallel or serially, and can understand their outputs. It only triggers functions as needed. Function definitions are given as JSON Schema Objects, similar to OpenAI GPT function calls.

Documentation and more examples: functionary.meetkai.com

## Changelog: (click to expand)

- [2024/12/24] We release meetkai/functionary-v4r-small-preview - our first version of Functionary that can generate the reasoning steps first before using the tools
- [2024/10/21] New server powered by SGLang!
- [2024/08/21] We release meetkai/functionary-small-v3.2 and meetkai/functionary-medium-v3.2
- [2024/08/11] Our newest model (meetkai/functionary-medium-v3.1) is ranked 2nd in Berkeley Function-Calling Leaderboard
- [2024/08/08] We release 128k-context length 70B-model: meetkai/functionary-medium-v3.1 that are based on meta-llama/Meta-Llama-3.1-70B-Instruct
- [2024/08/07] We release 2 128k-context length models that are based on meta-llama/Meta-Llama-3.1-8B-Instruct:
- meetkai/functionary-small-v3.1:
**using Meta's original prompt template**as described in: User-defined Custom tool calling - meetkai/functionary-small-v3.2: using
**our own prompt template**. This model is**better**than meetkai/functionary-small-v3.1

- meetkai/functionary-small-v3.1:
- [2024/06/14] We release meetkai/functionary-medium-v3.0 (based on meta-llama/Meta-Llama-3-70B-Instruct) with better capability for function calling
- [2024/05/17] We release meetkai/functionary-small-v2.5 with better capability for function calling and code interpreter compared with functionary-small-v2.4
- [2024/05/06] Streaming support for functionary v2 to v2.4 models is released in llama-cpp-python!
- [2024/05/03] Added support for serverless vLLM deployment on Modal.com
- [2024/04/02] We release meetkai/functionary-small-v2.4 and meetkai/functionary-medium-v2.4! The first functionary models with code-interpreter ability (by passing in
`{type: "code_interpreter"}`

in tools)!

Functionary can be deployed using either our vLLM or SGLang servers. Choose either one depending on your preferences.

**vLLM**

`pip install -e .[vllm]`

**SGLang**

`pip install -e .[sglang] --find-links https://flashinfer.ai/whl/cu124/torch2.5/flashinfer-python`

**vLLM**

`python3 server_vllm.py --model "meetkai/functionary-v4r-small-preview" --host 0.0.0.0 --port 8000 --max-model-len 8192`

**SGLang**

`python3 server_sglang.py --model-path "meetkai/functionary-v4r-small-preview" --host 0.0.0.0 --port 8000 --context-length 8192`

Our medium models require: 4xA6000 or 2xA100 80GB to run, need to use: `tensor-parallel-size`

or `tp`

(SGLang)

**vLLM**

```
# vllm requires to run this first: https://github.com/vllm-project/vllm/issues/6152
export VLLM_WORKER_MULTIPROC_METHOD=spawn
python server_vllm.py --model "meetkai/functionary-medium-v3.1" --host 0.0.0.0 --port 8000 --max-model-len 8192 --tensor-parallel-size 2
```

**SGLang**

`python server_sglang.py --model-path "meetkai/functionary-medium-v3.1" --host 0.0.0.0 --port 8000 --context-length 8192 --tp 2`

Similar to LoRA in vLLM, our server supports serving LoRA adapters both at startup and dynamically.

To serve a LoRA adapter at startup, run the server with the `--lora-modules`

argument:

`python server_vllm.py --model {BASE_MODEL} --enable-lora --lora-modules {name}={path} {name}={path} --host 0.0.0.0 --port 8000`

To serve a LoRA adapter dynamically, use the `/v1/load_lora_adapter`

endpoint:

```
python server_vllm.py --model {BASE_MODEL} --enable-lora --host 0.0.0.0 --port 8000
# Load a LoRA adapter dynamically
curl -X POST http://localhost:8000/v1/load_lora_adapter \
-H "Content-Type: application/json" \
-d '{
"lora_name": "my_lora",
"lora_path": "/path/to/my_lora_adapter"
}'
# Example chat request to lora adapter
curl -X POST http://localhost:8000/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{
"model": "my_lora",
"messages": [...],
"tools": [...],
"tool_choice": "auto"
}'
# Unload a LoRA adapter dynamically
curl -X POST http://localhost:8000/v1/unload_lora_adapter \
-H "Content-Type: application/json" \
-d '{
"lora_name": "my_lora"
}'
```

We also provide a service that performs inference on Functionary models using Text-Generation-Inference (TGI). Follow these steps to get started:

-
Install Docker following their installation instructions.

-
Install the Docker SDK for Python


`pip install docker`

- Start up the Functionary TGI server

At start-up, the Functionary TGI server tries to connect to an existing TGI endpoint. In this case, you can run the following:

`python3 server_tgi.py --model <REMOTE_MODEL_ID_OR_LOCAL_MODEL_PATH> --endpoint <TGI_SERVICE_ENDPOINT>`

If the TGI endpoint does not exist, the Functionary TGI server will start a new TGI endpoint container with the address provided in the `endpoint`

CLI argument via the installed Docker Python SDK. Run the following commands for remote and local models respectively:

`python3 server_tgi.py --model <REMOTE_MODEL_ID> --remote_model_save_folder <PATH_TO_SAVE_AND_CACHE_REMOTE_MODEL> --endpoint <TGI_SERVICE_ENDPOINT>`

`python3 server_tgi.py --model <LOCAL_MODEL_PATH> --endpoint <TGI_SERVICE_ENDPOINT>`

- Make either OpenAI-compatible or raw HTTP requests to the Functionary TGI server.

**Docker**

If you're having trouble with dependencies, and you have nvidia-container-toolkit, you can start your environment like this:

```
cd <ROOT>
# vLLM
sudo docker build -t functionary-vllm -f dockerfiles/Dockerfile.vllm .
sudo docker run --runtime nvidia --gpus all -p 8000:8000 functionary-vllm
# SGLang
sudo docker build -t functionary-sglang -f dockerfiles/Dockerfile.sgl .
sudo docker run --runtime nvidia --gpus all -p 8000:8000 functionary-sglang
```

```
from openai import OpenAI
client = OpenAI(base_url="http://localhost:8000/v1", api_key="functionary")
client.chat.completions.create(
model="meetkai/functionary-v4r-small-preview",
messages=[{"role": "user",
"content": "What is the weather for Istanbul?"}
],
tools=[{
"type": "function",
"function": {
"name": "get_current_weather",
"description": "Get the current weather",
"parameters": {
"type": "object",
"properties": {
"location": {
"type": "string",
"description": "The city and state, e.g. San Francisco, CA"
}
},
"required": ["location"]
}
}
}],
tool_choice="auto"
)
```

## Details (click to expand)

```
import requests
data = {
'model': 'meetkai/functionary-v4r-small-preview', # model name here is the value of argument "--model" in deploying: server_vllm.py or server.py
'messages': [
{
"role": "user",
"content": "What is the weather for Istanbul?"
}
],
'tools':[ # For functionary-7b-v2 we use "tools"; for functionary-7b-v1.4 we use "functions" = [{"name": "get_current_weather", "description":..., "parameters": ....}]
{
"type": "function",
"function": {
"name": "get_current_weather",
"description": "Get the current weather",
"parameters": {
"type": "object",
"properties": {
"location": {
"type": "string",
"description": "The city and state, e.g. San Francisco, CA"
}
},
"required": ["location"]
}
}
}
]
}
response = requests.post("http://127.0.0.1:8000/v1/chat/completions", json=data, headers={
"Content-Type": "application/json",
"Authorization": "Bearer xxxx"
})
# Print the response text
print(response.text)
```

| Model | Description | VRAM FP16 |
|---|---|---|
| meetkai/functionary-v4r-small-preview | 128k context, code interpreter, using our own prompt template |
24GB |
| functionary-medium-v3.2 | 128k context, code interpreter, using our own prompt template |
160GB |
| functionary-small-v3.2 / GGUF | 128k context, code interpreter, using our own prompt template |
24GB |
| functionary-medium-v3.1 / GGUF | 128k context, code interpreter, using original Meta's prompt template |
160GB |
| functionary-small-v3.1 / GGUF | 128k context, code interpreter, using original Meta's prompt template |
24GB |
| functionary-medium-v3.0 / GGUF | 8k context, based on meta-llama/Meta-Llama-3-70B-Instruct | 160GB |
| functionary-small-v2.5 / GGUF | 8k context, code interpreter | 24GB |
| functionary-small-v2.4 / GGUF | 8k context, code interpreter | 24GB |
| functionary-medium-v2.4 / GGUF | 8k context, code interpreter, better accuracy | 90GB |
| functionary-small-v2.2 / GGUF | 8k context | 24GB |
| functionary-medium-v2.2 / GGUF | 8k context | 90GB |
| functionary-7b-v2.1 / GGUF | 8k context | 24GB |
| functionary-7b-v2 / GGUF | Parallel function call support. | 24GB |
| functionary-7b-v1.4 / GGUF | 4k context, better accuracy (deprecated) | 24GB |
| functionary-7b-v1.1 | 4k context (deprecated) | 24GB |
| functionary-7b-v0.1 | 2k context (deprecated) Not recommended, use 2.1 onwards | 24GB |

- v1 models are compatible with both OpenAI-python v0 and v1.
- v2 models are designed for compatibility with OpenAI-python v1.

The difference between OpenAI-python v0 and v1 you may refer to the official documentation here

| Feature/Project | Functionary | NexusRaven | Gorilla | Glaive | GPT-4-1106-preview |
|---|---|---|---|---|---|
| Single Function Call | ✅ | ✅ | ✅ | ✅ | ✅ |
| Parallel Function Calls | ✅ | ✅ | ✅ | ❌ | ✅ |
| Following Up on Missing Function Arguments | ✅ | ❌ | ❌ | ❌ | ✅ |
| Multi-turn | ✅ | ❌ | ❌ | ✅ | ✅ |
| Generate Model Responses Grounded in Tools Execution Results | ✅ | ❌ | ❌ | ❌ | ✅ |
| Chit-Chat | ✅ | ❌ | ✅ | ✅ | ✅ |
| Code Interpreter | ✅ | ❌ | ❌ | ❌ | ✅ |

**You can find more details of the features in here**

Example for inference using LLama-cpp-python can be found in: llama_cpp_inference.py.

Besides, functionary was also integrated into LLama-cpp-python, however the integration might not be **quickly updated**, so if there is something wrong or weird in the result, please use: llama_cpp_inference.py instead. Currently, v2.5 hasn't been integrated, so if you are using **functionary-small-v2.5-GGUF**, please use: llama_cpp_inference.py

Make sure that the latest version of llama-cpp-python is successully installed in your system. Functionary v2 is fully integrated into llama-cpp-python. You can perform inference using Functionary's GGUF models either via normal chat completion or through llama-cpp-python's OpenAI-compatible server which behaves similarly to ours.

The following is the sample code using normal chat completion:

```
from llama_cpp import Llama
from llama_cpp.llama_tokenizer import LlamaHFTokenizer
# We should use HF AutoTokenizer instead of llama.cpp's tokenizer because we found that Llama.cpp's tokenizer doesn't give the same result as that from Huggingface. The reason might be in the training, we added new tokens to the tokenizer and Llama.cpp doesn't handle this successfully
llm = Llama.from_pretrained(
repo_id="meetkai/functionary-small-v2.4-GGUF",
filename="functionary-small-v2.4.Q4_0.gguf",
chat_format="functionary-v2",
tokenizer=LlamaHFTokenizer.from_pretrained("meetkai/functionary-small-v2.4-GGUF"),
n_gpu_layers=-1
)
messages = [
{"role": "user", "content": "what's the weather like in Hanoi?"}
]
tools = [ # For functionary-7b-v2 we use "tools"; for functionary-7b-v1.4 we use "functions" = [{"name": "get_current_weather", "description":..., "parameters": ....}]
{
"type": "function",
"function": {
"name": "get_current_weather",
"description": "Get the current weather",
"parameters": {
"type": "object",
"properties": {
"location": {
"type": "string",
"description": "The city and state, e.g., San Francisco, CA"
}
},
"required": ["location"]
}
}
}
]
result = llm.create_chat_completion(
messages = messages,
tools=tools,
tool_choice="auto",
)
print(result["choices"][0]["message"])
```

The output would be:

`{'role': 'assistant', 'content': None, 'tool_calls': [{'type': 'function', 'function': {'name': 'get_current_weather', 'arguments': '{\n "location": "Hanoi"\n}'}}]}`

For more details, please refer to the Function Calling section in llama-cpp-python. To use our Functionary GGUF models using llama-cpp-python's OpenAI-compatible server, please refer to here for more details and documentation.

**Note:**

- For Functionary in llama-cpp-python, the default system messages are added automatically during the API call. Therefore, there is no need to provide the default system messages in
`messages`

. - Streaming feature for Functionary models in both the normal chat completion and in llama-cpp-python's OpenAI-compatible server is officially supported from v0.2.70 onwards.

To call the real python function, get the result and extract the result to respond, you can use chatlab. The following example uses chatlab==0.16.0:

Please note that Chatlab currently doesn't support Parallel Function calls. This sample code is compatible only with Functionary Version 1.4 and may not work correctly with Functionary Version 2.0.

```
from chatlab import Conversation
import openai
import os
openai.api_key = "functionary" # We just need to set this something other than None
os.environ['OPENAI_API_KEY'] = "functionary" # chatlab requires us to set this too
openai.api_base = "http://localhost:8000/v1"
# now provide the function with description
def get_car_price(car_name: str):
"""this function is used to get the price of the car given the name
:param car_name: name of the car to get the price
"""
car_price = {
"tang": {"price": "$20000"},
"song": {"price": "$25000"}
}
for key in car_price:
if key in car_name.lower():
return {"price": car_price[key]}
return {"price": "unknown"}
chat = Conversation(model="meetkai/functionary-7b-v2")
chat.register(get_car_price) # register this function
chat.submit("what is the price of the car named Tang?") # submit user prompt
# print the flow
for message in chat.messages:
role = message["role"].upper()
if "function_call" in message:
func_name = message["function_call"]["name"]
func_param = message["function_call"]["arguments"]
print(f"{role}: call function: {func_name}, arguments:{func_param}")
else:
content = message["content"]
print(f"{role}: {content}")
```

The output will look like this:

```
USER: what is the price of the car named Tang?
ASSISTANT: call function: get_car_price, arguments:{
"car_name": "Tang"
}
FUNCTION: {'price': {'price': '$20000'}}
ASSISTANT: The price of the car named Tang is $20,000.
```


Serverless deployment of Functionary models is supported via the *modal_server_vllm.py* script. After signing up and installing Modal, follow these steps to deploy our vLLM server on Modal:

**Create dev environment**

`modal environment create dev`

If you have a dev environment created already, there is no need to create another one. Just configure to it in the next step.

**Configure dev environment**

`modal config set-environment dev`

**Serve Functionary Model**

`modal serve modal_server_vllm`

**Deploy Runner**

`modal deploy modal_server_vllm`

Here are a few examples of how you can use this function calling system:

The function `plan_trip(destination: string, duration: int, interests: list)`

can take user input such as "I want to plan a 7-day trip to Paris with a focus on art and culture" and generate an itinerary accordingly.

## Details (click to expand)

```
client.chat.completions.create((
model="meetkai/functionary-7b-v2",
messages=[
{"role": "user", "content": 'I want to plan a 7-day trip to Paris with a focus on art and culture'},
],
tools=[
{
"type": "function",
"function": {
"name": "plan_trip",
"description": "Plan a trip based on user's interests",
"parameters": {
"type": "object",
"properties": {
"destination": {
"type": "string",
"description": "The destination of the trip",
},
"duration": {
"type": "integer",
"description": "The duration of the trip in days",
},
"interests": {
"type": "array",
"items": {"type": "string"},
"description": "The interests based on which the trip will be planned",
},
},
"required": ["destination", "duration", "interests"],
}
}
}
]
)
```

Response will have:

`{"role": "assistant", "content": null, "tool_calls": [{"type": "function", "function": {"name": "plan_trip", "arguments": '{\n "destination": "Paris",\n "duration": 7,\n "interests": ["art", "culture"]\n}'}}]}`

Then you need to call `plan_trip`

function with provided arguments.
If you would like a commentary from the model, then you'll call the model again with the response from the function, the model will write necessary commentary.

A function like estimate_property_value(property_details: dict) could allow users to input details about a property (such as location, size, number of rooms, etc.) and receive an estimated market value.

## Details (click to expand)

```
client.chat.completions.create(
model="meetkai/functionary-7b-v2",
messages=[
{
"role": "user",
"content": 'What is the estimated value of a 3-bedroom house in San Francisco with 2000 sq ft area?'
},
{
"role": "assistant",
"content": None,
"tool_calls": [
{
"type": "function",
"function": {
"name": "estimate_property_value",
"arguments": '{\n "property_details": {"location": "San Francisco", "size": 2000, "rooms": 3}\n}'
}
}
]
}
],
tools=[
{
"type": "function",
"function": {
"name": "estimate_property_value",
"description": "Estimate the market value of a property",
"parameters": {
"type": "object",
"properties": {
"property_details": {
"type": "object",
"properties": {
"location": {
"type": "string",
"description": "The location of the property"
},
"size": {
"type": "integer",
"description": "The size of the property in square feet"
},
"rooms": {
"type": "integer",
"description": "The number of rooms in the property"
}
},
"required": ["location", "size", "rooms"]
}
},
"required": ["property_details"]
}
}
}
],
tool_choice="auto"
)
```

Response will have:

`{"role": "assistant", "content": null, "tool_calls": [{"type": "function", "function": {"name": "plan_trip", "arguments": '{\n "destination": "Paris",\n "duration": 7,\n "interests": ["art", "culture"]\n}'}}]}`

Then you need to call `plan_trip`

function with provided arguments.
If you would like a commentary from the model, then you'll call the model again with the response from the function, the model will write necessary commentary.

A function `parse_customer_complaint(complaint: {issue: string, frequency: string, duration: string})`

could help in extracting structured information from a complex, narrative customer complaint, identifying the core issue and potential solutions. The `complaint`

object could include properties such as `issue`

(the main problem), `frequency`

(how often the issue occurs), and `duration`

(how long the issue has been occurring).

## Details (click to expand)

```
client.chat.completions.create(
model="meetkai/functionary-7b-v2",
messages=[
{"role": "user", "content": 'My internet has been disconnecting frequently for the past week'},
],
tools=[
{
"type": "function",
"function": {
"name": "parse_customer_complaint",
"description": "Parse a customer complaint and identify the core issue",
"parameters": {
"type": "object",
"properties": {
"complaint": {
"type": "object",
"properties": {
"issue": {
"type": "string",
"description": "The main problem",
},
"frequency": {
"type": "string",
"description": "How often the issue occurs",
},
"duration": {
"type": "string",
"description": "How long the issue has been occurring",
},
},
"required": ["issue", "frequency", "duration"],
},
},
"required": ["complaint"],
}
}
}
],
tool_choice="auto"
)
```

Response will have:

`{"role": "assistant", "content": null, "tool_calls": [{"type": "function", "function": {"name": "parse_customer_complaint", "arguments": '{\n "complaint": {"issue": "internet disconnecting", "frequency": "frequently", "duration": "past week"}\n}'}}]}`

Then you need to call parse_customer_complaint function with provided arguments. If you would like a commentary from the model, then you'll call the model again with the response from the function, the model will write necessary commentary.

We convert function definitions to a similar text to TypeScript definitions. Then we inject these definitions as system prompts. After that, we inject the default system prompt. Then we start the conversation messages.

The prompt example can be found here: V1 (v1.4), V2 (v2, v2.1, v2.2, v2.4) and V2.llama3 (v2.5)

We don't change the logit probabilities to conform to a certain schema, but the model itself knows how to conform. This allows us to use existing tools and caching systems with ease.

We are ranked 2nd in the Berkeley Function-Calling Leaderboard (Last Updated: 2024-08-11)

| Model Name | Function Calling Accuracy (Name & Arguments) |
|---|---|
| meetkai/functionary-medium-v3.1 | 88.88% |
| GPT-4-1106-Preview (Prompt) | 88.53% |
| meetkai/functionary-small-v3.2 | 82.82% |
| meetkai/functionary-small-v3.1 | 82.53% |
| FireFunction-v2 (FC) | 78.82.47% |

We also evaluate our models on ToolSandbox, this benchmark is much more difficult than **Berkeley Function-Calling Leaderboard**. This benchmark includes stateful tool execution, implicit state dependencies between tools, a built-in user simulator supporting on-policy conversational evaluation and a dynamic evaluation strategy for intermediate and final milestones over an arbitrary trajectory. The authors of this benchmark showed that there is a huge performance gap between open source models and proprietary models.

From our evaluation result, our models are comparable to best proprietary models and much better than other open source models.

| Model Name | Average similarity score |
|---|---|
| GPT-4o-2024-05-13 | 73 |
| Claude-3-Opus-20240229 | 69.2 |
Functionary-medium-v3.1 |
68.87 |
| GPT-3.5-Turbo-0125 | 65.6 |
| GPT-4-0125-Preview | 64.3 |
| Claude-3-Sonnet-20240229 | 63.8 |
Functionary-small-v3.1 |
63.13 |
| Gemini-1.5-Pro-001 | 60.4 |
Functionary-small-v3.2 |
58.56 |
| Claude-3-Haiku-20240307 | 54.9 |
| Gemini-1.0-Pro | 38.1 |
| Hermes-2-Pro-Mistral-7B | 31.4 |
| Mistral-7B-Instruct-v0.3 | 29.8 |
| C4AI-Command-R-v01 | 26.2 |
| Gorilla-Openfunctions-v2 | 25.6 |
| C4AI-Command R+ | 24.7 |

Evaluation function call prediction in SGD dataset. The accuracy metric measures the overall correctness of predicted function calls, including function name prediction and arguments extraction.

| Dataset | Model Name | Function Calling Accuracy (Name & Arguments) |
|---|---|---|
| SGD | meetkai/functionary-medium-v3.1 | 88.11% |
| SGD | gpt-4o-2024-05-13 | 82.75% |
| SGD | gemini-1.5-flash | 79.64% |
| SGD | c4ai-command-r-plus | 45.66% |

See training README

- OpenAPI specification based plugin support.
- Fast inference server
- vLLM
- text-generation-inference
- Streaming Support
- function_call parameter to server

- Parallel function calling support
- Python function calling support (Automatic detection of type annotations and calling them automatically)
- Real world usage examples, such as creating agents.
- Train Mixtral based model
- Code interpreter support
**Please consider opening a PR for future requests**

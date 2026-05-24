---
domain: levelup.gitconnected.com
fetch_date: '2026-05-18T12:46:22.747734'
status: ok
url: https://levelup.gitconnected.com/how-to-add-an-image-creator-agent-to-the-multi-agent-application-faedd684995b
---

# How to Add an Image Creator Agent to the Multi-agent Application

## A Quick Tutorial of Building a Visualized AutoGen App with both GPT-4o and Dalle-3 Agents

[ ![Yeyu Huang](https://miro.medium.com/v2/resize:fill:64:64/1*9GJQ8Fr2_9qFSaHWeQtp8w@2x.jpeg) ](<https://medium.com/@wenbohuang0307?source=post_page---byline--faedd684995b--------------------------------------->)

[Yeyu Huang](<https://medium.com/@wenbohuang0307?source=post_page---byline--faedd684995b--------------------------------------->)

9 min read

·

Jul 28, 2024

\--

Listen

Share

More

Press enter or click to view image in full size

Image by author

If you’ve ever been amazed by what AI agents can do, you’ve probably wondered how they work. Building an AI agent, or even a group of them, will significantly benefit your LLM application, from breaking down a big job into smaller tasks and planning each step logically to using powerful AI expertise. These include retrieval augmented generation (RAG), code interpreter and execution, function calling, structured data output, and utilizing different tools and APIs. With today’s advanced frameworks like AutoGen and CrewAI, plus prompting strategies, groups of AI agents can be set up to tackle complex problems automatically and boost business and life efficiency like never before.

We now see AI image generators like Stable Diffusion and Midjourney creating amazing artwork. OpenAI’s Dalle-3, a huge upgrade from Dalle-2, integrates into ChatGPT and the OpenAI API package. This makes it one of the most exciting AI art models out there. Given Dalle-3’s capabilities, connecting our agents with this powerful model is crucial to see whether our AI application can solve artwork creation tasks.

## Why need a Dalle-3 agent?

There are various practical uses of a Dalle-3 agent in your automated task workflow.

For example, when you need to create marketing copywriting, it normally requires agents like data researchers, copywriters, critics, and output wrappers to fit the final output text into a structured file like HTML or Word. The marketing material should also have some relevant illustrator to make it more attractive and professional, and that’s the responsibility of the Dalle-3 agent who follows the agents’ speeches to catch the text content, convert the key idea to prompt text and generate the images to the output package.

Here is the diagram of such a group chat workflow:

Press enter or click to view image in full size

Additionally, the copywriter, prompt agent, and Dalle-3 agent can iterate the sub-task several times by user directions to ensure each paragraph can be supported by a relevant image. That’s the advanced usage of a custom image agent compared to the standalone ChatGPT playground.

## The Design of this Demo

To focus on implementing the Image agent in the multi-agent application, I will show you a simple demo development in the AutoGen framework that includes a prompt agent and a Dalle-3 agent. The two agents play a key role in any artwork generation task, which works together to create and iterate the user's desired image.

Like always, I will select one easy-to-use UI framework to handle the visualization; in this demo, the Panel will be used.

### Here are the screenshots:

1. I asked for a logo for “YeyuLab” in Silicon Valley style.

Press enter or click to view image in full size

First version generated

2\. It looks like a chemistry lab, so I asked for an AI-related logo with further direction.

Press enter or click to view image in full size

Second version

3\. Looks much better, but I still feel it too busy in elements

Press enter or click to view image in full size

Final version

Now, Despite the missing character (which is still normally happening), the logo looks nice, and I didn’t even make any refined prompt by myself.

The implementation is not complicated, so let’s quickly see the Python code.

## Code Walkthrough

### 1\. Install Dependencies

Make sure you have the necessary packages installed, including AutoGen, OpenAI, and Panel:

```python pip install --upgrade pyautogen==0.2.32 openai==1.36.1 panel==1.4.4 ```

### 2\. Include these libraries, classes, and functions

For AutoGen with OpenAI:

```python import autogenfrom autogen import AssistantAgent, ConversableAgent, UserProxyAgentimport openaifrom openai import OpenAI ```

For Panel:

```python import panel as pnfrom panel.chat import ChatMessage ```

Miscellaneous:

```python import osimport timeimport asyncio ```

### 3\. Setup the Chat UI of Panel

Suppose you have learned how to develop apps with Panel’s innovative UI framework. In that case, you will be surprised by how easy it is to set up the Chat UI layout to wrap conversations between human users and LLM assistants.

Sketching of ChatInterface architecture from [Panel](<https://panel.holoviz.org/reference/chat/ChatInterface.html>)

Such a couple of lines can be used to implement the layout above.

``` pn.extension(design="material")chat_interface = pn.chat.ChatInterface(callback=callback)chat_interface.send("Send a message!", user="System", respond=False)pn.template.MaterialTemplate( title="Multi-agent with image generation", header_background="black", main=[chat_interface],).servable() ```

The key enabler here is creating a `chat_interface` object that makes all the chat widgets accessible and controllable by application code. In this place, we have registered a `callback` to the interface, which will be triggered each time input content is added to the chat input widget in the `chat_interface`.

Let’s see the callback.

### 4\. Callback Handler

To fit the architecture of AutoGen, there are two paths for the callback handler triggered by the user’s text input,

a) Start a group chat task

b) Further directions to the agents

```python initiate_chat_task_created = Falseinput_future = Noneasync def callback(contents: str, user: str, instance: pn.chat.ChatInterface): global initiate_chat_task_created global input_future if not initiate_chat_task_created: asyncio.create_task(delayed_initiate_chat(user_proxy, manager, contents)) else: if input_future and not input_future.done(): input_future.set_result(contents) else: print("There is currently no input being awaited.") ```

The global variable `initiate_chat_task_created = false` will create an `asyncio` task to run the core process of AutoGen in `delayed_initiate_chat()` function by providing agents and contents. The `input_future` variable is used to store and signal the subsequent input.

Here is the simple `delayed_initiate_chat()`function:

```python async def delayed_initiate_chat(agent, recipient, message): global initiate_chat_task_created # Indicate that the task has been created initiate_chat_task_created = True # Wait for 2 seconds await asyncio.sleep(2) # Now initiate the chat await agent.a_initiate_chat(recipient, message=message) ```

It just simply calls the AutoGen method `a_initiate_chat()` after a short wait.

### 5\. Agents Creation — User_Proxy

OK, now we are moving to the most critical part of this application — building agents.

Three agents need to be built: the `user_proxy` who acts as the human admin, the prompt_assistant, the `prompt_assistant` who writes high-quality prompts for Dalle-3 generation, and the `dalle_agent` who generates images.

Here is the user proxy:

``` user_proxy = MyConversableAgent( name="Admin", system_message="A human admin.", code_execution_config=False, human_input_mode="ALWAYS",) ```

As a non-AI agent, the user proxy’s role is to request and deliver user input to the core process of AutoGen and print it. To integrate these inputs with Panel UI, we should define a custom class, `MyConversableAgent`, to overwrite the input handler `a_get_human_input` from the original `ConversableAgent`.

```python class MyConversableAgent(autogen.ConversableAgent): async def a_get_human_input(self, prompt: str) -> str: global input_future chat_interface.send(prompt, user="System", respond=False) # Create a new Future object for this input operation if none exists if input_future is None or input_future.done(): input_future = asyncio.Future() # Wait for the callback to set a result on the future await input_future input_value = input_future.result() input_future = None print("input_value: ", input_value) return input_value ```

In the new `a_get_human_input` function, we print the system prompt to the panel UI to inform the user to input and then wait for the message object `input_future`, which will be set by the text input from the Panel UI in our previous `callback` function.

### 6\. Agents Creation — Prompt_Assistant

The next agent should have the capability to generate a decent prompt text for image creation so that we will use GPT-4o for this agent.

```json gpt4_config = {"config_list": [{'model': 'gpt-4o',}]}prompt_assistant = AssistantAgent( name="Prompt_Assistant", human_input_mode="NEVER", llm_config=gpt4_config, system_message='''You are a prompt engineer for image generation tasks using the DALL-E model. Your goal is to generate creative and accurate image prompts for the model based on user input. **Your Responsibilities:** 1. **Analyze User Input:** Carefully read the user's message and identify their desired image 2. **Understand User Preferences:** Determine the user's preferred style, tone, and overall aesthetic (e.g., realistic, cartoon, abstract, whimsical). 3. **Generate Image Prompts:** Craft one or more detailed image generation prompts based on the user's message and preferences. - **Clarity is Key:** Make sure your prompts are clear, specific, and easy for the DALL-E model to interpret. - **Include Details:** Provide information about subject, setting, action, style, and composition. - **Use Descriptive Language:** Choose words and phrases that evoke the desired visual style and imagery. Please make sure your response only contains prompt sentences, without including any description or introduction of this prompt. ''',) ```

Besides the system message, there is nothing special about creating such an `AssistantAgent`. However, we should do additional work redirecting the agent’s output to the Panel UI.

```python def print_messages(recipient, messages, sender, config): print(f"print - Messages from: {sender.name} sent to: {recipient.name} | num messages: {len(messages)} | message: {messages[-1]}") content = messages[-1]['content'] if all(key in messages[-1] for key in ['name']): chat_interface.send(content, user=messages[-1]['name'], respond=False) else: chat_interface.send(content, user=recipient.name, respond=False) return False, None # required to ensure the agent communication flow continuesprompt_assistant.register_reply( [autogen.Agent, None], reply_func=print_messages, config={"callback": None},) ```

Here we define a `print_message` function to call `chat_interface.send()` method to send the content and its relevant sender to the front end. Then, register this function to the agent `prompt_assistant`’s reply function, meaning the `print_message()` will be triggered each time the agent receives a message from the orchestrator.

### 7\. Agent Creation — Dalle_Agent

Last but not least, it’s time to create the Dalle agent to create images. Since no agent classes in AutoGen are integrated with the Dalle model, we have to customise one.

First, let’s create a normal `ConversableAgent` with a name and an auto-reply message to indicate the image is generated (In the Dalle-3 model, there will be a temporary URL for this image).

``` dalle_agent = ConversableAgent( name="Dalle_Agent", default_auto_reply= f"Image URL generated",) ```

Second, we register a `generate_image()` function to the reply function of this agent. Now, each time the prompt message from the `Prompt_Assistant` agent is delivered to this agent, the process of creating an image, like calling Dalle-3 model API, can run. We input the `dalle3_config` to the function as a config parameter for later use.

```json dalle3_config = {"config_list": [{"model": "dall-e-3"}]}dalle_agent.register_reply( [autogen.Agent, None], reply_func=generate_image, config={"llm_config": dalle3_config}, ) ```

Moving forward, see what is done in `generate_image()` function.

```python def generate_image(recipient, messages, sender, config): print(f"image - Messages from: {sender.name} sent to: {recipient.name} | num messages: {len(messages)} | message: {messages[-1]}") prompt = messages[-1]["content"] if all(key in messages[-1] for key in ['name']): chat_interface.send(prompt, user=messages[-1]['name'], respond=False) else: chat_interface.send(prompt, user=recipient.name, respond=False) client=OpenAI() response = client.images.generate( model=config['llm_config']['config_list'][0]['model'], prompt=prompt, size="1024x1024", quality="standard", n=1, ) image_url = response.data[0].url print("image_url:", image_url) jpg_pane = pn.pane.Image(image_url, width=400) content = ChatMessage(jpg_pane, user=dalle_agent.name) chat_interface.send(content) return False, {"content": content} ```

Three steps here:

1. print the prompt message that is delivered by the `prompt_assistant` agent.
2. Use OpenAI API to generate the image through Dalle-3 mode. The response will be a URL of an image file.
3. Create an image message object in the Panel and display it to the front end.

### 8\. Manager Creation

To follow the definition of AutoGen’s group chat structure, we must create a manager agent to orchestrate all three agents in the group. Just create a group chat with the agents included, then create the manager with the GPT-4o model as well.

``` groupchat = autogen.GroupChat(agents=[user_proxy, prompt_assistant, dalle_agent], messages=[], max_round=20)manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_config) ```

## Run & Test

We have successfully created the `user_proxy` and `manager`, which is enough to initial a group chat in the previous call `asyncio.create_task(delayed_initiate_chat(user_proxy, manager, contents))`, it’s time to wrap up and run the code.

It’s a panel-based Python code, so we should run the Panel command (assuming the code file is `autogen_panel_image.py`):

``` panel serve autogen_panel_image.py ```

If you see this output, your app goes live. The URL for the internal network is `http://localhost:5006/autogen_panel_image` with default port 5006, and it’s also externally accessible if you have a public IP.

Press enter or click to view image in full size

This demo shows just the tip of the iceberg when it comes to building image-creation agents. Now it’s your turn to unleash your creativity and build even more amazing and sophisticated applications!

Thanks for reading. If you think it’s helpful, please Clap 👏 for this article. Your encouragement and comments mean a lot to me, mentally and financially. 🍔

**Before you go:**

✍️ If you have any questions, please leave me responses or find me on [**X**](<https://twitter.com/Yeyu2HUANG/>)**** and [**Discord**](<https://discord.gg/KPTCE4CEmp>) where you can have my active support on development and deployment.

☕️ If you would like to have exclusive resources and technical services, subscribing to the services on my****[**Ko-fi**](<https://ko-fi.com/yeyuh>)**** will be a good choice.

💯 **I am also open to being hired for any innovative and full-stack development jobs.**

---
domain: levelup.gitconnected.com
fetch_date: '2026-05-18T12:52:56.660624'
status: ok
url: https://levelup.gitconnected.com/creating-an-ai-agent-that-uses-a-computer-like-people-do-288f7ad97169
---

# Creating an AI Agent That Uses a Computer Like People Do

## Sees Your Desktop, Performs Tasks

[ ![Fareed Khan](https://miro.medium.com/v2/resize:fill:64:64/1*feiUXOR8sid6IPHSHufA-g.jpeg) ](<https://medium.com/@fareedkhandev?source=post_page---byline--288f7ad97169--------------------------------------->)

[Fareed Khan](<https://medium.com/@fareedkhandev?source=post_page---byline--288f7ad97169--------------------------------------->)

22 min read

·

Feb 24, 2025

\--

Listen

Share

More

Read this story for free: [link](<https://medium.com/@fareedkhandev/288f7ad97169?sk=9d517bf967a1420187bb21ba218ad22e>)

In this blog, we will build an AI Agent from scratch to handle interactive tasks, like:

> Buy me a Soccer ball from Amazon

It opens Chrome, searches a query, scrolls, and adds the first soccer ball to the cart.

Press enter or click to view image in full size

Buying task (Created by

[Fareed Khan](<https://medium.com/u/b856005e5ecd?source=post_page---user_mention--288f7ad97169--------------------------------------->)

)

> Open Google Chrome and search google share price

Press enter or click to view image in full size

Google share price task (Created by

[Fareed Khan](<https://medium.com/u/b856005e5ecd?source=post_page---user_mention--288f7ad97169--------------------------------------->)

)

Claude last year released a beta version of computer use, an AI agent that can do desktop tasks, but still it is in beta, where Developers can direct Claude to use computers the way people do by looking at a screen, moving a cursor, clicking buttons, and typing text.

> We will do the same, make the LLM see our screen and take actions accordingly

## GitHub Code

All the code, along with the proper setup, is available in my GitHub repo.

## [GitHub - FareedKhan-dev/ai-desktop: AI agent that controls a computerAI agent that controls a computer. Contribute to FareedKhan-dev/ai-desktop development by creating an account on…github.com](<https://github.com/FareedKhan-dev/ai-desktop?source=post_page-----288f7ad97169--------------------------------------->)

The codebase is organized as follows:

``` /ai-desktop │── /OmniParser # Screen Parsing Repo submodule│── main.py # Entry point for running the agent│── utils.py # Backend logic│── config.py # API, LLM name setting and more!│── requirements.txt # Dependencies │── README.md # Project overview ```

## Table of Contents

* How Our Agent Works
* Setting up the Stage
* Coding the Omni Parser
* Screenshot Taker
* Giving Our Agent Hands
* Making Actions Real
* Moving and Clicking
* Action Orchestrator
* Thinking Methodology
* Structuring the Prompt for Clarity
* Building the VLM Agent
* Calling Everything
* Performing Tasks
* Use OmniParser + OmniTool

## How Our Agent Works

Before writing the technical code, we need to understand what our approach would be, what we are coding, and how it can be efficient.

Let’s visualize it first to have a better view.

Press enter or click to view image in full size

Computer Use AI Agent Architecture (Created by

[Fareed Khan](<https://medium.com/u/b856005e5ecd?source=post_page---user_mention--288f7ad97169--------------------------------------->)

)

1. First, the user provides an input command to our agent like **“Open Chrome and buy me a milk”**.
2. The **VLMAgent** (Vision language model) receives the user input and starts processing it.
3. The agent parses the screen using **Omniparser** to extract relevant information.
4. The agent analyzes the screen and determines what action needs to be taken using **LLM OpenAI**.
5. **Omniparser** processes the screen content and extracts key details, such as buttons, text fields, or links.
6. The **LLM OpenAI** interprets the extracted information and decides the next steps.
7. The agent generates actions such as mouse movements, typing, and clicking.
8. These actions are sent for execution on the computer.
9. The computer processes the actions, such as opening Chrome, searching for milk, adding it to the cart, and proceeding to checkout.
10. The system gathers feedback from the executed actions to check if the task is completed.
11. If the task is not yet complete, the loop repeats until success.
12. Once all actions are executed successfully, the task is marked as complete, and the system confirms the result.

Now that we have understand a basic overview of our approach, It’s time to start coding.

## Setting up the Stage

Clone the repository and install the required libraries using the following commands:

```python # Cloning the reo with submodule omniparsergit clone --recursive https://github.com/FareedKhan-dev/ai-desktopcd ai-desktop/OmniParser# Installing the dependenciespip install -r requirements.txt ```

Now, let’s import the required libraries.

```python import logging # Logging events.import os # OS interactions.import sys # System functions.import re # Regular expressions.import math # Math operations.from dataclasses import dataclass, field # Data classes.from typing import List, Optional, Dict, Any, Tuple # Type hinting.import base64 # Base64 encoding/decoding.import io # Data streams.from PIL import Image # Image processing.import pyautogui # GUI automation.import torch # PyTorch (deep learning).import asyncio # Asynchronous programming.from pathlib import Path # file paths# OmniParser custom modules (they are in the OmniParser submodule)from OmniParser.utils.display import get_yolo_model, get_caption_model_processor, get_som_labeled_img, check_ocr_box ```

## Coding the Omni Parser

Press enter or click to view image in full size

Omni Parser Workflow (Created by

[Fareed Khan](<https://medium.com/u/b856005e5ecd?source=post_page---user_mention--288f7ad97169--------------------------------------->)

)

A quick overview of [Omni Parser](<https://github.com/microsoft/OmniParser/>) is that it is a recent model released by Microsoft for screen parsing. You can consider it a breakthrough due to its accuracy.

You can check its [official GitHub repository](<https://github.com/microsoft/OmniParser/>), it requires proper setup before we can use it with our AI agent.

First, we need to clone their repo and download the Omni Parser model weights.

``` # Clone OmniParser Repo and navigating to the directorygit clone https://github.com/microsoft/OmniParser/cd OmniParser ```

After cloning the repo and navigating to the directory, we can simply download the model.

``` # Download the model checkpoints to the local directory OmniParser/weights/for f in icon_detect/{train_args.yaml,model.pt,model.yaml} \ icon_caption/{config.json,generation_config.json,model.safetensors}; do huggingface-cli download microsoft/OmniParser-v2.0 "$f" --local-dir weightsdone# Rename the downloaded 'icon_caption' directorymv weights/icon_caption weights/icon_caption_florence ```

It will start downloading weights. Make sure to rename the weights folder correctly as I have done in the above command.

You can simply use their [demo notebook](<https://github.com/microsoft/OmniParser/blob/master/demo.ipynb>) or [Gradio script](<https://github.com/microsoft/OmniParser/blob/master/gradio_demo.py>) to see how Omni Parser works. For example, this is what its performance looks like for my Windows desktop screenshot.

Press enter or click to view image in full size

Omni Parser detection on my Desktop

It has correctly identified most of the icons and text, so yeah, it’s pretty good.

We need to define some important parameters that will help configure the OmniParser effectively.

```json # Define configuration parametersconfig = { "som_model_path": "weights/icon_detect/model.pt", "caption_model_name": "microsoft/OmniParser-v2.0", "caption_model_path": "weights/icon_caption_florence", "BOX_TRESHOLD": 0.5, # Adjust threshold for bounding box detection} ```

These parameters specify the paths for the structured object model (SOM) and captioning model, as well as the threshold for detecting UI elements.

Now that we have defined the configurations, let’s initialize and load the required models.

OmniParser uses a YOLO-based structure object model to detect UI elements and a captioning model to extract meaningful descriptions.

Here’s how we load the models:

```python def load_models(config: Dict): device = "cuda" if torch.cuda.is_available() else "cpu" # Load the Structured Object Model (SOM) for UI detection som_model = get_yolo_model(model_path=config["som_model_path"]) # Load the captioning model processor caption_model_processor = get_caption_model_processor( model_name=config["caption_model_name"], model_name_or_path=config["caption_model_path"], device=device ) print("OmniParser models loaded successfully!") return som_model, caption_model_processor ```

This function make sure that the models are correctly loaded onto the appropriate device (CPU or GPU).

SOM model helps detect UI components, while the captioning model processes text and labels extracted from the screen.

Now, let’s create the main function that takes a screenshot, processes it using OmniParser, and extracts structured information.

```python def parse_screen(image_base64: str, som_model, caption_model_processor) -> Tuple[str, List[Dict[str, Any]]]: # Decode base64 image image_bytes = base64.b64decode(image_base64) image = Image.open(io.BytesIO(image_bytes)) print("Image size:", image.size) # Define scaling for overlay box_overlay_ratio = max(image.size) / 3200 draw_bbox_config = { "text_scale": 0.8 * box_overlay_ratio, "text_thickness": max(int(2 * box_overlay_ratio), 1), "text_padding": max(int(3 * box_overlay_ratio), 1), "thickness": max(int(3 * box_overlay_ratio), 1), } # Perform OCR and get bounding boxes (text, ocr_bbox), _ = check_ocr_box( image, display_img=False, output_bb_format="xyxy", easyocr_args={"text_threshold": 0.8}, use_paddleocr=False ) # Process the screen using the SOM model and captioning model dino_labeled_img, label_coordinates, parsed_content_list = get_som_labeled_img( image, som_model, BOX_TRESHOLD=config["BOX_TRESHOLD"], output_coord_in_ratio=True, ocr_bbox=ocr_bbox, draw_bbox_config=draw_bbox_config, caption_model_processor=caption_model_processor, ocr_text=text, use_local_semantics=True, iou_threshold=0.7, scale_img=False, batch_size=128 ) return dino_labeled_img, parsed_content_list ```

We are decoding the base64 image then extracts text and bounding boxes using OCR by Processing the screen through OmniParser models in a result it will returns labeled UI elements and structured data.

let’s test our OmniParser on an actual desktop screenshot. We will load a sample image, process it using our function, and see how well it extracts UI elements.

``` # Load modelssom_model, caption_model_processor = load_models(config)# Load a desktop screenshot image (convert it to base64)with open("desktop_screenshot.jpg", "rb") as image_file: image_base64 = base64.b64encode(image_file.read()).decode("utf-8")# Run OmniParserlabeled_img, parsed_content = parse_screen(image_base64, som_model, caption_model_processor)# Print the parsed contentprint(parsed_content)#### OUTPUT ####[{'type': 'text', 'bbox': [0.091, 0.004, 0.137, 0.028], 'interactivity': False, 'content': 'G Google', 'source': 'box_ocr_content_ocr'}, {'type': 'text', 'bbox': [0.088, 0.040, 0.1895, 0.062], 'interactivity': False, 'content': 'https://www.google.com', 'source': 'box_ocr_content_ocr'},...]#### OUTPUT #### ```

When we run this code, we see the parsed content containing bounding boxes, its type, and many other pieces of information that are important to be used by our vision-language model.

Right now, we have only implemented the part where our AI can parse the screenshot, such as drawing bounding boxes and extracting information.

## Screenshot Taker

Before our AI agent can parse the UI elements using OmniParser, it first needs to capture the screen.

While we can manually take a screenshot and feed it into the model, our goal is to automate the entire process. This means the AI agent should be able to “see” the screen by capturing a screenshot on demand.

To achieve this, we will use `pyautogui`, a simple and effective library for taking screenshots in Python. The captured screenshot will then be processed by our OmniParser.

First, let’s define a function to capture the current screen and save it as an image file.

```python # Output directory where temporary screenshot are savedOUTPUT_DIR = "temp/"def get_screenshot() -> Tuple[Image.Image, Path]: # Create the output directory if it doesn't exist OUTPUT_DIR.mkdir(parents=True, exist_ok=True) # Capture the entire screen img = pyautogui.screenshot() # Returns a PIL Image # Define the screenshot file path screenshot_path = OUTPUT_DIR / "screenshot.png" # Save the screenshot img.save(screenshot_path) # returning the bounded image and bounded boxes return img, screenshot_path ```

We first create a temporary directory (`tmp/`) to store the screenshot after that we uses `pyautogui.screenshot()` to take a full-screen screenshot and the image get saved in the `tmp/` directory as `screenshot.png` and our function returns both the screenshot as a `PIL.Image` object and its file path.

Now that we have automated screenshot capture, let’s feed the captured image into our OmniParser and extract structured data.

``` # Step 1: Capture the screenshotscreenshot, screenshot_path = get_screenshot()# Step 2: Convert the screenshot to base64 format for processingwith open(screenshot_path, "rb") as image_file: image_base64 = base64.b64encode(image_file.read()).decode("utf-8")# Step 3: Load the OmniParser modelssom_model, caption_model_processor = load_models(config)# Step 4: Parse the screen using OmniParserlabeled_img, parsed_content = parse_screen(image_base64, som_model, caption_model_processor) ```

If we run the above code, our OmniParser will analyze the captured screenshot and extract structured UI elements but this time it will be automated.

## Giving Our Agent Hands

Press enter or click to view image in full size

How agent takes action (Created by

[Fareed Khan](<https://medium.com/u/b856005e5ecd?source=post_page---user_mention--288f7ad97169--------------------------------------->)

)

So far, we have make our AI agent with eyes it can see the screen and understand what’s on it thanks to OmniParser and pyautogui. But just seeing isn’t enough.

To be truly helpful, we need to make our agent to _do_ things. It needs to be able to interact with the computer just like we do, using a mouse and keyboard. This is where we move into the step of **action execution**.

To make our agent interactive, we need to define a set of actions it can take. These actions will be the building blocks for any task we want to automate.

When you use a computer, what do you actually _do_? You might:

* **Move the mouse** : You guide the cursor around the screen to point at things.
* **Click** : You select buttons, links, and icons by clicking with the mouse. You might left-click, right-click, or even double-click.
* **Type** : You enter text into search bars, forms, and documents using the keyboard.
* **Press Keys** : You use keys for shortcuts, navigation, and commands — like pressing ‘Enter’ to submit a form, or ‘Ctrl+C’ to copy text.
* **Scroll** : You move up and down web pages or documents to see more content.

These are the fundamental ways we interact with our desktops.

To make our AI agent capable, we need to give it the same abilities. Let’s define a list of these basic actions for our agent:

``` # Let's list the actions our agent will understandpossible_actions = [ "key_press", # To simulate pressing keys on the keyboard "type_text", # For typing out words and sentences "move_mouse", # To move the cursor around the screen "click_left_mouse", # For standard selections and interactions "click_right_mouse",# To open context menus and more "click_double_mouse",# For actions that require a double click "capture_screenshot",# For the agent to re-examine the screen "get_cursor_position", # To know where the mouse is currently located "pause_briefly", # To allow time for actions to register "scroll_up_page", # To navigate content vertically "scroll_down_page",# Also for vertical navigation "hover_mouse_over" # To highlight or trigger interface changes] ```

This possible_actions list is our agent’s action vocabulary. It’s a set of commands it can understand and execute.

In the next step, we’ll create a tool that knows how to translate these abstract action names into real computer operations.

## Making Actions Real

Now we have a list of actions our agent _understands_. But how does it actually _perform_ these actions on the computer?

We need a tool that can bridge the gap between the agent action commands and the computer input system. Let’s call this tool ComputerActions.

The ComputerActions tool will be like a set of robotic arms for our agent. When the agent decides to “**click_left_mouse** ”, the ComputerActions tool will use **pyautogui** to simulate a left mouse click at the current cursor position. Similarly, for “type_text”, it will use pyautogui to simulate typing on the keyboard.

Let’s sketch out the structure of our ComputerActions tool.

```python # tool to perform actions on the computerclass ComputerActions_Tool: tool_name = "computer_actions" # We'll name our tool 'computer_actions' def __init__(self): # We can set up any initial configurations here if needed # For now, we might just need to handle special key names self.key_name_mapping = { "PageDown": "pagedown", # Mapping friendly names to pyautogui names "PageUp": "pageup", "WindowsKey": "win", "EscapeKey": "esc", "EnterKey": "enter" } async def perform_action(self, action_type, action_details=None): # This function will take the action type and details and execute it try: if action_type == "move_mouse": # Move the mouse to a given coordinate if action_details is None or 'coordinates' not in action_details: raise Exception("Mouse movement needs coordinates (x, y).") x_coord, y_coord = action_details['coordinates'] pyautogui.moveTo(x_coord, y_coord, duration=0.2) # Smooth mouse movement return {"action_result": f"Mouse moved to ({x_coord}, {y_coord})"} elif action_type == "click_left_mouse": # Perform a left mouse click pyautogui.click() return {"action_result": "Left mouse click performed."} # ... we would add similar 'elif' blocks for other actions like: # 'click_right_mouse', 'click_double_mouse', 'type_text', 'key_press', # 'capture_screenshot', 'get_cursor_position', 'pause_briefly', # 'scroll_up_page', 'scroll_down_page', 'hover_mouse_over' else: raise Exception(f"Unknown action type: {action_type}") except Exception as action_error: return {"action_error_message": f"Error during action: {action_error}"} ```

In this ComputerActions_Tool class, the perform_action function is the heart of the tool.

It takes the action_type (like “move_mouse” or “click_left_mouse”) and action_details (which might include coordinates or text to type).

Inside this function, we use pyautogui to translate these commands into actual computer interactions. We’ve started with handling “move_mouse” and “click_left_mouse” as examples, and we would expand it to include all the actions in our possible_actions list.

## Moving and Clicking

Let’s look a little deeper into how the perform_action function in our ComputerActions_Tool handles specific actions. Consider the “move_mouse” and “click_left_mouse” actions.

When the agent wants to move the mouse, it will send a command to the ComputerActions_Tool with the action_type as “move_mouse” and action_details containing the target coordinates.

Look at this part of the code again:

```json if action_type == "move_mouse": if action_details is None or 'coordinates' not in action_details: raise Exception("Mouse movement needs coordinates (x, y).") x_coord, y_coord = action_details['coordinates'] pyautogui.moveTo(x_coord, y_coord, duration=0.2) return {"action_result": f"Mouse moved to ({x_coord}, {y_coord})"} ```

First, it checks if the action_details are provided and if they include ‘coordinates’. If not, it raises an error because moving the mouse requires knowing _where_ to move it.

Then, it extracts the x_coord and y_coord from the action_details. Finally, it uses pyautogui.moveTo(x_coord, y_coord, duration=0.2) to smoothly move the mouse cursor to the specified location over a short duration (0.2 seconds).

The function then returns a confirmation message.

For a **left click** , the process is simpler. The agent sends a command with action_type as “click_left_mouse”. Here’s how it’s handled:

```json elif action_type == "click_left_mouse": pyautogui.click() return {"action_result": "Left mouse click performed."} ```

In this case, no action_details are needed. The pyautogui.click() function, when called without any arguments, performs a left mouse click at the _current_ mouse cursor position.

The function then returns a simple confirmation message.

You can see how straightforward it is to add more actions. For “type_text”, we would use pyautogui.typewrite(text), for “key_press” we would use pyautogui.press(key), and so on.

pyautogui provides functions to simulate all the basic mouse and keyboard interactions we need.

## Action Orchestrator

We now have a ComputerActions_Tool that can perform actions. But who tells this tool _what_ to do and _when_?

We need a component that acts as a central coordinator, receiving action _instructions_ from the AI agent and then using the appropriate tool to _execute_ them. Let’s call this component the ActionOrchestrator.

Our ActionOrchestrator job is to:

1. **Receive Action Commands** : It will get instructions from the main AI agent, telling it which action to perform and with what parameters (like coordinates or text).
2. **Select the Right Tool** : In our current setup, we only have the ComputerActions_Tool. But in the future, we might have other tools (e.g., a tool to interact with web APIs directly). The ActionOrchestrator will decide which tool is needed for the given action.
3. **Execute the Action** : It will use the selected tool to perform the action, passing in the necessary parameters.
4. **Handle Results and Errors** : It will receive feedback from the tool — whether the action was successful, if there was an error, or if there’s any output from the action. It will then pass this information back to the main AI agent.

Let’s outline the ActionOrchestrator class.

```python # class to orchestrate the actionsclass ActionOrchestrator_Agent: def __init__(self, feedback_callback_function): # Needs a function to provide feedback (e.g., for logging or display) self.computer_tool = ComputerActions_Tool() # Initialize our ComputerActions tool self.feedback_callback = feedback_callback_function # Store the feedback function async def execute_agent_action(self, tool_name, action_input_details): # This function takes the tool name and action details and executes self.feedback_callback(f"Attempting to use tool: {tool_name}, with details: {action_input_details}", "agent_message") # Informative message try: if tool_name == "computer_actions": # If the tool is 'computer_actions', use our ComputerActions_Tool action_type_to_use = action_input_details.get("action") # Get the action type action_parameters = action_input_details.get("parameters", None) # Get parameters if any action_result = await self.computer_tool.perform_action( # Execute the action using the tool action_type=action_type_to_use, action_details=action_parameters ) if action_result.get("action_error_message"): # Check for errors self.feedback_callback(f"Tool reported an error: {action_result['action_error_message']}", "agent_error") # Report error else: if action_result.get("action_result"): # Report success output self.feedback_callback(action_result["action_result"], "agent_output") # Report action output return action_result # Return the result of the action else: return {"action_error_message": f"Unknown tool requested: {tool_name}"} # Error for unknown tool except Exception as orchestration_error: return {"action_error_message": f"Unexpected problem during action orchestration: {orchestration_error}"} # Error for unexpected problems ```

ActionOrchestrator_Agent class is initialized with a feedback_callback_function, which allows it to send messages about what it’s doing (for logging or display purposes).

The execute_agent_action function is the main entry point. It takes the tool_name and action_input_details as input.

Currently, it only handles the “computer_actions” tool. It extracts the action_type and action_parameters from the action_input_details, calls the perform_action function of the ComputerActions_Tool, and then handles the result, reporting any errors or outputs back through the feedback_callback_function.

With the ActionOrchestrator in place, we have completed the action execution pipeline. Our agent can now “see” the screen, decide on an action, and then use the ActionOrchestrator and ComputerActions_Tool to actually perform that action on the computer.

The next big step is to bring in the “brain” which is the LLM to make intelligent decisions about which actions to take in the first place!

## Thinking Methodology

We’ve built the **eyes** (OmniParser) and **hands** (Action Execution) of our AI agent, but it needs a **brain** to understand user goals, analyze the screen, and decide what to do next.

This is where the **Large Language Model (LLM)** comes in. It interprets natural language commands like _“Open Chrome and search for cat videos”_ , processes UI elements from OmniParser, plans actions, and generates commands such as `move_mouse` or `type_text`.

This makes our agent **intelligent and adaptive** rather than blindly following instructions.

To make decisions, the LLM needs two inputs: the **user’s goal** (e.g., _“Book a flight to Paris”_) and the **current screen state** (structured UI data from OmniParser).

The UI data is formatted into a clear prompt, listing elements like buttons and text fields, allowing the LLM to understand what’s visible on screen. For example:

```json [ { "type": "button", "text": "Search", "bounding_box": [100, 200, 150, 220] }, { "type": "text_field", "placeholder": "Enter search term", "bounding_box": [80, 180, 300, 200] }] ```

The LLM responds with a structured action plan, specifying the **next action** , required **parameters** (like coordinates or text), and optional **reasoning** for debugging. For example, if the user wants to open Chrome:

```json { "reasoning": "The user wants to open Chrome. The desktop contains a Chrome icon. I should double-click it.", "next_action": "click_double_mouse", "target_element_id": "chrome_icon_id"} ```

This decision-making connects to the **Action Execution** system through a continuous loop: **Observe → Decide → Act → Observe**.

The agent captures the screen, formats data, sends it to the LLM, extracts the response, executes the action via **ActionOrchestrator** , and repeats. This enables real-time adaptability.

In our next steps we will include LLM prompts, optimizing workflows, handling errors, and improving efficiency. With this setup, our AI agent can truly **see, think, and act** , transforming how we interact with computers.

## Structuring the Prompt for Clarity

To control our desktop AI agent, we guide the LLM with **prompting,** giving clear instructions so it makes the right decisions.

A good prompt includes:

1. **User Goal:** What the user wants (e.g., “Open a browser” or “Get stock prices”).
2. **Current Screen State:** What is visible on the screen (from OmniParser).

By combining these, the LLM can determine the best action to take.

we want to give the LLM a clear **“job description”** the tools it has available, the current situation (screen state), the goal (user query), and the format in which it should deliver its decision (JSON response).

``` # First line of our job description prompt"""You are a desktop AI agent that controls a computer using a mouse and keyboard.""" ```

We’re immediately telling it _who_ it is. It’s not just any AI, it’s a _desktop AI agent_. And what does a desktop AI agent do? It controls a computer! And _how_ does it do that? Using a mouse and keyboard, just like you and me.

Now that the LLM knows _what_ it is, we need to tell it _what it can do_.

This is where we list out all the actions our ComputerActions_Tool we built earlier can perform. Remember that possible_actions list?

We’re putting that into the prompt:

``` # Action tools availablity"""Your available actions are:- move_mouse: Moves the mouse cursor to a specific (x, y) coordinate on the screen.- click_left_mouse: Performs a left mouse click at the current cursor position.- type_text: Types the given text using the keyboard.- key_press: Presses a specific key or key combination (e.g., 'Enter', 'Ctrl+C').- ... (and so on for all actions in our 'possible_actions' list)""" ```

By listing these actions _clearly_ and _descriptively_ , we’re telling the LLM exactly what it’s capable of. It can’t invent new actions; it has to choose from this list. This is super important for keeping things controlled and predictable.

So the LLM knows its job and its tools. But it’s still blind! It needs to _see_ the screen to make decisions. This is where we feed it the output from our OmniParser.

Look at this part of the prompt:

``` # Visibilty Feature"""Here is the information about what is currently visible on the screen:[Start of Screen Information][Structured output from OmniParser will be inserted here.For example:- Element type: Button, Text: 'Submit', Coordinates: (100, 200, 150, 250)- Element type: Text Field, Placeholder: 'Search...', Coordinates: (50, 50, 300, 100)- ... and so on for all detected UI elements][End of Screen Information]""" ```

We are showing the LLM a picture of the desktop, but not just a raw image. We’re giving it a _structured_ view, thanks to OmniParser.

It’s like saying, “Hey LLM, on the screen right now, I see a button that says ‘Submit’ at these coordinates, and a text field that says ‘Search…’ over here”.

Now the LLM can see its workspace and knows its tools. But what’s the _goal_? What does the user want it to do? This is where we inject the user query:

``` # User QUery"""The user's request is: {User Query}""" ```

We are directly telling the LLM what the user has asked for, like “Open Google Chrome” or “Buy milk online”.

This is the _objective_ the LLM needs to achieve.

We need it to _communicate its decisions back to us_ in a way our system can understand. That’s why we specify the response format! We want JSON!

Let’s look at this part:

```json # Communication ability"""Respond in JSON format. Your JSON response should have the following fields:- "reasoning": (Explain your thought process step-by-step. Why did you choose this action?)- "next_action": (The action to perform next. Choose one from the available actions listed above.)- "action_parameters": (A dictionary containing parameters needed for the action. For 'move_mouse', include 'coordinates': [x, y]. For 'type_text', include 'text_to_type': 'the text'. For 'key_press', include 'key_name': 'the key'. If no parameters are needed, this field can be an empty dictionary.)""" ```

We are setting up a clear communication protocol. We’re saying, “LLM, when you decide what to do, tell me in JSON format. And make sure your JSON includes these specific fields: reasoning, next_action, and action_parameters.”

Finally, to make it _extra_ clear, we give the LLM an example of the JSON response we’re expecting.

```json # Response format"""Example JSON Response:json{ "reasoning": "The user wants to click the 'Submit' button. I see a button with text 'Submit' on the screen. I should move the mouse to its coordinates and perform a left click.", "next_action": "move_mouse", "action_parameters": { "coordinates": [125, 225] } // Example coordinates - use actual coordinates from parsed info}""" ```

So to sum up, our whole prompt as a detailed instruction manual for the LLM. We are not just asking it to do something, we are carefully guiding it through the entire decision making process:

1. **Understand your role.** (Desktop AI Agent)
2. **Know your capabilities.** (Available Actions)
3. **See the current situation.** (Screen Information)
4. **Understand the goal.** (User Request)
5. **Communicate your decision clearly.** (JSON Response Format)
6. **Here’s an example of what I expect.** (Example JSON)

## Building the VLM Agent

We have all the pieces now:

1. eyes (OmniParser)
2. hands (Action Execution)
3. brain (LLM)
4. and a way to talk to it (Prompting)

The next important step is to bring all these components together and create the central orchestrator for our AI agent. Let’s call this class VLMAgent (Vision Language Model Agent).

The most important part of the VLMAgent class is its main method, let’s call it run. This method will be the entry point for executing a user’s task. Let’s outline what the run method should do step-by-step:

```python class VLMAgent_Agent: # ... (Initialization of OmniParser, ActionOrchestrator, LLM config, etc. would go here) ... async def run_agent_task(self, user_query): # Main method to run the agent for a given user query previous_agent_messages = [] # To keep track of conversation history (for context) while True: # Keep looping until task is completed or agent decides to stop # Step 1: Capture Screenshot screenshot_image, screenshot_path = get_screenshot() # Use our screenshot function # Step 2: Parse Screen using OmniParser labeled_image_base64, parsed_screen_content = parse_screen( # Use our OmniParser function screenshot_image, self.omni_parser_models, self.omni_parser_config ) # Step 3: Formulate Prompt for LLM prompt_to_llm = create_llm_prompt( # Function to create prompt (we'll define this) user_query=user_query, screen_content=parsed_screen_content, previous_messages=previous_agent_messages # Pass history for context ) # Step 4: Send Prompt to LLM and Get Response llm_response_text, _ = send_prompt_to_llm_api( # Function to interact with LLM API prompt=prompt_to_llm, llm_api_config=self.llm_config # LLM API configuration ) self.output_feedback_function(f"LLM Response: {llm_response_text}", "llm_response") # Show LLM response # Step 5: Parse LLM Response to Get Action Command action_command_from_llm = parse_llm_response_for_action(llm_response_text) # Function to parse JSON # Step 6: Execute Action using ActionOrchestrator if action_command_from_llm and action_command_from_llm.get("next_action"): # Check if action is suggested action_description = generate_action_description(action_command_from_llm) # For output self.output_feedback_function(action_description, "agent_action") # Show action description action_name = "computer_actions" # For now, we only have computer actions action_input = prepare_action_input(action_command_from_llm) # Prepare input for ActionOrchestrator action_result = await self.action_orchestrator.execute_agent_action( # Execute the action tool_name=action_name, tool_input=action_input ) # Step 7: Handle Feedback and Update Conversation History previous_agent_messages = update_conversation_history( # Function to update history previous_messages=previous_agent_messages, llm_response=llm_response_text, action_description=action_description, action_result=action_result ) user_query = "Continue with the previous task" # Agent asks LLM to continue in next loop if action_result.get("error"): # If there is an error, maybe LLM can fix it in next turn previous_agent_messages.append({"role": "user", "content": action_result["error"]}) # Feedback error to LLM else: self.output_feedback_function("Task completed or no action needed.", "agent_status") # Task finished break # Exit the loop if no action needed self.output_feedback_function("Agent task finished.", "agent_status") # Final status message ```

Our run_agent_task method contains the entire workflow of our agent. It is a loop that continues until the agent decides it’s done. Each step in the loop corresponds to one of the core functionalities we’ve built:

1. screenshot
2. parsing
3. prompting the LLM
4. action execution
5. feedback handling

We have used placeholder function names like create_llm_prompt, send_prompt_to_llm_api, parse_llm_response_for_action, etc to indicate where these sub-functions would fit in.

Here’s a concise breakdown of the helper functions for `run_agent_task`:

* **create_llm_prompt** : Builds the LLM prompt using the user query, screen content, and conversation history.
* **send_prompt_to_llm_api** : Sends the prompt to the LLM API and returns the response.
* **parse_llm_response_for_action** : Extracts the action and parameters from the LLM’s response (handles JSON parsing errors).
* **prepare_action_input** : Formats the LLM’s action output for the ActionOrchestrator.
* **update_conversation_history** : Logs the LLM’s response, action, and results for continuity.
* **generate_action_description** : Converts the action into a human-readable description.
* **get_screenshot & parse_screen**: Capture and process the screen content using OmniParser.

In the next parts, we will flesh out some of these helper functions and see how to put everything together in a main.py script to actually run our agent.

## Calling Everything

Finally, to make our agent runnable, we would create a main asyn function. It will call everything we have coded so far.

```python async def main_function_agent(user_query): # ... (Set up configurations, API keys, model paths, etc.) ... executor = LocalExecutor_Agent(output_callback_function=print) agent = VLMAgent_Agent( omni_parser_config=omni_parser_config, llm_config=llm_config, action_orchestrator=executor, output_feedback_function=print ) print("Waiting for 5 seconds before execution...") await asyncio.sleep(5) # Add a 5-second delay await agent.run_agent_task(user_query=user_query)if __name__ == "__main__": if len(sys.argv) > 1: user_input = " ".join(sys.argv[1:]) # Combine all arguments as a single string else: user_input = input("Enter your command: ") asyncio.run(main_function_agent(user_input)) ```

It has to be an asynchronous function because it allows other tasks to run while waiting (e.g, during I/O operations like API calls, delays, or user input).

One more important thing, I added `sleep(5)`, a 5 second delay, because I need to minimize all windows, starting from the desktop. It is not mandatory, but capturing the screen from the desktop makes it easier since there are fewer icons visible.

## Performing Tasks

let’s test our agent and see how it is performing and where it is lagging.

> Provide me with Google’s share price for today

Press enter or click to view image in full size

Google share price task (Created by

[Fareed Khan](<https://medium.com/u/b856005e5ecd?source=post_page---user_mention--288f7ad97169--------------------------------------->)

)

It opens Chrome and correctly enters the string **“Google’s Share Price”** in the search box.

Although we can add functionality to read the browser search results screenshot and return the price value in the terminal, but the actions performed so far are correct.

> Buy me a Soccer ball from Amazon

Press enter or click to view image in full size

Buying task (Created by

[Fareed Khan](<https://medium.com/u/b856005e5ecd?source=post_page---user_mention--288f7ad97169--------------------------------------->)

)

For the buying task, it opens Chrome, searches for **“Soccer Ball Amazon”** selects the first link, and adds the first item to the cart.

We can, of course, make the prompt more descriptive for example, specifying a price limit but that would require upgrading our code accordingly.

> Clone this <My GitHub Repo link>

When I ask it to clone one of my GitHub repositories, it fails. Instead, it randomly clicks on different search boxes, navigates to unrelated sites, and does not reach the intended goal.

Press enter or click to view image in full size

Incorrect Action(Created by

[Fareed Khan](<https://medium.com/u/b856005e5ecd?source=post_page---user_mention--288f7ad97169--------------------------------------->)

)

## Use OmniParser + OmniTool

Though you can modify my code, a more powerful and advanced approach is to use **OmniParser** with **OmniTool** , which you can find in the [OmniParser GitHub repository](<https://github.com/microsoft/OmniParser/tree/master/omnitool>).

It is based on the OpenAI API, and the desktop environment will be virtual, not your actual environment, for safety reasons. This approach is more developed and fully functional, you should check it out.

In fact, one developer even customized it for the open-source LLM **Qwen 2.5 Vision Model** for those who prefer not to use OpenAI.

Qwen 2.5 Vision Model Omnitool Repo:

## [GitHub - OminousIndustries/OmniParserLocal: A simple screen parsing tool towards pure vision based…A simple screen parsing tool towards pure vision based GUI agent - OminousIndustries/OmniParserLocalgithub.com](<https://github.com/OminousIndustries/OmniParserLocal?source=post_page-----288f7ad97169--------------------------------------->)

> Happy Reading!

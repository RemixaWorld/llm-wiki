---
domain: ai.gopubby.com
fetch_date: '2026-05-18T12:55:21.207539'
status: ok
url: https://ai.gopubby.com/building-an-agentic-object-detection-pipeline-34e1f3a47323
---

# Building an Agentic Object Detection Pipeline

## Implementing an agentic workflow for object detection

[ ![Anand Subramanian](https://miro.medium.com/v2/resize:fill:64:64/1*IfxBBsal-XaXfAXh_c9g1A.jpeg) ](<https://medium.com/@anand.subu10?source=post_page---byline--34e1f3a47323--------------------------------------->)

[Anand Subramanian](<https://medium.com/@anand.subu10?source=post_page---byline--34e1f3a47323--------------------------------------->)

23 min read

·

Jun 23, 2025

\--

Listen

Share

More

**Written by**[**Anand Subramanian**](<https://www.linkedin.com/in/anand-subu/>)

**Implemented by**[**Anand Subramanian**](<https://www.linkedin.com/in/anand-subu/>)**and**[**Bharath Sripathy**](<https://www.linkedin.com/in/bharath-sripathy-866666156/>)

Andrew NG shared a [post](<https://www.linkedin.com/posts/andrewyng_introducing-agentic-object-detection-given-activity-7293302466249441280-GxAl?utm_source=share&utm_medium=member_desktop>) a couple of months back, where he introduced “**Agentic Object Detection** ” — a system that takes a text description from the user, and detects the objects in an agentic fashion.

## [Introducing Agentic Object Detection! | Andrew NgIntroducing Agentic Object Detection! Given a text prompt like "unripe strawberries" or "Kellogg's branded cereal" and…www.linkedin.com](<https://www.linkedin.com/embed/feed/update/urn:li:ugcPost:7293299270349135873?source=post_page-----34e1f3a47323--------------------------------------->)

This marks a very fascinating period of time. We’re entering an era where agentic workflows are gaining real momentum, driven by multiple factors. Vision-Language Models (VLMs) are not only improving rapidly but also becoming more widespread, reaching a level of reliability that makes them extremely viable for agentic workflows.

## Table of Contents

1. **Introduction**
2. **Implementing Agentic Object Detection****
2.1**. **High Level Design****
2.2.****Verification and Inference Time Compute****
2.3.****Why Extra Compute**
3. **Pipeline Implementation****
3.1.****VLM Tool****
3.2.****Agentic Object Detection Pipeline****
3.3.****Running the Object Detector****
3.4.****Why Numbered Batching for Inferencing****
3.5.****Critiquing and Refining the Query****
3.6.****Validating Bounding Box Predictions utilizing the VLM**
4. **Results**
5. **Conclusion**
6. **References**

## Introduction

Traditionally, computer vision tasks such as image classification, object detection, and semantic segmentation have been framed as closed-set problems, with models restricted to recognizing only the classes they were trained on. Even as deep learning with CNNs pushed performance forward, adapting to new domains or recognizing unseen objects still required retraining or fine-tuning.

A major shift occurred with the advent of transformer-based architectures, particularly CLIP (Contrastive Language-Image Pretraining) [1]. By jointly training text and image encoders on hundreds of millions of captioned pictures, CLIP learned a shared representation space for images and text. Since both modalities exist in the same embedding space, you can prompt the model with arbitrary text, such as a new class label or a descriptive phrase and CLIP can associate it with relevant visual features, even if the model has never encountered that exact object or phrase during training.

CLIP’s image‒text pre-training enabled **open-vocabulary detection and segmentation**. Models like **DINO [2]** and **OWL-ViT [3]** can localize phrases such as “blue recycling bin” or “stop sign with graffiti” without retraining. Successive efforts merged perception with text. Multimodal LLMs (GPT-4V [4] , Gemini [5] , Claude-Sonnet [6]) took CLIP-like image encoders and trained them with a text decoder, to enable multimodal capabilities. The shift from fixed-category CV models to adaptable VLM-based systems is driving agentic frameworks. Instead of manual label engineering or retraining, developers can handle diverse tasks through simple language commands. Agents can be directed in real time to detect objects, segment regions, or interpret scenes beyond their training data. This approach removes the constraints of traditional label-based methods, allowing vision tasks to be combined and adjusted in real time.

OpenAI’s recently-released **o3** model [7] (the one available through the UI) realizes this paradigm as a fully agentic vision system. Beyond generating bounding boxes directly, o3 can autonomously call external tools, such as writing Python code to zoom, rotate, or adjust contrast on an image, launch a web search for additional context, feed the results back into its own reasoning, and iterate. This capability is a big step toward truly autonomous computer-vision agents that mix perception, tool use, and iterative self-critique in a single inference pass.

## Implementing Agentic Object Detection

In this blog post, we describe how we can build an agentic object detection framework leveraging open-vocabulary object detectors in tandem with VLMs as critiques and verifiers.

### High Level Design

Press enter or click to view image in full size

Agentic Object Detection Workflow (Image by Author)

We begin with an open-set object detector that takes an image and a user-provided text prompt describing the object(s) to identify.

1. **Concept Inference:** Given a user-uploaded image and request, we first use a VLM (GPT-4o [8]) to infer relevant object concepts. If specific objects are mentioned in the request, those are extracted directly. Otherwise, the VLM identifies all salient objects visible in the image.
2. **Initial Detection:** The inferred object concepts are passed to an open-set object detector (Grounding DINO [9]) to generate bounding boxes.
3. **Visualization:** Detected objects are annotated on the image with arrows and unique numeric labels, padded with a white border for clarity.
4. **Query Critique and Refinement:** This annotated image, along with the extracted concepts and original user request, is analyzed by a VLM reasoner (OpenAI’s o1 [10]) using Chain-of-Thought reasoning. If misclassifications or low-level labels are detected, the model refines object categories to higher-level abstractions (e.g., “poodle” → “dog”, “cricketers” → “people”, “bats” → “bat”).
5. **Refined Detection:** These revised concepts are provided back into the object detector along with the original image to produce updated bounding boxes.
6. **Final Filtering:** The updated detections are annotated again. This final image is reviewed by a VLM (GPT-4o) using Chain-of-Thought reasoning to filter out irrelevant detections, keeping only those aligned with the user’s intent.
7. **Output:** The result is a final image annotated with validated bounding boxes that correspond precisely to the user’s request.

### Verification and Inference Time Compute

LLMs and VLMs can serve as critics to inspect and verify outputs from primary models, which are often less capable, thereby enhancing the overall quality of results. Additionally, researchers have explored methods that allow models more computational resources at inference time, referred to as **inference-time compute** or **test-time compute** , enabling them to “think longer” through approaches such as multi-step Chain-of-Thought reasoning and self-consistency sampling. An important characteristic of inference-time compute is that it does not involve any updates to the model’s weights.

Our pipeline integrates these two ideas. After the first open-set detection pass, we perform two successive verification steps driven by a VLM reasoner and a detection step:

**Validation & Abstraction (Step 4): **The VLM reviews every bounding box and its label on an annotated image. When it finds misclassifications or overly specific categories, it suggests higher-level abstractions, (poodle → dog, cricketers → people _)_ and refinements to the original query. This is one full forward pass of reasoning.

**Refined Detection (Step 5):** With the corrected concept list in hand, the system reruns the detector on the original image. This second localization pass consumes more compute but potentially leads to better recall due to playing to the strenghts of open-vocabulary models in recognizing more coarse categories.

**Final Filtering (Step 6):** A final reasoning pass utilizing a VLM cross-checks the updated detections against the user’s explicit request, discarding boxes that are still irrelevant.

### Why Extra Compute

1. **Model-Agnostic Gains:** Since verification happens only at inference, newer detectors or reasoners can drop in with no retraining or extra data collection. The improvement comes purely from extra compute.
2. **Explainability & Debuggability**: Chain-of-Thought logs reveal why a prediction was rejected, providing insights for developers and stakeholders.

By explicitly allocating **inference-time compute for verification and critique** , the pipeline turns raw open-set detection into an agentic system that aims for user-aligned, high-precision results without collecting new data or retraining models.

## Pipeline Implementation

_All code and resources used in this blog post are available at this_[ _link on github_](<https://github.com/anand-subu/implementing_agentic_object_detection>) _with a mirror of the repo available in my original_[ _blog-related repository_](<https://github.com/anand-subu/blog_resources>) _._

To implement the pipeline, we first begin by implementing a functionality to extract high-level concepts or objects present in the image provided by the user.

### VLM Tool

In order to send images to the OpenAI VLMs through the API, we need to encode them as b64 strings. We implement a helper function for that:

```python import base64def encode_image(image_path): """ Encodes an image file into a base64-encoded string. Args: image_path (str): Path to the image file to be encoded. Returns: str: Base64-encoded string of the image content. None: If an error occurs during encoding. Raises: Exception: If the file cannot be opened or encoded. """ try: with open(image_path, "rb") as image_file: return base64.b64encode(image_file.read()).decode("utf-8") except Exception as e: print(f"Error encoding image: {e}") return None ```

We first implement**VLMTool** as a lightweight wrapper around the OpenAI API to interact with the VLMs.

```python import base64import jsonfrom openai import OpenAIfrom utils.image_utils import encode_imageclass VLMTool: def __init__(self, api_key): pass def chat_completion(self, messages, model="o1", max_tokens=300, temperature=0.1, response_format=None): pass def extract_objects_from_request(self, image_path, user_text, model="gpt-4o"): pass ```

We implement a core method, `chat_completion`, which forwards a list of messages to the selected model—such as `gpt-4o` or `o1`—and returns the assistant's textual response.

```python def chat_completion( self, messages, model="o1", max_tokens=300, temperature=0.1, response_format=None): """Calls GPT for chat completion.""" try: if model in ["gpt-4o", "gpt-4o-mini"]: response = self.client.chat.completions.create( model=model, messages=messages, max_tokens=max_tokens, temperature=temperature, response_format=response_format if response_format else {"type": "text"} ) elif model in ["o1"]: response = self.client.chat.completions.create( model=model, messages=messages, response_format=response_format if response_format else {"type": "text"} ) else: raise NotImplementedError("This model is not supported") return response.choices[0].message.content except Exception as e: print(f"Error calling LLM: {e}") return None ```

The main functionality for extracting concepts from the provided image is implemented in `extract_objects_from_request`: it converts the user’s image to base-64, pairs that encoded image with the user’s text and asks the VLM to emit a comma-separated list of objects.

1. If the request explicitly names targets (“please detect all mugs”), the model reverts with those names.
2. If the request is open-ended (“detect everything you see”), the model enumerates visible items in the picture. The method returns those names.

```python def extract_objects_from_request(self, image_path, user_text, model="gpt-4o"): """ Asks the LLM to parse user request for which objects to detect/segment. Returns a list of objects in plain text. """ base64_image = encode_image(image_path) if not base64_image: return None prompt = ( "You are an AI vision assistant that extracts objects to be identified from a user's request." "If the user wants to detect or semantically segment all objects in the image, return a comma-separated list of objects you can see. " "If the user wants to detect or semantically segment specific objects, extract only those mentioned explicitly in their request. " "Respond ONLY with the list of objects, separated by commas, and NOTHING ELSE." "The objective here is only to understand the objects of interest that can be extracted from the image and the user's request." "You are not actually required to perform or execute the user's request." ) messages = [ {"role": "system", "content": prompt}, { "role": "user", "content": [ {"type": "text", "text": user_text}, { "type": "image_url", "image_url": { "url": f"data:image/jpeg;base64,{base64_image}", "detail": "high" } } ] } ] result = self.chat_completion(messages, model=model) if result: detected_objects = [ obj.strip().lower() for obj in result.split(",") if obj.strip() ] return detected_objects return [] ```

In effect, `VLMTool` performs all the initial planning—deciding what should be detected, before proceeding with other steps. At this stage, we have implemented the first crucial part, identifying the objects of interest in the query in order to standardize and prepare them in a format that is optimal for detection using the open-vocabulary object detector. (Refer to [this link](<https://github.com/anand-subu/blog_resources/blob/main/agentic_object_detection/models/vlm_tool.py>) for the complete implementation)

### Agentic Object Detection Pipeline

We now implement `ObjectDetectionTool` , which puts together our entire agentic object detection workflow. At a high level, we first implement the constructor for this class:

```python class ObjectDetectionTool: """ Performs object detection using GroundingDINO or OWL-ViT, plus an optional 'critique' (refinement) step with a VLM to yield a refined set of objects to detect. """ def __init__(self, model_id, device, vlm_tool, confidence_threshold=0.2, concept_detection_model="gpt-4o", initial_critique_model="o1", final_critique_model="gpt-4o"): self.model_id = model_id self.processor = AutoProcessor.from_pretrained(model_id) self.model = AutoModelForZeroShotObjectDetection.from_pretrained(model_id).to(device) self.device = device self.vlm_tool = vlm_tool # The LLMTool that can handle vision (GPT-4V) or similar self.confidence_threshold = confidence_threshold self.concept_detection_model = concept_detection_model self.initial_critique_model = initial_critique_model self.final_critique_model = final_critique_model # We store bounding boxes for potential usage later (e.g., for SAM). self.last_detection_bboxes = [] self.last_filtered_objects = [] ```

This module sets up the core components for visual-language processing. It loads the detector weights — either Grounding-DINO or OWL-ViT — onto the CPU or GPU (We run with Grounding-DINO for all our cases in this blog). It initializes the language model weights, storing the shared `VLMTool` instance along with the specified LLMs used for the initial and final verification stages. It also configures confidence thresholds for bounding boxes and allocates caches to store the most recent detection results.

### Running the Object Detector

We implement a method `_run_detector` to do the first forward pass using the open-vocab object detector. The pipeline first adapts the prompt to the target model — OWLVIT needs a list such as [“An image of cat”, …], whereas DINO prefers a period-separated string like “cat. dog.”. Next, it executes a forward pass through the transformer under `torch.no_grad()` . The raw, normalized bounding boxes are then converted to pixel coordinates and anything below the confidence threshold is discarded. Finally, arrows and numeric labels are drawn on the image so a language model can later refer unambiguously to objects by, for example, “box #3.” We implement a utility function to draw arrows and boxes as well:

```python def draw_arrows_and_numbers(image_path, detected_objects): """ Draws arrows and numbers on an image to label detected objects. This function dynamically places numbers near the borders with arrows pointing from object centers to the borders. Arrows are dashed for clarity, and the numbering avoids overlap when possible. Args: image_path (str): Path to the input image. detected_objects (list): List of tuples containing object information in the format (number, object_name, bounding_box), where bounding_box is (x1, y1, x2, y2). Returns: str: Path to the saved labeled image ('labeled_objects_optimized.jpg'). Note: - Arrows are drawn from object centers to the nearest border. - Numbers are displayed with semi-transparent backgrounds for readability. """ img = cv2.imread(image_path) font = cv2.FONT_HERSHEY_SIMPLEX used_positions = [] # Pad the image with a white border top, bottom, left, right = 50, 50, 50, 50 img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[255, 255, 255]) height, width, _ = img.shape for i, (num, obj, box) in enumerate(detected_objects): x1, y1, x2, y2 = map(int, box) cx, cy = (x1 + x2) // 2, (y1 + y2) // 2 # Center of the bounding box # Adjust coordinates for padded image x1 += left y1 += top x2 += left y2 += top cx += left cy += top # Determine arrow direction towards the nearest border distances = {'top': cy, 'bottom': height - cy, 'left': cx, 'right': width - cx} direction = min(distances, key=distances.get) if direction == 'top': arrow_end = (cx, top) text_position = (cx - 10, top - 10) elif direction == 'bottom': arrow_end = (cx, height - bottom) text_position = (cx - 10, height - 5) elif direction == 'left': arrow_end = (left, cy) text_position = (left - 30, cy + 5) else: arrow_end = (width - right, cy) text_position = (width - 30, cy + 5) # Draw the dashed arrow from the object center to the border color = (0, 0, 0) # Black color for all arrows line_type = cv2.LINE_4 cv2.arrowedLine(img, (cx, cy), arrow_end, color, 2, tipLength=0.3) # Draw a semi-transparent rectangle behind the text overlay = img.copy() cv2.rectangle(overlay, (text_position[0] - 5, text_position[1] - 20), (text_position[0] + 30, text_position[1] + 5), (0, 0, 0), -1) alpha = 0.5 cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img) # Draw the number at the border with black text cv2.putText(img, str(num), text_position, font, 0.8, color, 2) labeled_image_path = "labeled_objects_optimized.jpg" cv2.imwrite(labeled_image_path, img) return labeled_image_path ``` ```python def _run_detector(self, image_path, query_list): """ Low-level routine to run the detection model on `query_list`. Returns: (detected_objects_final, labeled_image_path) Where `detected_objects_final` = [(num, label, [x1,y1,x2,y2]), ...]. """ from PIL import ImageFont # Format queries for the model if INV_MODEL_TYPES[self.model_id] == "owlvit": formatted_queries = [f"An image of {q}" for q in query_list] elif INV_MODEL_TYPES[self.model_id] == "grounding_dino": formatted_queries = " ".join([f"{q}." for q in list(set(query_list))]) else: raise NotImplementedError("Model not supported") # Load image img = Image.open(image_path).convert("RGB") inputs = self.processor( text=formatted_queries, images=img, return_tensors="pt", padding=True, truncation=True ).to(self.device) self.model.eval() with torch.no_grad(): outputs = self.model(**inputs) # Post-process bounding boxes if INV_MODEL_TYPES[self.model_id] == "grounding_dino": results = self.processor.post_process_grounded_object_detection( outputs, inputs.input_ids, box_threshold=0.4, text_threshold=0.3, target_sizes=[img.size[::-1]] ) boxes = results[0]["boxes"] scores = results[0]["scores"] labels = results[0]["labels"] elif INV_MODEL_TYPES[self.model_id] == "owlvit": # OWL-ViT logits = torch.max(outputs["logits"][0], dim=-1) scores = torch.sigmoid(logits.values).cpu().numpy() labels = logits.indices.cpu().numpy() boxes = outputs["pred_boxes"][0].cpu().numpy() else: raise NotImplementedError("Model not supported") detected_objects_final = [] idx = 1 for score, box, label_idx in zip(scores, boxes, labels): if score < self.confidence_threshold: continue detected_objects_final.append((idx, label_idx, box.tolist())) idx += 1 # Draw numbers labeled_image_path = draw_arrows_and_numbers(image_path, detected_objects_final) return detected_objects_final, labeled_image_path ```

### Why Numbered Batching for Inferencing

The most straightforward way to verify detections is to treat **every bounding box as an independent task**. After the detector fires, the pipeline would loop over the _n_ boxes it produced and perform the following sequence for **each** box:

1. **Isolate the crop:** Extract the rectangular region defined by the box and/or draw a bounding box around the candidate object.
2. **Base-64 encode that crop:** Encode and send**** the new image as its own `data:image/jpeg;base64,…` string.
3. **Compose a dedicated prompt:** Write a prompt that embeds the image and asks a VLM something like: _“Does the bounding box in the image contain a mug? Answer ‘yes’ or ‘no’.”_
4. **Send the prompt to the VLM:** The model runs a full forward pass — parsing the prompt, decoding the image, and producing a textual verdict.
5. **Parse and act on the result:** If the model answers “no,” discard the box; otherwise keep it.

The loop repeats until every box has been checked. In a busy scene the detector may return dozens of boxes, so the verifier must run dozens of times.

The downside of this approach is the **processing, costs and latency overhead**. Each crop triggers a fresh API call, image upload, and model forward pass. Twenty-five detections mean twenty-five calls, which is twenty-five times the latency and token/image-billing cost.

Numbered-arrow annotation sidesteps all those drawbacks by converting the verification phase into **one single, context-rich VLM pass**. Annotating every detection with a numbered arrow, then handing **one** composite image to the language model, pays off in three interconnected ways — speed, cost, and reasoning quality.

**1\. Faster processing and scaling:** By overlaying arrows and numbers on a single canvas, the pipeline sends just one image and one prompt, slashing the verification bill and the overall processing time.**This works as a batch processing mechanism.** In high-object scenes, batching keeps verification time roughly constant even as detections climb. The only marginal cost is drawing a few extra arrows, which is negligible compared to additional detector or LLM passes.

**2\. Deterministic, reference-friendly IDs:** Arrows with stable numbers act as **primary keys** across the pipeline. The LLM can say “Boxes 3 and 6 are irrelevant,” the code can filter on the exact integers, and a human can glance at the picture and see those numbers. If you relied on textual descriptions alone (“the blue cup under the spoon”) you’d face brittle string matching or error-prone heuristics. Numeric IDs make the hand-off between vision code and language model lossless.

**3\. Better use of the LLM’s visual token budget:** VLMs have a finite resolution budget — often a single image plus a few thousand text tokens. Arrows barely cover any area, so they preserve the original detail while still giving the model explicit pointers.

In a nutshell, the brute-force crop loop is simple but computationally and financially inefficient, while the arrow-batching enables faster and cheaper processing through efficient use of the VLM’s context window.

### Critiquing and Refining the Query

The LLM is shown the current detections along with the user’s text, and asked whether the concepts are too narrow. If so, it suggests broader terms (“dog” instead of “teacup poodle”) as a comma-separated list. This step trades compute for robustness: it uses another LLM pass and reruns the detector only if the list changes, deliberately spending more compute when the verifier flags the initial attempt as insufficient.

```python def _critique_and_refine_query(self, user_request, original_concepts, labeled_image_path, objects_detected, model="o1"): """ Asks the VLM/LLM: "We tried to detect <objects_detected> for the user request, but maybe we need a refined set of objects. Return a new list of objects or concepts to detect." """ base64_labeled_image = encode_image(labeled_image_path) # For clarity, let's pass the original user request and # the currently detected object list to the LLM. # The LLM can propose a refined set of objects to detect. refine_messages = [ { "role": "system", "content": """ You are an AI system that refines detection queries. You are provided with the outputs from an object detection model, along with the user's request and the objects from the user's request that were extracted and provided to the object detection model. Your task is to analyze whether the object detector has extracted the results properly to the user's request and, if not, refine the queries by generalizing concepts where possible. Important guidelines: 1. If the detection results are already good, no need to refine. - In that case, provide reasoning indicating no refinement was necessary and return the same list. 2. If the detection results are poor or null, propose synonyms or more generic categories and explain why. Wherever possible, retain the singular version of the concept. 3. Return your final answer as a JSON object with exactly two fields: "reasoning" and "refined_list". - "reasoning" is a short explanation of why you refined or didn't refine. - "refined_list" is a comma-separated list of object names that should be re-tried in detection. 4. Output ONLY the JSON, and no other text. Below are some examples: EXAMPLE 1 User's Request: Detect the teacup poodle Original concept: "Teacup poodle" Final output: { "reasoning": "The provided image does not have any detections for the concept of teacup poodle. The concept "teacup poodle" might be a very specific concept for the model to detect. This could be refined to a more higher-level and generic concept like 'Dog', "refined_list": "dog" } EXAMPLE 2 User's Request: Detect the sparkly stiletto shoe Original concept: "Sparkly stiletto shoe" Final output: { "reasoning": "The provided image does not specific detections that correspond for 'Sparkly stiletto shoe'. 'Sparkly stiletto shoe' might be too specific for the model. Refining to 'shoe', a more generic concept might increase the likelihood of detection.", "refined_list": "shoe" } EXAMPLE 3 User's Request: Detect the hydrangea Original concept: "Hydrangea" Final output: { "reasoning": "No detections found for 'hydrangea'. The model might struggle with specific flower types. Refining to the more general concept 'flower' could yield better results.", "refined_list": "flower" } EXAMPLE 4 User's Request: Detect the gourmet cheeseburger Original concept: "Gourmet cheeseburger" Final output: { "reasoning": "No detections observed for 'Gourmet cheeseburger'. 'Gourmet cheeseburger' might be too specific. Refining to 'hamburger' as it aligns with the detected object.", "refined_list": "hamburger" } EXAMPLE 5 User's Request: Detect the red sports car Original concept: "Red sports car" Final output: { "reasoning": "The provided image does not have any reliable detections for 'red sports car'. Color-based detection might be challenging. Refining to the more general concept 'car' could improve detection.", "refined_list": "car" } Remember: • If no refinement is needed (the concept is recognized well), explain that in the reasoning and return the same concept. • When refinement is necessary, prioritize more generic or abstract categories that may be more reliably detected by the model. • Provide only the JSON. • No extra commentary. """ }, {"role": "user", "content": [ {"type": "text", "text": f"User's request: {user_request}
Original Concepts for Detection: {original_concepts}"}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_labeled_image}", "detail": "high"}} ]} ] refine_response = self.vlm_tool.chat_completion(refine_messages, model=model, response_format={"type": "json_object"}) refined_response_objects = json.loads(refine_response)["refined_list"].split(",") if not refined_response_objects: return [] refined_list = [r.strip().lower() for r in refined_response_objects if r.strip()] return refined_list ```

Generally open-vocabulary detectors can recognise only a few hundred **coarse-grained classes** — “dog,” “car,” “flower” — yet users often ask for far more **fine-grained** targets: teacup poodle, sparkly stiletto shoe __ etc. When the requested label is outside the detector’s comfort zone, the model may return nothing or a batch of low-confidence boxes.

During the **critique and refine stage** , the LLM receives three things at once: the user’s original text, the arrow-annotated image, and the exact concept list that was passed to the detector. It then reasons: “Did the detector find anything meaningful under these labels? If not, are the labels simply **too specific**?” Whenever that is the case, the LLM deliberately **abstracts** each concept upward to the next higher concept, ex: sub-breed becomes breed (_teacup poodle → dog_), elaborate colour concepts are stripped away (_bright-red vintage sports car → car_). The model returns these higher-level categories as a comma-separated string.

Only if the refined list **differs** from the original does the pipeline pay for a second detector pass, where we run the object detector again with the refined categories. That means extra inference-time compute is spent **selectively** , precisely when the first attempt failed to bridge the gap between the user’s intent and the detector’s vocabulary. In short, the LLM maps the user’s request to categories more familiar with the detector, providing another shot at obtaining outputs through calling the object detector a second time.

### Validating Bounding Box Predictions utilizing the VLM

The arrow-annotated image is encoded and passed to a language model, which is prompted to accept or reject each numbered box based on the user’s request. The output must be strict JSON (e.g., {“3”: “cup”, “5”: “teapot”}) to ensure deterministic parsing. This marks the next verification step, utilizing the VLM to filter the detector’s outputs**.**

```python def _validate_bboxes_with_llm(self, user_request, labeled_image_path, model="o1"): """ Pass the labeled image to the LLM to filter bounding boxes based on user request. Returns 'valid_numbers' list. """ base64_labeled_image = encode_image(labeled_image_path) messages = [ {"role": "system", "content": "You are an AI reviewing an object detection output.
" "All detected objects have been marked with an arrow mapping to a corresponding number.
" "The image contains arrows labeled with numbers pointing to specific objects.
" "Your task is to identify the objects indicated by these arrows and determine whether each detected object is relevant to the user's query.
" "For each numbered arrow:
" "1. Identify the object being pointed to.
" "2. Provide a brief description of the object (e.g., 'top-left cup with blue leaves', 'bottom-right cup with watermelon pattern', or 'background birdcage').
" "3. Analyze whether the object is valid based on the context and the user's instructions.
" "4. Provide a clear, step-by-step explanation for each object's validity decision.
" "Return a JSON object with the reasoning and list of valid numbers matching the user's request.
" "Example output:
" "{ "reasoning": <reasoning> , "valid_numbers": {object_num :"object_name"} }" }, {"role": "user", "content": [ {"type": "text", "text": f"The user's original request was: {user_request}"}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_labeled_image}", "detail": "high"}} ] } ] valid_numbers_json = self.vlm_tool.chat_completion( messages, model=model, response_format={"type": "json_object"} ) try: valid_numbers_data = json.loads(valid_numbers_json) return valid_numbers_data.get("valid_numbers", {}) except json.JSONDecodeError: return [] ```

After the refined concept list runs through the object detector a second time, the pipeline now moves to checking the predictions. The new bounding boxes are drawn onto the original frame, each marked with its own arrow and index. Rather than sending every crop separately, the entire arrow-labeled image is base-64 encoded and passed to the language model in one payload.

The verification step focusses on a narrow task: Does box 7, exactly as shown, fulfill the user’s request? The prompt compels the model to answer with a strict JSON map like {“3”: “cup”, “5”: “teapot”}. The integers align deterministically with the arrow numbers, letting the code accept or reject boxes without any ambiguity or fuzzy matching.

In short, the two VLM steps operate back-to-back: the first stage rewrites the user’s query to align more with the detector’s vocabulary when the first set of predictions for the initial query are not satisfactory, and the second stage reviews and filters the predictions of the model to provide the final outputs.

The final predictions obtained from this step are then drawn as bounding boxes back on the image. Putting together the complete flow, this is our final implementation:

```python def run(self, image_path, user_request, do_critique=True): """ Full pipeline: 1. Extract objects from user request (LLM). 2. Detect bounding boxes with that query. 3. LLM-based validation step => filter bounding boxes. 4. (Optional) Critique Step => refine the query if needed. 5. Re-run detection with refined queries. 6. Final LLM validation => final bounding boxes and annotation. """ # --------------------------------------------------- # Step 1: initial user queries from request # --------------------------------------------------- objects_to_detect = self.vlm_tool.extract_objects_from_request(image_path, user_request, model=self.concept_detection_model) if not objects_to_detect: return None, "⚠️ No objects to detect or invalid request." # --------------------------------------------------- # Step 2: run detection with the initial user queries # --------------------------------------------------- detected_objects_final, labeled_image_path = self._run_detector(image_path, objects_to_detect) # ------------------------------------------------------ # Step 3: Initial Critique and Object Concept Refinement # ------------------------------------------------------ if do_critique: current_labels = ",".join(set([str(lbl) for _, lbl, _ in detected_objects_final])) refined_query_list = self._critique_and_refine_query( user_request=user_request, original_concepts=current_labels, labeled_image_path=labeled_image_path, objects_detected=current_labels, model=self.initial_critique_model ) # If the refined list is empty or identical, we might skip re-running # But let's suppose we only re-run if we actually get a new set. if refined_query_list and set(refined_query_list) != set(objects_to_detect): # Re-run detection with refined query detected_objects_final, labeled_image_path = self._run_detector(image_path, refined_query_list) if not detected_objects_final: return None, "No objects found for the initial query." # --------------------------------------------------- # Step 4: LLM-based critique # --------------------------------------------------- valid_numbers = self._validate_bboxes_with_llm(user_request, labeled_image_path, model=self.final_critique_model) # filter bounding boxes if valid_numbers: filtered_objects = [(n, valid_numbers[str(n)], box) for (n, lbl, box) in detected_objects_final if str(n) in valid_numbers] else: filtered_objects = detected_objects_final # store them self.last_detection_bboxes = [x[-1] for x in filtered_objects] self.last_filtered_objects = filtered_objects # --------------------------------------------------- # Step 5: Produce final annotated image # --------------------------------------------------- final_img = draw_bounding_boxes(image_path, filtered_objects) final_text = ( f"🔍 Validated objects: {', '.join(set(str(lbl) for _, lbl, _ in filtered_objects))}" ) return final_img, final_text ```

The complete implementation of this class is provided in [this link](<https://github.com/anand-subu/blog_resources/blob/main/agentic_object_detection/models/object_detection_tool.py>).

## Results

We implement this functionality and expose it through a Gradio app. We demonstrate the working of this pipeline with the help of a sample image. We utilize the prompt “Detect the top left ipod and bottom right iphone.” to test the detection capabilities of our agent. The pipeline extracts those two device concepts, runs the detector, lets the LLM broaden or refine if necessary, and finally verifies each numbered box.

Press enter or click to view image in full size

Gradio Interface for the Agentic Object Detection Pipeline. Photo used in this demo taken by [Tron Le](<https://unsplash.com/@tronle_sg?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash>) on [Unsplash](<https://unsplash.com/photos/white-iphone-5s-and-black-iphone-5-FctyNl5YCbs?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash>). (Overall image by author)

Press enter or click to view image in full size

Press enter or click to view image in full size

Top Left: Input Image, Top Right: Detections from the Open-vocab Object Detector. Photo used in this demo taken by [Tron Le](<https://unsplash.com/@tronle_sg?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash>) on [Unsplash](<https://unsplash.com/photos/white-iphone-5s-and-black-iphone-5-FctyNl5YCbs?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash>). (Images by Author)

Press enter or click to view image in full size

Press enter or click to view image in full size

Bottom Left: Detected Images with arrows and numbers (numbered batching), Bottom Right: Final Filtered Detections utilizing the VLM. Photo used in this demo taken by [Tron Le](<https://unsplash.com/@tronle_sg?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash>) on [Unsplash](<https://unsplash.com/photos/white-iphone-5s-and-black-iphone-5-FctyNl5YCbs?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash>). (Images by Author)

This example highlights the one of the pipeline’s key advantage: **directional precision**. The open-vocab detector already excels at spotting iPhones and iPods, delivering high recall already. The VLM then reasons over the whole, arrow-annotated image and pinpoints only the devices that match the user’s spatial instructions. By filtering detections through this global, context-aware check, the system enables high precision, returning exactly the objects the prompt calls for.

We also demonstrate the strengths of this pipeline with a second example. We utilize an image with two coffee cups, each with foam art. We prompt the agentic system to detect only the coffee cup with the foam art “Coffee Chat?”.

Press enter or click to view image in full size

Gradio Interface for the Agentic Object Detection Pipeline. Photo utilized for this demo taken by [Frank Leuderalbert](<https://unsplash.com/@frank_leuderalbert?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash>) on [Unsplash](<https://unsplash.com/photos/blue-ceramic-cup-with-saucer-on-table-RTVYnQsLgZ0?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash>). (Overall image by author)

Press enter or click to view image in full size

Press enter or click to view image in full size

Top Left: Input Image, Top Right: Detections from the Open-vocab Object Detector. Photo utilized for this demo taken by [Frank Leuderalbert](<https://unsplash.com/@frank_leuderalbert?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash>) on [Unsplash](<https://unsplash.com/photos/blue-ceramic-cup-with-saucer-on-table-RTVYnQsLgZ0?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash>). (Images by Author)

Press enter or click to view image in full size

Press enter or click to view image in full size

Bottom Left: Detected Images with arrows and numbers (numbered batching), Bottom Right: Final Filtered Detections utilizing the VLM. Photo utilized for this demo taken by [Frank Leuderalbert](<https://unsplash.com/@frank_leuderalbert?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash>) on [Unsplash](<https://unsplash.com/photos/blue-ceramic-cup-with-saucer-on-table-RTVYnQsLgZ0?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash>). (Images by Author)

This scenario showcases another strength of the agentic pipeline: **identifying objects that contain readable text.** In the top-right example, the detector correctly flags both coffee mugs, achieving high recall. However, only one mug contains the foam art specified by the user’s prompt. Since the VLM reviews the entire arrow-annotated image and can understand the text printed on each mug, it filters out the irrelevant cup and keeps the prediction that matches the query. This text-aware reasoning, which is absent in the object detector, helps in obtaining targeted and precise results.

## Conclusion

Agentic Object Detection offers a powerful and flexible framework for obtaining targeted object detection results. In this blog post, we demonstrated how an open-vocabulary detector like Grounding DINO can be augmented with an agentic layer powered by VLMs. This agent not only interprets and refines the user’s request, but also critiques and verifies the detector’s outputs in context, leading to more precise, user-aligned results. By combining detection with reasoning, the system moves beyond simple object spotting towards more targeted visual understanding.

A key limitation of the current pipeline is that it can only detect what the underlying open-vocabulary detector already knows. If a user requests a class the detector cannot recognise, such as a specific flower or a new gadget, no amount of VLM reasoning in the current pipeline can help, as the current pipeline utilizes VLMs only for reviewing and critiquing the results of the initial object detector. By contrast, the VLMs, such as OpenAI’s **o3,** Google Gemini**** and other research models, can generate bounding boxes directly as part of their multimodal output. Rather than relying on separate systems for separate tasks, capabilities like object detection are increasingly being baked in to existing VLMs during their training phase.

## References

[1] Radford, Alec, et al. “Learning transferable visual models from natural language supervision.” _International conference on machine learning_. PmLR, 2021.

[2] Zhang, Hao, et al. “Dino: Detr with improved denoising anchor boxes for end-to-end object detection.” _arXiv preprint arXiv:2203.03605_ (2022).

[3] Minderer, Matthias, et al. “Simple open-vocabulary object detection.” _European conference on computer vision_. Cham: Springer Nature Switzerland, 2022.

[4] <https://openai.com/index/gpt-4v-system-card/>

[5] <https://storage.googleapis.com/model-cards/documents/gemini-2.5-pro-preview.pdf>

[6] <https://www.anthropic.com/claude/sonnet>

[7] <https://openai.com/index/introducing-o3-and-o4-mini/>

[8] <https://openai.com/index/hello-gpt-4o/>

[9] Liu, Shilong, et al. “Grounding dino: Marrying dino with grounded pre-training for open-set object detection.” _European Conference on Computer Vision_. Cham: Springer Nature Switzerland, 2024.

[10] <https://openai.com/o1/>

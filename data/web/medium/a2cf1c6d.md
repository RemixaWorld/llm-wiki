---
domain: blog.stackademic.com
fetch_date: '2026-05-18T12:47:40.504546'
status: ok
url: https://blog.stackademic.com/multimodal-cpp-4you-be527a827ebf
---

# MultiModal-CPP-4you

## Run a Visual Language Model on your Laptop in 10 minutes with the powers of Llama.cpp. No GPU required.

[ ![Fabio Matricardi](https://miro.medium.com/v2/resize:fill:64:64/1*p4ShYlP7zymOUeIZ5DSbfg.png) ](<https://medium.com/@fabio.matricardi?source=post_page---byline--be527a827ebf--------------------------------------->)

[Fabio Matricardi](<https://medium.com/@fabio.matricardi?source=post_page---byline--be527a827ebf--------------------------------------->)

13 min read

·

May 14, 2024

\--

Listen

Share

More

Press enter or click to view image in full size

image created by the author

In the past moths a relevant focus has shifted toward Multi-Modal Language Models.

Visual Language Models refer to artificial intelligence systems that can understand, process, and generate text based on visual information. These models combine the capabilities of natural language processing (NLP) with computer vision to interpret images or videos and then produce relevant descriptions, captions, or even engage in conversations about the visual content.

These Artificial Intelligence Models are quite heavy, but what if I tell you there is a way to run and test them even on an average Laptop?

What if we can start using them to prepare our data or to power up our applications?

> There is a way, and here is how it is done.

## What are Visual Language Models

Visual Language Models often use deep learning architectures, such as convolutional neural networks (CNNs) for image analysis and recurrent neural networks (RNNs), transformers, or their variants for natural language generation and understanding.

These models are trained on large datasets that pair visual data with corresponding text annotations to learn how to connect visual elements with their linguistic descriptions.

We may want to use Visual Language Models for specific tasks, like for example:

1. Image Captioning: Generating descriptive captions for images, understanding the objects, actions, and context within an image.
2. Visual Question Answering (VQA): Answering questions based on the content of an image or video, requiring both comprehension of the question and the ability to analyze the visual data.
3. Visual Dialog: Continuing a conversational dialogue with a user about a specific image or sequence of images, requiring an understanding of previous dialogue turns and the visual context.
4. Scene Graph Generation: Creating a structured representation of an image, including objects, their attributes, and the relationships between them.
5. Image-to-Text Translation: Converting visual content into textual narratives, which could be applied in areas like generating alt-text for accessibility or summarizing complex visual data.
6. Video Understanding: Similar to image analysis but extended to sequences, understanding actions, events, and context over time in videos.

If you want to see a preview of what these models are capable of, you can watch this amazing video from the [Prompt Engineering youtube channel](<https://www.youtube.com/@engineerprompt>). I am a big fan of him, so consider subscribing, because his videos are really well done.

In the past few months generative models with images have pushed the boundaries in their capabilities to assist in creating visual content, and their performance in computer vision tasks such as object detection, segmentation, captioning, and much more. This is exactly what LLaVA can do for us.

Ok, let’s learn how to use these models on our computers.

Further on we will have a look to practical use cases.

## Llama.CPP with Llava models

I will never stop saying that [Llama.cpp](<https://github.com/ggerganov/llama.cpp>) is probably the most important project in the AI community. When [G.Gerganov](<https://github.com/ggerganov>) created [his GitHub repository](<https://github.com/ggerganov/llama.cpp>) to be able to run the Llama models on his Mac, opened the doors to Million of peoples, finally able to run an AI locally.

His first project, `whisper.cpp` started in October 2022: at that time almost no one knew anything about generative AI. `Llama.cpp` started to sky rocket in march 2023 (and you can guess why…)

Press enter or click to view image in full size

number of starts GGerganov repositories by [star-history.com](<https://star-history.com/#ggerganov/llama.cpp&ggerganov/whisper.cpp&Date>)

Just look at these numbers!!! This repository was forked (used be someone else to build another project…) 8.000 times, and other 57.000 other programmers liked it!

Press enter or click to view image in full size

statistics from [GitHub](<https://github.com/ggerganov/llama.cpp>)

Llama.cpp is a software written in pure C/C++ to run inference (generation) on Llama models. The main goal of `llama.cpp` is to enable LLM inference with minimal setup and state-of-the-art performance on a wide variety of hardware - locally and in the cloud.

You can install this really slim repo on basically any device and start chatting with a Language model immediately. As of today you can use llama.cpp on Mac OS, Linux, Windows (via CMake), Docker, FreeBSD and also [on Android](<https://github.com/ggerganov/llama.cpp?tab=readme-ov-file#building-the-project-using-android-ndk>)!

### What you can do with llama.cpp?

The main function of this library is to run chat inference with Language Models. But Gerganov was not happy only with that: so now you can use also Visual Language models, Audio models like Whisper with the twin brother `whisper.cpp`, or even Stable Diffusion models (with sister `[stable-diffusion.cpp](<https://github.com/leejet/stable-diffusion.cpp>)`[, a fork](<https://github.com/leejet/stable-diffusion.cpp>) created from llama.cpp). I already wrote two articles on the last ones: I will put the links at the bottom.

Back to **Visual Language Models: the actual supported Multimodal models by llama.cpp** are:

* [LLaVA 1.5 models](<https://huggingface.co/collections/liuhaotian/llava-15-653aac15d994e992e2677a7e>), [LLaVA 1.6 models](<https://huggingface.co/collections/liuhaotian/llava-16-65b9e40155f60fd046a5ccf2>)
* [BakLLaVA](<https://huggingface.co/models?search=SkunkworksAI%2FBakllava>)
* [Obsidian](<https://huggingface.co/NousResearch/Obsidian-3B-V0.5>)
* [ShareGPT4V](<https://huggingface.co/models?search=Lin-Chen%2FShareGPT4V>)
* [MobileVLM 1.7B/3B models](<https://huggingface.co/models?search=mobileVLM>)
* [Yi-VL](<https://huggingface.co/models?search=Yi-VL>)
* [Mini CPM](<https://huggingface.co/models?search=MiniCPM>)
* [Moondream](<https://huggingface.co/vikhyatk/moondream2>)
* Llava-Phi variants [here ](<https://huggingface.co/marianna13/llava-phi-2-3b>)and [here](<https://huggingface.co/MBZUAI/LLaVA-Phi-3-mini-4k-instruct>)

As you can see, almost all these model have the acronym LLava in it. **LLaVA** (**L** arge **L** anguage-**a** nd-**V** ision **A** ssistant) is an end-to-end trained large multimodal model that connects a vision encoder (multi modal projector) and a LLM for general-purpose visual and language understanding.

The first LLaVA model structure: connects a pre-trained [CLIP ViT-L/14](<https://openai.com/research/clip>) visual encoder and large language model [Vicuna](<https://github.com/lm-sys/FastChat>), using a simple projection matrix. If you never heard about [CLIP you can read more here](<https://openai.com/index/clip>).

Press enter or click to view image in full size

Our textual application — look in [my GitHub Repo](<https://github.com/fabiomatricardi/imageCPP_aka_llamaCPP/tree/main>)

## How to use VLM in Python

Similarly to what we do with LLM, we can use python bindings library to work with Visual Language Models. Honestly, llama.cpp does have really a lot of programming languages support, but for python the absolute best one is [llama-cpp-python](<https://llama-cpp-python.readthedocs.io/en/stable/>).

Press enter or click to view image in full size

[Documentation ](<https://llama-cpp-python.readthedocs.io/en/stable/>)of the[ GitHub repo](<https://github.com/abetlen/llama-cpp-python>) really well done and maintained

So let’s do the usual good thing, and create a new virtual environment: after that we activate it and install the few dependencies we need.

> **NOTE** : this code is tested on Windows 11 computer (MiniPC) with no nVidia GPU and running Python 3.10.

```python # Create Virtual Environmentpython -m venv venv# Activate the Venvvenv\Scripts\activate# Install the libraries pip install llama-cpp-python==0.2.68pip install easygui ```

All of the above will work for everyone… but

### With Nvidia GPU

If you have a NVidia GPU you will have to set the flags for the compiler before calling the pip command:

```python $env:CMAKE_ARGS="-DLLAMA_CUBLAS=on"pip install llama-cpp-python[server]==0.2.62 ```

If you run into issues where it complains it can’t find `'nmake'` `'?'` or CMAKE_C_COMPILER, you can extract w64devkit as [mentioned in llama.cpp repo](<https://github.com/ggerganov/llama.cpp#openblas>) and add those manually to CMAKE_ARGS before running `pip` install:

``` $env:CMAKE_GENERATOR = "MinGW Makefiles"$env:CMAKE_ARGS = "-DLLAMA_OPENBLAS=on -DCMAKE_C_COMPILER=C:/w64devkit/bin/gcc.exe -DCMAKE_CXX_COMPILER=C:/w64devkit/bin/g++.exe" ```

See the above instructions and set `CMAKE_ARGS` to the BLAS backend you want to use.

To build the package with CUDA support remember to have installed the following:

* cuda toolkit for you NVidia GPU
* Visual Studio (with C++ packages)
* CMAKE for windows (you can [download it here](<https://cmake.org/download/>))

### Download the Visual Language Model quantized

Here comes the tricky part. The VLM works differently from a Language model: the multi-modality is achieved through a projection matrix model, called `mmproj`. This model create a sort of embeddings of the image (split in smaller pieces…) and than pass this rich information before the text tokens in the prompt: the same prompt than given to the VLM weights. we learned something about it in the previous section, right?

Why am I telling you all of this? Because we will have to download two different models:

* a mmproj
* a GGUF quantized model

For example, in this test code we are going to use the **LLaVA-Phi-3-mini-4k-instruct** quantized model. What you need to download in your subfolder (mine is called `LLaVA-Phi-3-mini-4k-instruct`) are the following file from [the official GGUF repo](<https://huggingface.co/dragonSwing/LLaVA-Phi-3-mini-4k-instruct-GGUF/tree/main>):

``` llava-phi3-mini-Q4_K_M.ggufand llava-phi3-mini-mmproj-f16.gguf ```

And that’s it, really. Done! 👏

ehm.. we won’t be able to run 110B model…But it is to show you that there is really a large movement around visual Languages

## The Core of the Application

This is a textual python application: the Streamlit version maybe will come in the future. But for the main use cases of Visual Language this shall be perfect.

When CLIP came out, the main purpose of the model was to automatically label images, adding tags, classifications and now also description. Improving your future or existing vector database also with images, based on the captions/descriptions from a VLM is a great feat!

So, the python bindings are the quick way to use llava-phi3-mini-instruct. We load the 2 models and we set up the prompt. Create a new python file: mine is called `LLaVA-Phi-3-mini-4k-instruct.py`.

NOTE: the code is available also in [my GitHub Repo](<https://github.com/fabiomatricardi/imageCPP_aka_llamaCPP/tree/main>), so don’t worry too much.

```python from llama_cpp import Llamafrom llama_cpp.llama_chat_format import Llava15ChatHandler# load the Projectorchat_handler = Llava15ChatHandler(clip_model_path="LLaVA-Phi-3-mini-4k-instruct/llava-phi3-mini-mmproj-f16.gguf")# Load the VLMllm = Llama(model_path="LLaVA-Phi-3-mini-4k-instruct/llava-phi3-mini-Q4_K_M.gguf", chat_handler=chat_handler, n_ctx=2048, # n_ctx should be increased to accomodate the image embedding verbose=False ) ```

With this the main part is done. Note that there are several configurations you can use according to the model family. Inspecting [the library code](<https://github.com/abetlen/llama-cpp-python/blob/main/llama_cpp/llama_chat_format.py>) in here I found at least these:

```python class Llava15ChatHandler (row 2477)class ObsidianChatHandler(Llava15ChatHandler) (row 2868)class MoondreamChatHandler(Llava15ChatHandler) (row 2926)class Llava16ChatHandler(Llava15ChatHandler) (row 2974)class NanoLlavaChatHandler(Llava15ChatHandler) (row 3028)class Llama3VisionAlpha(Llava15ChatHandler) .... ```

You have to check them, in case you will try to experiment by yourself any new model in the future 🌟

Anyway, now comes the second hard part: load the image and feed the `mmproj `with it. I will try to make it simple:

1. if the image is from the we, you have 0 issues, simply paste the url.
2. if the image is a local image, we need to encode and convert it into a binary string (we **convert it into a string-like object**). Here is the magic:

* we open the image as if it is a stream object
* we encode it to base64
* we decode it into utf-8
* we pass it to the prompt in a string format the CLIP model is able to understand.

In my scenario, i want to load my images, so we will proceed with the encoding. I am using the easiest method to interact with the files and folders with an amazing micro library called `[easygui](<https://easygui.readthedocs.io/en/master/api.html>)`: go and check it because it is amazing and simple!

```python print('Select an image to chat with')import easygui #https://easygui.readthedocs.io/en/master/api.htmlfile_path = easygui.fileopenbox(filetypes = ["*.png","*.jpg"])print(f'Loaded image - {file_path}')# CONVERT THE IMAGE TO BASE64print('converting the image to base64...')import base64def image_to_base64_data_uri(file_path): with open(file_path, "rb") as img_file: base64_data = base64.b64encode(img_file.read()).decode('utf-8') return f"data:image/png;base64,{base64_data}"# Replace 'file_path.png' with the actual path to your PNG file# file_path = 'image3_2.PNG' - replaced by EasyGUI loadingdata_uri = image_to_base64_data_uri(file_path) ```

Press enter or click to view image in full size

the first thing is that you are asked to select an image — thanks **easygui**

## Talk to your images

And now we are here. Once the image is correctly prepared for the inference, we can finally pass it together with the prompt.

First thing, we display the image: since for this article i am providing only a basic textual interface, we will want to have the image along side us.

The PIL library comes to our help:

```python # dISPlAY THE IMAGEfrom PIL import ImagetargetImage = Image.open(file_path)targetImage.show() ```

I am using a temporary variable: we first load it, and then display it.

The `llama-cpp-python` can use the chat completion method, that is honestly a blessing: we don’t have to care about the prompt format at all, because the tokenizer and chat template are already hardcoded in the GGUF file. The only difference is that visual language models wants also the image included in the prompt. It is done like here below:

```json messages = [ {"role": "system", "content": "You are an assistant who perfectly describes images."}, { "role": "user", "content": [ {"type": "image_url", "image_url": {"url": data_uri }}, {"type" : "text", "text": "Describe this image in detail. If you know it, tell me the name of this place."} ] }] ```

In the user/content section there are the image and the prompt. The Inference is called with the same `[create_chat_completion](<https://github.com/abetlen/llama-cpp-python#chat-completion>)` method I talked about many times:

``` response = llm.create_chat_completion(messages=messages, stop=["###", "[ENDOFTEXT]"], max_tokens=350, temperature=0.1, repeat_penalty=1.2) ```

Now we only need to print the result, stored in the response variable:

``` print(response["choices"][0]["message"]["content"]) ```

Note that we have to access a structured output, where the content is only a small portion of it.

Save the python file, and with the `venv `still active, from your terminal run

``` python LLaVA-Phi-3-mini-4k-instruct.py ```

The first thing is that you are asked to select an image — thanks **easygui.** What happens next is as expected: the image will be displayed with your default image viewer, and the inference will start.

Press enter or click to view image in full size

preview of the image and start of the generation

The initial prompt asks to _Describe this image in detail. If you know it, tell me the name of this place._

Press enter or click to view image in full size

the final answer…

That basically is it. You can create a loop to keep talking to the image by yourself (even though you can find in the GitHub repo an example for it). It is important that you pass every time the image in the prompt.

## What can I use it for?

Everything looks really cool, but is there any kind of real world use of visual languages?

Visual Language Models (VLMs) combine computer vision and natural language processing to understand and generate text related to visual content. They have indeed a wide range of applications. To give yo some examples we can use them for:

1. Image Captioning: Generating descriptive captions for images, making them more accessible to visually impaired users or enhancing user experience in social media and e-commerce.
2. Visual Question Answering (VQA): Answering questions based on the content of an image or video, useful in education, customer support, and interactive media.
3. Object Detection and Recognition: Labeling objects within an image and describing their relationships, important for autonomous vehicles, surveillance systems, and retail inventory management.
4. Image Retrieval: Searching for images based on text queries or finding similar images to a given example, helpful in stock photo databases and law enforcement forensics... or simply in your Picture folder
5. Translation with Visual Context: Translating text while considering the visual context, improving accuracy when translating signs, menus, or documents with graphics.
6. Accessibility Tools: Enabling tools like alt-text generation for images on the web, making digital content more inclusive.
7. Document Understanding: Analyzing scanned documents with mixed text and images, improving document classification and data extraction processes.

If you are interested in more technical you can start havng a look at here…

## Conclusions

These are only few of the things we can do with Visual Languages. Now that we have a way to run them even on low spec hardware, it make sense to explore this modality and check if we can include them in any of our projects.

Visual Language Models are continuously evolving and finding new applications as they become more sophisticated, bridging the gap between human communication and visual understanding for machines.

What are you going to create with them?

Hope you enjoyed the article. If this story provided value and you wish to show a little support, you could:

1. Clap a lot of times for this story
2. Highlight the parts more relevant to be remembered (it will be easier for you to find them later, and for me to write better articles)
3. **Learn how to start Build Your Own AI** , Download [This Free eBook](<https://build-your-own-ai.ck.page/97a99ce2f7>)
4. Sign up for a Medium membership using [my link](<https://medium.com/@fabio.matricardi/membership>) — ($5/month to read unlimited Medium stories)
5. Follow me on Medium
6. Read my latest articles <https://medium.com/@fabio.matricardi>

Here the GitHub Repo

## [GitHub - fabiomatricardi/imageCPP_aka_llamaCPP: Repo of the code from the Medium article About…Repo of the code from the Medium article About Visual Languages and Llama.CPP - fabiomatricardi/imageCPP_aka_llamaCPPgithub.com](<https://github.com/fabiomatricardi/imageCPP_aka_llamaCPP?source=post_page-----be527a827ebf--------------------------------------->)

Here are some other interesting readings:

## [From Stochastic Parrots to mindful machines: learn Langchain’s path to intelligent AIAn honest review of Ben Auffarth’s new book Generative AI with Langchain. LLM limitations and solutions…medium.com](<https://medium.com/the-ai-explorer/from-stochastic-parrots-to-mindful-machines-learn-langchains-path-to-intelligent-ai-f985c85712b3?source=post_page-----be527a827ebf--------------------------------------->)

## [The ultimate DIY guide: Upscale your images 4x without limitsMaster the art of Upscaling and shatter the constraints to your creativity with AI on your Laptopblog.stackademic.com](</the-ultimate-diy-guide-upscale-your-images-4x-without-limits-346b4d12647a?source=post_page-----be527a827ebf--------------------------------------->)

## [You don’t mess with the Qwen!Qwen unveiled — When AI meets Zohan’s humor, a new Hero emerges.blog.stackademic.com](</you-dont-mess-with-the-qwen-43c8b781c29a?source=post_page-----be527a827ebf--------------------------------------->)

## [Generate-images-CPP... is this a thing?You can generate images even on a CPU with stable-diffusion-cpp-python, and here is how.generativeai.pub](<https://generativeai.pub/generate-images-cpp-is-this-a-thing-d7f5f11a0e0e?source=post_page-----be527a827ebf--------------------------------------->)

To study and research some more…

## [GitHub - abetlen/llama-cpp-python: Python bindings for llama.cppPython bindings for llama.cpp. Contribute to abetlen/llama-cpp-python development by creating an account on GitHub.github.com](<https://github.com/abetlen/llama-cpp-python?source=post_page-----be527a827ebf--------------------------------------->)

## [GitHub - ggerganov/llama.cpp: LLM inference in C/C++LLM inference in C/C++. Contribute to ggerganov/llama.cpp development by creating an account on GitHub.github.com](<https://github.com/ggerganov/llama.cpp?source=post_page-----be527a827ebf--------------------------------------->)

## [Vision Models (GGUF) - a lmstudio-ai CollectionHow to use: Download a "mmproj" model file + one or more of the primary model files.huggingface.co](<https://huggingface.co/collections/lmstudio-ai/vision-models-gguf-6577e1ce821f439498ced0c1?source=post_page-----be527a827ebf--------------------------------------->)

## [abetlen (Andrei)User profile of Andrei on Hugging Facehuggingface.co](<https://huggingface.co/abetlen?source=post_page-----be527a827ebf--------------------------------------->)

## [easygui API - easygui 0.98.1-RELEASED documentationA dialog to get a directory name. Note that the msg argument, if specified, is ignored. Returns the name of a…easygui.readthedocs.io](<https://easygui.readthedocs.io/en/master/api.html?source=post_page-----be527a827ebf--------------------------------------->)

### Additional study resources:

## [LLaVAVisual Instruction Tuningllava-vl.github.io](<https://llava-vl.github.io/?source=post_page-----be527a827ebf--------------------------------------->)

## [Learning Transferable Visual Models From Natural Language SupervisionState-of-the-art computer vision systems are trained to predict a fixed set of predetermined object categories. This…arxiv.org](<https://arxiv.org/abs/2103.00020?source=post_page-----be527a827ebf--------------------------------------->)

## [MBZUAI/LLaVA-Phi-3-mini-4k-instruct · Hugging FaceWe're on a journey to advance and democratize artificial intelligence through open source and open science.huggingface.co](<https://huggingface.co/MBZUAI/LLaVA-Phi-3-mini-4k-instruct?source=post_page-----be527a827ebf--------------------------------------->)

## [kejcao/llava-phi-2-GGUF at mainWe're on a journey to advance and democratize artificial intelligence through open source and open science.huggingface.co](<https://huggingface.co/kejcao/llava-phi-2-GGUF/tree/main?source=post_page-----be527a827ebf--------------------------------------->)

## Stackademic 🎓

Thank you for reading until the end. Before you go:

* Please consider **clapping** and **following** the writer! 👏
* Follow us [**X**](<https://twitter.com/stackademichq>)**|**[**LinkedIn**](<https://www.linkedin.com/company/stackademic>)**|**[**YouTube**](<https://www.youtube.com/c/stackademic>)**|**[**Discord**](<https://discord.gg/in-plain-english-709094664682340443>)
* Visit our other platforms: [**In Plain English**](<https://plainenglish.io>)**|**[**CoFeed**](<https://cofeed.app/>)**|**[**Venture**](<https://venturemagazine.net/>)**|**[**Cubed**](<https://blog.cubed.run>)
* Tired of blogging platforms that force you to deal with algorithmic content? Try [**Differ**](<https://differ.blog/>)
* More content at [**Stackademic.com**](<https://stackademic.com>)

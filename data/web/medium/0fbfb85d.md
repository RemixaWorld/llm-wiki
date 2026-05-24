---
domain: medium.com
fetch_date: '2026-05-18T12:47:48.424676'
status: ok
url: https://medium.com/artificial-corner/multimodal-retrieval-augmented-generation-for-sustainable-finance-with-code-5a910f3b666c
---

# Multimodal Retrieval Augmented Generation Applied To Real World Case — With Code

[ ![Zoumana Keita](https://miro.medium.com/v2/resize:fill:64:64/1*oJPMGtCfDYVZlimVEFYafA.jpeg) ](</@zoumanakeita?source=post_page---byline--5a910f3b666c--------------------------------------->)

[Zoumana Keita](</@zoumanakeita?source=post_page---byline--5a910f3b666c--------------------------------------->)

28 min read

·

Jul 19, 2024

\--

\--

Listen

Share

More

Complete guide to building a RAG system to interact with text, images, tables and audio.

![Multimodal RAG — Weaviate](https://miro.medium.com/v2/resize:fit:700/1*SfjTe1O4PPaeqWeukDmDhw.gif)

## Introduction

Imagine your company’s core expertise is to evaluate ESG (Environmental, Social, and Governance) factors in emerging markets for strategic investment decisions. As a financial analyst in that company, you’re responsible for analyzing vast amounts of diverse data to inform these critical choices.

Wouldn’t it be great if you had an intelligent system that could:

* Automatically process data of various natures
* Answer specific questions about ESG factors in different markets
* Provide accurate insights without the risk of costly mistakes due to AI hallucinations?

In this article, you will learn how Multimodal Retrieval Augmented Generation (RAG) can create such a system, enabling you to:

* Analyze multiple data types simultaneously, including PDFs, images, and audio
* Leverage the power of Large Language Models (LLMs) while mitigating their limitations
* Make more informed and reliable investment decisions in emerging markets

## Multimodal and Retrieval Augmented Generation for ESG Analysis

Retrieval Augmented Generation and Multimodal Learning are two different fundamental components, once combined lead to a more powerful tool. Let’s have a clear understanding of each one of them.

### What is Multimodal Learning?

Multimodal Learning refers to Artificial Intelligence system’s capability to simultaneously process and understand multiple senses such as text, audio, images, videos, unlike tradition unimodal AI tools, which are trained to perform a specific task on a single types of data.

Multimodal learning mimic human perception, which integrates information from various senses to create a comprehensive understanding of the world. In the context of ESG, multimodal learning can combine diverse data sources such as:

![Multimodal learning — diverse source of data (Image by Author)](https://miro.medium.com/v2/resize:fit:700/1*YNo9RpoKAfeQ-11EuSyhoA.png)

* Text: reports, news articles, policy documents for textual data
* Images: satellite imagery, environment impact visuals for images data
* Audio: recordings from conferences discussing ESG strategies and performance
* Tables: structured financial data, ESG ratings, and key performance indicators

### Why Use Multimodal Learning for ESG Analysis?

Multimodal learning provides many benefits for ESG analysts:

* Analysts can make more informed investment decisions by integrating multiple data types
* Multimodal models are well equipped to handle distribution shifts, allowing them to generalize across different data types and sources common in ESG analysis.
* ESG analysts can develop more meaningful and better representations of complex ESG factors, capturing nuances that might be missed in single-modality approaches.
* Multimodal learning enables tasks that bridge different data types, such as generating textual descriptions of environmental impact visuals or answering questions about ESG policies based on both text and image from other documents like PDFs.

### Challenges of Multimodal Learning

Like any AI implementation approach, multimodal learning also has its own challenges and it is necessary to be aware of them. The main ones are illustrated below:

![Multimodal learning challenges (Image by Author)](https://miro.medium.com/v2/resize:fit:700/1*7gWLCsKz_nOtrgyJ5sIl2A.png)

* **Multimodal representation** can be tricky, because each type of data has its own quirks, and relevant details that we do not want to lose.
* Sometimes, with **multimodal translations** , we need to turn a given information into another type, like getting the textual description of a satellite imagery. That translation could not get everything right, leading to information loss.
* In fact checking scenario, **multimodal alignment** is crucial, and could lead to making wrong decisions when not done right. For instance, when comparing companies positioning in a specific market, we might want to check if those companies sustainability report align with their environmental practices.
* In the context of ESG, **multimodal fusion** is relevant for making a comprehensive ESG assessment. Expert can merge financial statements, news articles, social media sentiments, and environmental monitoring data to have a holistic ESG score for investment recommendation.
* We mainly refer to **multimodal Co-learning** when we don’t have enough information in one area, we try to use what we know from other areas to fill in the gaps. This is challenging because different types of information don’t always transfer easily from one context to another.
* An audio data mainly contains multiple speakers, and identifying who is speaking at what timeframe can lead to a more robust answer, which allows the model to capture the person speaking. This process called **speech diarization** is a common challenge for speech recognition tasks.

### Multimodal Retrieval Augmented Generation (RAG)

Accuracy is crucial in ESG analysis. While traditional large language models are powerful, they can sometimes produce outdated or unsourced information and opaque reasoning.

Using such tools may increase the risk of inefficient investment, and no financial analyst can afford when making critical investment decisions.

> This is where Retrieval Augmented Generation (RAG) comes in.

Built upon the foundations of multimodal learning, Multimodal RAG improves the accuracy of large language models by integrating relevant, current ESG data from external sources.

In the context of ESG analysis multimodal RAG offers the following benefits:

* Retrieval: The system searches across diverse data types (text, images, audio, etc.) to find relevant information for a given ESG query.
* Augmentation: Retrieved information from multiple modalities is combined and contextualized.
* Generation: An LLM uses the augmented information to produce accurate, well-informed responses.

This approach addresses the limitations of traditional LLMs by:

* Minimizing misinformation and outdated insights
* Delivering context-specific answers to ESG-related queries
* Enriching the model’s knowledge base with the latest market data

By leveraging multimodal RAG in ESG analysis, financial analysts can make more informed and reliable investment decisions.

Let’s have a comprehensive overview of the following multimodal retrieval augmented generation workflow for our use case, with a specific focus on on the the `Retriever` module and `Augmented Generation` .

The full source code is available on [my GitHub](<https://github.com/keitazoumana/multimodal-rag-esg/tree/main>), and can be downloaded to follow along this article.

![General workflow](https://miro.medium.com/v2/resize:fit:700/1*aURKAJVxwRmZORvqJ9TPjw.gif)

**Retriever component**

That section is where the analyst’s query is used to retrieve from the vector database, the most similar chunks, and the process is as follows:

![Retriever component — Image by Author](https://miro.medium.com/v2/resize:fit:1000/1*6gZ99fknrWMiKw6NeGwRHw.png)

* First, the analyst submits a query to find an answer. In this illustration the user’s query is:

> What was the total net inflow for global sustainable funds in Q1 2024?

* The query is then embedded by an embedding model, which sends it to the vector database to extract the top N similar chunks/documents related to the analyst’s query.

**Augmented Generation component**

This is the last component of the chain, responsible for generating the final answer to the user. The process is illustrated below:

* The most similar chunks/documents to the analyst’s query are combined to the actual query to create the response for the user.

![Augmented Generation — Image by Author](https://miro.medium.com/v2/resize:fit:1000/1*Z8MTsKvV6BPxwCm_mQalNw.png)

## Building a Multimodal RAG for ESG with Weaviate

This section focuses on the technical implementation of each architecture component mentioned above. Before diving into the implementation, it is important to understand the component that makes the data digestible by the generative models: `Data Modeling`.

If you prefer watching video walkthrough instead, check out the following link.

### Data Modeling

Imagine choosing between two systems, both capable of providing accurate responses. However, the second system goes a step further by also giving additional information such as the `page number` , `paragraph number` , `source document` the `url` or the `source audio`, and even an example `image` of the answer.

> Which one of these two systems would Analysts be likely to choose?

![System 1 — Image by Author](https://miro.medium.com/v2/resize:fit:1000/1*SK5nJIYv-j8KrSgr8eCBjg.png) ![System 2 — Image by Author](https://miro.medium.com/v2/resize:fit:1000/1*kjfl0Uklu30ewi-lWlFNgA.png)

Even without expertise in ESG, I can confidently say that the choice will favor the second system. This is mainly due to the modeling part, which prepares the data for the model to provide such detailed information.

Choosing the second system can have the following benefits:

* Investment validation: This allows analysts to verify the facts behind investment recommendations, which is crucial for high-stakes decisions in emerging markets.
* Multimodal context: Referencing specific images, audio clips, or sections of PDFs provides richer context for ESG factors that may not be fully captured in text alone.
* Audit trail: Maintaining a clear reference between the system’s responses and sources creates a valuable audit trail for both internal reviews and external audits. A system equipped with these features is more transparent and useful to analysts.

The main document types covered in this article are `PDF` containing `images` , `tables` and `raw text`. In addition to these types of `PDF` files, `audio` files are also considered.

The above illustration of systems 1 and 2 fits a scenario where the response generated is from textual data, such as raw text data.

Let’s have a full overview of what to expect when dealing with the remaining types of data.

1. **Image data**

For image data, we have the following details:

* Page number: The page where the image is from.
* Source document: The document the image is from.
* Image path: The absolute path where the image has been saved. This can be useful when embedding the image into the response for quick visualization.

**2\. Table data**

Tables have a similar structure to images:

* Page number: The page where the table is from.
* Source document: The document the table is from.

**3\. Audio data**

If the answer comes from an audio source, we might also want to know the origin of the response, which in this case is the link to the original YouTube page discussion.

Great, we have a full picture of the modeling process. Now the question is how to do it!

That’s what will be covered in the next sections.

### Data Collection

To successfully implement our use case, we utilize the following data. The two YouTube videos are freely available and the PDF file is free to use upon registration using email.

* [Global Sustainable Fund Flows: Q1 2024](<https://assets.contentstack.io/v3/assets/blt4eb669caa7dc65b2/bltc4c7114f9f208d6b/662fe107b000392869b5cb75/Global_ESG_Q1_2024_Flows_Report.pdf>): this is a of 43-page PDF document containing multiple images, tables, and text.
* [ESG investing is ‘a complete fraud’](<https://www.youtube.com/watch?v=_p58cZIHDG4>): this a two-minutes thirty-seconds clip of Venture capitalist Chamath Palihapitiya expressing his opinion about ESG investing.
* [How to Invest with your Conscience: ESG Investing](<https://www.youtube.com/watch?v=qP1JKWBBy80>): this six minutes video covers strategies for investing in ESG.

**Prerequisites**

To properly implement the code and avoid package conflicts and installation issues, it is recommended to create a virtual environment as follows:

* Create a virtual environment named `weaviate_venv`.

``` python3 -m venv weaviate_venv ```
* Activate the Virtual Environment

``` source weaviate_venv/bin/activate ```

This command activates the virtual environment. `(weaviate_venv)` should be displayed in the terminal prompt, indicating the virtual environment is active.

* Link the environment to jupyter notebook after installing the `ipykernel`

```python pip install ipykernelpython -m ipykernel install --user --name=weaviate_venv ```

The last command links the virtual environment `weaviate_venv` to Jupyter Notebook.

Now, after launching Jupyter Notebook, we can select `weaviate_venv` as a kernel to run our notebook with this environment's Python interpreter and installed packages as shown below:

![image](https://miro.medium.com/v2/resize:fit:700/1*QSoppdIJwusw7uh-mu0cZg.png)

**1.Audio data**

The original format of this data is video, so there are intermediate steps involved in converting them into audio after downloading.

This process is achieved using the helper class `YouTubeAudioDownloader`, which depends on the `pytube` Python library used for downloading videos from YouTube.

After successfully installing the `pytube` package, it can be used as follows, in addition to the `os` and `re` libraries.

```python pip install pytube ```

Now we can import them

```python from pytube import YouTubeimport osimport re ```

Finally the `YouTubeAudioDownloader` class is implemented as follows:

```python class YouTubeAudioDownloader: def __init__(self, output_folder): self.output_folder = os.path.abspath(output_folder) self.audio_files_dict = {} def get_safe_filename(self, filename): safe_filename = re.sub(r'[^\w\\-.]', '_', filename) safe_filename = re.sub(r'_+', '_', safe_filename) safe_filename = safe_filename[:50].strip('_') return safe_filename def download_audio(self, video_url): try: yt = YouTube(video_url) video = yt.streams.filter(only_audio=True).first() safe_title = self.get_safe_filename(yt.title) safe_title = safe_title.replace(' ', '_') out_file = video.download(output_path=self.output_folder, filename=safe_title) base, ext = os.path.splitext(out_file) new_file = base + '.mp3' os.rename(out_file, new_file) print(f"Audio file downloaded: {new_file}") self.audio_files_dict[video_url] = new_file return new_file except Exception as e: print(f"Error downloading audio from {video_url}: {str(e)}") return None def download_multiple_audios(self, video_urls): for url in video_urls: print(f"Processing video: {url}") audio_file = self.download_audio(url) if audio_file is None: print(f"Failed to download audio from video: {url}") return self.audio_files_dict ```

Let’s understand what is happening here:

* The input of the `YouTubeAudioDownloader` class is a folder where the downloaded audio files are saved. It has the following three main functions:
* `get_safe_filename` cleans up file names to avoid issues such as spacing and special characters when saving audio files. This ensures smooth loading for further analysis.
* `download_audio` collects audio from a single YouTube video and saves it as an MP3.
* `download_multiple_audios` handles the downloading of audio from a list of YouTube links.

By specifying the output directory `data` and the two YouTube URLs, we can successfully perform the download.

``` downloader = YouTubeAudioDownloader(output_folder="../data")video_urls = ["https://www.youtube.com/watch?v=qP1JKWBBy80", "https://www.youtube.com/watch?v=_p58cZIHDG4"]audio_files = downloader.download_multiple_audios(video_urls)print("Downloaded audio files:")for audio_file in audio_files: print(audio_file) ```

After downloading we get the following `audio` files in the audio folder:

![Content of the data folder — Image by Author](https://miro.medium.com/v2/resize:fit:700/1*eJZg2rOpdsjLec9JtVXzhw.png)

**2\. PDFs, Images and tables**

The PDF file is obtained through a simple download process after registering with personal information such as email, first name, and last name.

The PDF file looks like this:

![Content of the PDF file — Animation by Author](https://miro.medium.com/v2/resize:fit:600/1*RcunQH8B__5DAOln-YyzDw.gif)

### Data Processing

The goal of data processing is to normalize all data types into the same format by converting them into text, which is then transformed into vectors.

![Data processing component — Image by Author](https://miro.medium.com/v2/resize:fit:1000/1*8FHtpSGVaielvqo5yoIU9w.png)

This is achieved by:

* Transcribing the `.mp3` files into their textual representation.
* Extracting the textual summaries of each image and table from the PDF file.
* Maintaining the textual format of the raw text data.

1. **Audio Transcription**

OpenAI’s `Whisper` is a great candidate for this task. In addition to transcription, it also offers speech recognition, translation, and language identification capabilities for multiple languages.

`Whisper` requires the installation of `ffmpeg` to function, and it can be installed on any system as described on the [official page](<https://ffmpeg.org/>).

```python pip install openai-whisper ```

Next, the `AudioTranscriber` class is used to transcribe each audio file, resulting in a dictionary with three main keys:

* The URL of the original video
* The path of the audio file
* The transcription of the audio

```python class AudioTranscriber: def __init__(self, input_folder): self.input_folder = os.path.abspath(os.path.join(os.getcwd(), input_folder)) self.whisper_model = None self.transcriptions_dict = {} def transcribe_audio(self, audio_file): try: if not os.path.exists(audio_file): print(f"Audio file not found: {audio_file}") return None file_size = os.path.getsize(audio_file) if file_size == 0: print(f"Audio file is empty: {audio_file}") return None transcription = self.whisper_model.transcribe(audio_file) return transcription["text"] except Exception as e: print(f"Error in transcribe_audio: {str(e)}") return None def transcribe_all_audios(self, audio_files_dict): for url, audio_path in audio_files_dict.items(): if not audio_path.endswith('.mp3'): print(f"Skipping non-mp3 file: {audio_path}") continue transcription = self.transcribe_audio(audio_path) if transcription is not None: # Add to transcriptions dictionary self.transcriptions_dict[url] = { 'url': url, 'audio_path': audio_path, 'transcription': transcription } else: print(f"Failed to transcribe audio: {audio_path}") return self.transcriptions_dict ```

Two main functions are used to perform the transcription tasks:

* `transcribe_audio` generates the transcription for a single audio file.
* `transcribe_all_audio`, on the other hand, leverages `transcribe_audio` to generate transcriptions for all the audio files.

`Whisper` offers five different model sizes. The larger the model, the better its performance, but it requires more memory and consequently more time to load.

For our use case, we are using the medium version of `Whisper` to achieve a balance between performance and speed.

![Different sizes of Whisper models — Source](https://miro.medium.com/v2/resize:fit:700/1*cdfB6NqhqB99LkHUdkK5qg.png)

Before using the model, we need to import both `torch` and `Whisper`, and then set the device to use either CPU or a CUDA GPU.

``` # Set the devicedevice = "cuda" if torch.cuda.is_available() else "cpu"# Load the modelwhisper_model = whisper.load_model("medium", device=device) ```

Now we trigger the transcription process as follows:

``` transcriber = AudioTranscriber(input_folder=r"../data")transcriber.whisper_model = whisper_modeltranscriptions_dict = transcriber.transcribe_all_audios(audio_files)for url, data in transcriptions_dict.items(): print(f"URL: {url}") print(f"Audio file: {data['audio_path']}") print(f"Transcription: {data['transcription'][:100]}...") # Print first 100 characters print("---") ```

A successful execution of the above code generates the following result, showing for each transcription, the first hundred characters.

![Result of the data transcription — Image by Author](https://miro.medium.com/v2/resize:fit:1000/1*g9d1RhFWZbnfY-2oKyFkbw.png)

Now, we create the full audio data which corresponds to a list of dictionaries, where each dictionary is the transcription of each audio file along with additional metadata.

```python import jsonaudio_data = [ { "url": value["url"], "audio_path": value["audio_path"], "transcription": value["transcription"] } for value in transcriptions_dict.values()]# Print the resultprint(json.dumps(audio_data, indent=2)) ```

The truncated result is given below:

![Audio data converted into list of dictionaries — Image by Author](https://miro.medium.com/v2/resize:fit:1000/1*Cz6knXXoQB0Pb7ugle9lvw.png)

**2\. Images, Tables and Text**

By leveraging the `unstructured` library, we can extract all tables, images, and raw text data from a given PDF file.

This library requires the installation of `pillow`, `pdf-miner`, `matplotlib`, `unstructured-inference`, `unstructured-pytesseract`, and `tesseract-ocr`, which are installed below from notebook:

```python %%bashpip install pdfminer.sixpip install pillow-heif==0.3.2pip install matplotlibpip install unstructured-inferencepip install unstructured-pytesseractpip install tesseract-ocr ```

Now we import the `partition_pdf`function, which is used to partition a given PDF file into different components such as images, tables, and raw text.

```python from unstructured.partition.pdf import partition_pdf ```

* **Raw data extraction**

Next, the target ESG report is loaded, while setting the `extract_images_in_pdf` parameter to True, which allows saving images in the `images` folder with high resolution.

``` esg_report_path = "../data/Global_ESG_Q1_2024_Flows_Report.pdf” ``` ``` esg_report_raw_data =partition_pdf( filename=esg_report_path, strategy="hi_res", extract_images_in_pdf=True, extract_image_block_to_payload=False, extract_image_block_output_dir="../data/images/" ) ```

From the above `esg_report_raw_data` we can extract both text, tables and Images.

* **Images extraction**

The helper function `extract_image_metadata` is used to create a list of images along with their metadata, as specified in the data modeling section.

```python from unstructured.documents.elements import Image ``` ```python def extract_image_metadata(esg_report, source_document): image_data = [] for element in esg_report: if isinstance(element, Image): page_number = element.metadata.page_number image_path = element.metadata.image_path if hasattr(element.metadata, 'image_path') else None image_data.append({ "source_document": source_document, "page_number": page_number, "image_path": image_path }) return image_data ```

By applying the `extract_image_metadata` function to the report and the raw data, we obtain the underlying metadata for each image.

``` extracted_image_data = extract_image_metadata(esg_report_raw_data, esg_report_path) ```

With the `display_images_from_metadata` function, we can display each image along with the page number from which it was extracted. This is useful for visualizing images and their respective page sources.

```python import matplotlib.pyplot as pltfrom PIL import Imageimport math ```

We start by importing the relevant libraries such as `matplotlib` , `Image` and `math` .

```python def display_images_from_metadata(extracted_image_data, images_per_row=4):valid_images = [img for img in extracted_image_data if img['image_path']] if not valid_images: print("No valid image data available.") return num_images = len(valid_images) num_rows = math.ceil(num_images / images_per_row) fig, axes = plt.subplots(num_rows, images_per_row, figsize=(20, 5*num_rows)) axes = axes.flatten() if num_rows > 1 else [axes] for ax, img_data in zip(axes, valid_images): try: img = Image.open(img_data['image_path']) ax.imshow(img) ax.axis('off') ax.set_title(f"Page {img_data['page_number']}", fontsize=10) except Exception as e: print(f"Error loading image {img_data['image_path']}: {str(e)}") ax.text(0.5, 0.5, f"Error loading image
{str(e)}", ha='center', va='center') ax.axis('off') for ax in axes[num_images:]: fig.delaxes(ax) plt.tight_layout() plt.show() ```

With the helper function, a maximum of four images is displayed per row.

![Images from PDF — By Author](https://miro.medium.com/v2/resize:fit:1000/1*n_VrsYdb1Pg9UgVVYSB0Sw.png)

All 37 images have been displayed with their respective page numbers. For instance:

* The first page contains only one image, which is the Morning Star logo.
* There are no images on the second page.
* The third page has one image, and the fourth page has two images.
* **Text extraction**

Each native textual information from the PDF is represented by the `NarrativeText` component, which can be used to target and extract all textual data. Additionally, each `NarrativeText` has a `page_number` attribute that can be used to identify the paragraph number.

```python from unstructured.documents.elements import NarrativeText ```

The `extract_text_with_metadata` function is used to extract all these properties, including the actual text and source document.

```python def extract_text_with_metadata(esg_report, source_document): text_data = [] paragraph_counters = {} for element in esg_report: if isinstance(element, NarrativeText): page_number = element.metadata.page_number if page_number not in paragraph_counters: paragraph_counters[page_number] = 1 else: paragraph_counters[page_number] += 1 paragraph_number = paragraph_counters[page_number] text_content = element.text text_data.append({ "source_document": source_document, "page_number": page_number, "paragraph_number": paragraph_number, "text": text_content }) return text_data ```

After running the function, the result is saved in the `extracted_data` attribute:

``` extracted_data = extract_text_with_metadata(esg_report_raw_data, esg_report_path) ```

* **Tables extraction**

This final step is similar to the previous ones and focuses on extracting table content. Each table element is represented by the `Table` component.

```python from unstructured.documents.elements import Table ```

The helper function `extract_table_metadata` is used to get tables data and metadata.

```python def extract_table_metadata(esg_report, source_document): table_data = [] for element in esg_report: if isinstance(element, Table): page_number = element.metadata.page_number # Extract table content as a string table_content = str(element) table_data.append({ "source_document": source_document, "page_number": page_number, "table_content": table_content }) return table_data ```

The final result is saved in the `extracted_table_data` attribute as follows:

``` extracted_table_data = extract_table_metadata(esg_report_raw_data, esg_report_path) ```

**Image, and Table Content Summarization**

At this stage, all data types have been collected, and the last step is to convert each image and table into their textual descriptions for a concise and precise representation. This is achieved through prompt engineering.

* Each table is summarized using `tables_summarizer_prompt`.
* Each image is summarized using `images_summarizer_prompt`.

To ensure the model efficiently describes the tables and images specified in the placeholder `{}`, clear instructions need to be provided so that it can. The prompts are defined as follows:

``` tables_summarizer_prompt = """As an ESG analyst for emerging markets investments, provide a concise and exact summary of the table contents. Focus on key ESG metrics (Environmental, Social, Governance) and their relevance to emerging markets. Highlight significant trends, comparisons, or outliers in the data. Identify any potential impacts on investment strategies or risk assessments. Avoid bullet points; instead, deliver a coherent, factual summary that captures the essence of the table for ESG investment decision-making.Table: {table_content}Limit your summary to 3-4 sentences, ensuring it's precise and informative for ESG analysis in emerging markets.""" ``` ``` images_summarizer_prompt = """As an ESG analyst for emerging markets investments, provide a concise and exact description of the image. Focus on ESG-relevant content (Environmental, Social, Governance) and any emerging market context. Describe the type of visual (e.g., chart, photograph, infographic) and its key elements. Highlight significant data points or trends that are relevant to investment analysis. Avoid bullet points; instead, deliver a coherent, factual summary that captures the essence of the image for ESG investment decision-making.Image: {image_element}Limit your description to 3-4 sentences, ensuring it's precise and informative for ESG analysis.""" ```

Once the prompt is defined, we leverage the `GPT-4O` model from OpenAI to generate the summaries. This requires having OpenAI credentials.

Before proceeding, we need to install the `langchain-core` and `langchain-openai` libraries, and then import the `ChatPromptTemplate` and `ChatOpenAI` modules.

```python %%bashpip install langchain-corepip install langchain-openai ```

Now, we set up the environment to use the model.

``` OPENAI_API_TOKEN="YOUR KEY"model_ID = "gpt-4o"os.environ["OPENAI_API_KEY"] = OPENAI_API_TOKEN ```

Finally, the helper functions `extract_table_metadata_with_summary` and `extract_image_metadata_with_summary` are used to generate the summary/description of a given table and image, in addition to the initial metadata.

```python def extract_table_metadata_with_summary(esg_report, source_document, tables_summarizer_prompt):table_data = [] prompt = ChatPromptTemplate.from_template(tables_summarizer_prompt) for element in esg_report: if isinstance(element, Table): page_number = element.metadata.page_number table_content = str(element) # Generate summary using the OpenAI model messages = prompt.format_messages(table_content=table_content) description = description_model.predict_messages(messages).content table_data.append({ "source_document": source_document, "page_number": page_number, "table_content": table_content, "description": description }) return table_data ``` ```python def extract_image_metadata_with_summary(esg_report_raw_data, esg_report_path, images_summarizer_prompt):image_data = [] # Create ChatPromptTemplate instance prompt = ChatPromptTemplate.from_template(images_summarizer_prompt) # Create ChatOpenAI instance description_model = ChatOpenAI(model=model_ID) for element in esg_report_raw_data: if "Image" in str(type(element)): page_number = element.metadata.page_number if hasattr(element.metadata, 'page_number') else None image_path = element.metadata.image_path if hasattr(element.metadata, 'image_path') else None if image_path and os.path.exists(image_path): # Generate description using the OpenAI model messages = prompt.format_messages(image_element=image_path) description = description_model.predict_messages(messages).content # Read the image file and encode it to base64 with open(image_path, "rb") as image_file: encoded_string = base64.b64encode(image_file.read()).decode('utf-8') image_data.append({ "source_document": esg_report_path, "page_number": page_number, "image_path": image_path, "description": description, "base64_encoding": encoded_string }) else: print(f"Warning: Image file not found or path not available for image on page {page_number}") return image_data ```

For each image, a `base64` encoding is created, which can be useful when displaying the image instead of using the physical `.png` file.

Now we extract the result of both data types as follows:

``` extracted_table_data_with_summary = extract_table_metadata_with_summary(esg_report_raw_data, esg_report_path, tables_summarizer_prompt) ```

Below is the truncated result for the first few tables from the `print` statement.

``` for table in extracted_table_data_with_summary: print(f"Table on Page {table['page_number']}:") print(f"Table source: {table['source_document']}") print(f"Description: {table['description']}") print("---") ```

![Truncated result of tables on pages 2, 5 and 7 — Image by Author](https://miro.medium.com/v2/resize:fit:1000/1*E_yzwwqd6oI1CRbYfHEusg.png)

By applying similar approach to images, we get the following result:

``` extracted_image_data = extract_image_metadata_with_summary(esg_report_raw_data, esg_report_path, images_summarizer_prompt) ``` ``` for image in extracted_image_data: print(f"Image on Page {image['page_number']}:") print(f"Path: {image['image_path']}") print(f"Description: {image['description']}") print(f"Base 64: {image['base64_encoding']}") print("---") ```

And, the truncated result for the above `print` statement is given below:

![Truncated result of images on pages 3 and 4 — Image by Author](https://miro.medium.com/v2/resize:fit:1000/1*Nf9GVmgjchneBt4M9GmAcg.png)

Perfect! All the data is ready for ingestion. But before that, we need to transform them into the same embedding space.

### Data Ingestion

The term of this section is Vector Database, and there are multiple providers out there both open-source and paid. However our use case mainly focuses on `Weaviate`

> But, why Weaviate, and not other vector database?

`Weaviate` is an open-source vector database designed to store objects and their corresponding vectors. It offers efficient vector search and structured filtering capabilities, making data retrieval effective.

Also, it supports diverse data types, including text and images, and is modular, cloud-native, and real-time, facilitating scalable machine learning models.

It integrates seamlessly with popular AI services and frameworks, providing a robust foundation for building AI-native applications.

All these reasons make it the perfect fit for our use case. This section covers all the steps, from creating a `Weaviate` account, setting up a vector database instance to ingesting all the data.

For instance, the original tables, images, text, and audio have been converted into a common embedding space.

This allows for the comparison of different types of documents with each other. This is a crucial transitional step for storing data in the vector database.

The graphic illustration demonstrates how documents related to Climate Change and Air Pollution are closely linked, as are those concerning Labor Practices and Human Rights. Conversely, documents from different groups are distinctly separated from each other.

This proximity is automatically determined by the vector similarity search, a topic that will be covered in the subsequent sections.

![Data ingestion to vector database — Image by Author](https://miro.medium.com/v2/resize:fit:1000/1*lLdeuKVSrQADd2kK4KJ1KQ.png)

1. **Create a Weaviate cloud account**

The following information is required to successfully the data ingestion process:

* Have a `Weaviate` account. This is done from the cloud account page, using email and password
* Already an OpenAI credentials

Before beginning data ingestion, it’s essential to have the vector representation of all the data processed so far. This process starts with creating a vector database instance, following these four steps after logging into the cloud account:

* Select `Create cluster` to initiate the creation of a cluster for hosting the vector database instance
* Choose the `Free sandbox` option
* Provide a meaningful name for the cluster; ours is `esg-rag-vector-instance`
* Finally click `Create` to complete the cluster creation

![Four main steps to create a Weaviate cluster — Image by Author](https://miro.medium.com/v2/resize:fit:1000/1*S9BfgReKiqoDmz2kSLkIHw.png)

After clicking the `Create`button, it might take a few minutes to create the instance. All instances are displayed under the `Weaviate Clusters` section, where we can see that ours has been successfully created with the name **_esg-rag-vector-instance-aufn6coj ,_** where **_aufn6cojis_** the unique identifier of the instance in the cluster.

![Our Weaviate cluster — Image by Author](https://miro.medium.com/v2/resize:fit:1000/1*ZDh8psdO2SkMCaYMC2ZEyA.png)

We also notice that the vector database is currently empty, which is normal since we haven’t ingested any data yet. The next section covers the steps to define the schema of the database and ingest data.

![Empty vector database — Image by Author](https://miro.medium.com/v2/resize:fit:1000/1*M_tOuRCGfXd_H94QCI3gzQ.png)

**2\. Connect to Weaviate vector database**

The first step to ingesting data is to create a Weaviate client so that we can:

* Connect to the vector database
* Create a collection for the data to be ingested into the database

Let’s begin by installing the Weaviate client as follows:

```python pip install weaviate-client ```

Next, we import the module, set the environment variables with the cluster `URL` and `APIKEY`

![Cluster URL and API KEY — Image by Author](https://miro.medium.com/v2/resize:fit:1000/1*R5OoBv2_hAxunoQvcIhAAA.png)

```python import weaviate URL = os.getenv("WCS_URL")APIKEY = os.getenv("WCS_API_KEY") ```

With the `connect_to_wcs` function, we can connect to the vector database by specifying the above variables and the initial OpenAI token.

``` client = weaviate.connect_to_wcs( cluster_url=URL, auth_credentials=weaviate.auth.AuthApiKey(APIKEY), headers = { "X-OpenAI-Api-Key": OPENAI_API_TOKEN }) ```

> Wait, why are we using OpenAI within Weaviate?

This integration with OpenAI gives us the ability to:

* Import objects directly into Weaviate without the need to manually specify embeddings.
* Build our RAG pipeline with generative models from providers other than OpenAI. For instance, we could use models from `Cohere`, `AWS`, `Google`, `Hugging Face`, `Azure OpenAI`, `Mistral`, and [more](<https://weaviate.io/developers/weaviate/model-providers>).

**3\. Create multimodal ESG collection**

A collection is created by specifying the following parameters:

* `name` of the collection, which is `ESGDocument` for our use case.
* `properties` as the list of all attributes of the collection.
* `vectorizer_config` provides details of the embedding model to use; we are using the `text-embedding-3-large` model from OpenAI.

Our collection is defined as follows, with properties including:

* `TEXT` fields such as `source_document`, `description`, `audio_path`, `text`, `table_content`, `transcription`, `content_type`, and `url`.
* `Numeric` fields like `page_number` and `paragraph number`.
* `BLOB` for base64 encoding.

```python import weaviate.classes.config as wc ``` ``` properties = [ wc.Property(name="source_document", data_type=wc.DataType.TEXT, skip_vectorization=True), wc.Property(name="page_number", data_type=wc.DataType.INT, skip_vectorization=True), wc.Property(name="paragraph_number", data_type=wc.DataType.INT, skip_vectorization=True), wc.Property(name="text", data_type=wc.DataType.TEXT), wc.Property(name="image_path", data_type=wc.DataType.TEXT, skip_vectorization=True), wc.Property(name="description", data_type=wc.DataType.TEXT), wc.Property(name="base64_encoding", data_type=wc.DataType.BLOB, skip_vectorization=True), wc.Property(name="table_content", data_type=wc.DataType.TEXT), wc.Property(name="url", data_type=wc.DataType.TEXT, skip_vectorization=True), wc.Property(name="audio_path", data_type=wc.DataType.TEXT, skip_vectorization=True), wc.Property(name="transcription", data_type=wc.DataType.TEXT), wc.Property(name="content_type", data_type=wc.DataType.TEXT, skip_vectorization=True),] ```

We set the `skip_vectorization` parameter to `True` for properties that do not require vectorization. Only the properties such as text data, image description, audio transcription, and table description require vectorization for performing a search.

Now, we can create the collection using the `create` function, while setting the `vectorizer_config` to `None`. This tells Weaviate that we will specify our own vectorizer when uploading data into the vector database.

``` client.collections.create( name="ESGDocuments", properties=properties, vectorizer_config=None) ```

From the `Collections` tab we can observe that all twelve properties have been created, along with the embedding model being used.

![Collection properties — Image by Author](https://miro.medium.com/v2/resize:fit:1000/1*BDIZxuPE9JaKpnUxlTKpow.png)

**4\. Ingest data**

The collection is properly set up for data ingestion, and the following helper functions are leveraged to ingest data into the vector database: a function for each specific data type and a final function that utilizes these unique functions to ingest all data.

We begin by importing the relevant libraries as follows:

```python from weaviate.util import generate_uuid5from tqdm import tqdmfrom openai import OpenAIopenai_client = OpenAI() ``` ```python # Function to get embeddingsdef get_embedding(text): response = openai_client.embeddings.create( input=text, model="text-embedding-3-large" ) return response.data[0].embedding# Ingestion functionsdef ingest_audio_data(collection, audio_data): with collection.batch.dynamic() as batch: for audio in tqdm(audio_data, desc="Ingesting audio data"): vector = get_embedding(audio['transcription']) audio_obj = { "url": audio['url'], "audio_path": audio['audio_path'], "transcription": audio['transcription'], "content_type": "audio" } batch.add_object( properties=audio_obj, uuid=generate_uuid5(audio['url']), vector=vector )def ingest_text_data(collection, text_data): with collection.batch.dynamic() as batch: for text in tqdm(text_data, desc="Ingesting text data"): vector = get_embedding(text['text']) text_obj = { "source_document": text['source_document'], "page_number": text['page_number'], "paragraph_number": text['paragraph_number'], "text": text['text'], "content_type": "text" } batch.add_object( properties=text_obj, uuid=generate_uuid5(f"{text['source_document']}_{text['page_number']}_{text['paragraph_number']}"), vector=vector )def ingest_image_data(collection, image_data): with collection.batch.dynamic() as batch: for image in tqdm(image_data, desc="Ingesting image data"): vector = get_embedding(image['description']) image_obj = { "source_document": image['source_document'], "page_number": image['page_number'], "image_path": image['image_path'], "description": image['description'], "base64_encoding": image['base64_encoding'], "content_type": "image" } batch.add_object( properties=image_obj, uuid=generate_uuid5(f"{image['source_document']}_{image['page_number']}_{image['image_path']}"), vector=vector )def ingest_table_data(collection, table_data): with collection.batch.dynamic() as batch: for table in tqdm(table_data, desc="Ingesting table data"): vector = get_embedding(table['description']) table_obj = { "source_document": table['source_document'], "page_number": table['page_number'], "table_content": table['table_content'], "description": table['description'], "content_type": "table" } batch.add_object( properties=table_obj, uuid=generate_uuid5(f"{table['source_document']}_{table['page_number']}"), vector=vector )def ingest_all_data(collection_name, audio_data, text_data, image_data, table_data): collection = client.collections.get(collection_name) ingest_audio_data(collection, audio_data) ingest_text_data(collection, text_data) ingest_image_data(collection, image_data) ingest_table_data(collection, table_data) if len(collection.batch.failed_objects) > 0: print(f"Failed to import {len(collection.batch.failed_objects)} objects") else: print("All objects imported successfully") ```

Finally, the `ingest_all_data` function is used to ingest data in the `ESGDocument` collection.

``` ingest_all_data(collection_name="ESGDocument", audio_data=audio_data, text_data=extracted_data, image_data=extracted_image_data, table_data=extracted_table_data_with_summary ) ```

After ingesting data, we count 252 objects, which corresponds to the total count of all objects, including text, images, tables, and audio.

![Total number of objects in the collection — Image by Author](https://miro.medium.com/v2/resize:fit:1000/1*ZV4Pr8EUANewxgLnaoNqig.png)

### Build Multimodal RAG for ESG

This final section includes all the steps for implementing the multimodal RAG search, from nearest search to implementing the prompt to augment the large language model’s response.

1. **Nearest search**

The nearest search logic is implemented in `search_multimodal`, which generates the top three results by default

![Nearest neighbor search — Image by Author](https://miro.medium.com/v2/resize:fit:1000/1*woCIahDCAM19QQZPL9FPRw.png)

The function allows for semantic search across text, audio, images, and table data based on the query’s meaning rather than exact keyword matching.

Matched objects are returned with all their properties. This is useful for capturing attributes specific to each data type.

```python import weaviate.classes.query as wq ``` ```python def search_multimodal(query: str, limit: int = 3): query_vector = get_embedding(query) esg_documents = client.collections.get("ESGDocument") response = esg_documents.query.near_vector( near_vector=query_vector, limit=limit, return_metadata=wq.MetadataQuery(distance=True), return_properties=[ "content_type", "url", "audio_path", "transcription", "source_document", "page_number", "paragraph_number", "text", "image_path", "description", "table_content" ] ) return response.objects ```

The `search_and_print_results` function displays the search results by properly formatting the output.

```python def search_and_print_results(query, limit=5): search_results = search_multimodal(query, limit) print(f"Search Results for query: '{query}'") for item in search_results: print(f"Type: {item.properties['content_type']}") if item.properties['content_type'] == 'audio': print(f"URL: {item.properties['url']}") print(f"Transcription: {item.properties['transcription'][:100]}...") elif item.properties['content_type'] == 'text': print(f"Source: {item.properties['source_document']}, Page: {item.properties['page_number']}") print(f"Text: {item.properties['text'][:100]}...") elif item.properties['content_type'] == 'image': print(f"Source: {item.properties['source_document']}, Page: {item.properties['page_number']}") print(f"Description: {item.properties['description']}") elif item.properties['content_type'] == 'table': print(f"Source: {item.properties['source_document']}, Page: {item.properties['page_number']}") print(f"Description: {item.properties['description']}") print(f"Distance to query: {item.metadata.distance:.3f}") print("---") return search_results ```

Now, let’s find the top three similar entries to the following query:

``` query = "What are the main environmental challenges in renewable energy?"search_and_print_results(query) ```

The truncated result of the search is displayed below:

![Nearest neighbor search result — Image by Author](https://miro.medium.com/v2/resize:fit:1000/1*GqYTlWMZDMEttQrYqrFXDQ.png)

**2\. Set up the generation prompt**

Providing analysts with the above result can be confusing and may not bring any value to their experience. This is where the augmented generation section comes into play.

![Augmented Generation — Image by Author](https://miro.medium.com/v2/resize:fit:1000/1*WnsOWYUNdP45TCaJ2ZJRfw.png)

To achieve that, we need to define the prompt to be used by the generative model as follows in the `generate_response` function. It takes a user’s question and relevant context, then uses AI (GPT-4) to create an expert ESG analysis answer for emerging markets

```python def generate_response(query: str, context: str) -> str: prompt = f""" You are an AI assistant specializing in ESG (Environmental, Social, and Governance) analysis for emerging markets. Use the following pieces of information to answer the user's question. If you cannot answer the question based on the provided information, say that you don't have enough information to answer accurately.Context: {context} User Question: {query} Please provide a detailed and accurate answer based on the given context: """ response = openai_client.chat.completions.create( model="gpt-4-1106-preview", messages=[ {"role": "system", "content": "You are an expert ESG analyst for emerging markets."}, {"role": "user", "content": prompt} ], temperature=0 ) return response.choices[0].message.content ```

The `esg_analysis` function leverages the `search_multimodal` and `generate_response` functions to generate the final response for the user.

This function is lengthy due to data formatting in the end.

```python def esg_analysis(user_query: str): # Step 1: Retrieve relevant information search_results = search_multimodal(user_query)# Step 2: Prepare context for RAG context = "" for item in search_results: if item.properties['content_type'] == 'audio': context += f"Audio Transcription from {item.properties['url']}: {item.properties['transcription']}

" elif item.properties['content_type'] == 'text': context += f"Text from {item.properties['source_document']} (Page {item.properties['page_number']}, Paragraph {item.properties['paragraph_number']}): {item.properties['text']}

" elif item.properties['content_type'] == 'image': context += f"Image Description from {item.properties['source_document']} (Page {item.properties['page_number']}, Path: {item.properties['image_path']}): {item.properties['description']}

" elif item.properties['content_type'] == 'table': context += f"Table Description from {item.properties['source_document']} (Page {item.properties['page_number']}): {item.properties['description']}

" # Step 3: Generate response using RAG response = generate_response(user_query, context) # Step 4: Format and return the final output sources = [] for item in search_results: source = { "type": item.properties["content_type"], "distance": item.metadata.distance } if item.properties["content_type"] == 'text': source.update({ "document": item.properties["source_document"], "page": item.properties["page_number"], "paragraph": item.properties["paragraph_number"] }) elif item.properties["content_type"] == 'image': source.update({ "document": item.properties["source_document"], "page": item.properties["page_number"], "image_path": item.properties["image_path"] }) elif item.properties["content_type"] == 'table': source.update({ "document": item.properties["source_document"], "page": item.properties["page_number"] }) elif item.properties["content_type"] == 'audio': source.update({ "url": item.properties["url"] }) sources.append(source) # Sort sources by distance (ascending order) sources.sort(key=lambda x: x['distance']) final_output = { "user_query": user_query, "ai_response": response, "sources": sources } return final_output ```

Instead of having truncated results as shown in the previous illustrations, we can use the helper function `wrap_text` to format the output with a maximum of one hundred characters per line.

First, install the library as follows:

```python !pip install textwrap3 ```

The `fill` function is used to specify the maximum character number, which defaults to 120.

```python import textwrap ``` ```python def wrap_text(text, width=120): wrapped_text = textwrap.fill(text, width=width) return wrapped_text ```

Lastly, the overall question-answering result is provided by the `analyze_and_print_esg_results` function below:

```python def analyze_and_print_esg_results(user_question): result = esg_analysis(user_question) ``` ``` print("User Query:", result["user_query"]) print("
AI Response:", wrap_text(result["ai_response"])) print("
Sources (sorted by relevance):") for source in result["sources"]: print(f"- Type: {source['type']}, Distance: {source['distance']:.3f}") if source['type'] == 'text': print(f" Document: {source['document']}, Page: {source['page']}, Paragraph: {source['paragraph']}") elif source['type'] == 'image': print(f" Document: {source['document']}, Page: {source['page']}, Image Path: {source['image_path']}") elif source['type'] == 'table': print(f" Document: {source['document']}, Page: {source['page']}") elif source['type'] == 'audio': print(f" URL: {source['url']}") print("---") ```

**3\. Question answering**

It’s time to test some queries and see how our AI-powered ESG system responds.

``` user_question = "Is ESG investment a fraud?"analyze_and_print_esg_results(user_question) ```

Result:

![Answer to fraud question — Image by Author](https://miro.medium.com/v2/resize:fit:1000/1*r65-HCvLWKnAOK-WJJlAJg.png)

The answer of the system to weather ESG investment is a fraud is provided below by relevance:

* Audio: A [YouTube video](<https://www.youtube.com/watch?v=_p58cZIHDG4>) (most relevant, distance 0.408)
* Table: From “Global_ESG_Q1_2024_Flows_Report.pdf”, page 7 (distance 0.455)
* Text: From the same PDF, page 8, paragraph 3 (distance 0.468)

For the second query, we have:

``` user_question = "What was the total net inflow for global sustainable funds in Q1 2024?"analyze_and_print_esg_results(user_question) ```

Result:

![Answer to second query — Image by Author](https://miro.medium.com/v2/resize:fit:1000/1*aPJOidHO3WyC52vfbowlEw.png)

The system provides three relevant text sources from the same PDF report.

* Most relevant (Distance: 0.220): Page 2, Paragraph 6
* Second (Distance: 0.227): Page 6, Paragraph 2
* Third (Distance: 0.230): Page 2, Paragraph 4 (which matches the citation in the answer)

We can see that the system did quite a good job providing the correct response, and the page number.

However, the paragraph number is not always accurate, when a table is present in that page, because the processing module may be confused about how which section can be considered as a paragraph when dealing with tables.

![Reference section — Image by Author](https://miro.medium.com/v2/resize:fit:1000/1*FfkvBJLt-m0zLIeBlHZk5w.png)

Overall the system is doing a great job!

Let’s have a look at a last example:

``` user_question = "What is the net flows for Parnassus Mid Cap Fund?"analyze_and_print_esg_results(user_question) ```

Result:

![Query answer about net flows — Image by Author](https://miro.medium.com/v2/resize:fit:1000/1*1N_ZiHsFA0Nc49pCl3ri8A.png)

Three relevant text sources from the Global ESG Q1 2024 Flows Report:

* Most relevant (Distance: 0.320): Page 20, Paragraph 4
* Second (Distance: 0.344): Page 17, Paragraph 5
* Third (Distance: 0.414): Page 9, Paragraph 7

The system provides context about the fund’s performance but clearly states the limitations of the available information. It explains what additional data would be needed to answer the question precisely, demonstrating transparency about the information gaps.

Whenever information is unavailable in the knowledge base, the model clearly states that fact instead of speculating.

Now, let’s check the correctness of the response.

![Reference section — Image by Author](https://miro.medium.com/v2/resize:fit:1000/1*rg8qDKCUj2Z4XK9nSzQNtA.png)

## Integration into Business Workflow

One of the biggest challenges after building a Retrieval Augmented Generation use case is testing it ourselves and also getting relevant feedback from users for faster iteration.

For that reason, we might want to build a quick User Interface for testing and also automate that testing process. Tools like Gradio, MESOP can be used to build such interface, but this use case leverages Streamlit, and below is the illustration.

![Analyst interacting with the Multimodal RAG — Animation by Author](https://miro.medium.com/v2/resize:fit:600/1*jFW03MI8vsHinC4d_O3AqQ.gif)

## Conclusion

This article provided a comprehensive overview of Multimodal Retrieval Augmented Generation (RAG) and its application to ESG investment analysis. It began by explaining multimodal learning, its relevance to multimodal RAG, and the associated limitations.

Next, the article guided readers through the process of implementing multimodal RAG using Weaviate. This included creating a Weaviate cloud account, setting up a vector database instance, modeling the use case data, and implementing the overall chatting system.

Finally, it explained how to integrate the end result into a business workflow by building a Streamlit interface.

> So, where do we go from here? How can improve the current system?

The current system while providing great results is not perfect. There are multiple ways to enhance it, and some of them include the use of [generative feedback loops](<https://weaviate.io/gen-feedback-loops>), which consists on improving the system’s response based on the users’ feedback to previously generated results.

Another approach is to continuously update the knowledge base to help the system provide accurate, and up-to-date responses, thereby improving the overall user experience.

While multimodal RAG is promising for ESG scenarios, continuous improvements are crucial to its overall success.

Also, If you enjoy reading my stories and wish to support my writing, consider becoming a Medium member. It’s $5 a month, giving you unlimited access to thousands of Python guides and Data science articles.

By signing up using[ my link](<https://zoumanakeita.medium.com/membership>), I will earn a small commission at no extra cost to you.

Feel free to follow me on [Twitter](<https://twitter.com/zoumana_keita_>), and [YouTube](<https://www.youtube.com/channel/UC9xKdy8cz6ZuJU5FTNtM_pQ>), or say Hi on [LinkedIn](<https://www.linkedin.com/in/zoumana-keita/>).

Before you leave, there are more great resources below you might be interested in reading!

[How to Chat With Any PDFs and Image Files Using Large Language Models — With Code](<https://towardsdatascience.com/how-to-chat-with-any-file-from-pdfs-to-images-using-large-language-models-with-code-4bcfd7e440bc>)

[Introduction to Text Embeddings with the OpenAI API](</geekculture/introduction-to-text-embeddings-with-the-openai-api-1f83d2a15fda>)

[How to Extract Text from Any PDF and Image for Large Language Model](</towards-data-science/how-to-extract-text-from-any-pdf-and-image-for-large-language-model-2d17f02875e6>)

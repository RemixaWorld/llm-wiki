---
domain: alain-airom.medium.com
fetch_date: '2026-05-18T12:58:12.121039'
status: ok
url: https://alain-airom.medium.com/granite-4-0-1b-speech-model-is-out-and-its-dynamite-6a623544eda6
---

# Granite 🪨 4.0 1b speech model is out and it’s dynamite 🧨

A Simple implementation of “ibm-granite/granite-4.0–1b-speech”!

![](https://miro.medium.com/v2/resize:fit:700/1*0tnvkBfwHM4EYPhcELpThg.png)

## The Granite Bedrock: An Introduction to IBM’s Enterprise AI Family

In the rapidly shifting landscape of generative AI, the **IBM Granite** model family stands out as a “workhorse” designed specifically for the rigors of the modern enterprise. Unlike general-purpose models that prioritize sheer scale, Granite is built on a philosophy of **transparency, efficiency, and safety**. Released under the permissive Apache 2.0 license, these models provide developers and businesses with a “glass-box” approach to AI — offering full visibility into the curated, ethically-sourced datasets used for training. This commitment to governance makes Granite a go-to choice for highly regulated industries like finance, healthcare, and legal, where auditability isn’t just a feature, but a requirement.

The Granite family has evolved into a versatile ecosystem of specialized models, each tailored for high-performance tasks:

**Granite for Language:**Optimized for complex reasoning, summarization, and RAG (Retrieval-Augmented Generation) across dozens of languages.**Granite for Code:**Trained on 116+ programming languages to power state-of-the-art coding assistants that can explain, fix, and generate code with high precision.**Granite 4.0 & Nano:**The latest generation introducing**hybrid Mamba-Transformer architectures**, delivering massive gains in memory efficiency and speed for local, on-device deployments.**Specialized Variants:**Including**Granite Guardian**for advanced safety and hallucination detection,**Granite Time Series**for forecasting, and**Granite-Docling**for structured document conversion.

By focusing on “doing more with less,” IBM has positioned Granite as a scalable solution that bridges the gap between massive cloud-based LLMs and efficient, private, local AI. Whether you are building an autonomous agentic workflow or a lightweight mobile app, the Granite family provides the architectural stability and ethical foundation needed to move from experimental prototypes to production-ready enterprise applications.

## The Model Family

The **IBM Granite 4.0** family represents a major shift in enterprise AI, moving away from “bigger is better” toward **hyper-efficiency** and **precision**. By blending traditional Transformer power with the linear scaling of Mamba-2, these models solve the “quadratic bottleneck” — the phenomenon where standard AI models become exponentially slower and more memory-hungry as you feed them longer documents.

## The Hybrid Engine: Mamba-Transformer Architecture

Most AI models (like GPT-4 or Llama 3) use a pure **Transformer** architecture. While accurate, they require massive amounts of RAM for long conversations. Granite 4.0 uses a **9:1 Hybrid Ratio**:

**Mamba-2 Layers (90%):**Handles the “heavy lifting” of long sequences with linear scaling. If you double the text, it only takes double the work (not quadruple).**Transformer Layers (10%):**Injected periodically to maintain high accuracy for complex reasoning and “copying” tasks where pure Mamba models sometimes struggle.

## The 4.0 Model Lineup

IBM offers Granite in several sizes to fit everything from a Raspberry Pi to a high-end data center:

`| Model Name | Parameters | Best Use Case |`

| --------------------- | --------------- | ------------------------------------------------------------ |

| **Granite 4.0 Small** | 32B (9B Active) | **The Workhorse:** Enterprise RAG, complex agents, and tool-calling. Uses "Mixture of Experts" (MoE) to stay fast. |

| **Granite 4.0 Tiny** | 7B (1B Active) | **The Balanced Choice:** Low-latency local apps and high-volume basic tasks. |

| **Granite 4.0 Micro** | 3B | **The Edge Specialist:** Fits on modest consumer GPUs; perfect for fast function calling in agents. |

| **Granite 4.0 Nano** | 350M - 1B | **The On-Device Hero:** Designed for mobile phones and offline PC applications. |

## Granite-4.0–1B-Speech: Multilingual ASR & Translation

The **1B-Speech** model is a specialized variant that aligns the Granite 4.0 backbone with audio embeddings. It is specifically built for **Edge AI** — situations where you need transcription or translation without sending audio to the cloud.

**Multilingual Support:**Native ASR for English, French, German, Spanish, Portuguese, and Japanese.**Bidirectional Translation:**Can translate between these languages and English (e.g., French audio → English text).**Keyword Biasing:**A unique feature allowing you to provide a list of “special words” (like project names or technical acronyms) to ensure the model doesn’t misspell them.**Performance:**Recently ranked**#1 on the OpenASR leaderboard**, achieving a Word Error Rate (WER) as low as 5.52% while being 50% smaller than previous generations.

## Keyword Biasing

Implementing **keyword biasing** is one of the standout features of Granite-4.0–1b-speech. It allows you to “nudge” the model to correctly recognize technical terms, brands, or unique names that it might otherwise misspell.

To use this, you provide a list of terms at the end of your text prompt. The model’s tokenizer and processor handle the alignment during the generation phase.

**Python Implementation via Transformers:**hereafter a concise example of how to load the model and apply a custom keyword list for transcription.

`import torch`

import torchaudio

from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor


# 1. Setup device and model

device = "cuda" if torch.cuda.is_available() else "cpu"

model_id = "ibm-granite/granite-4.0-1b-speech"


processor = AutoProcessor.from_pretrained(model_id)

model = AutoModelForSpeechSeq2Seq.from_pretrained(

model_id,

torch_dtype=torch.float16 if device == "cuda" else torch.float32

).to(device)


# 2. Define your biased keywords

# Adding specific terms helps the model avoid generic phonetic guesses

keywords = ["IBM Granite", "Mamba-2", "RAG", "VAD"]

keyword_prompt = f" Keywords: {', '.join(keywords)}"


# 3. Create the chat-style prompt

# The model expects a prompt instructing it on the task

messages = [

{

"role": "user",

"content": "Transcribe the following speech into English text." + keyword_prompt

}

]

text_prompt = processor.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)


# 4. Load audio (Must be 16kHz mono)

audio, sampling_rate = torchaudio.load("your_audio_file.wav")

if sampling_rate != 16000:

resampler = torchaudio.transforms.Resample(sampling_rate, 16000)

audio = resampler(audio)


# 5. Generate with biasing

inputs = processor(text=text_prompt, audio=audio, return_tensors="pt", sampling_rate=16000).to(device)


output_ids = model.generate(

**inputs,

max_new_tokens=256,

do_sample=False, # Greedier decoding often works better with biasing

)


transcript = processor.batch_decode(output_ids, skip_special_tokens=True)[0]

print(f"Transcript: {transcript}")

## The model’s excerpt from Hugging Face

Model Summary: Granite-4.0–1b-speech is a compact and efficient speech-language model, specifically designed for multilingual automatic speech recognition (ASR) and bidirectional automatic speech translation (AST).

The model was trained on a collection of public corpora comprising of diverse datasets for ASR and AST as well as synthetic datasets tailored to support Japanese ASR, keyword-biased ASR and speech translation. Granite-4.0–1b-speech was trained by modality aligning granite-4.0–1b-base to speech on publicly available open source corpora containing audio inputs and text targets. Compared to granite-speech-3.3–2b and granite-speech-3.3–8b, this model has the following additional capabilities and improvements:

- Supports multilingual speech inputs in English, French, German, Spanish, Portuguese and Japanese,
- Provides higher transcription accuracy for English ASR and faster inference through better encoder training and speculative decoding,
- Has half the number of parameters of granite-speech-3.3–2b for running on resource-constrained devices,
- Adds keyword list biasing capability for enhanced name and acronym recognition

Supported Languages: English, French, German, Spanish, Portuguese, Japanese

**Intended Use**: The model is intended to be used in enterprise applications that involve processing of speech inputs. In particular, the model is well-suited for English, French, German, Spanish, Portuguese and Japanese speech-to-text and speech translations to and from English for the same languages, plus English-to-Italian and English-to-Mandarin.

**Generation: **Granite Speech model is supported natively in `transformers>=4.52.1`

. Below is a simple example of how to use the `granite-4.0-1b-speech`

model.

## Get Alain Airom (Ayrom)’s stories in your inbox

Join Medium for free to get updates from this writer.

Several samples are provided on the model’s page on Hugging Face which could be used as-is just by copy/pasting the codes.

- Usage with Transformers

`pip install transformers torchaudio soundfile`

`import torch`

import torchaudio

from huggingface_hub import hf_hub_download

from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor


device = "cuda" if torch.cuda.is_available() else "cpu"


model_name = "ibm-granite/granite-4.0-1b-speech"

processor = AutoProcessor.from_pretrained(model_name)

tokenizer = processor.tokenizer

model = AutoModelForSpeechSeq2Seq.from_pretrained(

model_name, device_map=device, torch_dtype=torch.bfloat16

)


# Load audio

audio_path = hf_hub_download(repo_id=model_name, filename="multilingual_sample.wav")

wav, sr = torchaudio.load(audio_path, normalize=True)

assert wav.shape[0] == 1 and sr == 16000 # mono, 16kHz


# Create text prompt

user_prompt = "<|audio|>can you transcribe the speech into a written format?"

# Add "Keywords: <kw1>, <kw2> ..." at the end for keyword biasing

chat = [

{"role": "user", "content": user_prompt},

]

prompt = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)


# Run the processor + model

model_inputs = processor(prompt, wav, device=device, return_tensors="pt").to(device)

model_outputs = model.generate(

**model_inputs, max_new_tokens=200, do_sample=False, num_beams=1

)


# Transformers includes the input IDs in the response

num_input_tokens = model_inputs["input_ids"].shape[-1]

new_tokens = model_outputs[0, num_input_tokens:].unsqueeze(0)

output_text = tokenizer.batch_decode(

new_tokens, add_special_tokens=False, skip_special_tokens=True

)

print(f"STT output = {output_text[0]}")

- Usage with
`vLLM`


`pip install vllm`

`from transformers import AutoTokenizer`

from vllm import LLM, SamplingParams

from vllm.assets.audio import AudioAsset


model_id = "ibm-granite/granite-4.0-1b-speech"

tokenizer = AutoTokenizer.from_pretrained(model_id)


def get_prompt(question: str, has_audio: bool):

"""Build the input prompt to send to vLLM."""

if has_audio:

question = f"<|audio|>{question}"

chat = [

{

"role": "user",

"content": question

}

]

return tokenizer.apply_chat_template(chat, tokenize=False)


model = LLM(

model=model_id,

max_model_len=2048, # This may be needed for lower resource devices.

limit_mm_per_prompt={"audio": 1},

)


question = "can you transcribe the speech into a written format?"

prompt_with_audio = get_prompt(

question=question,

has_audio=True,

)

audio = AudioAsset("mary_had_lamb").audio_and_sample_rate


inputs = {

"prompt": prompt_with_audio,

"multi_modal_data": {

"audio": audio,

}

}


outputs = model.generate(

inputs,

sampling_params=SamplingParams(

temperature=0.2,

max_tokens=64,

),

)

print(f"Audio Example - Question: {question}")

print(f"Generated text: {outputs[0].outputs[0].text}")

- Specific online mode usage code;

`"""`

Launch the vLLM server with the following command:


vllm serve ibm-granite/granite-4.0-1b-speech \

--api-key token-abc123 \

--max-model-len 2048

"""


import base64


import requests

from openai import OpenAI


from vllm.assets.audio import AudioAsset


# Modify OpenAI's API key and API base to use vLLM's API server.

openai_api_key = "token-abc123"

openai_api_base = "http://localhost:8000/v1"


client = OpenAI(

# defaults to os.environ.get("OPENAI_API_KEY")

api_key=openai_api_key,

base_url=openai_api_base,

)


model_name = "ibm-granite/granite-4.0-1b-speech"

# Any format supported by librosa is supported

audio_url = AudioAsset("mary_had_lamb").url


# Use base64 encoded audio in the payload

def encode_audio_base64_from_url(audio_url: str) -> str:

"""Encode an audio retrieved from a remote url to base64 format."""

with requests.get(audio_url) as response:

response.raise_for_status()

result = base64.b64encode(response.content).decode("utf-8")

return result


audio_base64 = encode_audio_base64_from_url(audio_url=audio_url)


question = "can you transcribe the speech into a written format?"

chat_completion_with_audio = client.chat.completions.create(

messages=[{

"role": "user",

"content": [

{

"type": "text",

"text": question

},

{

"type": "audio_url",

"audio_url": {

# Any format supported by librosa is supported

"url": f"data:audio/ogg;base64,{audio_base64}"

},

},

],

}],

temperature=0.2,

max_tokens=64,

model=model_name,

)



print(f"Audio Example - Question: {question}")

print(f"Generated text: {chat_completion_with_audio.choices[0].message.content}")

- Usage with
`mlx-audio`

for Apple Silicon M series chips;

`pip install -U mlx-audio`

`from mlx_audio.stt.utils import load_model`

from mlx_audio.stt.generate import generate_transcription


model = load_model("mlx-community/granite-4.0-1b-speech-8bit")

transcription = generate_transcription(

model=model,

audio="audio.wav",

output_path="transcript.txt",

format="txt",

verbose=True,

)

print(transcription.text)

- There is also an online demo mode which could be used for tests (and more…)

![](https://miro.medium.com/v2/resize:fit:700/1*PZN6cALuFED7TaVg18Y1Lw.png)

## From Documentation to Deployment: Building with Granite 4.0

After diving into the **Hugging Face model card** and experimenting with the provided samples, I was impressed by the model’s efficiency. I decided to move beyond basic testing and build a fully functional, end-to-end application.

With **Bob** (our friendly implementation SDLC) leading the way, I’ve developed a streamlined tool that showcases exactly how **IBM Granite-4.0–1b-speech** handles complex, multilingual tasks in real-time. Below, I’m excited to share the architecture and the application itself.

`┌─────────────────────────────────────────────────────────────┐`

│ User Browser │

│ ┌────────────────────────────────────────────────────┐ │

│ │ Web Interface (index.html) │ │

│ │ • Drag & Drop Upload │ │

│ │ • Task Selection (Transcribe/Translate) │ │

│ │ • Language Selection │ │

│ │ • Results Display & Download │ │

│ └────────────────────────────────────────────────────┘ │

└─────────────────────────────────────────────────────────────┘

│

│ HTTP/REST API

▼

┌─────────────────────────────────────────────────────────────┐

│ Flask Web Server │

│ (app.py) │

│ ┌────────────────────────────────────────────────────┐ │

│ │ API Endpoints │ │

│ │ • GET / → Serve UI │ │

│ │ • GET /api/health → Health check │ │

│ │ • POST /api/process → Process audio │ │

│ └────────────────────────────────────────────────────┘ │

│ │ │

│ ▼ │

│ ┌────────────────────────────────────────────────────┐ │

│ │ Audio Processing Pipeline │ │

│ │ 1. File Upload & Validation │ │

│ │ 2. Audio Loading (Librosa) │ │

│ │ 3. Resampling to 16kHz │ │

│ │ 4. Tensor Conversion │ │

│ └────────────────────────────────────────────────────┘ │

└─────────────────────────────────────────────────────────────┘

│

▼

┌─────────────────────────────────────────────────────────────┐

│ ML Model Layer (PyTorch) │

│ ┌────────────────────────────────────────────────────┐ │

│ │ GraniteSpeechProcessor │ │

│ │ • Tokenization │ │

│ │ • Audio Feature Extraction │ │

│ │ • Input Preparation │ │

│ └────────────────────────────────────────────────────┘ │

│ │ │

│ ▼ │

│ ┌────────────────────────────────────────────────────┐ │

│ │ Granite-4.0-1b-speech Model │ │

│ │ • 1 Billion Parameters │ │

│ │ • Multilingual ASR/AST │ │

│ │ • CPU Execution (Apple Silicon) │ │

│ └────────────────────────────────────────────────────┘ │

│ │ │

│ ▼ │

│ ┌────────────────────────────────────────────────────┐ │

│ │ Output Processing │ │

│ │ • Token Decoding │ │

│ │ • Text Formatting │ │

│ │ • Result Preparation │ │

│ └────────────────────────────────────────────────────┘ │

└─────────────────────────────────────────────────────────────┘

│

▼

┌─────────────────────────────────────────────────────────────┐

│ Storage Layer │

│ • Model Cache: ~/.cache/huggingface/ │

│ • Uploads: ./uploads/ (temporary) │

│ • Virtual Env: ./venv/ │

└─────────────────────────────────────────────────────────────┘

![](https://miro.medium.com/v2/resize:fit:700/1*n7K-kmL5eLe9otBnr8TUBQ.png)

## Why this implementation works:

**Zero-Latency VAD:**Uses Voice Activity Detection to ensure we only process actual speech.**Hybrid Power:**Leverages the Mamba-Transformer architecture for high-speed processing on standard hardware.**Enterprise-Ready:**Built with the safety and transparency benchmarks that the Granite family is known for.

### The application

- The core (main / backend) part of the appliction is in Python, provided below;

`import os`

import torch

import torchaudio

import librosa

import numpy as np

from flask import Flask, request, jsonify, send_file, render_template

from flask_cors import CORS

from werkzeug.utils import secure_filename

from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor

import tempfile

import logging


# Configure logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


app = Flask(__name__)

CORS(app)


# Configuration

UPLOAD_FOLDER = 'uploads'

OUTPUT_FOLDER = 'outputs'

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'ogg', 'm4a'}

MAX_FILE_SIZE = 100 * 1024 * 1024 # 100MB


os.makedirs(UPLOAD_FOLDER, exist_ok=True)

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE


# Global variables for model and processor

model = None

processor = None

device = None


def allowed_file(filename):

"""Check if file extension is allowed"""

return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def initialize_model():

"""Initialize the Granite speech model for CPU execution on Apple Silicon"""

global model, processor, device


try:

logger.info("Initializing Granite-4.0-1b-speech model...")


# Force CPU usage (optimized for Apple Silicon)

device = "cpu"

logger.info(f"Using device: {device}")


model_name = "ibm-granite/granite-4.0-1b-speech"


# Load processor

logger.info("Loading processor...")

processor = AutoProcessor.from_pretrained(model_name)


# Load model with CPU optimization

logger.info("Loading model (this may take a few minutes)...")

model = AutoModelForSpeechSeq2Seq.from_pretrained(

model_name,

torch_dtype=torch.float32, # Use float32 for CPU

low_cpu_mem_usage=True,

)

model.to(device)

model.eval() # Set to evaluation mode


logger.info("Model initialized successfully!")

return True


except Exception as e:

logger.error(f"Error initializing model: {str(e)}")

return False


def transcribe_audio(audio_path, task="transcribe", source_lang="en", target_lang=None):

"""

Transcribe or translate audio file


Args:

audio_path: Path to audio file

task: "transcribe" for ASR or "translate" for AST

source_lang: Source language code (en, fr, de, es, pt, ja)

target_lang: Target language code (only for translation)

"""

try:

logger.info(f"Processing audio: {audio_path}")

logger.info(f"Task: {task}, Source: {source_lang}, Target: {target_lang}")


# Load audio - try torchaudio first, fallback to librosa for unsupported formats

logger.info("Loading audio...")

try:

wav, sr = torchaudio.load(audio_path, normalize=True)

logger.info(f"Loaded with torchaudio: shape={wav.shape}, sample_rate={sr}")

except Exception as e:

logger.info(f"torchaudio failed ({str(e)}), trying librosa...")

# Fallback to librosa for formats like M4A

audio_array, sr = librosa.load(audio_path, sr=None, mono=False)

# Convert to torch tensor with shape [channels, samples]

if audio_array.ndim == 1:

wav = torch.from_numpy(audio_array).unsqueeze(0) # Add channel dimension

else:

wav = torch.from_numpy(audio_array)

logger.info(f"Loaded with librosa: shape={wav.shape}, sample_rate={sr}")


# Resample to 16kHz if needed

if sr != 16000:

resampler = torchaudio.transforms.Resample(sr, 16000)

wav = resampler(wav)

sr = 16000

logger.info(f"Resampled to 16kHz: shape={wav.shape}")


# Prepare prompt based on task

if task == "translate" and target_lang:

user_prompt = f"<|audio|>translate from {source_lang} to {target_lang}"

else:

user_prompt = f"<|audio|>can you transcribe this audio"


# Create chat template

chat = [

{"role": "user", "content": user_prompt}

]

prompt = processor.tokenizer.apply_chat_template(

chat, tokenize=False, add_generation_prompt=True

)


# Process inputs - processor does NOT accept device_map

logger.info("Processing audio with model...")

model_inputs = processor(prompt, wav)


# Debug: Check what processor returns

logger.info(f"Processor output type: {type(model_inputs)}")

logger.info(f"Processor output: {model_inputs if not isinstance(model_inputs, dict) else 'dict with keys: ' + str(model_inputs.keys())}")


# Handle if processor returns a list (convert to dict)

if isinstance(model_inputs, list):

# Processor returned a list, need to convert to proper format

logger.info("Processor returned a list, converting...")

model_inputs = {

"input_ids": model_inputs[0] if len(model_inputs) > 0 else None,

"attention_mask": model_inputs[1] if len(model_inputs) > 1 else None,

}


# Convert lists to tensors and move to device

for k, v in model_inputs.items():

if isinstance(v, list):

model_inputs[k] = torch.tensor(v)

if isinstance(model_inputs[k], torch.Tensor):

model_inputs[k] = model_inputs[k].to(device)


# Generate transcription/translation

with torch.no_grad():

model_outputs = model.generate(

**model_inputs,

max_new_tokens=2048, # Increased to allow longer transcriptions

do_sample=False

)


# Decode output - decode the full output and extract the response

output_text = processor.tokenizer.decode(

model_outputs[0], skip_special_tokens=True

)


# Extract only the assistant's response (after the generation prompt)

# The output typically contains the full conversation including the prompt

if "<|assistant|>" in output_text:

output_text = output_text.split("<|assistant|>")[-1].strip()


logger.info(f"Processing complete. Output: {output_text}")

return output_text


except Exception as e:

logger.error(f"Error during transcription: {str(e)}")

raise


@app.route('/')

def index():

"""Serve the main UI"""

return render_template('index.html')


@app.route('/api/health', methods=['GET'])

def health_check():

"""Health check endpoint"""

return jsonify({

'status': 'healthy',

'model_loaded': model is not None,

'device': str(device) if device else None

})


@app.route('/api/transcribe', methods=['POST'])

def transcribe():

"""Transcribe audio file"""

try:

# Check if model is loaded

if model is None:

return jsonify({'error': 'Model not initialized'}), 500


# Check if file is present

if 'audio' not in request.files:

return jsonify({'error': 'No audio file provided'}), 400


file = request.files['audio']


if file.filename == '':

return jsonify({'error': 'No file selected'}), 400


if not allowed_file(file.filename):

return jsonify({'error': f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'}), 400


# Get parameters

task = request.form.get('task', 'transcribe')

source_lang = request.form.get('source_lang', 'en')

target_lang = request.form.get('target_lang', None)


# Save uploaded file

filename = secure_filename(file.filename)

filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

file.save(filepath)


try:

# Process audio

result = transcribe_audio(filepath, task, source_lang, target_lang)


# Save result to file

output_filename = f"{os.path.splitext(filename)[0]}_output.txt"

output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)


with open(output_path, 'w', encoding='utf-8') as f:

f.write(result)


return jsonify({

'success': True,

'text': result,

'output_file': output_filename

})


finally:

# Clean up uploaded file

if os.path.exists(filepath):

os.remove(filepath)


except Exception as e:

logger.error(f"Error in transcribe endpoint: {str(e)}")

return jsonify({'error': str(e)}), 500


@app.route('/api/download/<filename>', methods=['GET'])

def download_file(filename):

"""Download transcription result"""

try:

filepath = os.path.join(app.config['OUTPUT_FOLDER'], secure_filename(filename))

if os.path.exists(filepath):

return send_file(filepath, as_attachment=True)

else:

return jsonify({'error': 'File not found'}), 404

except Exception as e:

logger.error(f"Error in download endpoint: {str(e)}")

return jsonify({'error': str(e)}), 500


@app.route('/api/languages', methods=['GET'])

def get_languages():

"""Get supported languages"""

languages = {

'en': 'English',

'fr': 'French',

'de': 'German',

'es': 'Spanish',

'pt': 'Portuguese',

'ja': 'Japanese'

}

return jsonify(languages)


if __name__ == '__main__':

logger.info("Starting Granite Speech Application...")

logger.info("Initializing model (this may take a few minutes on first run)...")


if initialize_model():

logger.info("Model loaded successfully!")

logger.info("Starting Flask server...")

logger.info("Open http://localhost:8080 in your browser")

app.run(host='0.0.0.0', port=8080, debug=False)

else:

logger.error("Failed to initialize model. Exiting.")


# Made with Bob

- The requirements.txt which should be used;

`transformers==4.57.6`

torch==2.7.0

torchaudio==2.7.0

soundfile>=0.12.1

flask>=3.0.0

flask-cors>=4.0.0

werkzeug>=3.0.0

librosa>=0.10.0

numba>=0.58.0

numpy<2.0.0

- And the UI is full HTML based template;

`<!DOCTYPE html>`

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Granite Speech - ASR & Translation</title>

<style>

* {

margin: 0;

padding: 0;

box-sizing: border-box;

}


body {

font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;

background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

min-height: 100vh;

display: flex;

justify-content: center;

align-items: center;

padding: 20px;

}


.container {

background: white;

border-radius: 20px;

box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);

max-width: 800px;

width: 100%;

padding: 40px;

}


.header {

text-align: center;

margin-bottom: 40px;

}


.header h1 {

color: #333;

font-size: 2.5em;

margin-bottom: 10px;

}


.header p {

color: #666;

font-size: 1.1em;

}


.badge {

display: inline-block;

background: #667eea;

color: white;

padding: 5px 15px;

border-radius: 20px;

font-size: 0.9em;

margin-top: 10px;

}


.upload-section {

border: 3px dashed #ddd;

border-radius: 15px;

padding: 40px;

text-align: center;

margin-bottom: 30px;

transition: all 0.3s ease;

cursor: pointer;

}


.upload-section:hover {

border-color: #667eea;

background: #f8f9ff;

}


.upload-section.dragover {

border-color: #667eea;

background: #f0f2ff;

}


.upload-icon {

font-size: 4em;

margin-bottom: 20px;

}


.file-input {

display: none;

}


.btn {

background: #667eea;

color: white;

border: none;

padding: 12px 30px;

border-radius: 8px;

font-size: 1em;

cursor: pointer;

transition: all 0.3s ease;

margin: 5px;

}


.btn:hover {

background: #5568d3;

transform: translateY(-2px);

box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);

}


.btn:disabled {

background: #ccc;

cursor: not-allowed;

transform: none;

}


.btn-secondary {

background: #48bb78;

}


.btn-secondary:hover {

background: #38a169;

}


.options {

background: #f7fafc;

padding: 25px;

border-radius: 10px;

margin-bottom: 20px;

}


.option-group {

margin-bottom: 20px;

}


.option-group:last-child {

margin-bottom: 0;

}


.option-group label {

display: block;

color: #333;

font-weight: 600;

margin-bottom: 8px;

}


.option-group select {

width: 100%;

padding: 10px;

border: 2px solid #e2e8f0;

border-radius: 8px;

font-size: 1em;

background: white;

cursor: pointer;

}


.option-group select:focus {

outline: none;

border-color: #667eea;

}


.radio-group {

display: flex;

gap: 20px;

}


.radio-option {

display: flex;

align-items: center;

cursor: pointer;

}


.radio-option input[type="radio"] {

margin-right: 8px;

cursor: pointer;

}


.result-section {

background: #f7fafc;

padding: 25px;

border-radius: 10px;

margin-top: 20px;

display: none;

}


.result-section.show {

display: block;

}


.result-text {

background: white;

padding: 20px;

border-radius: 8px;

border: 1px solid #e2e8f0;

min-height: 100px;

max-height: 300px;

overflow-y: auto;

white-space: pre-wrap;

word-wrap: break-word;

line-height: 1.6;

color: #333;

}


.loading {

text-align: center;

padding: 20px;

display: none;

}


.loading.show {

display: block;

}


.spinner {

border: 4px solid #f3f3f3;

border-top: 4px solid #667eea;

border-radius: 50%;

width: 50px;

height: 50px;

animation: spin 1s linear infinite;

margin: 0 auto 20px;

}


@keyframes spin {

0% { transform: rotate(0deg); }

100% { transform: rotate(360deg); }

}


.error {

background: #fed7d7;

color: #c53030;

padding: 15px;

border-radius: 8px;

margin-top: 20px;

display: none;

}


.error.show {

display: block;

}


.success {

background: #c6f6d5;

color: #22543d;

padding: 15px;

border-radius: 8px;

margin-top: 20px;

display: none;

}


.success.show {

display: block;

}


.file-info {

background: #e6fffa;

padding: 15px;

border-radius: 8px;

margin-top: 15px;

display: none;

}


.file-info.show {

display: block;

}


.file-info strong {

color: #234e52;

}


.actions {

text-align: center;

margin-top: 20px;

}


.footer {

text-align: center;

margin-top: 30px;

color: #666;

font-size: 0.9em;

}


.footer a {

color: #667eea;

text-decoration: none;

}


.footer a:hover {

text-decoration: underline;

}

</style>

</head>

<body>

<div class="container">

<div class="header">

<h1>🎙️ Granite Speech</h1>

<p>Multilingual Speech Recognition & Translation</p>

<span class="badge">Powered by IBM Granite-4.0-1b-speech</span>

</div>


<div class="upload-section" id="uploadSection">

<div class="upload-icon">📁</div>

<h3>Drop your audio file here or click to browse</h3>

<p style="color: #666; margin-top: 10px;">Supported formats: WAV, MP3, FLAC, OGG, M4A (Max 100MB)</p>

<input type="file" id="fileInput" class="file-input" accept=".wav,.mp3,.flac,.ogg,.m4a">

</div>


<div class="file-info" id="fileInfo">

<strong>Selected file:</strong> <span id="fileName"></span>

</div>


<div class="options">

<div class="option-group">

<label>Task:</label>

<div class="radio-group">

<label class="radio-option">

<input type="radio" name="task" value="transcribe" checked>

Transcribe (Speech to Text)

</label>

<label class="radio-option">

<input type="radio" name="task" value="translate">

Translate (Speech to Speech)

</label>

</div>

</div>


<div class="option-group">

<label for="sourceLang">Source Language:</label>

<select id="sourceLang">

<option value="en">English</option>

<option value="fr">French</option>

<option value="de">German</option>

<option value="es">Spanish</option>

<option value="pt">Portuguese</option>

<option value="ja">Japanese</option>

</select>

</div>


<div class="option-group" id="targetLangGroup" style="display: none;">

<label for="targetLang">Target Language:</label>

<select id="targetLang">

<option value="en">English</option>

<option value="fr">French</option>

<option value="de">German</option>

<option value="es">Spanish</option>

<option value="pt">Portuguese</option>

<option value="ja">Japanese</option>

</select>

</div>

</div>


<div class="actions">

<button class="btn" id="processBtn" disabled>Process Audio</button>

</div>


<div class="loading" id="loading">

<div class="spinner"></div>

<p>Processing your audio... This may take a moment.</p>

</div>


<div class="error" id="error"></div>

<div class="success" id="success"></div>


<div class="result-section" id="resultSection">

<h3 style="margin-bottom: 15px;">Result:</h3>

<div class="result-text" id="resultText"></div>

<div class="actions">

<button class="btn btn-secondary" id="downloadBtn">Download Result</button>

<button class="btn" id="newBtn">Process Another File</button>

</div>

</div>


<div class="footer">

<p>Optimized for Apple Silicon • Offline Execution</p>

<p><a href="https://huggingface.co/ibm-granite/granite-4.0-1b-speech" target="_blank">Learn more about Granite Speech</a></p>

</div>

</div>


<script>

let selectedFile = null;

let outputFilename = null;


const uploadSection = document.getElementById('uploadSection');

const fileInput = document.getElementById('fileInput');

const fileInfo = document.getElementById('fileInfo');

const fileName = document.getElementById('fileName');

const processBtn = document.getElementById('processBtn');

const loading = document.getElementById('loading');

const error = document.getElementById('error');

const success = document.getElementById('success');

const resultSection = document.getElementById('resultSection');

const resultText = document.getElementById('resultText');

const downloadBtn = document.getElementById('downloadBtn');

const newBtn = document.getElementById('newBtn');

const taskRadios = document.querySelectorAll('input[name="task"]');

const targetLangGroup = document.getElementById('targetLangGroup');


// Handle task change

taskRadios.forEach(radio => {

radio.addEventListener('change', (e) => {

if (e.target.value === 'translate') {

targetLangGroup.style.display = 'block';

} else {

targetLangGroup.style.display = 'none';

}

});

});


// Click to upload

uploadSection.addEventListener('click', () => {

fileInput.click();

});


// Drag and drop

uploadSection.addEventListener('dragover', (e) => {

e.preventDefault();

uploadSection.classList.add('dragover');

});


uploadSection.addEventListener('dragleave', () => {

uploadSection.classList.remove('dragover');

});


uploadSection.addEventListener('drop', (e) => {

e.preventDefault();

uploadSection.classList.remove('dragover');

const files = e.dataTransfer.files;

if (files.length > 0) {

handleFileSelect(files[0]);

}

});


// File input change

fileInput.addEventListener('change', (e) => {

if (e.target.files.length > 0) {

handleFileSelect(e.target.files[0]);

}

});


function handleFileSelect(file) {

selectedFile = file;

fileName.textContent = file.name;

fileInfo.classList.add('show');

processBtn.disabled = false;

hideMessages();

resultSection.classList.remove('show');

}


// Process button

processBtn.addEventListener('click', async () => {

if (!selectedFile) return;


const task = document.querySelector('input[name="task"]:checked').value;

const sourceLang = document.getElementById('sourceLang').value;

const targetLang = document.getElementById('targetLang').value;


const formData = new FormData();

formData.append('audio', selectedFile);

formData.append('task', task);

formData.append('source_lang', sourceLang);

if (task === 'translate') {

formData.append('target_lang', targetLang);

}


processBtn.disabled = true;

loading.classList.add('show');

hideMessages();

resultSection.classList.remove('show');


try {

const response = await fetch('/api/transcribe', {

method: 'POST',

body: formData

});


const data = await response.json();


if (response.ok && data.success) {

resultText.textContent = data.text;

outputFilename = data.output_file;

resultSection.classList.add('show');

success.textContent = 'Processing completed successfully!';

success.classList.add('show');

} else {

throw new Error(data.error || 'Processing failed');

}

} catch (err) {

error.textContent = `Error: ${err.message}`;

error.classList.add('show');

} finally {

loading.classList.remove('show');

processBtn.disabled = false;

}

});


// Download button

downloadBtn.addEventListener('click', () => {

if (outputFilename) {

window.location.href = `/api/download/${outputFilename}`;

}

});


// New file button

newBtn.addEventListener('click', () => {

selectedFile = null;

outputFilename = null;

fileInput.value = '';

fileInfo.classList.remove('show');

resultSection.classList.remove('show');

processBtn.disabled = true;

hideMessages();

});


function hideMessages() {

error.classList.remove('show');

success.classList.remove('show');

}


// Check server health on load

window.addEventListener('load', async () => {

try {

const response = await fetch('/api/health');

const data = await response.json();

if (!data.model_loaded) {

error.textContent = 'Model is not loaded. Please check the server logs.';

error.classList.add('show');

}

} catch (err) {

error.textContent = 'Cannot connect to server. Please ensure the server is running.';

error.classList.add('show');

}

});

</script>

</body>

</html>

- And below the full application up and running 🎉

![](https://miro.medium.com/v2/resize:fit:700/1*WFPrOYI3ZHoUWCBHElUSFw.png)

Here, making a simple voice message and uploading it through the UI, the result is displyed on the screen and could be downloaded as a text file.

## Conclusion

![](https://miro.medium.com/v2/resize:fit:700/1*bJQVypHvrCbIiNd7tS_c1g.png)

In conclusion, the provided implementation demonstrates the seamless transition from a theoretical model to a production-ready application. By combining the high-performance **IBM Granite-4.0–1b-speech** model with a robust, Apple Silicon-optimized architecture, this project achieves efficient, offline multilingual transcription and translation. From the detailed architecture to the interactive web interface, these resources serve as a comprehensive blueprint for enterprise-grade AI deployment. With the creative power of **Bob** at the helm of the implementation, we can see that even the most advanced 1-billion parameter models can be made accessible, functional, and ready for real-world impact.

**>>> Thanks for reading **🙌 **<<<**

## Links

- IBM Granite: https://www.ibm.com/fr-fr/granite
- ibm-granite/granite-4.0–1b-speech: https://huggingface.co/ibm-granite/granite-4.0-1b-speech
- Live IBM Granite 4.0 1B Speech Recognition & Translation Demo: https://huggingface.co/spaces/ibm-granite/granite-speech
- IBM Granite Models on Hugging Face: https://huggingface.co/ibm-granite

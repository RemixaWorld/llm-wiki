---
domain: github.com
fetch_date: '2026-05-18T12:35:31.252792'
status: ok
url: https://github.com/deepdoctection/deepdoctection
---

Version `v.1.0`

includes a major refactoring. Key changes include:

- PyTorch-only support for all deep learning models.
- Support for many more fine-tuned models from the Huggingface Hub (Bert, RobertA, LayoutLM, LiLT, ...)
- Decomposition into small sub-packages: dd-core, dd-datasets and deepdoctection
- Type validations of core data structures
- New test suite


**deep**doctection is a Python library that orchestrates Scan and PDF document layout analysis, OCR and document
and token classification. Build and run a pipeline for your document extraction tasks, develop your own document
extraction workflow, fine-tune pre-trained models and use them seamlessly for inference.

- Document layout analysis and table recognition in PyTorch with
**Detectron2**and**Transformers**, - OCR with support of
**Tesseract**,**DocTr**and**AWS Textract**, - Document and token classification with the
**LayoutLM**family,**LiLT**and and many**Bert**-style models including features like sliding windows. - Text mining for native PDFs with
**pdfplumber**, - Language detection with with transformer based
`papluca/xlm-roberta-base-language-detection`

. - Deskewing and rotating images with
**jdeskew**or**Tesseract**. - Fine-tuning object detection, document or token classification models and evaluating whole pipelines.
- Lot's of tutorials

Have a look at the **introduction notebook** for an easy start.

Check the **release notes** for recent updates.

Check the demo of a document layout analysis pipeline with OCR on 🤗
**Hugging Face spaces**.

The following example shows how to use the built-in analyzer to decompose a PDF document into its layout structures.

```
import deepdoctection as dd
from IPython.core.display import HTML
from matplotlib import pyplot as plt
analyzer = dd.get_dd_analyzer() # instantiate the built-in analyzer similar to the Hugging Face space demo
df = analyzer.analyze(path = "/path/to/your/doc.pdf") # setting up pipeline
df.reset_state() # Trigger some initialization
doc = iter(df)
page = next(doc)
image = page.viz(show_figures=True, show_residual_layouts=True)
plt.figure(figsize = (25,17))
plt.axis('off')
plt.imshow(image)
```

```
HTML(page.tables[0].html)
```


```
print(page.text)
```


- Python >= 3.10
- PyTorch >= 2.6
- To fine-tune models, a GPU is recommended.

We recommend using a virtual environment.

For a simple setup which is enough to parse documents with the default setting, install the following

```
uv pip install timm # needed for the default setup
uv pip install transformers
uv pip install python-doctr
uv pip install deepdoctection
```


This setup is sufficient to run the **introduction notebook**.

The following installation will give you a general setup so that you can experiment with various configurations. Remember, that you always have to install PyTorch separately.

First install **Detectron2** separately as it is not distributed via PyPi. Check the instruction
here or try:

```
uv pip install --no-build-isolation detectron2@git+https://github.com/deepdoctection/detectron2.git
```


Then install **deep**doctection with all its dependencies:

```
uv pip install deepdoctection[full]
```


You can install **deep**doctection using Conda or Mamba with the provided `environment.yml`

:

```
# Using conda
conda env create -f environment.yml
conda activate deepdoctection
# Using mamba (faster)
mamba env create -f environment.yml
mamba activate deepdoctection
```

For further information, please consult the **full installation instructions**.

Download the repository or clone via

```
git clone https://github.com/deepdoctection/deepdoctection.git
```


The easiest way is to install with make. A virtual environment is required

`make install-dd`

Pre-existing Docker images can be downloaded from the Docker hub.

Additionally, specify a working directory to mount files to be processed into the container.

```
docker compose up -d
```


will start the container. There is no endpoint exposed, though.

We thank all libraries that provide high quality code and pre-trained models. Without, it would have been impossible to develop this framework.

...you can easily support the project by making it more visible. Leaving a star or a recommendation will help.

Distributed under the Apache 2.0 License. Check LICENSE for additional information.

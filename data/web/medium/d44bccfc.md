---
domain: medium.com
fetch_date: '2026-05-18T12:46:23.016659'
status: ok
url: https://medium.com/@matt.noe/tutorial-how-to-train-layoutlm-on-a-custom-dataset-with-hugging-face-cda58c96571c
---

# [Tutorial] How to Train LayoutLM on a Custom Dataset with Hugging Face

[ ![Matt Noe](https://miro.medium.com/v2/da:true/resize:fill:64:64/0*Ei674BEvLE29THyN) ](</@matt.noe?source=post_page---byline--cda58c96571c--------------------------------------->)

[Matt Noe](</@matt.noe?source=post_page---byline--cda58c96571c--------------------------------------->)

7 min read

·

Nov 9, 2022

\--

\--

Listen

Share

More

## Overview

LayoutLMv3 is a pre-trained transformer model published by Microsoft that can be used for various document AI tasks, including:

1. Information Extraction
2. Document Classification
3. Document Question Answering

LayoutLMv3 incorporates both text and visual image information into a single multimodal transformer model, making it quite good at both text-based tasks (form understanding, id card extraction and document question answering) and image-based tasks (document classification and layout analysis).

![image](https://miro.medium.com/v2/resize:fit:700/0*vrQYZuLVJFIlZA81.png)

If you’d like to learn more about what LayoutLMv3 is, you can check out the [white paper](<https://arxiv.org/pdf/2204.08387.pdf>) or the [Github repo](<https://github.com/microsoft/unilm/tree/master/layoutlmv3>).

## What this guide will cover

Many great guides exist on how to train LayoutLM on common large public datasets such as FUNSD and CORD. If that is what you are looking for, we recommend taking a look at [this great python notebook](<https://github.com/NielsRogge/Transformers-Tutorials/blob/master/LayoutLMv3/Fine_tune_LayoutLMv3_on_FUNSD_\(HuggingFace_Trainer\).ipynb>) that Niels Rogge from Hugging Face team has put out.

When it comes to building a document processing model for real-world applications, you’ll typically be training a model on your own custom documents, rather than one of these common datasets.

This guide is intended to walk you through the process of training LayoutLM on your own custom documents.

We’ll walk through a python notebook that covers:

1. Building your annotated document dataset using the [Butler](<https://www.butlerlabs.ai/>) UI
2. Converting annotated documents into the format expected by LayoutLMv3 using the [_DocAI_ SDK](<https://github.com/butlerlabs/docai>)
3. Using Hugging Face transformers to train LayoutLMv3 on your custom dataset
4. Running inference on your trained model

For the purposes of this guide, we’ll train a model for extracting information from US Driver’s Licenses, but feel free to follow along with any document dataset you have.

If you just want the code, you can check it [out here](<https://colab.research.google.com/drive/1KtzdLOpLQhHrca8oRM5s8fjKiMgkl5mb#scrollTo=P_bmoVcShf6E>).

Let’s get to it!

## Preparing the LayoutLM Development Environment

To start off, let’s install all of the necessary packages:

## Building your annotated dataset

Now that our environment is set up, we’ll need to prepare our annotated document dataset so that we can use it during training.

We’ll use the Butler document annotation interface for this purpose. If you haven’t already, head over to the [Butler app](<https://app.butlerlabs.ai/>) and create your account.

We won’t cover the full details of how to use the Butler UI to annotate documents in this guide (feel free to[ check out the documentation](<https://docs.butlerlabs.ai/reference/building-custom-form-extraction-models>) if you want to learn more), but we’ll cover most of the key points.

## Upload Documents

Once you have created your first model and given it a helpful name, you’ll want to upload your unannotated documents. Typically when training a LayoutLM model, you’ll want a training dataset that includes a few hundred annotated documents in it.

For this guide, we’ll get started with just 50 example driver’s licenses. We can always annotate more after we see how the model initially performs.

![image](https://miro.medium.com/v2/resize:fit:700/0*Mzk3xCnSSZ9axQDh.png)

Once the initial OCR has finished on your documents, you should see the documents loaded and ready for annotation.

## Define Schema and Annotate your Documents

The next step is to define what information you’d like to extract from your documents. We’ll be extracting the following fields from our driver’s licenses:

1. First Name (we’ll include Middle Initial here as well)
2. Last Name
3. Address
4. Date of Birth
5. Expiration Date
6. Driver’s License Number

Click on the Add button to add each individual field. Once finished, your extraction schema is defined, and you are ready to start annotating:

![image](https://miro.medium.com/v2/resize:fit:700/0*cTHzRX-bKpZRsY_S.png)

To annotate, make sure the right field is selected and simply drag a box around the text in the document. You can also click on individual pieces of text if you’d like.

![image](https://miro.medium.com/v2/resize:fit:700/0*P2svmq4ApJiKzSPl.png)

Once your first document is annotated, you can deselect the active field, and you’ll be able to see all of the values you annotated on the document.

Great work! Now we’ll go through and annotate the remaining documents.

A few quick hot keys you might find helpful:

1. **Tab (and Shift+Tab):** Switch between fields
2. **Cmd+A:** While annotating a table, adds a new row
3. Note: **Windows Key + A** on Windows machines

## Converting your annotations into LayoutLM Format

## Download annotations from Butler

Now that we have our annotated dataset, we need to download it from Butler, so that we can prepare it for use with LayoutLM in the transformers library. This is very easy to do with the [DocAI Python SDK](<https://github.com/butlerlabs/docai>):

First, we download all the annotations from the model we created in Butler. You can follow [this guide to find your API Key](<https://docs.butlerlabs.ai/reference/authentication>) and [this guide to find your model id](<https://docs.butlerlabs.ai/reference/finding-a-model-id>).

The _load_annotations_ function returns an Annotations object which enables you to convert your annotations into different formats.

## Prepare for use with LayoutLM

We’ll then need to convert into a format more readily usable by the transformers library and LayoutLMv3 specifically.

There is a lot actually occurring in these two simple lines of code.

First, we convert our annotations into a common NER format. Let’s take a look:

![image](https://miro.medium.com/v2/resize:fit:700/0*riWq2hE0Be3veSfC.png)

Here is a brief description of each field:

1. **id:** The id of the document in Butler
2. **tokens:** The words in the document
3. **bboxes:** The bounding box for the corresponding word in tokens. Bounding boxes are in Min/Max format: [x_min, y_min, x_max, y_max]
4. **ner_tags:** The string form of the annotation for the corresponding word in tokens. Notice that we called _as_ner_ with _as_iob2=True_ so the annotations have been broken up into[ Inside-Outside-Beginning format.](<https://www.google.com/search?q=iob+format&oq=iob&aqs=chrome.0.69i59j69i57.1093j0j7&sourceid=chrome&ie=UTF-8>)
5. **image:** A pillow image

Note: The load_annotations function does not currently support multi-page documents. Only the first page of a multi-page document is included.

After loading in the NER format, we normalize the bounding boxes so that they are between 0 and 1000, which is the format that LayoutLMv3 expects.

Finally, we load our annotations into a Hugging Face Dataset object:

We are now ready to train our model!

## Training LayoutLMv3 on the Custom Dataset

Let’s create a few helpful variables, as well as prepare our dataset for training:

Now our dataset is officially ready for training! From here on out, we’ll be following the guides put out by the Hugging Face team for how to fine-tune LayoutLM (here it is for [reference](<https://github.com/NielsRogge/Transformers-Tutorials/blob/master/LayoutLMv3/Fine_tune_LayoutLMv3_on_FUNSD_\(HuggingFace_Trainer\).ipynb>)).

## Convert dataset into LayoutLM format

First load the layoutlmv3-base processor from the Hugging Face hub:

Then prepare the train and eval datasets:

## Define evaluation metrics

Now we are ready to define the evaluation function. We’ll use a utility fn from the _DocAI_ SDK to do so:

## Train the model

Once that is done, we can define the model and training parameters:

There are a lot of different hyperparameters that can be tuned. Check out the Hugging Face documentation [here](<https://huggingface.co/docs/transformers/v4.23.1/en/main_classes/trainer#transformers.TrainingArguments>) to read through all of them.

Finally, the best part:

If everything was done correctly, your model will begin training.

Depending on the machine, this may take a little while, so sit back and relax. You can also explore some of the pre-trained document extraction models we have ready for use at [Butler](<https://app.butlerlabs.ai/library>) if you’d like :)

Once training finishes, you should see the metrics about how it performed on the eval dataset:

![image](https://miro.medium.com/v2/resize:fit:700/0*6o8dfYsC6EC90VA0.png)

You can see our model achieved a near 100% accuracy which is quite good. Given our dataset was a relatively simple set of example US Driver’s License images, we’d expect to see this high accuracy.

Even for more complicated use cases, LayoutLM can still reach impressively high accuracy!

If you want, you can publish your model to the Hugging Face hub for future use:

## Running inference

Now let’s try using our model to make predictions on a document. First we’ll generate the predictions:

Before visualizing the predicted results, let’s define a few utility functions to make this a bit easier:

Then let’s visualize the predicted results:

‍

![image](https://miro.medium.com/v2/resize:fit:700/0*xl_ZLPP7H2e1YE_B.png)

And compare against the actual ground truth values:

When comparing, we can see how accurate our LayoutLM model is:

![image](https://miro.medium.com/v2/resize:fit:700/0*LaVnY_WmPlGTk0cV.png)

## Conclusion

Great work! As you can see, LayoutLM is a powerful multimodal model that you can apply for many different Document AI tasks.‍

In this tutorial you:

1. Built an annotated dataset for your custom documents with Butler
2. Converted those annotations into a format usable by LayoutLMv3 using the [_DocAI_ SDK](<https://github.com/butlerlabs/docai>)
3. Trained a custom LayoutLMv3 model with Hugging Face transformers
4. Visualized the results of running inference on your trained model

You can find the full code available at our [Train LayoutLM on a Custom Dataset notebook](<https://colab.research.google.com/drive/1KtzdLOpLQhHrca8oRM5s8fjKiMgkl5mb#scrollTo=P_bmoVcShf6E>).

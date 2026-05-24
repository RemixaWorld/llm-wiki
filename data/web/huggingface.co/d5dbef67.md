---
domain: huggingface.co
fetch_date: '2026-05-18T12:37:48.118120'
status: ok
url: https://huggingface.co/blog/nadiinchi/provence
---

![](https://cdn-avatars.huggingface.co/v1/production/uploads/646cf8084eefb026fb8fd8bc/oCTqufkdTkjyGodsx1vo1.png)

# Provence: efficient and robust context pruning for retrieval-augmented generation

![image/png](https://cdn-uploads.huggingface.co/production/uploads/63bea3d44a2beec6555fd7dc/amhGbhr0bGwW_jtiqQdOH.png)

Acccepted to ICLR 2025

Paper: https://arxiv.org/abs/2501.16214

Model: https://huggingface.co/naver/provence-reranker-debertav3-v1

Acronym: *Pruning and Reranking Of retrieVEd relevaNt ContExts*

Developed at Naver Labs Europe

Provence is a method for training a lightweight **context pruning model** for retrieval-augmented generation, particularly optimized for question answering. Given a user question and a retrieved passage, Provence **removes sentences from the passage that are not relevant to the user question**. This **speeds up generation** and **reduces context noise**, in a plug-and-play manner **for any LLM or retriever**.

Here is how we train Provence in a nutshell (more details below):

We create synthetic targets for training, using an LLM (for context pruning) or a pretrained reranker (for reranking scores), and tune a pretrained reranker on the synthetised data so that the final unified model can perform efficient context pruning and reranking. The simplifid version of the model (standalone context pruner without reranking) can be trained by tuning a pretrained Deberta model (or any BERT-based model) on the LLM-produced pruning targets. Combining context pruning and reranking in a unified model does not hurt neither reranking performance nor context pruning performance.

Key features of Provence (Pruning and Reranking Of retrieVEd relevaNt ContExt):

**Provence encodes all sentences in the passage and the user question together**: this enables capturing of coreferences between sentences and provides more accurate context pruning.**Provence automatically detects the number of sentences to keep**, based on a threshold. We found that the default value of a threshold works fine across various domains, but the threshold can be adjusted further to better meet the particular use case needs.**Provence is efficient**: Provence provides a compact DeBERTa-based model, and it can be used either as a**standalone context pruner**or as a**unified reranking+context pruning model**. In the later case, we incorporate context pruning into reranking, an already existing stage of modern RAG pipelines. The unification of reranking+pruning makes context pruning almost**zero cost in the RAG pipeline**!**Provence is robust across domains**and**works out-of-the-box with any LLM and retriever**.

Below we discuss these features in more detail, as well as model training and evaluation results.

## Retrieval-augmented generation

Let's first discuss the case of a standalone context pruning model.

A typical RAG pipeline consists of three steps:

Here (1) retrieval + (2) reranking* provide a set of passages, or contexts, relevant to the given question, and (3) generation provides a final answer, relying on the provided contexts and internal LLM capabilities.

* The difference between retrieval and reranking will be discussed below.

**Context pruning** is usually applied before step (3), i.e. it performs postprocessing of the relevant contexts. The purpose of context pruning is to reduce the length of the contexts, which will enable speed up in generation, and also to decrease the context noise.

This is how the final RAG pipeline will look with context pruning, in more details:

## How we train standalone Provence

**Data**: MS-Marco, often used to train retrieval models. We use the document-level version and split documents into passages of random length (1-10 sentences) to ensure robustness of the final model w.r.t. the context length.

**Step 1**: retrieve passages relevant to the train questions from MS-Marco

**Step 2**: prompt LLama-3-8B to select relevant sentences for each question-passage pair. This will be used as synthetic labels for context pruning.

**Step 3**: tune the pretrained Deberta-v3 model:

- model input: a concatenation of a question and a passage
- model output: per-token binary mask, with 1 for tokens of the sentences marked as relevant in the synthetic labeling, and 0 for all other tokens
- this model is called
*cross-encoder*since it encodes a passage together with a question.

At the inference time, we use a threshold to binarize model predictions, and prune sentences with more predicted 0s than 1s. Due to the sentence-level targets, model predictions naturally cluster within each sentence, i.e. in most cases model predictions within one sentence will be close to each other.

## Properties of Provence

Existing context pruners encode sentences *independently*, losing information about coreferences between sentences. In the example below, the highlighted sentences are unclear without the preceding sentences (that they are about pumpkin), and may be mistakenly pruned out if sentences are processed independently. On the contrary, **Provence encodes all sentences together using the cross-encoder architecture and processes such cases correctly**.

Another important feature is that **Provence automatically detects the number of relevant sentences in the provided context**. Existing pruners often require providing the number of sentences to keep as a hyperparameter, which is an unrealistic setting. The following example demonstrates that the number of relevant sentences depends on the particular question-context pair:

Finally, **Provence is fast**: Provence relies on a lightweight DeBERTa-based architecture instead of billion-sized LLMs and treats context pruning as an extractive labeling task, instead of a slow autoregressive generation paradigm. The following figure demonstrates the efficiency comparison between the standalone Provence and other compressors, as well as the obtained generation speed up:

Furthermore, we propose to incorporate context pruning into reranking, making context pruning zero-cost in the RAG pipeline. Let's discuss this part now.

## Unifying context pruning and reranking in Provence

As discussed above, a typical high-performing RAG pipeline consists of three components:

The **reranking** step is often overlooked in academic RAG settings (as we discuss in our Bergen work), however it is a must-have step in strong information retrieval systems and an essential part of high-performing search pipelines in production (see e.g. this blogpost).

The first stage **retrieval** encodes queries and passages independently for efficiency, i.e. passages are pre-encoded offline, and when a user asks a question, only the question gets encoded and the fast search is being performed. The second stage, **reranking**, operates on top of the results of the first stage (hence a much smaller number of passages, e.g. 50), and **encodes each context together with the question**, i.e. using a **cross-encoder**. This provides much more informative embeddings and substantially improves search results.

**In Provence, we propose to enhance the reranker with the context pruning capabilities.** This is possible because:

- both models are cross-encoders, i.e. they have the same input of a [BOS] symbol + a question + a passage
- the output spaces of models do not overlap: the reranking score is output for the [BOS] position and the context pruning mask is output for passage tokens positions
- the objectives of reranking and context pruning are related, meaning that these tasks may potentially transfer knowledge between each other.

**With this unification, context pruning becomes zero-cost in the RAG pipeline, since it is incorporated into an existing RAG step!**

This is how the RAG pipeline looks like when we unify reranking + context pruning:

**How we train a joint model**: we start training from an existing reranking model, e.g. Deberta-v3-reranker in our case, and add a self-distillation regularizer which promotes the preservation of the reranking capabilities.

With Steps 1 and 2 described above, we add Step 2a and modify Step 3:

**Step 2a:** save the reranking scores from the pretrained reranker, for each question-passage pair. These scores will be used as targets for the reranking training objective.

**Step3:** tune the pretrained reranker with two prediction heads: one for predicting the reranking score from the “BOS” embedding, and one for predicting the binary pruning mask from the embeddings of context tokens. The training loss is a weighted sum of the context pruning loss and the reranking self-distillation loss.

## Evaluation results

We compare Provence to existing context pruners, e.g. to those that process sentences independently (extractive RECOMP and DSLR), that treat context pruning as a generative task (e.g. abstractive RECOMP), and that perform token-level pruning (LLMLingua family, this is an orthogonal line of work to ours).

In all plots, metrics on both axes are the higher the better, i.e. the models need to approach **the top right corner**.

We find that Provence consistently outperforms other approaches, in all domains, and stays on the **Pareto front**. Furthermore, **Provence is the only model that performs context pruning with little-to-no drop in performance**.

### Provence automatically detects the number of relevant sentences in the context

An important distinguished feature of Provence is that at inference, it **automatically detects the number of relevant sentences in the given context**, as it may vary from zero to all sentences. This feature comes from the synthetic labeling which also contains various numbers of relevant sentences.

The number of selected sentences is influenced by a threshold, applied over model predictions to obtain a binary mask. In all the results plots presented above, Provence is represented by two dots: one with the pruning threshold of 0.1 and another dot with the pruning threshold of 0.5.

We observe that:

- the selected values of the threshold work well in all domains, meaning that
**the users can use the default threshold values**; - the pruning threshold of 0.1 leads to more conservative pruning with no performance drop or lowest performance drops, and the pruning threshold of 0.5 leads to higher compression.

The users can further adjust the value of the threshold to better meet the needs of a particular use case!

In the figure below we show that **the number of sentences selected by Provence correlates highly with “ground-truth” number of sentences** . The “ground-truth” number of sentences of zero corresponds to using randomly selected contexts for questions, and all the higher values come from the LLM-produced labeling.

## Provence is robust w.r.t the position of the relevant information in the context

We also conduct a **needle-in-the-haystack experiment**, with synthetically constructed contexts. In particular, we write a few keyword-oriented questions, e.g. question: *“How is the trained model called?”* -> needle: *“The trained model is called Provence”*, and place the needle sentence at various positions in randomly selected contexts from Wikipedia.

We consider 1-sentence needles (example above) and 2-sentence needles. An example of reformulation into a 2-sentence needle: *“How is the trained model called?”* -> 2-sent needle: *“We trained a model. It is called Provence”*. The model needs to detect that both sentences are needed to answer the question.

In the figure below, we show that Provence selects correct needle sentences in almost all cases, except the leftmost and rightmost positions which exhibit occasional drops, since these positions happen to be relevant very rarely (in the data and hence in practice).

We provide **more experiments in the paper**, e.g. an ablation study on various parts of the training pipeline, or **showing that Provence results are similar with various retrievers / rerankers / generators / passage lengths**!

## Summary

- Provence is an efficient plug-and-play context pruner for RAG, capable of removing context sentences irrelevant to the user question, with little-to-no drop in performance.
- Two main ingredients of Provence are (1) casting context pruning as sequence labeling, and (2) unifying context pruning and reranker in a single model;
- Provence automatically detects the number of relevant sentences in a given context, performs well in various domains, and can be used with any LLM or retrievers.

Paper: https://arxiv.org/abs/2501.16214

Model: https://huggingface.co/naver/provence-reranker-debertav3-v1

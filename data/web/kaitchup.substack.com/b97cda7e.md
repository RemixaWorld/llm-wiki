---
domain: kaitchup.substack.com
fetch_date: '2026-05-18T12:38:00.837581'
status: ok
title: 'Gemma 3 270M: Can Tiny Models Learn New Tasks?'
url: https://kaitchup.substack.com/p/gemma-3-270m-can-tiny-models-learn
---

![Image generated with ChatGPT](https://substackcdn.com/image/fetch/$s_!4irK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc024738b-02e2-466f-bca7-8d435a776177_1024x1024.png) 

At one end of the spectrum are giant open-weight models like DeepSeek and Kimi, which require multiple GPU nodes to keep their full weights in GPU memory. They’re among the strongest open-weights LLMs available.

At the other end are tiny, edge-friendly models, such as Qwen3-0.6B, SmolLM2-360M, and the recent LFM-2-350M, built to run on devices with tight memory and compute budgets, from smartphones to smartwatches. Google has also joined this camp with Gemma 3-270M, the smallest Gemma 3 variant.

That said, these ultralight models aren’t drop-in replacements for their larger counterparts. Used the same way, they often feel constrained, especially on instruction following, and their performance tends to degrade as prompts grow longer.

Google reports ~50 points of accuracy on IFEval for Gemma 3 270M, which is impressive for such a small model.

![image](https://substackcdn.com/image/fetch/$s_!sZHF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa81b3aad-a35d-4053-bb8a-032691097946_4001x2251.jpeg) 

Still, it highlights clear limits: scoring ~50% on an old benchmark, which has likely contaminated the pre-training data,1 trails well-known old baselines such as Mistral 7B Instruct and Llama 2 7B. In practice, Gemma 3 270M often fails to follow instructions and tends to produce low-utility answers.

Used “as is” for general-purpose tasks, tiny models like Gemma 3 270M can be great, but are unreliable too often for users to trust them. To be more useful, they should be fine-tuned for a narrowly defined task and domain. Constraining the scope, with a specific input format, a specific objective, and a specific domain vocabulary optimized in the weights, can dramatically improve reliability.

In this article, I show how to teach Gemma 3 270M a task it initially can’t perform, English→French translation, using an inexpensive full fine-tune you can run on a laptop. Out of the box, the model often produces broken French or misinterprets the instruction. After a targeted fine-tune, it becomes serviceable for this narrow task, yielding better translations than much larger models.

The fine-tuning notebook is here:

You can adapt the notebook to other Gemma 3 variants and translation directions by changing the model and language names. I recommend a 6 GB GPU; with a reduced sequence length, a 4 GB GPU can work.

Structure of the article:

  1. Brief review of Gemma 3 270M: its architecture and pretraining.

  2. Dataset preparation for fine-tuning.

  3. Fine-tuning with Unsloth.

  4. Learning-curve comparison and evaluation.

  5. Practical tips for reading curves and iterating to improve results.

## A Brief Review of Gemma 3 270M

The Gemma 3 family is mostly multimodal, but, like the [1B model](<https://huggingface.co/google/gemma-3-1b-it>), the [270M variant](<https://huggingface.co/google/gemma-3-270m>) is text-only. You can inspect its architecture directly from the model’s [config.json (this works for any model supported by Hugging Face Transformers).](<https://huggingface.co/google/gemma-3-270m/blob/main/config.json>)

**Scale and vocabulary.** Gemma 3 270M allocates roughly ~170M parameters to embeddings and ~100M to the transformer stack. Its vocabulary is unusually large for a model this small (262,144 tokens). In principle, that breadth helps with rare or domain-specific terms and makes a strong base for hyper-specialized fine-tunes. Including the token embeddings in your LoRA fine-tuning often pays off.

**Architecture.** It’s a decoder-only, causal LM with 18 transformer blocks, designed for long-context efficiency. Most layers use 512-token sliding-window attention; every sixth layer switches to full attention (layers 6, 12, and 18) to “refresh” global context without paying full attention costs everywhere.

Under the hood, the hidden size is 640 with a 2048-dim feed-forward (MLP). The activation is a smooth `gelu_pytorch_tanh`, chosen for stability in compact models. Attention uses multi-query attention (four query heads sharing a single key/value head), which shrinks the KV cache and speeds up decoding.

**Positions and context.** Rotary position embeddings (RoPE) are configured for long contexts (`rope_theta ≈ 1e6`, base frequency ≈ 10k), supporting sequences up to 32,768 tokens while maintaining coherence across distant spans, especially when combined with the hybrid attention layout.

**Precision.** Gemma 3 is **not** float16-friendly. Load and run it in **bfloat16** ; using float16 can misrepresent activations and lead to degraded or broken outputs.

## Full Fine-Tuning Gemma 3 270M with Unsloth

### Installation

Unsloth is now very easy to install on most machines. Simply run:
    
    
    pip install unsloth

This will also install all the dependencies. I recommend creating a virtual environment, as some versions of your current packages might be downgraded to ensure compatibility.

### Can Gemma 3 270M Translate?

We’ll fine-tune Gemma 3 270M for translation. This is intentionally challenging: the model is primarily pre-trained on English, with limited capacity for non-English features given its small parameter budget and modest embedding size. As a result, many language-specific patterns (including French morphology and syntax) are underrepresented.

To gauge the starting point, let’s test English→French.

**Systeme Prompt**
    
    
    You translate from English to French. You answer only with the translation.

**Source sentence to translate:**
    
    
    these days, even when something goes viral on a massive scale, we can't assume everyone has seen it.

**Gemma 3 270M-IT (instruct) output:**
    
    
    Parfait.
    

Which means “Perfect.”

When requesting to translate, the model will just answer “Parfait.”, most of the time. It can’t translate and doesn’t understand the instruction. Many times, it will also just answer the source sentence as in a normal dialogue.

For a more systematic check, I translated the [WMT24PP](<https://huggingface.co/datasets/google/wmt24pp>) English→French set and scored outputs with BLEU (a quick diagnostic metric).

  * BLEU: 2.23

  * Interpretation: This is extremely low and indicates the model effectively cannot translate to French out of the box.

> Note on machine translation metrics: BLEU is fine for rough diagnostics but shouldn’t be used for formal translation evaluation. For research-grade assessment, prefer **[COMET](<https://huggingface.co/Unbabel/wmt22-comet-da>)** , which correlates better with human judgments.

### Data Preprocessing for Machine Translation

Plenty of EN↔FR datasets are available on Hugging Face, especially for this high-resource language pair. For this tutorial, I used [Helsinki-NLP/opus-100](<https://huggingface.co/datasets/Helsinki-NLP/opus-100>) and [Helsinki-NLP/news_commentary](<https://huggingface.co/datasets/Helsinki-NLP/news_commentary>), evaluated separately, to compare:

  * a smaller corpus over multiple epochs vs.

  * a larger corpus for one epoch.

Both are reasonably clean and span many domains. That said, for tiny models like Gemma 3 270M, I strongly recommend narrowing the domain. If you know your model will translate short tourism sentences, build exactly that: filter OPUS-100 (or similar) to short, tourism-related pairs. You’ll gain substantial accuracy in-domain at the cost of worse performance elsewhere. There’s no free lunch with tiny models.

I preprocessed the corpora into English–French pairs and wrapped each example with a simple chat-style template:
    
    
    "<start>You are a professional translator that translates messages from {source_language} to {target_language}.<user>{source_text}<translator>{target_text}"+tokenizer.eos_token
    

We’ll fine-tune the base Gemma 3 270M with this template. For comparison, we’ll also fine-tune the IT (instruct) variant using Gemma 3’s native tokenizer/chat template.

> Throughput tip: Removing the system prompt reduces tokens and can speed training/inference. Many modern inference frameworks cache prompts, but fewer tokens still help, especially on small GPUs. A simpler template that could work:
> 
> EN:{source_text}<FR>{target_text}

The code to preprocess the dataset is in the notebook.

### Hyperparameters and Training Arguments

For full fine-tuning with Unsloth, we only have to pass the argument “`full_finetuning=True`“ when loading the model and the tokenizer. 
    
    
        model, tokenizer = FastLanguageModel.from_pretrained(
          model_name = model_name,
          fix_tokenizer=False,
          max_seq_length = mseqlen,
          dtype = compute_dtype,
          load_in_4bit=False,
      **full_finetuning=True**
        )

I reviewed full fine-tuning with Unsloth in this article:

Because we’re doing full fine-tuning (no LoRA) and the run is short on a tiny model, there aren’t many knobs to obsess over. The big one is the learning rate. Small models typically tolerate (and often need) higher LRs than much larger models. Start with 5e-5 or 1e-4, then decrease if you see the training is unstable (training loss going up and down, without a decreasing trend).

### GPU Requirements for Gemma 3 270M and Training Time 

The VRAM footprint is modest. Using **8-bit optimizer states (AdamW-8bit)** shrinks optimizer memory by roughly 4x versus standard 32-bit, with no noticeable quality loss in this setup. 

In practice, 12 GB of GPU memory is comfortable; with shorter sequences and gradient accumulation you can squeeze by on 6–8 GB (even ~4 GB with more aggressive cuts).

Training is fast: on an **RTX 4090** , the run completes in just a **few hours**.

### Learning Curves for Gemma 3 270M Base VS. IT

I drew the learning curves with the base and IT models:

![image](https://substackcdn.com/image/fetch/$s_!5Z-w!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F70157804-68df-4cfc-bda2-e28d94c37618_1200x742.png) 

![image](https://substackcdn.com/image/fetch/$s_!Sryy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc2cb8169-9356-4cb8-a700-c8e946840dc3_1200x742.png) 

With a small dataset, it’s normal for training loss to drop sharply each epoch. The learning curve (training loss) clearly shows that there were 4 training epochs. The model is gradually memorizing examples it sees repeatedly. Push this too far and you’ll overfit: the model becomes excellent on the training set (and look-alikes) but worse on truly new text.

To guard against this, use a validation set (`eval_dataset` in Transformers) that:

  * Is representative of your target use case, and

  * Shares no samples with the training data.

As long as validation loss keeps decreasing, the model is still learning generalizable patterns. When it stalls and then rises, you’re overfitting. Stop there and keep the checkpoint with the lowest validation loss (classic early stopping). Two epochs were optimal, as we can see the validation loss starts to increase again after that.

In my runs, the base model learned faster and reached a lower validation loss than the IT model. But is it _actually_ better in practice?

Let’s check!

### Evaluation

For the evaluation with BLEU, I used SacreBLEU.

![Training dataset: News-Commentary](https://substackcdn.com/image/fetch/$s_!yuWa!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F280b5cc9-d76e-45ae-80ce-06c0d01c20a6_1200x742.png) 

**Results.** On BLEU, the base model fine-tune edges out the IT variant.

**Data scale matters.** Using the larger OPUS-100 corpus for just one epoch boosts EN→FR quality to ~18 BLEU (not shown in the plot above), far above the run on the smaller news_commentary set.2 Even a 270M model benefits more from seeing more unique examples once than from many passes over a smaller corpus.

## Recommendations and Conclusion

Choosing a learning rate for tiny models is trickier than for larger ones. It depends heavily on your data and how “new” the task is to the model. The upside: runs are cheap, so you can sweep broadly. Try a small grid (e.g., 5e-5 → 2e-5) and pick what stabilizes fastest on your validation dataset.

### Gemma 3 270M: Base or IT?

It depends, but for translation (and many similar tasks), I recommend fine-tuning the base model.

Why not the IT (instruct) model?

  * LLM providers’ post-training often reinforces safety/assistant behaviors. When prompted with text containing “sensitive” content (politics, war news, etc.), an IT model may refuse (“As an AI…”) even if you only asked for a translation.

  * Borderline “unsafe” content can lead to degraded translations.

  * Questions in the source may get answered instead of translated.

Fine-tuning the base model largely avoids this. (It doesn’t guarantee zero refusals; some safety data may be in pretraining, but success rates are much higher.)

### Is Gemma 3 270M a good fine-tuning target?

Definitely. With minimal effort, we’ve taught it EN→FR. You can push further by restricting the domain (e.g., tourism) and shortening sequences if you only care about short texts. Both can yield sizable gains for tiny models.

### LoRA / QLoRA?

I don’t recommend them here. On a 270M model, typical LoRA configs leave too few trainable parameters for the model to truly learn the task. Full fine-tuning (so, including embeddings) works better for this size.

1

So many IFEval-like synthetic datasets have been created. I’m convinced it’s unlikely that recent models don’t see them during training.

2

For this task, after tuning the hyperparameters and using better datasets, I’ve found that Gemma 3 270M can nearly reach a score of 30 BLEU.

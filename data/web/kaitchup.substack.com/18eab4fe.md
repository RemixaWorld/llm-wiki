---
domain: kaitchup.substack.com
fetch_date: '2026-05-18T12:37:26.038825'
status: ok
title: 'LoRA at Scale on a Consumer GPU: Does It Work?'
url: https://kaitchup.substack.com/p/lora-at-scale-does-it-work
---

![Image generated with ChatGPT](https://substackcdn.com/image/fetch/$s_!53zz!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5599730e-ac52-449c-96fc-d680de063bcb_1024x1536.png) 

LoRA is well known for drastically cutting the cost of supervised fine-tuning (SFT), and many tutorials demonstrate how to get started. However, most of these focus on narrow tasks, small datasets, or lightweight demos. What they don’t address is the more important question for real-world use cases: _Can LoRA match the performance of full fine-tuning on a large-scale dataset, while costing 10 times less?_

That’s what we’ll explore in this article. And spoiler: the answer is (almost) yes. With LoRA and tools like Unsloth, it’s possible to replicate TULU 3’s state-of-the-art SFT recipe using just a single 24 GB GPU (e.g., an RTX 4090), while the original full fine-tuning setup from AI2 required multiple GPU nodes and several hours of compute. We’ll walk through how to reproduce their results, yielding a high-quality Llama 3.1 chat model, using a far more accessible setup. 

This is just the beginning: in a follow-up article, we’ll also test whether the same approach transfers well to other models, like Qwen3, or if the current recipe is uniquely tuned to Llama 3.1. 

My SFT recipe using LoRA, Unsloth, and a single 24 GB GPU, can be tried with this notebook:

_Note: As background, I’ve already broken down[TULU 3’s datasets](<https://thesalt.substack.com/p/tulu-3s-high-quality-synthetic-datasets>) and [post-training recipe](<https://thesalt.substack.com/p/tulu-3-the-post-training-recipe>) in previous posts on [The Salt](<https://thesalt.substack.com/>), though you won’t need to read them to follow along here; all the key details will be included in this article._

## A State-of-the-Art Recipe for Supervised Fine-Tuning

### Hyperparameters: From Full Fine-Tuning…

My goal was to see whether I could reproduce the results of TULU 3’s SFT checkpoint using LoRA instead of full fine-tuning. 

  * TULU 3’s SFT checkpoint: [allenai/Llama-3.1-Tulu-3-8B-SFT](<https://huggingface.co/allenai/Llama-3.1-Tulu-3-8B-SFT>)

To keep things comparable, I followed their hyperparameters closely, see Table 11 from the [TULU 3 paper](<https://arxiv.org/abs/2411.15124>) for reference.

![source (CC-BY)](https://substackcdn.com/image/fetch/$s_!CyVr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c446ed7-4112-41c1-b1a8-c24d96e19d43_283x186.png) 

The only major difference is the learning rate. The one used by AI2 is unusually low, but that’s because their training setup uses a custom loss accumulation strategy: they sum losses across microbatches without normalization. This approach addresses an issue with gradient accumulation that we discovered back in October 2024. 

As a result, their training pipeline deals with higher losses, which requires a lower learning rate.

By contrast, standard frameworks like TRL and Unsloth use a normalized loss by default, corrected to take into account padding tokens, so they don't require such low learning rates. For SFT on models in the 8B range, something between 1e-5 and 2e-4 tends to work well. I went with 1e-4 after testing lower values for 1,000 steps and finding they didn’t perform as well.

For batch size, I used the same effective configuration as TULU 3: 128 sequences of 4,096 tokens per batch. While that might seem large for training a LoRA adapter, it didn’t appear to hurt performance. I also trained for two epochs, consistent with the original setup. AI2 noted that more epochs didn’t improve results for Llama 3.1 8B on this dataset, and although I didn’t test longer training runs myself, it is possible that a third epoch would improve the results for the LoRA case.

### … to LoRA Fine-Tuning

Next, we need to configure our LoRA adapter. I went with a standard setup: setting `alpha = rank`. I won’t go into detail here about how LoRA works. If you’re unfamiliar with it, I cover the basics in [Chapter 1 of my book ](<https://benjaminmarie.gumroad.com/l/llms-on-a-budget>)_[LLMs on a Budget](<https://benjaminmarie.gumroad.com/l/llms-on-a-budget>)_.

The fine-tuning process will be relatively long: two full epochs over 939k examples (see next section). With that much data, a higher rank could help the adapter learn more effectively. But since we’re planning to work with consumer-grade hardware, we’re constrained by memory. Increasing the rank, and thus the number of trainable parameters, would cause out-of-memory errors. So, I opted for a rank of 32, which is also very standard.

For the target modules, we apply LoRA to all linear layers in the model, excluding the language modeling head. In practice, this means we target all the linear components in both the self-attention and MLP blocks. Since we’re fine-tuning a base model on instruction/chat data, we also need to train the embeddings and LM head to support the special tokens used in the chat format. 

While this can be done efficiently with ["trainable tokens" (see my earlier article for details)](<https://kaitchup.substack.com/p/lora-trainable-tokens-save-memory>), I chose to go with the more traditional approach of fully retraining the token embeddings and LM head. This isn't memory-efficient, but it may give better results. If you're short on VRAM, the "trainable tokens" method is a good alternative.

Finally, it’s worth noting that the [Unsloth team previously found that reducing the learning rate for the embeddings and LM head improves training stability](<https://unsloth.ai/blog/contpretraining>). I observed the same: during the first 1,000 steps, the model learned better when the learning rate for these components was set 10x lower than the LoRA learning rate. So I set it to 1e-5 for embeddings and the LM head.

## Excellent SFT Needs Excellent Data

To get a high-quality fine-tuned model, you need high-quality data. Since I wasn’t targeting a specific downstream task, and my main goal was to evaluate how closely LoRA fine-tuning can match the performance of TULU 3’s full fine-tuning, I decided to use the same dataset that AI2 used for the SFT stage of TULU 3.

  * [allenai/tulu-3-sft-mixture](<https://huggingface.co/datasets/allenai/tulu-3-sft-mixture>)

 _Note: AI2 released an updated version,[allenai/tulu-3-sft-olmo-2-mixture-0225](<https://huggingface.co/datasets/allenai/tulu-3-sft-olmo-2-mixture-0225>), which is better. I recommend it for real-world use cases rather than the one I used for this article._

The dataset is quite large, 939k examples, sourced from other open datasets or generated by advanced LLMs like GPT-4. It’s one of the largest and highest-quality publicly available datasets for SFT.

Each entry has three fields: `id`, `messages`, and `source`. For our purposes, we only care about the `messages` column. It’s already structured as a list of dictionaries with `"role"` and `"content"` keys, making it directly compatible with standard chat templates.

Some samples are in non-English languages. If you’re not aiming for multilingual capabilities, filtering these out can reduce training time and speed up convergence.

## Dataset Pre-Processing: Applying the Chat Template of TULU 3

AI2 didn’t use the official chat template of Llama 3. They made a custom chat template as they found it performs slightly better:
    
    
    "chat_template": "{% for message in messages %}{% if message['role'] == 'system' %}{{ '<|system|>\n' + message['content'] + '\n' }}{% elif message['role'] == 'user' %}{{ '<|user|>\n' + message['content'] + '\n' }}{% elif message['role'] == 'assistant' %}{% if not loop.last %}{{ '<|assistant|>\n'  + message['content'] + eos_token + '\n' }}{% else %}{{ '<|assistant|>\n'  + message['content'] + eos_token }}{% endif %}{% endif %}{% if loop.last and add_generation_prompt %}{{ '<|assistant|>\n' }}{% endif %}{% endfor %}",

This template uses a different set of special tokens, for example, replacing the `<|start_header_id|>assistant<|end_header_id|> `with a simple `<|assistant|>\n`, and relies on the `eos_token` to mark the end of a turn instead of the `<|eot_id|> `used by Llama 3.1 Instruct. Additionally, AI2 removed the trailing newline character (`\n`) at the end of messages, as they found it had a negative impact on model performance.

Applying this template looks like this:
    
    
    tokenizer_chat = AutoTokenizer.from_pretrained("allenai/Llama-3.1-Tulu-3-8B-SFT")
    def process(row):
        row["text"] = tokenizer_chat.apply_chat_template(row["messages"], tokenize=False, add_generation_prompt=False)
        return row
    
    ds_train = ds_train.map(
        process,
        num_proc= multiprocessing.cpu_count(),
        load_from_cache_file=False,
    )
    
    print(ds_train[0]['text'])

The training samples are now sequences of tokens in a new `text` column.

Then, I recommend removing the “messages” column:
    
    
    ds_train = ds_train.remove_columns(["messages"])

I do this manually because I don’t fully trust TRL/Unsloth’s preprocessing, which tends to be unclear and changes between versions. In some cases, they’ll try to automatically process the `messages` column, even when you’ve explicitly specified that you want to use the `text` column, or they might throw an error altogether, especially with base models like Llama 3.1 that don’t come with a built-in chat template.

## Mask Your Prompts!

This one cost me a lot of GPU hours to figure out: masking the prompt, i.e., not computing the loss over the prompt tokens, can significantly speed up convergence and, in some cases, improve final performance.

It’s not exactly an obscure trick, but it’s easy to overlook. In fact, I’ve had readers reach out after reading papers and realizing that most fine-tuning frameworks, like TRL or Unsloth, _don’t_ mask the prompt by default. None of my fine-tuning notebooks masks the prompt either. Usually, for very short training runs, masking doesn’t make much difference. But that’s not always true. There’s prior work, like the study by [Shi et al. (2024)](<https://arxiv.org/abs/2405.14394>), that shows the effect of prompt masking varies depending on several factors. In small datasets or few-shot regimes, keeping the prompt in the loss might help. But when the training set is large, as in this experiment, masking tends to be better.

It’s especially important in setups like ours, where we’re fine-tuning with LoRA. With so few trainable parameters, there's a higher risk of overfitting to repetitive parts of the input, like system messages or prompt templates. In my case, masking the prompt improved accuracy on IFEval by several points after just one epoch compared to not masking.

Prompt masking is not mentioned in the TULU 3 paper, unless I completely missed it, and I’m pretty sure I checked it a dozen times. The same goes for the TULU 2 paper. I had to dig into AI2’s _[Open Instruct](<https://github.com/allenai/open-instruct/tree/main/open_instruct>)_[ codebase](<https://github.com/allenai/open-instruct/tree/main/open_instruct>), which implements TULU 3’s post-training recipe, and there it was: prompt masking is enabled by default.
    
    
    # set the label to -100 for the non-assistant part
    labels[:, message_start_idx:message_end_idx] = -100

[source](<https://github.com/allenai/open-instruct/blob/008391357125259efb471ed2477cb870a47587f0/open_instruct/dataset_transformation.py#L686>)

This turned out to be such a critical factor in the success of the experiment that I’m still not entirely sure why masking the prompt has such a strong impact. As I mentioned earlier, it could be due to the combination of LoRA’s limited number of trainable parameters and the size of the dataset, which increases the risk of overfitting to repeated prompt structures. Either way, it’s not something I expected going in, and it would definitely make for a great follow-up study in its own right.

## Hardware Requirements: A 24 GB GPU Is All You Need!

To run the SFT stage of TULU 3, AI2 used 32 H100 GPUs for just 6 hours. At first glance, that doesn’t seem particularly expensive. On a platform like [RunPod (referral link)](<https://runpod.io?ref=1ip9lvtj>), renting an H100 cluster for the same duration would cost around $684 (~$114/hour for 4x H100 nodes).

But here’s what often gets overlooked when papers mention these numbers: that’s only the cost of the _final_ training run. It doesn’t account for everything that comes before it: hyperparameter tuning, debugging, dataset curation, implementation testing, all of which easily make the total cost 10x (or more) higher than the clean figure quoted for the final job. That was true in my case as well. Most of the ~$1000 I spent went into figuring out the right learning rate and realizing how important it is to train on completions only.

So sure, it’s tempting to brag about how cheap a run was, like DeepSeek AI claiming their model only cost a few million to train, or like I did at the beginning of this article, but in reality, those numbers represent just a fraction of the actual research cost.

For this experiment, since we’re training an 8B model with LoRA, a single 24 GB GPU is enough. An RTX 4090 works well; even an RTX 3090 could do the job, albeit more slowly.

But that 24 GB only gets you there if you apply the right optimizations: FlashAttention, gradient checkpointing, activation offloading, and paged optimizer states. Fortunately, all of these are supported in [Unsloth](<https://github.com/unslothai/unsloth>), which, at least to my knowledge, is currently the most memory-efficient framework available for this kind of fine-tuning.

## Fine-Tuning Code

The full fine-tuning code is available in the notebook. Here, I’ll just walk through the key parts.

We start by loading the model. Since we're not using QLoRA, we need to explicitly tell Unsloth not to quantize it, by default, `load_in_4bit=True`, so we need to override that setting.
    
    
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = model_name,
        fix_tokenizer=False,
        max_seq_length = mseqlen,
        dtype = compute_dtype,
        load_in_4bit=False
    )

I also set `fix_tokenizer=False` to ensure that Unsloth doesn’t attempt to modify the tokenizer. This is important because automatic adjustments could conflict with the TULU 3 chat template we’re using.

Next, we process the training dataset. This part was covered in the previous sections.

Then, we define the LoRA configuration:
    
    
    model = FastLanguageModel.get_peft_model(
        model,
        r = 32, 
        target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                          "gate_proj", "up_proj", "down_proj","embed_tokens", "lm_head"],
        lora_alpha = 32,
        use_gradient_checkpointing = "unsloth", # True or "unsloth" for very long context
        random_state = 3407,
    )

I used a fairly standard LoRA configuration, as mentioned in the previous sections.

While I reused most of the hyperparameters from AI2’s TULU 3 SFT setup, they were originally tuned for full fine-tuning and likely aren’t optimal for LoRA, which has far fewer trainable parameters. Aside from adjusting the learning rate, I didn’t experiment with alternative batch sizes or warmup strategies in this run.
    
    
    bs = 1 #Batch size per device (training and validation), bs = 1 *can* be faster
    gas = 128 #Gradient accumulation steps
    mseqlen = 4096 #Maximum sequence length; reduce if you run out of memory
    lr = 1e-4

I set the per-device batch size to 1. While it’s technically possible to increase this on a 24 GB GPU, doing so would lead to more frequent offloading of optimizer states and activations, which can slow things down. And with gradient checkpointing enabled, increasing the batch size doesn't always translate to better efficiency; often, it just adds overhead.

To match the effective batch size used in TULU 3, I set the gradient accumulation steps to 128. Since we’re running on a single GPU, that gives us a total batch size of 128.

For the maximum sequence length, I used the same value as TULU 3: 4096 tokens. Reducing this length would save significant memory, but at the cost of limiting the model's ability to handle long-context tasks, which is something I wanted to preserve.
    
    
    training_arguments = UnslothTrainingArguments(
            output_dir=output_dir,
            #eval_strategy="steps",
            #do_eval=True,
            optim="paged_adamw_8bit",
            per_device_train_batch_size=bs,
            gradient_accumulation_steps=gas,
            #per_device_eval_batch_size=bs,
            log_level="debug",
            save_strategy="steps",
            save_steps=1000,
            logging_steps=25,
            learning_rate = 5e-5*2,
            embedding_learning_rate = 1e-5,
            bf16 = True,
            #eval_steps=25,
            num_train_epochs=2,
            warmup_ratio=0.03,
            report_to = "none",
            lr_scheduler_type="linear",
            max_seq_length=mseqlen,
            dataset_text_field='text',
            dataset_num_proc=multiprocessing.cpu_count()
    )

Using 8-bit paged optimizers is essential to make this setup work on a 24 GB GPU. To check the impact of using 8-bit optimizer states, I ran a few thousand training steps on a 48 GB GPU using the unquantized `adam_torch` optimizer and didn’t observe any meaningful difference in training loss. This reinforced my decision to stick with the 8-bit version, which offers significant memory savings without sacrificing performance.

I didn’t question the use of the "linear" learning rate schedule, as it has been shown to perform as well as, or better than, other schedulers in most cases.

We're almost done, the last step is to tell Unsloth that we want to **mask the prompts** , so the loss is only computed over the completion tokens:
    
    
    trainer = UnslothTrainer(
        model = model,
        train_dataset=ds_train,
        #eval_dataset=ds_test,
        processing_class=tokenizer,
        data_collator = DataCollatorForSeq2Seq(tokenizer = tokenizer),
        args = training_arguments
    )
    
    from unsloth.chat_templates import train_on_responses_only
    trainer = train_on_responses_only(
        trainer,
        instruction_part = "<|user|>\n",
        response_part = "<|assistant|>\n",
    )

We need to set the special tokens for the `instruction_part` and `response_part` of the chat template before starting training.

Once that’s done, we can kick off the fine-tuning. Below is the learning curve from the run:

![image](https://substackcdn.com/image/fetch/$s_!SZ9G!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5d71a840-96f1-4859-bdbc-88d1efb0eb9e_1732x1018.png) 

Training took 205 hours to complete on an RTX 4090, running uninterrupted. At $0.34/hour, that brings the total cost to $70. While the run was fairly long, it clearly shows that full-length, low-cost fine-tuning is feasible on consumer hardware. A newer GPU like the RTX 5090 would likely reduce training time (probably by around 40 hours), but at the time of this experiment, Unsloth didn’t yet support it.

## Evaluation

Now, let's see how the model performed with our fine-tuned adapter against the SFT checkpoint of TULU 3. I evaluated the fine-tuned model on two tasks: MMLU-PRO and IFEval (following common practices, I only report the “prompt_loose” accuracy).

To ensure a fair comparison, using identical evaluation settings for both models, I ran the evaluations for TULU 3 SFT’s checkpoint myself, rather than relying on the published numbers from the paper. This way, any differences reflect actual model performance rather than inconsistencies in the evaluation setup.

![image](https://substackcdn.com/image/fetch/$s_!BRGY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc9444950-8865-4b55-94b5-ff76099d29ee_1768x984.png) 

After two full epochs, the LoRA adapter reached an accuracy of 29.54 on MMLU-PRO and 65.99 on IFEval. While these results are respectable, there's still a noticeable gap compared to TULU 3 SFT, which scores 32.26 and 73.75 on the same benchmarks.

If we were using IFEval’s accuracy as a validation metric for checkpoint selection, the best-performing checkpoint would actually be at step 11,000, where the model achieved 30.26 on MMLU-PRO and 68.58 on IFEval. Given that the stderr on IFEval is around ±2.0, TULU 3 SFT is not very far ahead with its 73.75 points.

One interesting observation is that with LoRA, the model quickly learns to follow instructions but doesn’t show clear signs of overfitting. For context, the base model (step 0) had virtually 0.0 accuracy on IFEval, as it couldn’t properly terminate its outputs. The LoRA adapter shows steady improvements, even into the second epoch. That said, the final accuracy still lags behind the full fine-tuning done by AI2. I’m confident that with better-tuned LoRA hyperparameters, access to a 32 GB GPU (to increase the rank), and possibly one more epoch, it’s possible for LoRA to close the gap.

## Conclusion — How to Improve the Results?

Yes, fine-tuning an 8B model using a state-of-the-art recipe on consumer hardware is entirely possible. It’s not fast, but it works. Upgrading to a slightly larger GPU doesn’t necessarily speed things up unless you go big, think 80 GB GPUs, so you can:

  * swap out the paged 8-bit optimizers for the faster full-precision `adamw_torch`

  * disable gradient checkpointing

  * and hold all activations in memory without offloading (though in practice, Unsloth always seems to offload embeddings, so full in-memory training might still be out of reach)

A more practical alternative could be the RTX 5090. While it doesn’t offer significantly more memory than the 4090, it is significantly faster.

As for improving results, there are a few directions to explore: increasing the LoRA rank, switching to [rsLoRA for better scaling](<https://kaitchup.substack.com/p/rsqlora-fine-tune-llama-3-with-higher>), tuning the learning rate more aggressively, training for an extra epoch, or experimenting with batch size, either doubling it or halving it, depending on how it interacts with the learning rate.

If you’re planning to explore these options, you don’t need to run full training each time. Instead, compare learning curves and benchmark accuracy (e.g., on IFEval) after a few thousand training steps, say, around 3,000, to get a good sense of where things are heading.

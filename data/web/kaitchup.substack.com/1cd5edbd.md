---
domain: kaitchup.substack.com
fetch_date: '2026-05-18T12:35:29.296939'
status: ok
title: Fine-tune Llama 2 on Your Computer with QLoRa and TRL
url: https://kaitchup.substack.com/p/fine-tune-llama-2-on-your-computer
---

Llama 2 is a state-of-the-art large language model (LLM) released by Meta.

[In the paper presenting the model](<https://arxiv.org/pdf/2307.09288>), Llama 2 demonstrates impressive capabilities on public benchmarks for various natural language generation and coding tasks.

Meta also released Chat versions of Llama 2. These chat models can be used as chatbots. They mimic OpenAI’s ChatGPT capabilities and can solve many problems with the right prompts.

Both versions of Llama 2 are currently available in different sizes: 7B, 13B, and 70B parameters. _Note: A 34B parameter version is presented in the paper but has not been released yet._

The 7B and 13B models are especially interesting if you want to run Llama 2 on your computer. With recent advances in quantization, using GPTQ or QLoRa, you can fine-tune and run these models on consumer hardware.

I have written about Llama 2 and GPTQ here: 

In this article, I go through all the steps to fine-tune Llama 2 with QLoRa on instruction datasets. I use Hugging Face’s TRL library which simplifies LLM fine-tuning with instruction datasets. After implementing this article, you will have your own Llama 2 chat model running on your computer. 

 _Note: Llama 2 is distributed with a license allowing commercial use. However, note that you cannot use Llama 2 for improving another LLM that is not Llama 2 as explicitly stated in the license. I wrote about this limit of the license in this other article:_

### How to get Llama 2?

_Note: If you already have access to Llama 2 on Hugging Face, you may skip this part._

You must register to get it from Meta. [The form to get it is there](<https://ai.meta.com/resources/models-and-libraries/llama-downloads/>). You should receive an email from Meta within one hour.

Then, since I’ll use Hugging Face Hub, you will also need to create a Hugging Face account. The email address you used to create this account must be the same email that you used to get the Llama 2 weights.

Then, go to a [Llama 2 model card](<https://huggingface.co/meta-llama/Llama-2-7b-chat-hf>), and follow the instructions (you should be logged in to your account and you will see a checkbox to check and a button to click at the top of the model card). This step takes more time, but you should get access to Llama 2 on the Hugging Face hub within 1 day.

You will also need to create an access token from your Hugging Face account. Go to “settings” in your Hugging Face account and generate one.

### How does QLoRa work?

QLoRa is a fine-tuning method for quantized LLM. 

You can think about it as LoRa for a quantized LLM (see the illustration below) with several optimizations to make it more memory efficient.

I wrote about QLoRa in a previous post. In a nutshell, it works as follows:

  1. The model is loaded and quantized on the fly with a special 4-bit precision (**4-bit NormalFloat**). There is also a double quantization that quantizes the quantization constants.

  2. The 4-bit LLM’s parameters are frozen.

  3. Low-rank adapters are added and initialized on top of the 4-bit LLM.

  4. The parameters of the adapters are trained with an Adam optimizer whose states are paged to the CPU to further reduce the VRAM usage.

![Illustration by the author.](https://substackcdn.com/image/fetch/$s_!8R9j!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F985671fe-a894-431d-9453-8c7d3e057d8d_1500x661.png) 

Since we keep in the background the original model, only training the additional LoRa parameters is sufficient to obtain a fine-tuned LLM that is almost as good as if it was fine-tuned with the standard pipeline, i.e., without quantization and frozen parameters.

_Note: You can also do pre-training from scratch with LoRa. This method is called ReLoRa and I explained it here:_

### Padding Llama 2

Llama 2 doesn’t have a padding token, but we want one since most fine-tuning libraries expect one.

Most tutorials I have read online for fine-tuning Llama 2 create a pad token like this:
    
    
    tokenizer.pad_token = tokenizer.eos_token

The PAD token is the same as the EOS token. Even though it may work, this is not correct. The EOS token has an important role: It signals the end of the sequence. The PAD tokens are just dummy tokens used to fill in the sequence up to its maximum length. They should ignore or only carry little attention in the Transformer.

I also found that this is unlikely to work if you don’t set:
    
    
    tokenizer.padding_side = "right"

Probably because the EOS token is always at the end of the sequence, so to the right. If you put the padding side to “left”, then during fine-tuning, the model sees for the first time sequences beginning with EOS tokens which never happened during pre-training. It makes fine-tuning much more difficult. _Note: It depends on how padding is implemented, see the comments below. But even if your padding implementation deals with pad tokens differently, I recommend avoiding using the EOS token since this token already has an important role._

Another simple solution is to set the pad_token as an unk_token:
    
    
    tokenizer.pad_token = tokenizer.unk_token

Here, you don’t have to worry about the padding side since a UNK token can be anywhere inside a sequence.

This is better since the unk_token should also be ignored by the Transformers. But yet, semantically speaking, PAD tokens are not UNK tokens, they shouldn’t be treated identically by the model.

In the [Llama 2 documentation written by Hugging Face](<https://huggingface.co/docs/transformers/main/model_doc/llama2>), they recommend the following:

> _The original model uses_`pad_id = -1` _which means that there is no padding token. We can’t have the same logic, make sure to add a padding token using_`tokenizer.add_special_tokens({"pad_token":"<pad>"})`_and resize the token embedding accordingly. You should also set the_`model.config.pad_token_id` _. The_`embed_tokens` _layer of the model is initialized with_`self.embed_tokens = nn.Embedding(config.vocab_size, config.hidden_size, self.config.padding_idx)`_, which makes sure that encoding the padding token will output zeros, so passing it when initializing is recommended._

It’s slightly more complicated than just assigning to the pad_token an existing token, but these recommendations can be implemented in a few lines:
    
    
    model_name = "meta-llama/Llama-2-7b-hf"
    ACCESS_TOKEN="hf_mytoken"
    #Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True, use_auth_token=ACCESS_TOKEN)
    
    #Create a new token and add it to the tokenizer
    tokenizer.add_special_tokens({"pad_token":"<pad>"})
    tokenizer.padding_side = 'left'
    model = LlamaForCausalLM.from_pretrained(model_name, use_auth_token=ACCESS_TOKEN)
    
    #Resize the embeddings
    model.resize_token_embeddings(len(tokenizer))
    
    #Configure the pad token in the model
    model.config.pad_token_id = tokenizer.pad_token_id

Note that I also set padding_side to “left“. If you put “right“, you would have a prompt ending with pad tokens. The EOS token would be inserted after the pad tokens, thus training your model to generate the maximum number of tokens.

Now, Llama 2 has a new token dedicated to padding.

### Fine-tuning Llama 2 on Guanaco

The notebook implementing this fine-tuning is [available on Google Colab](<https://colab.research.google.com/drive/1SYpgFpcmtIUzdE7pxqknrM4ArCASfkFQ?usp=sharing>).

By the way, if you find this article useful, please share it with friends!

#### Requirements

Fine-tuning the smallest version of Llama 2 requires at least a GPU with 8 GB of VRAM and 8 GB of CPU RAM. It can also run on a free instance of Google Colab, but you won’t be able to complete one training epoch without being disconnected by Google since the free runtime has a maximum duration of 12 hours.

First, we need Llama 2 7B. Make sure you have a Hugging Face access token. Then, you can simply clone the model repository locally:
    
    
    #Replace HF_TOKEN by your Hugging Face Token
    #Don't change hf_user
    git clone https://hf_user:HF_TOKEN@huggingface.co/meta-llama/Llama-2-7b-hf

As for the dependencies, you will need to install the following Python packages:
    
    
    pip install -q -U bitsandbytes
    pip install -q -U transformers
    pip install -q -U peft
    pip install -q -U accelerate
    pip install -q -U datasets
    pip install -q -U trl
    pip install -q -U einops

Once everything is installed, import the following:
    
    
    import torch
    from datasets import load_dataset
    from peft import LoraConfig, PeftModel
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        BitsAndBytesConfig,
        AutoTokenizer,
        TrainingArguments,
        GenerationConfig
    )
    from peft.tuners.lora import LoraLayer
    
    from trl import SFTTrainer

We are all set!

#### Processing Guanaco

We will fine-tune Llama 2 on the Guanaco instruction dataset (Apache 2.0 license). Its structure is simple and can be directly used as is, without formatting or a custom data collator.
    
    
    dataset = load_dataset("timdettmers/openassistant-guanaco")

For the tokenizer, we will use the one released with Llama 2 but modified to enable padding.
    
    
    model_name = "Llama-2-7b-hf"
    #Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    #Create a new token and add it to the tokenizer
    tokenizer.add_special_tokens({"pad_token":"<pad>"})

#### Setting up QLoRa for fine-tuning Llama 2

The BitsAndBytesConfig is initialized with the standard parameters of QLoRa.

Then, once the model is loaded, we can resize its embeddings to take into account the new token added for padding.
    
    
    compute_dtype = getattr(torch, "float16")
    bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=compute_dtype,
            bnb_4bit_use_double_quant=True,
    )
    model = AutoModelForCausalLM.from_pretrained(
              model_name, quantization_config=bnb_config, device_map={"": 0}
    )
    
    #Resize the embeddings
    model.resize_token_embeddings(len(tokenizer))
    #Configure the pad token in the model
    model.config.pad_token_id = tokenizer.pad_token_id
    model.config.use_cache = False # Gradient checkpointing is used by default but not compatible with caching

For LoRa, I use the same parameters suggested in the examples provided in the [Llama 2 recipes prepared by Meta](<https://github.com/facebookresearch/llama-recipes>). We will only target the modules q_proj and v_proj.
    
    
    peft_config = LoraConfig(
            lora_alpha=32,
            lora_dropout=0.1,
            r=8,
            bias="none",
            task_type="CAUSAL_LM",
            target_modules= ["q_proj","v_proj"]
    )

#### Fine-tuning with TRL

Here are the parameters I use for training. As usual, they are only set for demonstration purposes so that you can quickly check that everything is working. 

Then, change them as indicated in the comments.
    
    
    training_arguments = TrainingArguments(
            output_dir="./results",
            evaluation_strategy="steps",
            do_eval=True,
            per_device_train_batch_size=4,
            gradient_accumulation_steps=1,
            per_device_eval_batch_size=4,
            log_level="debug",
            optim="paged_adamw_32bit",
            save_steps=2, #change to 500
            logging_steps=1, #change to 100
            learning_rate=1e-4,
            eval_steps=5, #change to 200
            fp16=True,
            max_grad_norm=0.3,
            #num_train_epochs=3, # uncomment this line
            max_steps=10, #remove this line
            warmup_ratio=0.03,
            lr_scheduler_type="constant",
    )

I initialized the TRL’s trainer like this:
    
    
    trainer = SFTTrainer(
            model=model,
            train_dataset=dataset['train'],
            eval_dataset=dataset['test'],
            peft_config=peft_config,
            dataset_text_field="text",
            max_seq_length=512,
            tokenizer=tokenizer,
            args=training_arguments,
    )

If you want a faster generation, you may reduce the max_seq_length, for instance to 128.

By default, SFTTrainer doesn’t save the full model but only the adapter so it produces reasonably small checkpoints.

#### Inference with Llama 2 adapter

For inference, we just have to load the saved adapter on top of the original model.

_Note: The original model, Llama 2 7B, should be loaded as you did for training. For the tokenizer, since we modified it, you must load the one saved as part of the checkpoint._

In the following code sample, I load the last checkpoint saved by TRL:
    
    
    model = PeftModel.from_pretrained(model, "./results/checkpoint-10")
    
    def generate(instruction):
        prompt = "### Human: "+instruction+"### Assistant: "
        inputs = tokenizer(prompt, return_tensors="pt")
        input_ids = inputs["input_ids"].cuda()
        generation_output = model.generate(
                input_ids=input_ids,
                generation_config=GenerationConfig(temperature=1.0, top_p=1.0, top_k=50, num_beams=1),
                return_dict_in_generate=True,
                output_scores=True,
                max_new_tokens=256
        )
        for seq in generation_output.sequences:
            output = tokenizer.decode(seq)
            print(output.split("### Assistant: ")[1].strip())
    generate("Tell me about gravitation.")

For temperature, top_p, and top_k, again I used the default values given in Meta’s Llama 2 recipes.

The code above should output something like this:
    
    
    🤖 Gravitation is the force that pulls all objects towards each other in the universe. It is a fundamental force of nature that is responsible for holding the planets in orbit around the sun, keeping the moon in orbit around the earth, and keeping the earth in orbit around the sun. Gravitation is a long-range force, meaning that it can act over long distances and can be felt even when the objects are far apart. Gravitation is also a universal force, meaning that it is present in all parts of the universe and is the same for all objects. Gravitation is a weak force, meaning that it is not as strong as the other fundamental forces, such as electromagnetism and the strong nuclear force. Gravitation is also a conservative force, meaning that it only acts on objects that are moving and does not cause objects to move. Gravitation is a central force, meaning that it acts on the center of mass of an object and not on individual particles. Gravitation is also a universal force, meaning that it is present in all parts of the universe and is the same for all objects. Gravitation is a long-range force, meaning that it can act over long distances and can be felt

### Conclusion

Guanaco is a rather small dataset. You may want to try larger ones such as [Alpaca](<https://huggingface.co/datasets/tatsu-lab/alpaca>) if you are not satisfied with the results.

If you have a bigger GPU, for instance with 24 GB of VRAM (RTX 3080/3090 or 4080/4090), it may also work with the 13B version of Llama 2.

If you need any help or have any questions, leave a comment on this article. I will answer it as quickly as possible.

---
domain: kaitchup.substack.com
fetch_date: '2026-05-18T12:35:28.883461'
status: ok
title: Fine-tune Falcon-7B on Your GPU with TRL and QLoRa
url: https://kaitchup.substack.com/p/fine-tune-falcon-7b-on-your-gpu-with-trl-and-qlora-4490fadc3fbb
---

#### 

![Falcon — Photo by Viktor Jakovlev on Unsplash](https://substackcdn.com/image/fetch/$s_!G1MY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F413898fb-2bdd-4066-97cc-945f6e4cb0ff_800x534.jpeg) 

The Falcon models are state-of-the-art LLMs. They even outperform Meta AI’s LlaMa on many tasks. Even though they are smaller than LlaMa, fine-tuning the Falcon models still requires top-notch GPUs with more than 40 GB of VRAM.

Well, this was before the introduction of QLoRa. QLoRa quantizes LLMs in 4-bit. If you want to know more about it, I wrote a tutorial here:

In this short post, I discuss the requirements to fine-tune Falcon models 7B and 40B with TRL, the Hugging Face library for reinforcement learning. I also present the code to write to train a state-of-the-art LLM by yourself, on consumer hardware, with QLoRa and TRL.

### Hardware Requirements to Fine-Tune Falcon-7B and Falcon-40B

To fine-tune Falcon-40B models without QLoRa you would need 90 GB of VRAM. In other words, you would need GPUs that cost way more than $5,000.

With QLoRa, we reduce the VRAM requirements to 45 GB and less than 10GB, respectively for Falcon-40B and Falcon-7B. For Falcon-40B, this is still a lot. Even the A100 40 GB wouldn’t be enough. There aren’t any affordable GPUs with that much VRAM yet. But for Falcon-7B, [an nVidia RTX 3080 or 3090 with 24 GB would be more than enough.](<https://kaitchup.substack.com/p/best-gpus-under-1500-for-ai-should>)

Note that you also need 15GB of CPU RAM to fine-tune Falcon-7B. This is because we need to load the model before quantizing it. While most recent computers have enough RAM, the free instance of Google Colab won’t be enough here since it offers only between 12 and 13GB of CPU RAM.

### Training with the TRL’s Supervised Fine-tuning Trainer

 _Note: I share the notebook (#1) running all the following code on the AI Notebook page:_

TRL is a less-known library created by Hugging Face. It’s also very recent. It’s dedicated to reinforcement learning but I also use it to write clean and short code.

You only need to write a few lines with TRL to fine-tune a model. And it’s compatible with QLoRa!

Without QLoRa, you would need to write the following. It’s short, but it will run out of memory if you don’t have a big GPU.
    
    
    from datasets import load_dataset
    from trl import SFTTrainer
    from transformers import AutoTokenizer, AutoModelForCausalLM
    
    data = load_dataset("timdettmers/openassistant-guanaco")
    
    model_name = "tiiuae/falcon-7b"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)
    
    trainer = SFTTrainer(
        model,
        tokenizer=tokenizer
        train_dataset=dataset['train'],
        dataset_text_field="text",
        max_seq_length=512,
    )
    trainer.train()

With QLoRa, you need more lines, but this is still a very short code. You also need these libraries to be installed:
    
    
    pip install -q -U bitsandbytes
    pip install -q -U git+https://github.com/huggingface/transformers.git 
    pip install -q -U git+https://github.com/huggingface/peft.git
    pip install -q -U git+https://github.com/huggingface/accelerate.git
    pip install -q -U datasets
    pip install -q -U trl
    pip install -q -U einops

Then you can run:
    
    
    import torch, einops
    from datasets import load_dataset
    from peft import LoraConfig
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        BitsAndBytesConfig,
        AutoTokenizer,
        TrainingArguments
    )
    from peft.tuners.lora import LoraLayer
    
    from trl import SFTTrainer
    
    
    def create_and_prepare_model():
        compute_dtype = getattr(torch, "float16")
    
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=compute_dtype,
            bnb_4bit_use_double_quant=True,
        )
    
        model = AutoModelForCausalLM.from_pretrained(
            "tiiuae/falcon-7b", quantization_config=bnb_config, device_map={"": 0}, trust_remote_code=True
        )
    
        peft_config = LoraConfig(
            lora_alpha=16,
            lora_dropout=0.1,
            r=64,
            bias="none",
            task_type="CAUSAL_LM",
            target_modules=[
                "query_key_value"
            ],
        )
    
        tokenizer = AutoTokenizer.from_pretrained("tiiuae/falcon-7b", trust_remote_code=True)
        tokenizer.pad_token = tokenizer.eos_token
    
        return model, peft_config, tokenizer
    
    
    training_arguments = TrainingArguments(
        output_dir="./results",
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        optim="paged_adamw_32bit",
        save_steps=10,
        logging_steps=10,
        learning_rate=2e-4,
        fp16=True,
        max_grad_norm=0.3,
        max_steps=10000,
        warmup_ratio=0.03,
        group_by_length=True,
        lr_scheduler_type="constant",
    )
    
    model, peft_config, tokenizer = create_and_prepare_model()
    model.config.use_cache = False
    dataset = load_dataset("timdettmers/openassistant-guanaco", split="train")
    
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        peft_config=peft_config,
        dataset_text_field="train",
        max_seq_length=512,
        tokenizer=tokenizer,
        args=training_arguments,
        packing=True,
    )
    
    trainer.train()

**And that’s it!**

You have fine-tuned a state-of-the-art LLM for free!

A more complete version of the code is provided [here](<https://gist.github.com/pacman100/1731b41f7a90a87b457e8c5415ff1c14>).

If you have a machine big enough, at least with 48GB of VRAM, you can run the same for Falcon-40B.

If you have any questions, please drop a comment. I’ll be happy to help!

Thank you for reading The Kaitchup. This post is public so feel free to share it.

---
domain: github.com
fetch_date: '2026-05-18T12:36:15.052111'
status: ok
url: https://github.com/Ucas-HaoranWei/GOT-OCR2.0
---

Haoran Wei*, Chenglong Liu*, Jinyue Chen, Jia Wang, Lingyu Kong, Yanming Xu, Zheng Ge, Liang Zhao, Jianjian Sun, Yuang Peng, Chunrui Han, Xiangyu Zhang

- [2025/2/1] 🚀🚀🚀 GOT-OCR2.0 is merged to Huggingface-transformers/space. It supports inference batched. Thanks to the MLE of Huggingface Yoni.
- [2024/12/24] 🔥🔥🔥 My new work on system-2 perception is released slow-perception.
- [2024/12/18] 🚀🚀🚀 GOT-OCR2.0 is supported in PaddleMIX by Paddle Team. Thanks for the Paddle team!
- [2024/12/8] 🔥🔥🔥 The model download has exceeded 1M on Huggingface.
- [2024/12/5] The seven wechat group.
- [2024/11/4] The six wechat group.
- [2024/10/24] The previous four wechat groups are full, so we created a fifth group.
- [2024/10/11] Too many friends want to join the wechat group, so we created a fourth group.
- [2024/10/2] onnx and mnn versions of GOT-OCR2.0.
- [2024/9/29]🔥🔥🔥 The community has implemented the first version of llama_cpp_inference.
- [2024/9/24]🔥🔥🔥 Support ms-swift quick Fine-tune for your own data.
- [2024/9/23]🔥🔥🔥 We release the official Modelscope demo. Thanks very much for Modelscope providing the GPU resource.
- [2024/9/19]🔥🔥🔥 GOT-OCR2.0 achieves Huggingface trending #1.
- [2024/9/14]🔥🔥🔥 We release the official demo. Thanks very much for Huggingface providing the GPU resource.
- [2024/9/13]🔥🔥🔥 We release the Huggingface deployment.
- [2024/9/03]🔥🔥🔥 We open-source the codes, weights, and benchmarks. The paper can be found in this repo. We also have submitted it to Arxiv.
- [2024/9/03]🔥🔥🔥 We release the OCR-2.0 model GOT!

We encourage everyone to develop GOT applications based on this repo. Thanks for the following contributions :

OpenVINO~ contributor: @can-gaa-hou

GGUF and Llama.cpp inference~ contributor: @MosRat

vllm reference ~ contributor: @Jay

onnx and mnn supports ~ contributor: @BaofengZan

llama_cpp inference ~ contributor: @1694439208

Colab of GOT ~ contributor: @Zizhe Wang

CPU version of GOT ~ contributor: @ElvisClaros

Online demo ~ contributor: @Joseph Pollack

Dokcer & client demo ~ contributor: @QIN2DIM

GUI of GOT ~ contributor: @XJF2332

Towards OCR-2.0 via a Unified End-to-end Model

- Our environment is cuda11.8+torch2.0.1
- Clone this repository and navigate to the GOT folder

```
git clone https://github.com/Ucas-HaoranWei/GOT-OCR2.0.git
cd 'the GOT folder'
```

- Install Package

```
conda create -n got python=3.10 -y
conda activate got
pip install -e .
```

- Install Flash-Attention

```
pip install ninja
pip install flash-attn --no-build-isolation
```


- Huggingface
- Google Drive
- BaiduYun code: OCR2

- Google Drive
- BaiduYun code: OCR2

- plain texts OCR:

`python3 GOT/demo/run_ocr_2.0.py --model-name /GOT_weights/ --image-file /an/image/file.png --type ocr`

- format texts OCR:

`python3 GOT/demo/run_ocr_2.0.py --model-name /GOT_weights/ --image-file /an/image/file.png --type format`

- fine-grained OCR:

`python3 GOT/demo/run_ocr_2.0.py --model-name /GOT_weights/ --image-file /an/image/file.png --type format/ocr --box [x1,y1,x2,y2]`

`python3 GOT/demo/run_ocr_2.0.py --model-name /GOT_weights/ --image-file /an/image/file.png --type format/ocr --color red/green/blue`

- multi-crop OCR:

`python3 GOT/demo/run_ocr_2.0_crop.py --model-name /GOT_weights/ --image-file /an/image/file.png `

**Note**: This feature is not batch inference!! It works on the token level. Please read the paper and then correct use multi-page OCR (the image path contains multiple .png files):

`python3 GOT/demo/run_ocr_2.0_crop.py --model-name /GOT_weights/ --image-file /images/path/ --multi-page`

- render the formatted OCR results:

`python3 GOT/demo/run_ocr_2.0.py --model-name /GOT_weights/ --image-file /an/image/file.png --type format --render`

**Note**:
The rendering results can be found in /results/demo.html. Please open the demo.html to see the results.

- Train sample can be found here. Note that the '<image>' in the 'conversations'-'human'-'value' is necessary!
- This codebase only supports post-training (stage-2/stage-3) upon our GOT weights.
- If you want to train from stage-1 described in our paper, you need this repo.

```
deepspeed /GOT-OCR-2.0-master/GOT/train/train_GOT.py \
--deepspeed /GOT-OCR-2.0-master/zero_config/zero2.json --model_name_or_path /GOT_weights/ \
--use_im_start_end True \
--bf16 True \
--gradient_accumulation_steps 2 \
--evaluation_strategy "no" \
--save_strategy "steps" \
--save_steps 200 \
--save_total_limit 1 \
--weight_decay 0. \
--warmup_ratio 0.001 \
--lr_scheduler_type "cosine" \
--logging_steps 1 \
--tf32 True \
--model_max_length 8192 \
--gradient_checkpointing True \
--dataloader_num_workers 8 \
--report_to none \
--per_device_train_batch_size 2 \
--num_train_epochs 1 \
--learning_rate 2e-5 \
--datasets pdf-ocr+scence \
--output_dir /your/output/path
```

**Note**:

- Change the corresponding data information in constant.py.
- Change line 37 in conversation_dataset_qwen.py to your data_name.

Quick Fine-tune with ms-swift:

```
git clone https://github.com/modelscope/ms-swift.git
cd ms-swift
pip install -e .[llm]
```

```
# default：sft LLM & projector, freeze vision encoder
CUDA_VISIBLE_DEVICES=0 swift sft\
--model_type got-ocr2 \
--model_id_or_path stepfun-ai/GOT-OCR2_0 \
--sft_type lora \
--dataset latex-ocr-print#5000
# Deepspeed ZeRO2
NPROC_PER_NODE=4 \
CUDA_VISIBLE_DEVICES=0,1,2,3 swift sft \
--model_type got-ocr2 \
--model_id_or_path stepfun-ai/GOT-OCR2_0 \
--sft_type lora \
--dataset latex-ocr-print#5000 \
--deepspeed default-zero2
```

**With your data**:

```
--dataset train.jsonl
--val_dataset val.jsonl (optional)
```

**Data format**:

```
{"query": "<image>55555", "response": "66666", "images": ["image_path"]}
{"query": "<image><image>eeeee", "response": "fffff", "history": [], "images": ["image_path1", "image_path2"]}
{"query": "EEEEE", "response": "FFFFF", "history": [["query1", "response1"], ["query2", "response2"]]}
```

More details can be seen in ms-swift.

- We use the Fox and OneChart benchmarks, and other benchmarks can be found in the weights download link.
- The eval codes can be found in GOT/eval.
- You can use the evaluate_GOT.py to run the eval. If you have 8 GPUs， the --num-chunks can be set to 8.

`python3 GOT/eval/evaluate_GOT.py --model-name /GOT_weights/ --gtfile_path xxxx.json --image_path /image/path/ --out_path /data/eval_results/GOT_mathpix_test/ --num-chunks 8 --datatype OCR`

If you are interested in this work or have questions about the code or the paper, please join our communication Wechat group.

**Note**:
All six wechat groups are full, please join group 7.

Don't hesitate to contact me by email, weihaoran18@mails.ucas.ac.cn, if you have any questions.

- Vary: the codebase we built upon!
- Qwen: the LLM base model of Vary, which is good at both English and Chinese!

```
@article{wei2024general,
title={General OCR Theory: Towards OCR-2.0 via a Unified End-to-end Model},
author={Wei, Haoran and Liu, Chenglong and Chen, Jinyue and Wang, Jia and Kong, Lingyu and Xu, Yanming and Ge, Zheng and Zhao, Liang and Sun, Jianjian and Peng, Yuang and others},
journal={arXiv preprint arXiv:2409.01704},
year={2024}
}
@article{wei2023vary,
title={Vary: Scaling up the Vision Vocabulary for Large Vision-Language Models},
author={Wei, Haoran and Kong, Lingyu and Chen, Jinyue and Zhao, Liang and Ge, Zheng and Yang, Jinrong and Sun, Jianjian and Han, Chunrui and Zhang, Xiangyu},
journal={arXiv preprint arXiv:2312.06109},
year={2023}
}
```

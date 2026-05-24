---
domain: newsletter.kaitchup.com
fetch_date: '2026-05-18T12:36:11.784556'
status: ok
url: https://newsletter.kaitchup.com/p/gguf-quantization-with-imatrix-and-q-quants
---

# GGUF Quantization with Imatrix and K-Quantization to Run LLMs on Your CPU

### Fast and accurate GGUF models for your CPU

GGUF is a binary file format for efficient storage and fast large language model (LLM) loading with GGML, a C-based tensor library for machine learning.

GGUF encapsulates all necessary components for inference, including the tokenizer and code, within a single file. It supports converting various language models, such as Llama 3, Phi, and Qwen2. Additionally, it facilitates model quantization to lower precisions to improve speed and memory efficiency on CPUs.

We often write "GGUF quantization" but GGUF itself is only a file format, not a quantization method. There are several quantization algorithms implemented in llama.cpp to reduce the model size and serialize the resulting model in the GGUF format.

In this article, we will see how to accurately quantize an LLM and convert it to GGUF, using an importance matrix (imatrix) and the K-Quantization method. I provide the GGUF conversion code for Gemma 2 Instruct, using an imatrix. It works the same with other models supported by llama.cpp: Qwen2, Llama 3, Phi-3, etc. We will also see how to evaluate the accuracy of the quantization and inference throughput of the resulting models.

The code for the quantization, benchmarking, and GGUF conversion, using an important matrix and K-Quantization, is in this notebook:

## Accurate GGUF Quantization with Imatrix and K-Quantization

I won’t explain in this article how “GGUF Quantization” works as I already did it in this article:

In this section, we will focus on the importance matrix and K-quantization.

#### K-Quantization for a More Accurate GGUF

K-quantization (a.k.a. K-Quants) involves splitting the model's weights into "superblocks," which are further divided into smaller sub-blocks. Each sub-block gets its own scale and minimum value, which are quantized into a limited number of bits—typically 8, 6, or 4, depending on the specific quantization method like Q2_K, Q4_K, or Q5_K. These scales and minimum values help ensure that the model maintains accuracy even when the precision is reduced.

While the method is complex and the quantization somewhat slow (especially compared to a GGUF quantization without K-Quants), the resulting quantized model is highly efficient during inference.

Once the model is quantized, dequantization—the process of converting the quantized weights back to fp16—is simplified. It only requires multiplying by the pre-determined scale and adding the minimum value, and this can be done for entire sub-blocks at once. This approach is ideal for hardware accelerations like SIMD (Single Instruction, Multiple Data) and GPU computations.

*Source: For more details, I recommend this great explanation on Reddit.*

We can quantize a model with K-Quants, as follows:

`./llama.cpp/llama-quantize {original_model} {iqtype} {m}`



where {original_model} is the original model in the GGUF format, {iqtype} is the location where the quantized model will be saved, and {m} the quantization method, e.g., Q4_K_S for a smaller 4-bit model using k-quantization.

#### Importance Matrix (imatrix) for GGUF Quantization

In an LLM, weights are more or less used depending on the task. Some are also outliers and thus very difficult to quantize. We shouldn’t try to reduce their precision as they would have a significant quantization error.

With a calibration dataset, we can check what are the most “active” weights of the models and then preserve them from quantization. This is similar to what AWQ does.

Measuring the importance of the weights can be costly as it requires the model to perform a forward pass on the entire calibration dataset. I recommend doing it with a GPU.

The dataset for calibration should be carefully chosen. If you know the type of task for which the model will be used, you should use a somewhat large dataset illustrating the task. On the other hand, if you are planning to use the model without targeting a particular domain or task, you should use a dataset in a general domain, such as Wikipedia.

I used Wikipedia for the quantization examples in the notebook.

To compute the importance matrix with llama.cpp, run this command:

`./llama.cpp/llama-imatrix -m {original_model} -f en-h10000.txt -o imatrix.dat -ngl 99 `


This will produce an importance matrix file, imatrix.dat, in your current directory using the dataset “en-h10000.txt”, 10000 lines from English Wikipedia, for calibration.

Using a slow GPU such as Google Colab’s T4, this only takes a few minutes for a 2B parameter model.

Next, we can quantize the model with K-Quants, using this importance matrix:

`./llama.cpp/llama-quantize --imatrix imatrix.dat {original_model} {iqtype} {m}`


The only difference with the standard k-quantization is that we provide the imatrix file.

## GGUF K-Quantization for Gemma 2 with an Importance Matrix

We will quantize google/gemma-2-2b-it. First, install llama.cpp:

```
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp && GGML_CUDA=1 make && pip install -r requirements.txt
```


Set “GGML_CUDA=1” to use the CUDA backend if you want to use a GPU for quantization (much faster than using a CPU). The compilation will take some time (more than 10 minutes).

Then, we set the following variables and create directories:

```
from huggingface_hub import snapshot_download
model_name = "google/gemma-2-2b-it" # the model we want to quantize
methods = ['Q4_K_S','Q4_K_M'] #the methods to be used for quantization
base_model = "./original_model_gemma2-2b/" # where the FP16 GGUF model will be stored
quantized_path = "./quantized_model_gemma2-2b/" #where the quantized GGUF model will be stored
original_model = quantized_path+'FP16.gguf' #path of the FP16 GGUF file
mkdir {quantized_path}
```


We need to download the model that we will quantize:

`snapshot_download(repo_id=model_name, local_dir=base_model , local_dir_use_symlinks=False)`


Then, convert the model to GGUF, without quantization (fp16):

`python llama.cpp/convert_hf_to_gguf.py {base_model} --outfile {original_model}`


Next, we download the datasets that will be used for calibration and evaluation:

```
wget https://object.pouta.csc.fi/OPUS-Wikipedia/v1.0/mono/en.txt.gz
gunzip en.txt.gz
head -n 10000 en.txt > en-h10000.txt
sh llama.cpp/scripts/get-wikitext-2.sh
```


I will use 10000 lines of OPUS-Wikipedia to compute the importance matrix and wikitext-2’s test set to evaluate the models’ perplexity.

Then, we can compute the importance matrix as follows:

`./llama.cpp/llama-imatrix -m {original_model} -f en-h10000.txt -o {quantized_path}/imatrix.dat --verbosity 1 -ngl 99 `


Next, we quantize the model with and without the importance matrix for comparisons, and using two different methods, 'Q4_K_S' and 'Q4_K_M'. Q4_K_S yields slightly smaller models than Q4_K_M but it is less accurate.

```
for m in methods:
qtype = f"{quantized_path}/{m.upper()}.gguf"
iqtype = f"{quantized_path}/{m.upper()}_I.gguf"
./llama.cpp/llama-quantize {original_model} {qtype} {m}
./llama.cpp/llama-quantize --imatrix {quantized_path}/imatrix.dat {original_model} {iqtype} {m}
```


I released several GGUF models for gemma-2-2b-it that I have made using the notebook:

## Benchmarking Inference Throughput and Perplexity for GGUF K-Quantization Using an Imatrix

#### Benchmarking the Perplexity of a GGUF Model

A perfectly accurate quantization should yield a model that has the same perplexity as the not-quantized model on a given text. Here, the given text will be “wiki.test.raw”.

llama.cpp provides a utility to compute the perplexity of a GGUF model. You can run it as follows:

`./llama.cpp/llama-perplexity -m {qtype} -f wikitext-2-raw/wiki.test.raw`


where {qtype} is the path to your GGUF file.

I computed the perplexity for Q4_K_M and Q4_K_S, made with and without using an importance matrix, and compared it to the perplexity of the FP16, i.e., not quantized, model. *Note: Here, we can compare the perplexities of all these models since they were made from the same model. However, be aware that we can’t compare the perplexity of two different models, e.g., Gemma vs. Llama 3.1. I wrote about this in The Salt:*

The results for Gemma 2 2B Instruct:

*Note: A lower perplexity is better.*

We can see that the perplexity of the quantized models is close to the FP16 model. The use of an importance matrix helps.

#### Benchmarking the Inference Throughput and Memory Consumption of a GGUF Model

I benchmarked the inference throughput with another utility provided by llama.cpp, llama-bench:

`./llama.cpp/llama-bench -m {original_model} -m {quantized_path}/Q4_K_M.gguf -m {quantized_path}/Q4_K_M_I.gguf -m {quantized_path}/Q4_K_S.gguf -m {quantized_path}/Q4_K_S_I.gguf -n 128,256,512 `


I used the CPU backend.

To benchmark the models using only the CPU, compile llama.cpp without CUDA:

```
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp && make && pip install -r requirements.txt
```


The results:

Quantized models are significantly faster than the FP16 models on the CPU (around 19 tokens/second against 9 tokens/second). Small and Medium versions perform more or less the same. The models quantized with an important matrix don’t behave differently. For small LLMs like Gemma 2 2B, I think using the Medium version (Q4_K_M) is better since it’s only 70 MB larger than the Small version.

## Conclusion

K-quantization offers a more accurate approach to reducing model size by quantizing weights into smaller blocks with individual scales and minimum values, enabling efficient inference. While this method is more complex and slower during the quantization process, it results in a highly optimized model for inference. The importance matrix further improves the accuracy of the quantization.

The benchmark results show that models quantized with K-Quantization and an importance matrix yield accurate and fast models.

The quantization process itself is also fast and memory-efficient enough to be cheap.

this was very knowledgeable, thanks for this.

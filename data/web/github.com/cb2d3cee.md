---
domain: github.com
fetch_date: '2026-05-18T12:38:06.766037'
note_fallback: true
status: ok
url: https://github.com/huggingface/transformers.git`
---

# 使用SSD、分层加载等方式以小显存设备使用大体量LLM的框架oLLM

oLLM是一个基于Hugging Face Transformers和PyTorch构建的小型Python库，它通过创新的内存管理技术，使得在有限的GPU资源（如8GB VRAM）上运行大型语言模型（如Qwen3-next-80B）成为可能。其核心在于避免将整个模型加载到GPU内存中，而是通过数据流和任务卸载来优化资源使用。

**oLLM的关键特性**
- **直接流式加载权重**：模型权重直接从SSD流式传输到GPU，无需全部加载到内存。
- **磁盘KV缓存**：注意力机制的键值缓存存储在SSD上，减少GPU内存占用。
- **CPU卸载**：在GPU内存不足时，将部分层卸载到CPU RAM中处理。
- **无量化支持**：仅使用fp16/bf16精度，不依赖模型量化。
- **性能优化技术**：包括FlashAttention-2（提升注意力计算效率并降低内存使用）和分块MLP（将大型中间层分割以避免GPU内存溢出）。

**最新更新（版本0.4.2）**
- **更轻量和快速**：使用`.safetensor`文件，通过`mmap`避免占用过多RAM。
- **支持更大模型**：例如Qwen3-next-80B，结合DiskCache功能。
- **速度提升**：Qwen3-next-80B在8GB GPU上每秒生成约0.5个令牌。
- **全面FlashAttention-2**：增强稳定性并降低内存需求。
- **分块MLP**：拆分大型中间层，防止GPU内存爆炸。

**实施步骤**
1. **环境设置**：
   - 创建虚拟环境：`python3 -m venv ollm_env`，激活后安装oLLM：`pip install ollm`。
   - 如需源码版本，克隆GitHub仓库并安装依赖，包括调整CUDA版本的`kvikio-cu12`。
   - 对于特定模型（如Qwen3-next），需安装Transformers的开发版本：`pip install git+https://github.com/huggingface/transformers.git`。

2. **示例代码概述**：
   - 初始化推理对象，指定模型和设备（如"cuda:0"）。
   - 可选择将部分层卸载到CPU（例如`offload_layers_to_cpu`方法）。
   - 使用DiskCache管理长上下文键值缓存。
   - 应用聊天模板生成输入，并通过流式输出逐令牌显示结果。

**oLLM的工作原理**
- **按需权重加载**：从SSD逐层加载权重到GPU，避免一次性占用。
- **基于磁盘的KV缓存**：将注意力内存存储在SSD上。
- **CPU卸载**：在GPU内存紧张时，将计算密集型层转移到RAM。
- **高效注意力机制**：FlashAttention-2优化计算，减少大矩阵需求。
- **分块MLP**：拆分大型层，防止内存溢出。

**实际应用场景**
- **法律工作**：一次性处理完整合同或合规文档，避免上下文丢失。
- **医疗保健**：总结多年患者记录，无需分段处理。
- **安全分析**：离线解析大量日志或威胁报告。
- **客户支持**：扫描历史聊天记录，识别常见问题。

**性能数据（基于3060 Ti，8GB VRAM）**
- **Qwen3-80B**：上下文50k，基线VRAM约190GB，oLLM下仅需7.5GB，SSD占用180GB。
- **GPT-OSS-20B**：上下文10k，基线VRAM约40GB，oLLM下7.3GB，SSD占用15GB。
- **Llama-3-1B**：上下文100k，基线VRAM约16GB，oLLM下5GB，SSD占用15GB。
- **Llama-3-8B**：上下文100k，基线VRAM约71GB，oLLM下6.6GB，SSD占用69GB。

**未来发展路线图**
- 即将支持模型包括Gemma-3-27B、Voxtral-small-24B ASR和Qwen3-VL（视觉语言模型）。
- 研发多令牌预测功能，以提升Qwen3-next的性能。
- 优化权重加载速度，进一步加速推理过程。

oLLM通过智能资源管理，使得在低成本硬件上运行大型模型成为现实，推动了本地AI应用的普及。

https://medium.com/coding-nexus/ollm-how-i-ran-an-80b-model-on-my-8gb-gpu-501a5076fd0d

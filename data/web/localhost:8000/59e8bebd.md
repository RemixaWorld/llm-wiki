---
domain: localhost:8000
fetch_date: '2026-05-18T12:38:06.106805'
note_fallback: true
status: ok
url: http://localhost:8000/v1`
---

# 使用vLLM运行切换多个LoRA Adapter及其对应聊天模板（chat template）

**核心概念**
- **LoRA适配器（Low-Rank Adaptation）**：通过向基础大语言模型（LLM）的特定层附加低秩权重增量，实现模型在特定任务或领域的专业化。
- **vLLM**：一个高性能的LLM推理和服务引擎，支持同时加载多个LoRA适配器，并允许按请求动态切换适配器，几乎无延迟。
- **自定义聊天模板**：使用Jinja模板语言定义输入提示的格式化规则，确保推理时的输入格式与模型微调时的训练数据格式一致。

**实施步骤**

**1. 设置自定义聊天模板**
- 避免手动编写Jinja模板，而是通过提供示例格式（如包含系统提示、用户输入和模型回复的完整对话结构）让ChatGPT生成模板。
- 生成的模板需处理边缘情况，例如支持多模态内容（非纯文本消息）和条件控制流。
- 示例模板结构包括：
  - 提取系统消息（如果存在）并包装在``标签中。
  - 遍历非系统消息，根据角色（如`user`、`assistant`/`translator`）添加相应标签。
  - 在需要生成回复时添加``开头标签。
- 将模板保存为独立文件（如`chat_template.jinja`），而非嵌入到`tokenizer_config.json`中。

**2. 离线推理（Python API）**
- **安装vLLM**：通过`pip install vllm`安装。
- **加载基础模型和LoRA配置**：
  - 初始化LLM时指定基础模型（如Qwen3-4B-Base），启用LoRA（`enable_lora=True`），并设置`max_lora_rank`（例如32）以匹配适配器的秩。
  - 注意事项：
    - vLLM支持的LoRA秩上限为512，设置过高的`max_lora_rank`会导致内存浪费。
    - 仅支持包含LoRA A/B矩阵的适配器，不支持包含完整模块（如词嵌入层或输出层）的适配器。
- **创建LoRA请求对象**：为每个适配器定义`LoRARequest`，包含适配器名称、唯一ID和本地路径。
- **生成推理结果**：
  - 使用`llm.chat()`方法，传入提示列表、采样参数、目标适配器请求（`lora_request`）和自定义聊天模板。
  - 切换任务时只需更改`lora_request`和系统提示（如从翻译为法语改为日语），无需重新加载模型。

**3. 在线服务（HTTP服务器）**
- **启动vLLM服务器**：通过命令行指定基础模型、聊天模板文件、LoRA适配器路径和名称。
  - 示例命令：注册名为`enfr`和`enja`的两个适配器，并关联其检查点路径。
- **客户端请求**：
  - 使用OpenAI兼容的API客户端，将请求发送至vLLM服务器端点（如`http://localhost:8000/v1`）。
  - 在请求中通过`model`字段指定适配器名称（如`enfr`），系统提示和用户消息结构保持不变。
  - 服务器自动应用对应的适配器和聊天模板返回结果。

**扩展支持：QLoRA**
- **QLoRA（Quantized LoRA）**：在4位量化基础模型上应用LoRA。在vLLM中启用方式：
  - 加载模型时设置量化参数（如`quantization="bitsandbytes"`）。
  - 提供QLoRA适配器路径，引擎在加载时根据适配器元数据将基础模型量化为4位。
  - 请求时仍使用`LoRARequest`选择适配器，与FP16/BF16基础模型的操作方式一致。
- vLLM同样支持在其他量化基础（如AWQ、GPTQ）上使用LoRA。

**优势总结**
- **高效多任务服务**：无需重复加载模型，通过内存中驻留的多个适配器支持低延迟任务切换。
- **格式一致性**：自定义聊天模板确保推理输入与训练数据格式匹配，提升输出质量。
- **灵活性**：支持离线和在线部署，适配器管理简单，兼容OpenAI API标准。

https://kaitchup.substack.com/p/serve-multiple-lora-vllm

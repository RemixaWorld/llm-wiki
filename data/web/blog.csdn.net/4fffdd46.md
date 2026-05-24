---
domain: blog.csdn.net
fetch_date: '2026-05-18T12:36:03.415359'
status: ok
url: https://blog.csdn.net/qq_35166730/article/details/137816630
---

地址：https://arxiv.org/html/2404.06910v1

code：论文作者说会放出来代码仓库，先留个坑，开源了再来更新。

### 背景

RAG 不是简单地通过查询提示语言模型，而是通过将一组检索到的文档注入到提示中来增强提示。如果操作正确，这些文档将包含与查询相关的有用知识，这些知识应该会从模型中引出更准确和可靠的输出。广泛的工作表明 了RAG 对许多知识密集型任务有效。然而，**合并检索到的文档会显著延长输入序列长度，并引入额外的计算开销，从而引发效率问题。** 解决 RAG 的长上下文处理及其效率的问题已成为最近研究的重点。

### 相关技术

#### 长上下文相关

**Longformer** 改进了 Transformer 传统的 self-attention 机制。具体来说，每一个 token 只对固定窗口大小附近的 token 进行 local attention（局部注意力）。对每一个 token 进行编码时，普通的滑窗机制只能考虑到长度为 w 的上下文。进一步提出空洞滑窗机制，在不增加计算负荷的前提下，拓宽视野范围。且 Longformer 针对具体任务，在原有 local attention 的基础上增加了一种 global attention（全局注意力）。对于添加了 global attention 的 token，这些计算是n * n，而其他的token则是线性n * w，在只有少量token为global attention的情况下，复杂度近似为线性。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b419ed48f020d70d416863fef23ae2f0.png)


**Reformer** 将模型的复杂度从 O(n^2) 变为了 O(nlogn) 具体可见知乎详解

**Locality Sensitive Hashing Attention****Reversible layersRevNet****Chunking FFN layers**

### 方法概述

`说明：在本篇中，⊕ 表示文本拼接`


传统的RAG方法在生成阶段，一般prompt做法为：

𝒙 = 𝒑 ⊕ 𝒅1 ⊕ 𝒅2⊕ 𝒅3⊕ 𝒅4⊕ 𝒅5 …⊕𝒒

```
system_prompt
user_prompt：
前文信息（包括身份，背景，要求等）
拼接检索到的docs（doc1，doc2，.......docn）
用户query
```


如下图naive llm-rag所示：

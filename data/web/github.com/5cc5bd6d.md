---
domain: github.com
fetch_date: '2026-05-18T12:36:59.757367'
note_fallback: true
status: ok
url: https://github.com/run-llama/llamacloud-demo/blob/main/examples/document_workflows/contract_review/contract_review.ipynb
---

# 使用llamaindex的workflow来实现合同审查的RAG过程

大体流程：
- 离线：
    1. 读取法规和指南等参考信息；
    2. 使用schema来处理成明确段落内容；
    3. 索引成知识库。
- 在线：
    1. 读取合同文件；
    2. 从合同文件中提取schema定义的必要信息；
    3. 将合同的信息与知识库进行匹配；
    4. 将匹配项提供给LLM，令其判断合同中的不合规项。

https://github.com/run-llama/llamacloud-demo/blob/main/examples/document_workflows/contract_review/contract_review.ipynb

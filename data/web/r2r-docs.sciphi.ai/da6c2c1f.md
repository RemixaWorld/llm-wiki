---
domain: r2r-docs.sciphi.ai
fetch_date: '2026-05-18T12:35:25.475564'
note_fallback: true
status: ok
url: https://r2r-docs.sciphi.ai/cookbooks/knowledge-graph
---

# LLM的图RAG主流生态R2R系统框架的实践教程

R2R（一种图RAG系统）的提取、搜索和查询

- R2R可灵活选取自定义的模型后端、对话LLM、抽取LLM、embedding模型、向量数据库
    - 本教程的方案是：
        - 模型后端：litellm、ollama
        - 对话LLM：Llama3
        - 抽取LLM：Triplex-可将文句转换为三元组的SOTA LLM（可比肩GPT4o且成本低廉）
        - 知识图谱数据库：neo4j（知识图谱数据库层面目前仅支持该库）
        - embedding模型：mxbai-embed-large-v1
        - 向量数据库：PG Vector
- 搭建步骤：
    1. 定义搭建R2R环境的Dockerfile
    2. 设置Settings.json来配置自定义的模型、数据库等
    3. 启动Docker
    4. 定义启动Docker时的compose.yaml以在启动R2R时也一并启动neo4j
    5. 启动Docker-Compose
- 使用场景（可命令行、可restful api、可UI）：
    - 图数据抽取并存入neo4j
    - 输入文本问题进行查询

https://mychen76.medium.com/automatic-knowledge-rag-with-r2r-0e9841714d5b  
https://r2r-docs.sciphi.ai/cookbooks/knowledge-graph  
https://github.com/SciPhi-AI/R2R

其他：GraphRAG的提取和查询：https://medium.com/@mychen76/demystify-knowledge-rag-frameworks-638b59bb3bc9

---
domain: github.com
fetch_date: '2026-05-18T12:35:40.981259'
status: ok
url: https://github.com/InternLM/MindSearch/blob/main/README_zh-CN.md
---

MindSearch 是一个开源的 AI 搜索引擎框架，具有与 Perplexity.ai Pro 相同的性能。您可以轻松部署它来构建您自己的搜索引擎，可以使用闭源 LLM（如 GPT、Claude）或开源 LLM（InternLM2.5 系列模型经过专门优化，能够在 MindSearch 框架中提供卓越的性能；其他开源模型没做过具体测试）。其拥有以下特性：

- 🤔
**任何想知道的问题**：MindSearch 通过搜索解决你在生活中遇到的各种问题 - 📚
**深度知识探索**：MindSearch 通过数百网页的浏览，提供更广泛、深层次的答案 - 🔍
**透明的解决方案路径**：MindSearch 提供了思考路径、搜索关键词等完整的内容，提高回复的可信度和可用性。 - 💻
**多种用户界面**：为用户提供各种接口，包括 React、Gradio、Streamlit 和本地调试。根据需要选择任意类型。 - 🧠
**动态图构建过程**：MindSearch 将用户查询分解为图中的子问题节点，并根据 WebSearcher 的搜索结果逐步扩展图。

在深度、广度和生成响应的准确性三个方面，对 ChatGPT-Web、Perplexity.ai（Pro）和 MindSearch 的表现进行比较。评估结果基于 100 个由人类专家精心设计的现实问题，并由 5 位专家进行评分*。

* 所有实验均在 2024 年 7 月 7 日之前完成。`pip install -r requirements.txt`

启动 FastAPI 服务器

`python -m mindsearch.app --lang en --model_format internlm_server --search_engine DuckDuckGoSearch`

-
`--lang`

: 模型的语言，`en`

为英语，`cn`

为中文。 -
`--model_format`

: 模型的格式。`internlm_server`

为 InternLM2.5-7b-chat 本地服务器。`gpt4`

为 GPT4。 如果您想使用其他模型，请修改 models

-
`--search_engine`

: 搜索引擎。`DuckDuckGoSearch`

为 DuckDuckGo 搜索引擎。`BingSearch`

为 Bing 搜索引擎。`BraveSearch`

为 Brave 搜索引擎。`GoogleSearch`

为 Google Serper 搜索引擎。`TencentSearch`

为 Tencent 搜索引擎。

请将 DuckDuckGo 和 Tencent 以外的网页搜索引擎 API 密钥设置为

`WEB_SEARCH_API_KEY`

环境变量。如果使用 DuckDuckGo，则无需设置；如果使用 Tencent，请设置`TENCENT_SEARCH_SECRET_ID`

和`TENCENT_SEARCH_SECRET_KEY`

。

提供以下几种前端界面：

- React

首先配置Vite的API代理，指定实际后端URL

```
HOST="127.0.0.1"
PORT=8002
sed -i -r "s/target:\s*\"\"/target: \"${HOST}:${PORT}\"/" frontend/React/vite.config.ts
```

```
# 安装 Node.js 和 npm
# 对于 Ubuntu
sudo apt install nodejs npm
# 对于 Windows
# 从 https://nodejs.org/zh-cn/download/prebuilt-installer 下载
cd frontend/React
npm install
npm start
```

更多细节请参考 React

- Gradio

`python frontend/mindsearch_gradio.py`

- Streamlit

`streamlit run frontend/mindsearch_streamlit.py`

`python mindsearch/terminal.py`

该项目按照 Apache 2.0 许可证 发行。

如果此项目对您的研究有帮助，请参考如下方式进行引用：

```
@article{chen2024mindsearch,
title={MindSearch: Mimicking Human Minds Elicits Deep AI Searcher},
author={Chen, Zehui and Liu, Kuikun and Wang, Qiuchen and Liu, Jiangning and Zhang, Wenwei and Chen, Kai and Zhao, Feng},
journal={arXiv preprint arXiv:2407.20183},
year={2024}
}
```


关注我们其他在大语言模型上的一些探索，主要为LLM智能体方向。

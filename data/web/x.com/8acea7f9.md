---
domain: x.com
fetch_date: '2026-05-18T12:36:03.415282'
note_fallback: true
status: ok
url: https://x.com/algo_diver/status/1828091411721527530
---

# 基于RAG和直接基于LC（长上下文）的问答能力比较

结论：在普遍问题上整体相差不大，在一些刁钻问题之类的极端情况下LC的表现要更稳定、但成本更高。所以可以考虑引入路由机制来结合LC和RAG，从而降低成本。

try-catch路由机制：
1. 询问LLM是否可以使用RAG回答
2. 如果可以，则使用RAG模式进行回答
3. 如果不可以，则使用LC模式进行回答

https://x.com/algo_diver/status/1828091411721527530

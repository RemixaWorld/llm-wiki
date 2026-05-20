# Pipeline Implementation Details

Ingest 和 Query 两个核心管线的逐步实现说明，含输入输出示例。

---

## Ingest 管线（`src/ingest.py`）：`extract → chunk → generate_pages → write → update_links`

---

### Step 1: extract_text — 文本提取（`src/extract.py:103-120`）

入口是 `extract_source(path_or_url)`，自动判断来源类型：

- **URL**：用 `trafilatura` 下载网页 → 提取正文 + 元数据（标题）
- **PDF**：用 `pymupdf` 逐页 `page.get_text()` → 用 `\n\n` 拼接
- **文本/Markdown**：直接 `path.read_text()`

**输入输出示例：**

```
输入: source_path = "sources/attention-is-all-you-need.pdf"

输出: {
    "extracted_text": "Attention Is All You Need\n\nAshish Vaswani et al.\n\nAbstract\nThe dominant sequence transduction models are based on complex recurrent or convolutional neural networks...\nThe transformer is based solely on attention mechanisms...\n\n1 Introduction\nRecurrent neural networks have been widely used...",
    "source_title": "Attention Is All You Need",
}
```

---

### Step 2: chunk_source — 文本分块（`src/extract.py:126-181`）

用 `tiktoken`（cl100k_base）计算 token 数：

1. 总 token ≤ `max_chunk_tokens` → 直接返回 `[原文本]`
2. 否则按 `\n\n`（段落边界）拆分，逐段累加 token 数，超限就切出一个 chunk
3. 单个段落超限 → 再按单行 `\n` 拆分，继续贪心装箱

**输入输出示例：**

```
输入: extracted_text (假设 12000 tokens, max_chunk_tokens=4000)

输出: {
    "chunks": [
        "Attention Is All You Need\n\nAshish Vaswani et al.\n\nAbstract\nThe dominant...\n\n1 Introduction\nRecurrent neural networks...",   # ~3800 tokens
        "3 Model Architecture\nThe encoder-decoder structure...\n\n3.2 Attention\nScaled dot-product attention...\n\n3.2.2 Multi-Head Attention...",  # ~3600 tokens
        "5 Training\nThis section describes the training regime...\n\n6 Results\nOn the WMT 2014...",                                               # ~3500 tokens
    ]
}
```

---

### Step 3: generate_pages — LLM 生成 wiki 页面（`src/ingest.py:71-127`）

1. 把最多 5 个 chunk 用 `\n\n---\n\n` 拼接
2. 用 `count_tokens()` 计算 token 数，< 500 tokens 则启用短文本模式
3. 调用 `_build_batch_messages()` 构造 messages：
   - **[system]** 完全静态的 ingest_system prompt（不含动态内容，利于 provider caching）
   - **[user]** 按稳定性排列：Preferred tags → ingest mode 或 short text 指令（互斥）→ 已生成页面的 titles+briefs → 源文本
4. 调用 `complete_structured()`，返回 `IngestResult` 结构（1 个 source_summary + 若干 concept_pages + 若干 entity_pages）

**Ingest 模式（`schema.yaml` 中 `ingest_mode`）：**
- `focused`（默认）：约束 concept/entity 各 1-3 个，聚焦核心主题
- `comprehensive`：不限制，提取所有概念和实体

**短文本模式（< 500 tokens）：** 只生成 source_summary，概念以 [[WikiLink]] 嵌入，不生成 concept/entity 页面。与 focused mode 互斥。

**LLM 调用细节**（`src/llm.py:59-102`）：
- 用 `instructor` 把 Pydantic 模型转成 function calling schema
- Groq/Gemini 用 `instructor.Mode.TOOLS`（tool calling），Ollama 用 `instructor.Mode.JSON`（复杂嵌套模型 tool calling 会出错）
- 按优先级 fallback：Groq → Gemini → Ollama，某个失败 catch 异常试下一个

**输入输出示例：**

```
输入 messages:
  system: "You are a knowledge base editor... Preferred tags: attention, nlp, transformer, ..."
  user:   "Source: Attention Is All You Need\n\nCreate wiki pages from this source text:\n\n...(chunk 0)...\n\n---\n\n...(chunk 1)...\n\n---\n\n...(chunk 2)..."

输出 generated_pages:
  [
    GeneratedPage(
      title="Attention Is All You Need",
      body="# Attention Is All You Need\n\nVaswani et al. (2017) introduce the Transformer...\nSee also: [[Self-Attention]], [[Multi-Head Attention]]",
      page_type="source",
      tags=["transformer", "attention", "nlp", "paper"],
      confidence="high",
      related_titles=["Self-Attention", "Multi-Head Attention", "Positional Encoding"],
    ),
    GeneratedPage(
      title="Self-Attention",
      body="# Self-Attention\n\nSelf-attention computes attention weights within a single sequence...\n$$\\text{Attention}(Q,K,V) = \\text{softmax}(\\frac{QK^T}{\\sqrt{d_k}})V$$\nRelated: [[Multi-Head Attention]], [[Attention Is All You Need]]",
      page_type="concept",
      tags=["attention", "mechanism"],
      confidence="high",
      related_titles=["Multi-Head Attention", "Attention Is All You Need"],
    ),
    GeneratedPage(
      title="Multi-Head Attention",
      body="# Multi-Head Attention\n\nInstead of a single attention function, multi-head attention runs h parallel heads...\nRelated: [[Self-Attention]]",
      page_type="concept",
      tags=["attention", "mechanism"],
      confidence="high",
      related_titles=["Self-Attention"],
    ),
    GeneratedPage(
      title="Ashish Vaswani",
      body="# Ashish Vaswani\n\nLead author of [[Attention Is All You Need]]. Research scientist at Google Brain.",
      page_type="entity",
      tags=["researcher", "google"],
      confidence="medium",
      related_titles=["Attention Is All You Need"],
    ),
  ]
```

---

### Step 4: write_pages — 碰撞检测 + 写入磁盘（`src/ingest.py`）

每个 batch 的页面写入经过 4 阶段处理：

**Phase 1 — 收集碰撞对：**

对每个生成的页面进行两级碰撞检测：

1. **精确碰撞：** `slugify(title)` 在磁盘上找到同名文件
2. **模糊碰撞：** `BriefIndex.search(brief)` BM25 搜索 brief，score 超过阈值

无碰撞的页面直接写入磁盘；有碰撞的加入 `collision_pairs` 列表。

**Phase 2 — Batch collision decision（1 次 LLM 调用）：**

所有碰撞对一次性发给 `batch_collision_check()`，LLM 返回每个碰撞的 MERGE / SKIP 决策：
- **MERGE** → 调用 `merge_page()` 合并（patch → rewrite 回退）
- **Exact SKIP** → 丢弃新页面（同名文件已存在）
- **Fuzzy SKIP** → 写为新页面（不同主题，都应保留）

**Phase 3 — BriefIndex 更新：**

batch 内所有页面处理完后，统一调用 `brief_idx.add()`。避免同 batch 页面互相触发模糊碰撞。

**Bug 修复（内嵌在此阶段）：**
- 空标题页面在去重后过滤
- 已有页面 brief 为空时跳过 LLM 调用，直接 MERGE

**输入输出示例：**

```
输入: generated_pages (上一步的 4 个 GeneratedPage)

输出 written_paths:
  ["attention-is-all-you-need.md", "self-attention.md", "multi-head-attention.md", "ashish-vaswani.md"]
```

磁盘上每个文件的内容，例如 `wiki/self-attention.md`：

```markdown
---
title: Self-Attention
type: concept
sources:
- sources/attention-is-all-you-need.pdf
tags:
- attention
- mechanism
created: '2026-05-17'
updated: '2026-05-17'
confidence: high
related:
- multi-head-attention.md
- attention-is-all-you-need.md
---

# Self-Attention

Self-attention computes attention weights within a single sequence...

$$\text{Attention}(Q,K,V) = \text{softmax}(\frac{QK^T}{\sqrt{d_k}})V$$

Related: [[Multi-Head Attention]], [[Attention Is All You Need]]
```

---

### Step 5: update_links — 反向链接更新（`src/ingest.py:159-187`）

扫描刚写入的每个 page 的 body，用正则 `\[\[(.+?)\]\]` 提取 `[[WikiLink]]`，给被引用页补反向链接：

1. 找到被引用页面 → 检查其 `frontmatter.related` 是否已包含当前页
2. 没有就追加进去，重写文件

**输入输出示例：**

```
输入: written_paths = ["attention-is-all-you-need.md", "self-attention.md", "multi-head-attention.md", "ashish-vaswani.md"]

操作:
  扫描 self-attention.md body → 发现 [[Multi-Head Attention]]
  → 找到 multi-head-attention.md → related 里没有 "self-attention.md" → 追加并重写

  扫描 self-attention.md body → 发现 [[Attention Is All You Need]]
  → 找到 attention-is-all-you-need.md → related 里没有 "self-attention.md" → 追加并重写

输出 updated_pages:
  ["multi-head-attention.md", "attention-is-all-you-need.md"]
```

例如 `multi-head-attention.md` 的 frontmatter 被更新：

```yaml
# 之前
related:
- self-attention.md

# 之后（update_links 补上的反向链接）
related:
- self-attention.md
- attention-is-all-you-need.md
```

---

## Query 管线（`src/query.py`）：`search → retrieve → synthesize → persist`

用户执行 `wiki query "什么是多头注意力"`：

---

### Step 1: search_wiki — BM25 搜索（`src/search.py:51-75`）

1. `read_all_pages()` 读出所有 wiki markdown
2. 每页拼 `title + tags + body` → 正则 `\w+` 分词 + 小写化 → 建 `BM25Okapi` 索引
3. query 同样分词 → `get_scores()` → 过滤 score=0 → 降序取 top 5

**输入输出示例：**

```
输入: {"question": "什么是多头注意力"}

输出 search_results (按 BM25 分数降序):
  [
    WikiPage(path="multi-head-attention.md",  frontmatter.title="Multi-Head Attention", ...),
    WikiPage(path="self-attention.md",         frontmatter.title="Self-Attention", ...),
    WikiPage(path="attention-is-all-you-need.md", frontmatter.title="Attention Is All You Need", ...),
  ]
```

---

### Step 2: retrieve_pages — 构建上下文（`src/query.py:52-69`）

把搜索结果格式化拼成一个字符串给 LLM。

**输入输出示例：**

```
输入: search_results (上一步的 3 个 WikiPage)

输出 retrieved_context:
  "## Multi-Head Attention
   Type: concept | Confidence: high

   # Multi-Head Attention
   Instead of performing a single attention function, multi-head attention runs h parallel heads...

   ---

   ## Self-Attention
   Type: concept | Confidence: high

   # Self-Attention
   Self-attention computes attention weights within a single sequence...

   ---

   ## Attention Is All You Need
   Type: source | Confidence: high

   # Attention Is All You Need
   Vaswani et al. (2017) introduce the Transformer architecture..."
```

---

### Step 3: synthesize — LLM 生成回答（`src/query.py:72-106`）

从 `schema.yaml` 加载 query 提示词，构造 messages 调用 LLM，返回 `QueryAnswer`。

**输入输出示例：**

```
输入 messages:
  system: "Answer questions based on the wiki context..."
  user:   "Question: 什么是多头注意力\n\nWiki context:\n\n## Multi-Head Attention\n..."

输出:
  {
    "answer": "多头注意力（Multi-Head Attention）是 Transformer 的核心机制。它将 Q、K、V 分别线性投影 h 次，"
              "在每个子空间独立计算 scaled dot-product attention，然后拼接并做线性变换。\n\n"
              "论文使用 h=8 个头，每个头维度 d_k = d_model / h = 64。",
    "citations": ["Multi-Head Attention", "Self-Attention", "Attention Is All You Need"],
    "follow_up_queries": ["scaled dot-product attention 的计算细节？", "多头与单头注意力的区别？"],
    "should_persist": True,   # LLM 判断值得保存
  }
```

---

### Step 4（条件）: persist_synthesis（`src/query.py:109-136`）

仅当 `should_persist=True` 时执行。标题取 `"Synthesis: " + question[:60]`，创建 `type: synthesis` 的 wiki page。

**输入输出示例：**

```
输入: should_persist=True, answer=..., citations=["Multi-Head Attention", "Self-Attention", "Attention Is All You Need"]

输出: 写入 wiki/synthesis-什么是多头注意力.md:
```

```markdown
---
title: Synthesis: 什么是多头注意力
type: synthesis
sources: []
tags:
- synthesis
- query-generated
created: '2026-05-17'
updated: '2026-05-17'
confidence: medium
related:
- multi-head-attention.md
- self-attention.md
- attention-is-all-you-need.md
---

# Synthesis: 什么是多头注意力

多头注意力（Multi-Head Attention）是 Transformer 的核心机制...

## Sources
- [[Multi-Head Attention]]
- [[Self-Attention]]
- [[Attention Is All You Need]]
```

这个 synthesis 页之后也会被 BM25 索引，后续查询能检索到。

---

## Lint 机制（`src/lint.py`）：`check_missing_fields → check_broken_refs → check_orphans`

触发方式：手动执行 `wiki lint`（目前无自动触发）。

### 整体流程

```
lint_wiki()
    ├── check_missing_fields(wiki_dir)  → list[LintIssue]
    ├── check_broken_refs(wiki_dir)   → list[LintIssue]
    └── check_orphans(wiki_dir)         → list[LintIssue]
    └── 所有 issues 汇总返回
```

CLI 层按 severity 着色输出：`error` 红色并 exit 1，`warning` 黄色，`info` 青色。

### check_missing_fields

| 项目 | 说明 |
|------|------|
| **输入** | `read_all_pages(wiki_dir)` 读取所有页面 |
| **输出** | `list[LintIssue]` |
| **检查项** | `title` 缺失→error，`tags` 缺失→warning，`sources` 缺失→info |

```python
if not fm.title:   → LintIssue(severity="error",   message="missing title")
if not fm.tags:     → LintIssue(severity="warning", message="no tags defined")
if not fm.sources: → LintIssue(severity="info",     message="no sources linked")
```

### check_broken_refs

| 项目 | 说明 |
|------|------|
| **输入** | `list_pages()` 获取所有已存在文件名 |
| **输出** | `list[LintIssue]` |
| **检查项** | 遍历每页 body 中 `[[wikilink]]`，目标文件不存在则 warning |

```python
existing = set(list_pages(wiki_dir))  # e.g. {"bert.md", "transformer.md", ...}
for page in pages:
    for link in extract_wikilinks(page.body):
        target_path = title_to_path(link)  # "BERT" → "bert.md"
        if target_path not in existing:
            → LintIssue(severity="warning", message=f"broken link to [[{link}]]")
```

### check_orphans

| 项目 | 说明 |
|------|------|
| **输入** | 所有页面 |
| **输出** | `list[LintIssue]` |
| **检查项** | 页面没有被任何 wikilink 或 `related` 字段引用 |

```python
# 第一步：收集所有被链接的路径
linked_paths: set[str] = set()
for page in pages:
    for link in extract_wikilinks(page.body):
        linked_paths.add(title_to_path(link))
    for rel in page.frontmatter.related:
        linked_paths.add(rel)

# 第二步：找出从未被链接的页面
for page in pages:
    if page.path not in linked_paths:
        → LintIssue(severity="info", message="page is not linked from any other page")
```

### 关键依赖（`src/wiki.py`）

- `list_pages()` — 列出 wiki 目录下所有 `.md` 文件
- `read_all_pages()` — 读取并解析所有页面的 frontmatter + body
- `extract_wikilinks(text)` — 用正则 `\[\[(.+?)\]\]` 提取所有 wikilink
- `title_to_path(title)` — 标题转文件名：`"BERT"` → `"bert.md"`

---

## 图结构（LangGraph）

两个管线都用 `StateGraph` 模式：`TypedDict` 做 state，async 函数做节点，条件边检查 `errors` 有错误就跳 `END`。本质就是一个**有向图状态机**，state dict 在节点间传递数据。

```
Ingest:  file.pdf → 提取纯文本 → 按token分块 → LLM生成结构化页面 → 写.md文件 → 补反向链接
Query:   "问题"   → BM25检索top5页 → 拼上下文 → LLM生成回答 → (可选)保存synthesis页面
```

---

## Karpathy 原版 LLM Wiki 理念

来源：https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

### 核心思想

Karpathy 把 LLM Wiki 比作编译器：

```
源文件（raw/）   = source code（不可变）
ingest          = 编译（compile）
wiki/           = 编译产物（binary）
query           = 执行（execution）
lint            = 优化 pass
```

关键区别于传统 RAG：不是每次查询都从原始文档重新检索，而是 LLM **增量构建并维护一个持久的 wiki**。知识编译一次，持续更新，不在每次查询时重新推导。

### 三层架构

- **Raw sources**（`raw/`）：源文档，不可变，LLM 只读不写
- **Wiki**（`wiki/`）：LLM 生成和维护的 markdown 文件，摘要页、概念页、实体页、综述页，互相链接。LLM 拥有这一层，人只读
- **Schema**（`CLAUDE.md` / `AGENTS.md`）：告诉 LLM wiki 的结构、惯例、工作流程。人跟 LLM 共同迭代这个文件

### 原版查询方式：LLM 自主导航

Karpathy 原版没有搜索引擎、没有 BM25、没有向量检索。查询流程是：

```
用户提问
  → LLM 读 index.md（目录页，每页一行摘要）
  → LLM 自行判断哪些页面相关
  → LLM 读那些页面的完整内容
  → LLM 综合回答
```

`index.md` 是内容目录，每次 ingest 后 LLM 自动更新。在中等规模（~100 个源，~数百个页面）下，LLM 靠读 `index.md` 就能找到相关页面，不需要 embedding 或 RAG 基础设施。

这能工作是因为原版设计给 **Claude Code、Codex 等 Agent** 使用 — LLM 本身能直接读写文件系统，不需要代码层面的检索逻辑。

---

## 检索方案对比：本项目的两个问题

### 问题 1：只有 BM25

本项目的 query 管线只用了 `rank_bm25.BM25Okapi`（Python 库），没有向量/语义检索。这是起点但不是终点，大部分 LLM Wiki 实现都从关键词检索开始，向量搜索作为可选增强。

在 wiki 场景下 BM25 其实比在原始文档上好用 — wiki 页面已经是蒸馏过的单概念文档，关键词匹配更精准。

### 问题 2：查询时建索引

本项目的 BM25 索引在每次查询时重新构建（`query.py` 里 `read_all_pages()` → 新建 `WikiIndex()`），ingest 管线没有索引持久化步骤。这属于少数派做法。

---

## 各 LLM Wiki 实现的检索方案对比

### 检索方式

| 项目 | 检索方式 |
|---|---|
| Karpathy 原版 | 无搜索引擎，LLM 读 `index.md` 自主导航 |
| nashsu/llm_wiki | BM25 + 可选向量（LanceDB）+ 图扩展，3 阶段流水线 |
| Oshayr/LLM-Wiki | 关键词 + 向量语义 + 反向链接索引（SQLite） |
| lucasastorian/llmwiki | SQLite FTS 全文检索，写入时更新索引 |
| nvk/llm-wiki | BM25 + 分支路由（ROUTING.md） |
| SamurAIGPT/llm-wiki-agent | 纯符号导航（`index.md` + wikilinks），无搜索引擎 |
| Pratiyush/llm-wiki | 直接 `grep` 作为 MCP tool |
| danvega/karpathy-wiki | Spring AI GrepTool 作为主要检索 |
| Ar9av/obsidian-wiki | Agent 自带 Grep/Glob 为默认，可选集成 qmd |
| **本项目** | **BM25（rank-bm25），查询时建索引** |

### 索引构建时机

| 时机 | 项目 |
|---|---|
| **ingest/写入时建索引** | nashsu, Oshayr, lucasastorian, nvk |
| **查询时建索引** | 本项目, NiharShrotri |
| **不建索引，LLM 自主导航** | Karpathy 原版, SamurAIGPT, kfchou/wiki-skills |
| **用 Agent 自带 Grep/Glob** | Ar9av, danvega, nvk |

### 编译与查询是否分离

**所有实现都把 ingest（编译）和 query（查询）作为独立操作。** 这是 LLM Wiki 模式的基本共识。查询管线可自由定义 — 不同实现各有各的查询策略。

---

## Unix 风格的 LLM Wiki 实现

部分项目用终端命令（grep、ripgrep、find）而非 Python 搜索库或向量数据库做检索：

**Pratiyush/llm-wiki** — 把 `grep` 直接包成 MCP tool：
```
wiki_search(term, include_raw)  →  底层就是 grep -r 过 wiki/ 目录
```

**danvega/karpathy-wiki** — Java/Spring 实现，用 Spring AI 的 GrepTool 和 GlobTool 作为主要检索。

**Ar9av/obsidian-wiki** — Agent 自带的 Grep/Glob 为默认搜索，没配置搜索引擎时自动降级到 grep，可选集成 qmd。

更常见的模式是很多项目（SamurAIGPT、kfchou/wiki-skills、nvk/llm-wiki）自己不写搜索逻辑，让 LLM Agent 用其自带的文件搜索工具（底层是 ripgrep）：
```
用户提问 → Agent 读 index.md → Agent 用内置 Grep 搜关键词 → Agent 读命中的页面 → Agent 回答
```

---

## qmd：本地混合搜索引擎

qmd（https://github.com/tobi/qmd）是 Shopify CEO Tobi Lutke 写的本地混合搜索引擎，Karpathy 本人在原版 gist 里点名推荐。Node.js/TypeScript 实现，完全本地运行，不需要云 API。

### 核心特点

用 GGUF 格式的小模型做向量 embedding 和重排（首次使用自动下载）：

| 模型 | 用途 | 大小 |
|---|---|---|
| embeddinggemma-300M | 向量 embedding | ~300MB |
| qwen3-reranker-0.6b | 搜索结果重排 | ~640MB |
| qmd-query-expansion-1.7B | 查询扩展（微调过） | ~1.1GB |

索引存在 SQLite（FTS5）里，持久化，不需要每次查询时重建。

### 三种搜索模式

```bash
qmd search "project timeline"        # 纯 BM25 全文检索（最快）
qmd vsearch "how to deploy"          # 纯向量语义搜索
qmd query "quarterly planning"       # 混合：BM25 + 向量 + LLM 重排（最好）
```

`query` 是完整流水线：

```
用户查询
  → 查询扩展（LLM 生成 2 个变体 + 原始查询）
  → 每个查询并行跑 BM25（SQLite FTS5） + 向量搜索
  → RRF（倒数排名融合）合并结果，保留 top 30
  → LLM 重排（qwen3-reranker 给每个文档打分）
  → 按位置加权混合最终排序
```

### 用法

```bash
# 安装
npm install -g @tobilu/qmd

# 添加 wiki 目录
qmd collection add ~/projects/llm-wiki/wiki --name wiki

# 加上下文描述（帮助搜索理解内容）
qmd context add qmd://wiki "LLM Wiki 知识库"

# 建向量索引
qmd embed

# 搜索
qmd search "多头注意力"              # 关键词
qmd vsearch "注意力机制的原理"       # 语义
qmd query "Transformer 和 RNN 的区别"  # 混合最佳

# Agent 友好的输出格式
qmd query "error handling" --all --files --min-score 0.4   # 文件列表
qmd search "auth" --json -n 10                              # JSON
qmd get "docs/api-reference.md" --full                      # 完整文档
```

### Agent 集成

**方式 1：命令行 shell out** — LLM 直接 `subprocess` 调 qmd 命令。

**方式 2：MCP Server** — `qmd mcp` 启动 MCP 服务，暴露 `query`、`get`、`multi_get`、`status` 四个 tool，Claude Code 可以直接用。

```bash
qmd mcp                  # stdio 模式
qmd mcp --http            # HTTP 模式，常驻后台，模型不重复加载
```

### 与本项目集成的可能

集成 qmd 后 query 管线可简化为：
```
当前:  read_all_pages → 建BM25索引 → 搜索 → 拼上下文 → LLM生成
集成后: qmd query "问题" → 拿到排序好的结果 → 拼上下文 → LLM生成
```

BM25 + 向量 + 重排全部交给 qmd，不需要自己维护搜索引擎。

---

## 改进方向

| 方案 | 语言 | 说明 |
|---|---|---|
| 集成 qmd | Node（外部调用） | Python 里 `subprocess.run(["qmd", "query", ...])`，简单但多 Node 依赖 |
| SQLite FTS5 | Python 内置 | `sqlite3` 自带 FTS5，不用装额外库，比 `rank-bm25` 快且可持久化 |
| lancedb + sentence-transformers | 纯 Python | 本地向量搜索，不依赖外部服务 |
| 保持 BM25 + 加持久化 | 纯 Python | 把 `rank-bm25` 索引 pickle 到磁盘，ingest 时更新，query 时加载 |

---

## schema.yaml 自定义指南

`schema.yaml` 是 Karpathy LLM Wiki 模式的**第三层**（行为配置层）。各字段被代码使用的程度不同：

### 字段分类

| 字段 | 代码中是否使用 | 推荐自定义？ |
|------|---------------|-------------|
| `prompts.ingest_system` | `get_ingest_prompt()` 读取并注入 LLM | ✅ 完全值得自定义 |
| `prompts.query_system` | `get_query_prompt()` 读取并注入 LLM | ✅ 完全值得自定义 |
| `tags.allowed` | `get_allowed_tags()` 追加到 system prompt | ✅ 推荐自定义 |
| `page_types.*` | **未加载**，仅 prompt 里文字描述字数范围 | ⚠️ 看看就行，改了不影响行为 |
| `wiki.name/description` | **未读取**，无代码引用 | ❌ 改不改没区别 |

`page_types.*` 只是 prompt 里对 LLM 的文字描述，**无代码强制**。`config.py` 没有 `get_page_types()` 函数，没有任何 pydantic 验证或字数检查绑定。

### page_types 定义的是什么

LLM 从源文档中提炼以下类型的知识：

| page_type | 提炼什么 | 字数范围 | 典型内容 |
|-----------|---------|---------|---------|
| `concept` | 概念/技术思路 | 100–500 词 | 解释一个算法、思路、方法 |
| `entity` | 人物/组织/工具/框架 | 50–300 词 | 描述一个具体实体 |
| `source_summary` | 单篇文档摘要 | 150–600 词 | 总结整篇文档 |
| `synthesis` | 跨源综合连接 | 200–800 词 | 连接多个来源形成的新洞察 |

在 ingest 流程中的实际表现：

```python
# ingest.py:111
all_pages = [result.source_summary, *result.concept_pages, *result.entity_pages]
```

- **1 个** `source_summary` — 总结整个来源
- **若干** `concept_pages` — 提取核心概念
- **若干** `entity_pages` — 提取具名实体（人名/机构/工具名）

`synthesis` 不在 ingest 阶段产生，只在 query 阶段当 LLM 认为有必要时动态生成。

### tags.allowed 自定义最佳实践

**建议渐进式**，而非一次性枚举所有预期标签：

```
1. 先不限制（allowed 留空或注释掉），让 LLM 自由生成 tags
2. 运行一段时间后：用 wiki stats 查看 tag_counts 高频标签
3. 把高频且有意义的标签加入 allowed
4. 后续 LLM 会优先从词表选，少量新标签仍允许（半受控）
```

词表太大（>50个）会失去引导意义。核心目的是**引导 LLM 复用已有标签**，而不是穷举所有可能标签。

### prompts 自定义最佳实践

保持简短、明确，聚焦格式要求而非泛泛描述。LLM 对长 system prompt 尾 部信息衰减严重。建议：

- 追加领域特定术语定义（如"本 wiki 聚焦于 NLP 领域"）
- 如果 page_types 有增减，修改对应描述
- 不要塞太多废话

### 总结

真正值得修改的只有两个字段：

1. **`prompts.ingest_system / query_system`** — 改 system prompt 行为
2. **`tags.allowed`** — 控制 LLM 生成标签时的词汇选择

两者都建议**渐进式**——先用默认/空状态跑一段时间，观察实际输出，再针对性调整。

---

## LLM-Wiki + RLM（Recursive Language Models）组合调研

### RLM 是什么

**RLM（Recursive Language Models）** 是 arXiv:2512.24601，Khattab & Zhang (MIT CSAIL) 2025年12月发表的论文提出的推理时扩展范式。

核心思想：**不再把长上下文塞进 context window，而是把长上下文作为外部环境暴露给 LLM，让 LLM 自己写代码去探索、切割、递归查询。**

```
传统方式：context → LLM → 输出
RLM方式：  context 作为环境变量 → LLM 可以写代码读写/切片/grep/递归调用 sub-LLM → 输出
```

LLM 获得一个工具 `RLM_M(q̂, Ĉ)` — 可以在 REPL（Python/Jupyter）中 spawn 一个隔离的子 RLM 实例，处理子任务后把结果传回父级。相当于 **MapReduce + 递归 REPL**。

#### 关键组件

| 组件 | 说明 |
|------|------|
| **环境 ε** | 存储上下文变量的外部环境，最简单的是标准 model call，最复杂的是 Python REPL |
| **Python REPL 环境** | 上下文 C 作为变量预加载进 REPL，LM 可以执行 `result = rlm(query, slice(context, 0, 1000))` 这样的代码 |
| **sub-RLM 调用** | LM 写代码 spawn 隔离子进程处理子查询，结果递归传回父级 |
| **环境泛化** | ε 是抽象的，REPL 只是其中一种选择 — 可以替换成任意代码执行环境 |

#### RLM 的查询流程（Python REPL 环境）

```
用户提问
  → Root LLM 看到 REPL 环境里有 context 变量
  → LLM 写 Python 代码探查/切分 context
  → LLM 对子片段 spawn sub-RLM 处理子问题
  → Sub-RLM 结果返回，Root LLM 合成最终答案
```

关键区别：**LLM 不是被动接收 context，而是主动编程去探索 context。** 这解决了传统 RAG 的根本问题——检索层永远无法知道该切什么、怎么组合。

---

### LLM-Wiki 的编译特性

Karpathy 的 LLM Wiki 核心理念：

- **编译时做合成**：LLM 在 ingest 阶段就把原始文档合成成结构化、交叉链接的 markdown pages
- **知识积累**：wiki 是持久化、递增的 artifact，新信息不断整合进已有结构
- **Token 效率**：比传统 RAG 节省 up to 95% tokens，因为 query 时不需要重新从 raw chunks 合成
- **跨文档推理**：RAG 永远无法连接两个文档中的矛盾条款，但 LLM-Wiki 在编译时已经生成了综合页面

---

### 结合的可能路径

LLM-Wiki 的编译产物（结构化 markdown pages）天然适合作为 RLM 的环境：

```
LLM-Wiki ingest → wiki/ 目录（结构化页面）

Query 时：
  RLM 的 Python REPL 预加载 wiki 内容作为变量
  Root LLM 分析问题，partition wiki 内容，spawn sub-RLM 处理子查询
  Sub-RLM 结果递归传回，最终合成答案
```

#### 现有 LLM-Wiki 的不足

当前本项目的 query 管线（`src/query.py`）使用 BM25 检索 + LLM 合成，这是最简单的起点，但存在几个问题：

1. **BM25 无法处理复杂跨页查询** — 当问题需要连接多个概念时，BM25 的独立排序无法建模页面间关系
2. **没有递归分解能力** — 用户问"多头注意力和自注意力的区别与联系"，LLM 只能从 top-k 检索结果拼凑，无法主动切分子问题
3. **查询时重建索引** — 每次 query 都重新建 BM25，没有持久化

RLM 的思路可以解决第 2 点：用 sub-RLM 递归处理子查询，每个子查询在 wiki 的一个子集上执行，结果再汇总。

#### 分层架构设想

```
Layer 1: 编译层（LLM-Wiki ingest）
  raw sources → 结构化 wiki pages

Layer 2: 索引层（可选）
  wiki pages → BM25 / 向量索引 / knowledge graph

Layer 3: 递归查询层（RLM 思路）
  用户问题 → Root LLM 分析 + partition wiki 内容 → spawn sub-RLM
  → sub-RLM 在 wiki 子集上执行子查询 → 结果递归传回 → 合成答案
```

这和 RLM 论文中的 MapReduce 思路一致：父 LLM 做调度，子 LLM 做局部处理，结果 reduce 回父 LLM。

---

### 现状与挑战

| 方面 | 现状 |
|------|------|
| 学术研究 | RLM 论文刚发表（2025.12），9页 + appendix，有 demo 但未广泛落地 |
| 工程实现 | 未看到 LLM-Wiki + RLM 结合的开源实现 |
| RLM 环境 | 当前 RLM 主要用 Python REPL，wiki 作为环境变量的接口需要自己搭 |
| 本项目接入点 | 最现实的做法是在 `src/query.py` 的 retrieve 或 synthesize 节点引入 RLM 风格的递归调用 |
| 性能考量 | RLM 的多轮 sub-LLM 调用开销大，适合复杂问题，不适合简单查找 |

---

### 有意思的相关方向

1. **OmegaWiki**（Karpathy gist 末尾提到）— 在 Claude Code 中运行完整 LLM-Wiki loop 的实验，结合 typed knowledge graph + recursive synthesis
2. **InfraNodus** — 给 LLM-Wiki 增加 knowledge graph 可视化，用 MCP server 做实时图分析，识别中心概念、聚类、盲点
3. **GraphRAG** — Microsoft 的方案，用 knowledge graph 映射 chunks 间关系，和 LLM-Wiki 的交叉链接思路有重叠
4. **Oolong**（PrimeIntellect）— RLM 的开源实现，在长 context 任务上验证了显著的 token 效率提升

---

### 结论

LLM-Wiki + RLM 的组合**概念上高度契合**：

- LLM-Wiki 提供了编译后的结构化知识（减少 RLM 需要处理的 raw context 量）
- RLM 的递归分解能力可以弥补 LLM-Wiki 当前 query 管线的跨页推理缺陷

但两者结合**没有现成实现**，需要自己搭。最现实的切入点是：

1. 先深入理解 RLM 论文的 REPL 环境设计
2. 在 `src/query.py` 的 synthesize 节点尝试引入子问题分解逻辑（先用普通 LLM 调用模拟 sub-RLM，不一定用真正的递归）
3. 评估复杂度 vs 收益 — 复杂问题值得用，simple lookup 不值得

# 项目改动记录与经验总结

## 1. MiniMax LLM 接入

### 改动内容

将 MiniMax 作为最高优先级 LLM 提供商接入项目的 fallback 链。

**涉及文件：**

- `src/config.py` — 新增 MiniMax 配置项
- `src/llm.py` — 新增 MiniMax 提供商，修复兼容性问题
- `.env` / `.env.example` — 新增 MiniMax 环境变量

### 具体实现

**config.py 新增字段：**

```python
minimax_api_key: SecretStr = SecretStr("")
minimax_model: str = "minimax/minimax-m2.7"
minimax_api_base: str = "https://api.minimaxi.com/v1"
```

**llm.py `_get_providers()` 新增 MiniMax（最高优先级）：**

```python
# MiniMax (highest priority)
if settings.minimax_api_key.get_secret_value():
    providers.append((
        settings.minimax_model,
        "minimax",
        {
            "api_key": settings.minimax_api_key.get_secret_value(),
            "api_base": settings.minimax_api_base,
        },
    ))
```

**Fallback 链变为：** MiniMax → Groq → Gemini → Ollama

### 踩坑与解决

**问题 1：MiniMax API base URL 文档不一致**

- LiteLLM 文档写的是 `api.minimax.io/v1`
- MiniMax 官方平台文档写的是 `api.minimaxi.com/v1`（注意多了个 `i`）
- 实际使用的是 MiniMax 官方的 `https://api.minimaxi.com/v1`
- 参考来源：https://platform.minimaxi.com/docs/guides/quickstart-preparation

**问题 2：Instructor TOOLS 模式与 MiniMax 不兼容**

MiniMax 的响应包含 `reasoning_content` 字段（思考过程），导致 instructor 在 TOOLS 模式下报错：

```
Instructor does not support multiple tool calls, use List[Model] instead
```

解决方案：MiniMax 和 Ollama 一样使用 `instructor.Mode.JSON`：

```python
mode = instructor.Mode.JSON if name in {"ollama", "minimax"} else instructor.Mode.TOOLS
```

**Instructor 两种模式对比：**

| | TOOLS 模式 | JSON 模式 |
|---|---|---|
| 原理 | 用 provider 原生的 function calling API | 在 prompt 中注入 JSON schema，LLM 在 content 里返回 JSON |
| 可靠性 | 取决于 provider 对 tool calling 的支持 | 几乎所有 provider 都支持 |
| Token 消耗 | 较少 | 略多（schema 注入到 prompt） |
| 适用 | Groq, Gemini 等 tool calling 稳定的 provider | Ollama, MiniMax 等 tool calling 不稳定的 provider |

### 配置方式

在 `.env` 中设置：

```
WIKI_MINIMAX_API_KEY=你的key
WIKI_MINIMAX_API_BASE=https://api.minimaxi.com/v1
```

---

## 2. 页面标题冲突时自动合并（Merge on Collision）

### 背景

原来的逻辑：同名页面直接覆盖（页面内容丢失）
现在的逻辑：同名页面调用 LLM 合并（保留双方信息）

### 整体架构

```
merge_page()
  ├── 1. Patch 模式（最多 3 次 LLM 调用）
  │     LLM 输出 PatchedPage（edit ops）
  │     apply_edits() 应用 edits:
  │       a. 精确匹配 — str.find() 直接匹配
  │       b. 模糊匹配 — 归一化后匹配（尾部空白 + 弯引号）
  │       c. 失败 → 注入错误上下文，重试
  │     3 次都失败 ↓
  └── 2. Rewrite 模式（1 次 LLM 调用）
        LLM 输出 MergedPage（完整 body）
```

Patch 模式远优于 Rewrite：LLM 只输出变更部分（几十 token），而非重写整个页面（几百 token）。Fuzzy matching 进一步减少了因空白/引号差异导致的无效重试。

### 涉及文件

| 文件 | 职责 |
|------|------|
| `src/merge.py` | 调度 patch→rewrite 回退，合并 frontmatter |
| `src/patch.py` | `apply_edits()` 精确→模糊匹配，`_normalize_with_offsets()` 归一化 |
| `src/models.py` | `PatchedPage`/`MergedPage`/`EditOp` 数据模型 |

### Patch 模式（核心路径）

`merge_page()` 先调 LLM 生成 `PatchedPage`（一组 `EditOp`），再通过 `apply_edits()` 应用：

```python
# merge.py — patch 循环
for attempt in range(3):
    result = await complete_structured(messages, response_model=PatchedPage)
    try:
        body = apply_edits(existing.body, result.edits)  # 精确→模糊
        return _merge_frontmatter(...)
    except PatchError as e:
        last_error = str(e)  # 注入下一次 LLM 调用的 prompt
```

**`apply_edits()` 4 级回退（参考 Claude Code 实现）：**

1. **精确匹配** — `str.count()` 在原始 body 上匹配
2. **模糊匹配** — 归一化后匹配（仅两种归一化：行尾空白剥离 + 弯引号→直引号），通过 offset 映射回原始位置替换
3. **错误重试** — `PatchError` 注入下一次 LLM 调用，LLM 修正 `old_string`
4. **全文覆写** — 3 次重试都失败，退化为 `MergedPage` 重新生成完整 body

模糊匹配归一化（`_normalize_with_offsets()`）：

```python
def _normalize_with_offsets(s: str) -> tuple[str, list[int]]:
    # 1. 每行 strip trailing whitespace
    # 2. 弯引号 (' " " ") → 直引号 (' ")
    # 返回 (归一化字符串, 位置映射表)
    # offsets[i] = 归一化位置 i 对应的原始字符串位置
```

### Frontmatter 合并

无论 patch 还是 rewrite，frontmatter 合并逻辑一致：

- **sources**: 追加新 source（去重）
- **tags**: 取并集（去重、保持顺序）
- **related**: 取并集（双向 wikilink）
- **confidence**: 取 max（existing vs merged）
- **updated**: 更新为当天日期

### 触发条件

`process_batches_node` 写页面时，先查磁盘是否有同名页面：

```python
existing_page = get_page_by_title(gen_page.title, settings.wiki_dir)
if existing_page is not None:
    merged_fm, merged_body = await merge_page(existing_page, gen_page, source_path)
else:
    # 新建页面
```

### 实测效果

用 Flash Attention 相关 source 测试 merge 路径：
- LLM 生成 3 个 edit ops → `apply_edits()` attempt=1 成功
- Fuzzy matching 避免了因尾部空白/引号差异导致的无效重试
- Patch 模式输出约 30 token，vs Rewrite 模式需要 500+ token

---

## 3. Ingest 断点续传（Checkpoint Resume）

### 核心改进

将 ingest 管道从「一次性处理所有 chunk」改为「batch 分批处理 + checkpoint 持久化」，解决了大文档中断后无法续传的问题。

**涉及文件：**

- `src/ingest.py` — 重写为 batch 循环 + checkpoint 读写
- `src/models.py` — 新增 `Checkpoint` Pydantic model
- `src/config.py` — 新增 `checkpoint_dir`（默认 `.wiki-checkpoints/`）和 `batch_size`（默认 5）配置
- `src/cli.py` — 新增 `--fresh` 参数忽略 checkpoint 从头开始
- `src/merge.py` — 新增 `merge_page()` 函数（见上一节）
- `src/wiki.py` — 新增 `get_page_by_title()` 查询已有页面

### 实现细节

**Checkpoint 文件结构：**

```json
{
  "source": "data/web/arxiv.org/00f556a3.md",
  "source_title": "Attention Is All You Need",
  "total_chunks": 12,
  "batch_size": 5,
  "completed_batches": [0, 1],
  "generated_titles": ["BERT", "Transformer", "Attention Mechanism"],
  "created_at": "2026-05-19T10:00:00+00:00"
}
```

路径：`.wiki-checkpoints/<source-path-slug>.json`

**原子性保证：** 每个 batch 的流程是：
1. 调用 LLM 生成页面
2. 写页面到磁盘（合并则调用 merge_page）
3. **只有成功后**才更新 `completed_batches` 并写回 checkpoint

如果 LLM 调用成功但写页面失败，checkpoint 不更新，下次重跑时会重新处理该 batch。

**源文件变更检测：** 对比源文件的 mtime 和 checkpoint 创建时间，如果源文件更新则从头开始。

**跨 batch WikiLink 感知：** `_build_batch_messages()` 会把已生成页面的标题列表传给 LLM，LLM 可以在新页面中写 `[[已有页面]]` 建立关联。

### CLI 改动

```bash
wiki ingest path/to/file.pdf --fresh  # 忽略 checkpoint，从头开始
wiki ingest-all --fresh               # 批量 ingest 也支持 --fresh
```

---

## 4. Brief 去重机制（BriefIndex + 碰撞检测）

### 背景

页面标题的精确匹配无法发现"内容相同但标题不同"的重复页面（如 "Self-Attention" vs "自注意力"）。引入 brief（页面简述）+ BM25 模糊匹配来检测语义碰撞。

### 核心组件

**BriefIndex**（`src/search.py`）：基于 BM25 的 brief 索引，用于模糊碰撞检测。

```python
class BriefIndex:
    def add(self, path: str, brief: str)     # 添加页面到索引
    def search(self, query: str, top_k: int)  # 模糊搜索，返回 [(path, score)]
```

### 碰撞检测流程

每个生成的页面在写入前经过两级碰撞检测：

```
生成的页面 (GeneratedPage)
  │
  ├─ 精确碰撞：slugify(title) == 已有文件名
  │   → 进入 collision decision（MERGE / SKIP）
  │
  └─ 模糊碰撞：BriefIndex BM25 搜索 brief，score > 阈值
      → 进入 collision decision（MERGE / SKIP）
```

### Brief 生成

每个页面在写入时生成 1-3 句简述（LLM 在 IngestResult 中直接输出），存储在 frontmatter 的 `brief` 字段。用途：

1. **碰撞检测**：BriefIndex 用 brief 做 BM25 模糊匹配
2. **跨 batch 上下文**：后续 batch 可以看到之前已生成的页面标题和 brief
3. **索引展示**：未来可用于目录页/搜索结果预览

---

## 5. Ingest 成本优化

### 背景

e2e 测试暴露的问题：117 tokens 的短文本生成了 6+ 页面，每次碰撞触发 3-5 次 LLM 调用（MiniMax 每次调用 10-90 秒），导致单个碰撞页面耗时 1-3 分钟。

### 整体架构

六项针对性改动，不改变管线结构（仍然是单步 ingest），通过 bug 修复 + 批量决策 + 数量约束 + prompt 优化来降低 LLM 调用次数和成本。

```
优化前：短文本(53 tokens) → 6+ 页面，每个碰撞 3-5 次 LLM 调用
优化后：短文本(53 tokens) → 1 页面，所有碰撞 1 次 LLM 调用
```

### 涉及文件

| 文件 | 改动 |
|------|------|
| `src/ingest.py` | 空标题过滤、batch BriefIndex.add、空 brief 快捷路径、短文本模式、batch collision 收集、prompt 结构重构、ingest mode 选择、titles+briefs 上下文 |
| `src/merge.py` | 新增 `batch_collision_check()` 函数 |
| `src/models.py` | 新增 `BatchCollisionDecision` / `CollisionPair` / `CollisionDecision` 模型 |
| `src/config.py` | 新增 `get_ingest_mode()` |
| `schema.yaml` | 新增 `ingest_mode: focused`，ingest_system prompt 中移除 tag 指令（移至 user message） |
| `tests/test_ingest.py` | 新增测试：空标题过滤、batch brief adds、空 brief 快捷路径、prompt 结构、batch collision 流程 |
| `tests/test_merge.py` | 新增 `TestBatchCollisionCheck` |
| `tests/test_models.py` | 新增 `TestBatchCollisionModels` |
| `tests/test_config.py` | 新增 `TestIngestMode` |

### 5.1 Bug 修复（3 项）

**空标题过滤：** LLM 可能生成 title 为空的 `GeneratedPage`，写成 `.md` 文件。

```python
# process_batches_node 中，去重后过滤空标题
all_pages = [p for p in deduped if p.title.strip()]
```

**Batch BriefIndex.add：** 原来每个页面写完后立刻 `brief_idx.add()`，导致同 batch 后续页面的 brief 通过 BM25 碰到刚写的页面，触发不必要的碰撞检测。

```python
# 改为 batch 结束后统一 add
batch_brief_adds: list[tuple[str, str]] = []
# ... per-page loop ...
    batch_brief_adds.append((path, gen_page.brief))
# After loop
for path, brief in batch_brief_adds:
    brief_idx.add(path, brief)
```

**空 brief 快捷路径：** 旧页面没有 brief（空字符串），做 `brief_merge_check` 时 LLM 输入里 existing brief 为空，必然返回 MERGE。改为 existing brief 为空时直接跳过 LLM 调用，走 MERGE 路径。

### 5.2 短文本模式（< 500 tokens）

用 `count_tokens()`（tiktoken cl100k_base）计算 batch 文本 token 数。< 500 tokens 时，prompt 注入短文本指令：

```
This is a short source text. Only generate the source_summary.
Mention concepts and entities using [[WikiLink]] syntax within the body
--- do not create separate concept_pages or entity_pages.
```

**效果：** 53 tokens 的 Dropout 短文只生成 1 个 source_summary 页面（含 `[[regularization technique]]`、`[[overfitting]]` 等 WikiLink），不再生成空的或低价值的 concept/entity 页面。

**阈值选择：** 500 tokens（原方案 1000）。调低的原因是 focused mode + 重要性约束已经在数量端控制住了输出（1-3 个概念页），500-1000 tokens 的文本走 focused mode 反而能提取更完整的知识。

**与 focused mode 的关系：** 两者互斥。`is_short=True` 时只追加短文本指令，不追加 focused mode 指令。`is_short=False` 时才追加 focused mode。

### 5.3 可插拔 Ingest 模式（Focused / Comprehensive）

在 `schema.yaml` 中配置：

```yaml
ingest_mode: focused  # "focused" 或 "comprehensive"
```

- **focused**（默认）：prompt 约束 concept_pages 和 entity_pages 各 1-3 个，聚焦核心主题
- **comprehensive**：不限制数量，提取源文本中所有概念和实体

`config.py` 暴露 `get_ingest_mode()` 读取配置。`_build_batch_messages` 根据模式追加不同的 user message 指令。IngestResult 模型不变（列表无硬上限），约束完全由 prompt 控制。

**重要性定义（focused mode 的判断标准）：**
- 源文本的核心主题/论点（不是边缘提及）
- 具有独立知识价值的实体/概念（值得拥有自己的页面，而非只是示例或引用）
- 之前已生成页面未覆盖的知识

### 5.4 Batch Collision Decision（单次 LLM 调用）

**优化前：** 每个碰撞单独调 `brief_merge_check` 或 `topic_match_check`，N 个碰撞 = N 次 LLM 调用。

**优化后：** 收集所有碰撞对（精确 + 模糊），一次性发给 LLM 做 MERGE/SKIP 判断。

#### 数据模型

```python
class CollisionPair(BaseModel):
    new_title: str
    existing_title: str
    existing_brief: str
    collision_type: Literal["exact", "fuzzy"]
    new_brief: str = ""  # exact 碰撞不需要

class CollisionDecision(BaseModel):
    new_title: str
    action: Literal["MERGE", "SKIP"]
    reason: str

class BatchCollisionDecision(BaseModel):
    decisions: list[CollisionDecision]
```

#### Per-page 循环重构（4 阶段）

```
Phase 1: 收集碰撞对
  for each page:
    exact collision → 加入 collision_pairs
    fuzzy collision → 加入 collision_pairs
    else → 加入 new_pages，立即写入

Phase 2: 写入新页面（无碰撞的页面直接写磁盘）

Phase 3: Batch collision decision（1 次 LLM 调用）
  if collision_pairs:
    batch_decision = await batch_collision_check(collision_pairs)
    for decision in batch_decision.decisions:
      if MERGE → merge_page(existing, new_page)
      if SKIP + exact → 丢弃（同名页面已存在）
      if SKIP + fuzzy → 写为新页面（不同主题，都应保留）

Phase 4: BriefIndex adds（batch 结束后统一添加）
```

**关键细节 — SKIP 的两种行为：**
- **Exact SKIP**：标题完全相同但 LLM 判断内容不同 → 丢弃新页面（因为同名文件已存在）
- **Fuzzy SKIP**：brief 模糊匹配但 LLM 判断是不同主题 → 写为新页面（因为实际上是不同概念）

### 5.5 Prompt Caching 优化 + Titles+Briefs 上下文

为利用 provider 端的 prompt caching（KV cache 复用），将 prompt 结构按稳定性排序：

```
[system]  ← 完全静态（所有 batch 相同，可缓存）
[user]    ← 动态内容按稳定性排列：
             1. Preferred tags（同一次 ingest 内不变）
             2. Ingest mode 或 short text 指令（互斥，二选一）
             3. Previously generated pages（标题 + brief，逐 batch 增长）
             4. Source text（每个 batch 不同）
```

**系统 prompt 不含动态内容：** `allowed_tags` 注入从 system prompt 移至 user message，确保 `get_ingest_prompt()` 返回值始终相同。

**Titles+briefs 替代 title-only 列表：** 原来 `existing_titles` 只是标题列表（如 "A, B, C"），改为 `existing_briefs` 包含标题和 brief（如 `"Attention Mechanism": Brief summary of attention...`）。LLM 能看到之前已提取了什么知识，避免重复生成相同概念。

### E2E 测试验证

| 场景 | LLM 调用 | 耗时 | 生成页面 |
|------|---------|------|---------|
| 短文本首次 ingest (53 tokens) | 1 | ~12s | 1 source_summary |
| 中等文本首次 ingest (227 tokens) | 1 | ~37s | 1 source_summary |
| 重复 ingest (exact collision) | 4 | ~79s | 1 merged (7 edits) |

**对比优化前：** 117 tokens 短文本生成 6+ 页面，现在 < 500 tokens 只生成 1 个 source_summary。每次碰撞从 3-5 次 LLM 调用降为 1 次 batch collision decision。

---

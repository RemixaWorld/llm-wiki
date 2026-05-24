# 项目改动记录与经验总结

## 1. LLM Provider 接入

### 已接入 Provider

| Provider | LiteLLM 模型 | Instructor 模式 | 特点 |
|----------|-------------|----------------|------|
| DeepSeek V4 Flash | `deepseek/deepseek-v4-flash` | JSON | $0.14/M in, $0.28/M out, 1M context, 速度快 |
| MiniMax M2.7 | `minimax/minimax-m2.7` | JSON | 需要 `api_base` 配置 |
| Groq | `groq/meta-llama/llama-4-scout-17b-16e-instruct` | TOOLS | 免费额度 |
| Gemini | `gemini/gemini-2.5-flash` | TOOLS | 免费额度 |
| Ollama | `ollama/qwen2.5:3b` | JSON | 本地运行，始终可用 |

### 踩坑

**Instructor 模式选择：** 凡是支持 thinking/reasoning mode 的 provider 都可能不支持 `tool_choice`，需用 JSON 模式：

```python
mode = instructor.Mode.JSON if name in {"ollama", "minimax", "deepseek"} else instructor.Mode.TOOLS
```

| | TOOLS 模式 | JSON 模式 |
|---|---|---|
| 原理 | provider 原生 function calling | prompt 注入 JSON schema，content 返回 JSON |
| 适用 | Groq, Gemini | Ollama, MiniMax, DeepSeek |

**MiniMax API base URL：** LiteLLM 文档写 `api.minimax.io/v1`，实际应使用 MiniMax 官方的 `https://api.minimaxi.com/v1`（多了个 `i`）。

**DeepSeek V4 Flash `tool_choice` 不兼容：** 默认 thinking mode 不支持 `tool_choice`，报错 `deepseek-reasoner does not support this tool_choice`。切换到 JSON 模式解决。

### 可配置 Provider 选择

通过 `WIKI_LLM_PROVIDER` 选择主 provider，避免多个云 provider 之间的降级关系：

```python
# _get_providers() 过滤逻辑
chosen = settings.llm_provider.lower().strip() if settings.llm_provider else ""
if settings.deepseek_api_key.get_secret_value() and chosen in ("", "deepseek"):
    ...
```

```
# .env
WIKI_LLM_PROVIDER=deepseek  # 只用 DeepSeek + Ollama 降级
# WIKI_LLM_PROVIDER=minimax  # 只用 MiniMax + Ollama 降级
# （不设置）                   # 所有 provider 按顺序尝试
```

### Benchmark：DeepSeek vs MiniMax

同一文档（354 词），首轮创建 + 二轮 merge：

| | DeepSeek V4 Flash | MiniMax M2.7 |
|---|---|---|
| **首轮** | 24s | 3m35s |
| **二轮（merge）** | 56s | 5m09s |
| **总计** | **1m20s** | **8m44s** |

MiniMax merge 有多次 patch retry，DeepSeek 基本一次通过。

---

## 2. 页面冲突自动合并（Merge on Collision）

### 架构

```
merge_page()
  ├── 1. Patch 模式（最多 3 次）
  │     LLM → PatchedPage（edit ops）
  │     apply_edits() 4 级回退：
  │       精确匹配 → 模糊匹配 → 错误重试 → 全文覆写
  └── 2. Rewrite 模式（1 次）
        LLM → MergedPage（完整 body）
```

**涉及文件：** `src/merge.py`（调度）、`src/patch.py`（apply_edits + 模糊匹配）、`src/models.py`（数据模型）

### `apply_edits()` 4 级回退

1. **精确匹配** — `str.count()` 直接匹配
2. **模糊匹配** — 归一化后匹配（行尾空白剥离 + 弯引号→直引号），offset 映射回原位置
3. **错误重试** — `PatchError` 注入下一次 LLM prompt，LLM 修正 `old_string`
4. **全文覆写** — 3 次都失败，退化为完整重写

Patch 模式远优于 Rewrite：只输出变更（几十 token vs 几百 token）。

### Frontmatter 合并

sources 追加去重、tags 取并集、related 取并集、confidence 取 max、updated 更新日期。

---

## 3. Ingest 断点续传（Checkpoint Resume）

batch 分批处理 + checkpoint 持久化，解决大文档中断后无法续传的问题。

**涉及文件：** `src/ingest.py`（batch 循环 + checkpoint 读写）、`src/models.py`（Checkpoint model）、`src/config.py`（checkpoint_dir、batch_size）、`src/cli.py`（`--fresh` 参数）

### 关键设计

- **Checkpoint 路径：** `.wiki-checkpoints/<source-path-slug>.json`，记录 completed_batches、generated_titles
- **原子性：** batch 成功后才更新 checkpoint，失败则下次重跑该 batch
- **源文件变更检测：** mtime > checkpoint 创建时间 → 从头开始
- **跨 batch WikiLink 感知：** 已生成页面的标题+brief 传给后续 batch 的 LLM

---

## 4. Brief 去重（BriefIndex + 碰撞检测）

两级碰撞检测发现"内容相同但标题不同"的重复页面：

```
GeneratedPage
  ├─ 精确碰撞：slugify(title) == 已有文件名 → MERGE/SKIP
  └─ 模糊碰撞：BriefIndex BM25 搜索 brief，score > 阈值 → MERGE/SKIP
```

每个页面写入时生成 1-3 句 brief（存 frontmatter `brief` 字段），用于碰撞检测、跨 batch 上下文、搜索预览。

---

## 5. Ingest 成本优化

| # | 优化 | 效果 |
|---|------|------|
| 1 | 空标题过滤 | 过滤 LLM 生成的空标题页面 |
| 2 | Batch BriefIndex.add | 避免 batch 内误碰撞 |
| 3 | 空 brief 快捷路径 | 无 brief 时跳过 LLM 直接 MERGE |
| 4 | 短文本模式（< 500 tokens） | 只生成 1 个 source_summary |
| 5 | 可插拔 ingest mode | `schema.yaml` 控制页面数量（focused/comprehensive） |
| 6 | Batch collision decision | N 个碰撞 = 1 次 LLM 调用 |

### Batch Collision Decision 流程

```
Phase 1: 收集碰撞对（精确 + 模糊）
Phase 2: 写入无碰撞的新页面
Phase 3: 1 次 LLM 调用判断所有碰撞
Phase 4: BriefIndex adds（batch 结束后统一添加）
```

**SKIP 的两种行为：** Exact SKIP → 丢弃新页面；Fuzzy SKIP → 写为新页面（不同主题都应保留）

### Prompt Caching

按稳定性排序以利用 provider 端 KV cache 复用：

```
[system]  ← 完全静态
[user]    ← 1. tags  2. mode/短文本  3. 已生成页面 titles+briefs  4. source text
```

---

## 6. 并行 Ingest 管线（Async Concurrency）

### 两层并行架构

```
┌─ Inter-file（ingest-all）：asyncio.gather + file-level semaphore
└─ Intra-batch（merge）：asyncio.gather + per-page lock
```

三层并发控制：

| 层 | 机制 | 作用 |
|----|------|------|
| 全局 LLM 信号量 | `get_llm_semaphore()` in `src/llm.py` | 总并发 LLM 调用 ≤ `max_concurrent_llm` |
| Per-page Lock | `get_page_lock()` in `src/wiki.py` | 同一页面串行化 merge（覆盖整个 LLM 调用，不仅是写磁盘） |
| File-level semaphore | `ingest_all` in `src/cli.py` | `return_exceptions=True` 隔离单文件失败 |

**涉及文件：** `src/config.py`（max_concurrent_llm）、`src/llm.py`（全局信号量）、`src/wiki.py`（per-page lock）、`src/ingest.py`（gather merge）、`src/cli.py`（gather ingest）

### 实测效果

| 场景 | 串行 | 并行（2 文件） | 提速 |
|------|------|---------------|------|
| ingest-all | ~14s | ~7.7s | ~1.8x |

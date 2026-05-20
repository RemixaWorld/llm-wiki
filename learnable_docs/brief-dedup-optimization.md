# Brief Dedup 优化项

End-to-end 测试暴露的问题和待优化点。

## 计划修复

### 空 title 页面未过滤

LLM 可能生成 title 为空的 GeneratedPage，直接写成了 `.md` 文件。

**修法：** 处理循环里 skip 空 title。

### BriefIndex 在 batch 内增量 add 导致同 batch fuzzy 碰撞

每个页面写完后立刻 `brief_idx.add()`，同 batch 后续页面的 brief 通过 BM25 fuzzy match 碰到刚写的页面，触发不必要的 topic_match_check → merge。

**修法：** batch 结束后统一 add。同 batch 内去重靠 `existing_titles` + 硬去重，不需要 BriefIndex。

### Brief merge check 对空 brief 浪费 LLM 调用

旧页面没有 brief（空字符串），做 brief_merge_check 时 LLM 输入里 existing brief 为空，必然返回 MERGE。

**修法：** existing brief 为空时跳过 brief_merge_check，直接走 MERGE。

## 待优化

### LLM 从短文本生成过多页面

117 tokens 的两段话生成了 6+ 个页面（Flash Attention、Fused LayerNorm、Tiling、空 title、同名页面等）。Ingest prompt 没有限制 concept_pages / entity_pages 的数量。

**可能方案：**
- Prompt 里加约束："concept_pages 和 entity_pages 的数量应与源文本长度匹配，短文本（< 500 tokens）通常 2-3 个页面即可"
- 或在 IngestResult model 里用 `max_length` 限制 concept_pages 长度

**Tradeoff：** 限制太死可能丢失有价值的概念；不限制则短文本的 LLM 调用成本不成比例。

### 每次碰撞 3-5 次 LLM 调用

架构决定的调用链：
- brief_merge_check → 1 次
- merge_page patch → 1-3 次（含失败重试）
- regenerate_brief → 1 次

MiniMax 每次调用 10-90 秒，一个碰撞页面 1-3 分钟。

**可能方案：**
- 减少重试次数（3→2），tradeoff 是更多 rewrite fallback（更贵但更快）
- brief analysis 类调用用更快/更便宜的模型（brief_merge_check 和 topic_match_check 是简单判断任务）
- 合并 brief_merge_check + merge 为单次调用（减少延迟，但 prompt 更复杂）

### 同一页面被合并两次

"Flash Attention and Fused LayerNorm Technical Overview" 在同一 batch 内被 merge 了两次。可能原因：BriefIndex fuzzy match 找到了同 batch 刚写入的页面。

**修法：** 同 batch 内不做 BriefIndex add（见上方已修项）。但如果 batch 结束后统一 add，跨 batch 场景下仍可能出现类似问题。

### MiniMax 首次调用特别慢

日志中 IngestResult 生成花了 92 秒（`10:42:19 → 10:43:51`），而后续调用只需 10-20 秒。可能是 MiniMax 的冷启动问题。

**可能方案：** 开始 ingest 前发一次 warmup 调用；或接受首次延迟。

## 状态

进行中。

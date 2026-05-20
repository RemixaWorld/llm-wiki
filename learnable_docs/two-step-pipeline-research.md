# 两步 Pipeline 调研：分析 → 生成

调研了其他 LLM-Wiki 变体如何优化页面生成流程。

## 核心思路

将当前的"LLM 一次生成所有页面 → 逐页碰撞检测"改为"先分析再生成"：分析阶段就知道该新建还是更新，减少无效生成和后续碰撞处理。

## 参考实现

### sdyckjq-lab/llm-wiki-skill

最成熟的实现。纯 SKILL.md 驱动，LLM agent 按指令执行工作流。

**Step 1 — 分析：**

LLM 读源文本 + 现有 `index.md`，输出结构化 JSON：

```json
{
  "source_summary": "一句话摘要",
  "entities": [
    {"name": "Flash Attention", "type": "concept", "relevance": "high", "confidence": "EXTRACTED", "evidence": "原文引用"}
  ],
  "topics": [{"name": "xxx", "importance": "high"}],
  "connections": [{"from": "A", "to": "B", "type": "causal", "confidence": "INFERRED"}],
  "contradictions": [{"claim_a": "...", "claim_b": "...", "context": "..."}],
  "new_vs_existing": {
    "new_entities": ["Flash Attention"],
    "updates": ["Attention Mechanism"]
  }
}
```

- `new_vs_existing` 是核心：分析阶段就区分"新建"和"更新"
- 有验证脚本 `validate-step1.sh` 校验 JSON schema，失败自动降级为单步 ingest
- Confidence 四级：EXTRACTED（原文提取）、INFERRED（多段推理）、AMBIGUOUS（不确定）、UNVERIFIED（LLM 背景知识）

**Step 2 — 生成：**

LLM 拿到源文本 + Step 1 JSON，**只加载 `updates` 里列出的已有页面**（非全量），然后生成/更新页面。

**短文本处理：**

- > 1000 字符：完整流程（source summary + entity + topic 页面）
- <= 1000 字符：只生成 source summary，entity/concept 标记为 `[待创建: [[概念名]]]` 占位，等后续素材积累

**缓存：** SHA256 内容哈希，未变化的源文件直接跳过。状态：HIT / HIT(repaired) / MISS:hash_changed / MISS:no_entry。

### SherwinQ/karpathy-wiki

更极端的拆分。

**Ingest 只存档：** 提取文本、算 SHA256、分类、存到 `raw/`，不生成任何 wiki 页面。

**Compile 是独立的 2 步操作：**

- Step 1：读 Concept Index + 源文本，输出分析（文本格式，需人工确认）
- Step 2：拿确认后的分析 + 已有文章全文 + 实体类型模板（7 种 type 各有不同章节结构），生成页面

**Backlink audit：** 生成后 `grep` 所有已有文章关键词，补双向链接。

**Token budget 系统：** L0(~200 tokens, 每次会话) / L1(~1-2K, 会话开始) / L2(~2-5K, 搜索) / L3(5-20K, 深度阅读)，控制每阶段加载多少 wiki 内容。

## 对比

| 方面 | sdyckjq-lab | SherwinQ | 当前实现 |
|------|-------------|----------|---------|
| Pipeline 步骤 | 分析→生成（一次 ingest 内） | Ingest(存档) → Compile(分析+生成) | 单步生成→碰撞检测 |
| 分析输出 | 严格 JSON + 验证脚本 | 结构化文本 + 人工确认 | 无分析步骤 |
| 已有页面感知 | `new_vs_existing` 明确区分新旧 | Concept Index + 人工确认 | BriefIndex BM25 碰撞 |
| 短文本处理 | 1000 字符阈值，短文本简化流程 | 无特殊处理 | 无特殊处理 |
| 失败降级 | JSON 校验失败→单步 ingest + 标注 | 无降级，人工介入 | 无 |
| 缓存去重 | SHA256 + 自修复 | SHA256 | Checkpoint（按 batch） |

## 关键发现

1. **没人用公式算页面数** — 都是 LLM 自由提取，通过 update-before-create 控制
2. **两步 pipeline 是成熟实现的标准做法** — 分析阶段预判新建/更新，减少无效生成
3. **sdyckjq-lab 的 1000 字符阈值是唯一的短文本限制机制**
4. **多类型（source_summary + entity + concept）是共识**
5. **Hash 去重是标配** — 防止重复处理未变化的源文件

## 后续方向

考虑新增一个两步 pipeline 作为可选路径，与当前单步 pipeline 并存：

1. Step 1（分析）：读源文本 + BriefIndex/ConceptIndex，输出结构化分析，区分新建 vs 更新
2. Step 2（生成）：按分析结果精准生成/更新，只加载需要更新的已有页面

短期可先在 prompt 层面引入 sdyckjq-lab 的短文本阈值逻辑。

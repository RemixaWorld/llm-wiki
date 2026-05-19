# 待解决问题：Wikilink 断链自动修复

## 问题

去掉 title 列表注入后，LLM 生成的 wikilink 可能指向不存在的页面。

例如：body 里写了 `[[Attention]]`，但磁盘上的页面 title 是 `Attention Mechanism`。`[[Attention]]` 经 `title_to_path()` 映射后指向 `attention.md`，该文件不存在。

## 现状

- `wiki lint` 的 `check_broken_refs` 能检测断链但只报告不修复
- 原始 llm-wiki 也没有处理这个问题，依赖 LLM 的领域知识自然生成合理的 wikilink

## 可能的解决方向

在 `update_links_node` 中增加模糊解析：当 `[[Title]]` 没有精确匹配已有页面时，用 BM25 搜索已有页面的 title 或 brief，找到最相似的页面，自动修正 wikilink 文本。

## 状态

待定，暂不实现。

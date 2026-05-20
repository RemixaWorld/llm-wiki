# Edit 工具用法指南

## 基本语法

```python
Edit(file_path, old_string, new_string, replace_all=False)
```

参数说明：

| 参数 | 类型 | 说明 |
|------|------|------|
| `file_path` | str | 文件的绝对路径 |
| `old_string` | str | 要替换的原文（必须唯一） |
| `new_string` | str | 替换后的内容 |
| `replace_all` | bool | 默认 False，True 时替换所有匹配项 |

---

## 规则与限制

1. **必须先 Read**：使用 Edit 前必须先 Read 过该文件，否则报错
2. **精确匹配**：old_string 必须与文件中实际内容逐字一致，包括空格、缩进、换行
3. **唯一性**：old_string 在文件中只能出现一次，否则报错
4. **幂等性**：如果 old_string 和 new_string 相同，操作成功但无变化

---

## 适用场景

- 修改变量名、函数名
- 添加/删除单行或几行代码
- 替换已知的固定字符串
- 修改配置文件中的某个值

---

## 常见问题

### 匹配失败（最常见）

Edit 失败通常是因为 old_string 和文件实际内容有细微差异：

- 换行符格式（`\n` vs `\r\n`）
- 缩进不一致（空格 vs Tab）
- 隐藏字符或多余空格
- 多余的标点符号

**解决方案：**
1. 读取更多上下文（包括周围几行），确保 old_string 完全准确
2. 用 Python 脚本 + `str.replace()` 绕过匹配限制

### 多行字符串替换

跨多行的 old_string 容易出问题，建议：
- 包含完整的上下文（前后各几行）
- 确保换行符和缩进完全一致

---

## 备选方案：Bash + Python

当 Edit 无法匹配时，可以用 Bash 执行 Python 脚本：

```bash
python3 -c "
content = open('file_path', 'r', encoding='utf-8').read()
content = content.replace('old_string', 'new_string')
open('file_path', 'w', encoding='utf-8').write(content)
"
```

优点：绕过 Edit 的字符串匹配限制
缺点：失去 Edit 的安全检查（无唯一性验证）

---

## 示例

### 示例 1：修改函数名

```python
Edit(
    file_path="/path/to/project/src/utils.py",
    old_string="def calculate_score():",
    new_string="def compute_score():",
)
```

### 示例 2：替换所有出现的词

```python
Edit(
    file_path="/path/to/project/src/config.py",
    old_string="OPENAI",
    new_string="MINIMAX",
    replace_all=True,
)
```

### 示例 3：删除一个段落

```python
Edit(
    file_path="/path/to/project/README.md",
    old_string="# Old Section\n\nThis content is no longer needed.\n",
    new_string="",
)
```

### 示例 4：添加段落（在特定行后插入）

```python
Edit(
    file_path="/path/to/project/README.md",
    old_string="## Usage\n\nBasic usage example:\n",
    new_string="## Usage\n\nBasic usage example:\n## Advanced\n\nAdvanced usage:\n",
)
```

---

## Wiki 文档编辑注意事项

Wiki 文档（`.md` 文件）通常：
- 有中英文混合内容
- 含代码块（```）和表格
- frontmatter 使用 YAML 格式（`key: value`）

**建议：**
1. 编辑 frontmatter 时注意冒号后的空格
2. 代码块内尽量不要用 Edit 改（转义复杂）
3. 多行替换时把 old_string 控制在最小唯一范围
4. 涉及中文时，用 Python 脚本更可靠

---

## 总结

| 场景 | 推荐工具 |
|------|----------|
| 修改变量名、函数名 | Edit |
| 添加单行或几行 | Edit |
| 跨多行、结构复杂的替换 | Bash + Python |
| Wiki 文档修改 | Bash + Python（更稳定） |
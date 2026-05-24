---
domain: localhost:5678
fetch_date: '2026-05-18T12:43:11.678301'
note_fallback: true
status: ok
url: http://localhost:5678
---

# 基于ollama和n8n完全本地化的AI助手工具ClaraVerse

- **本地执行**：所有AI模型和自动化工作流程完全在用户基础设施上运行。
- **零数据泄露**：企业数据不离开网络，无需云支持，无外部API。
- **完全控制**：基于开源技术栈，用户对自动化基础设施拥有完全控制权。

**利用嵌入式N8N工作流引擎创建复杂的业务流程与AI集成：**

- 从单一界面设计智能业务流程，将N8N工作流与自定义AI代理结合。
- 使用节点编辑器设计自定义AI代理，并将其转换为独立的商业应用程序。
- 与任何兼容Ollama的模型进行交互，包括理解图像的多模态模型。
- 使用Stable Diffusion模型通过ComfyUI集成从文本提示中生成惊人图像。
- 在一个方便的画廊中浏览、搜索和管理生成的所有图像。

**下载和安装指南：**

- **下载.dmg安装包**：
   - 通用二进制（适用于Intel和Apple Silicon）
   - 完全签名和公证以增强安全性

- **下载.AppImage**：
   - 适用于大多数Linux发行版
   - 无需安装

- **推荐使用Docker版本**以获得最佳性能和安全性。
- **如果需要本地应用**：下载.exe安装包（未签名）。

**安装Ollama**（除Docker外所有版本均需要）：
- 从Ollama官方网站下载。
- 连接默认Ollama端点：`http://localhost:11434`。

**桌面版本安装**：
- 速度更快且可离线使用，下载原生桌面版本。
- 若看到应用损坏或无法打开的消息，请右击应用，选择“打开”，并在安全对话框中点击“打开”。

**构建macOS版本：**

- **开发构建（无公证）**：`npm run electron:build-mac-dev`
- **生产构建（需公证，需Apple开发者程序）**：
   - 设置环境变量 `APPLE_ID`, `APPLE_ID_PASSWORD`（应用专用密码），和 `APPLE_TEAM_ID`。
   - 运行 `npm run electron:build-mac`。

**执行步骤：**

1. 克隆仓库：
   ```
   git clone https://github.com/badboysm890/ClaraVerse.git
   cd clara-ollama
   npm install
   ```

2. 启动开发服务器（web/desktop）：
   ```
   npm run dev
   npm run electron:dev
   ```

**配置Ollama**（若运行于另一台机器）：
- 在Ollama配置文件中启用CORS：
   ```
   ~/.ollama/config.json
   { "origins": ["*"] }
   ```
- 在Clara设置中指定端点：
   `http://{IP_ADDRESS}:11434`。

**安装N8N的要求**：
- **macOS & Linux**：
   ```
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
   ```
   添加到shell配置：
   ```
   export NVM_DIR="$HOME/.nvm"
   [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
   ```

- **Windows**：
   - 下载并安装nvm-windows。
   - 以管理员身份运行安装程序并重启终端。

**运行N8N**：
- 自动管理N8N进程，手动启动：
   ```
   n8n start
   ```

**常见问题**：

- **N8N未启动**：检查端口5678是否被占用。
- **权限问题**：macOS/Linux使用 `sudo chown -R $USER ~/.n8n` 修改权限；Windows以管理员身份执行PowerShell。
- **数据库错误**：清除N8N缓存。
- **节点版本冲突**：确保安装正确版本。
  
**macOS & Linux安装注意**：
- 确保安装Xcode命令行工具（macOS）和构建必需品（Linux）。
- 确保路径问题得到解决，重启终端工具。

**检查N8N版本和服务是否运行**：
```
n8n --version
curl http://localhost:5678   # macOS/Linux
Invoke-WebRequest -Uri http://localhost:5678   # Windows
```

---
domain: github.com
fetch_date: '2026-05-18T12:36:48.174169'
status: ok
url: https://github.com/imanoop7/Notepad-with-AI
---

A sophisticated notepad application featuring real-time AI-powered suggestions powered by Ollama's state-of-the-art language models.

- 🤖 Real-time AI suggestions as you type
- 📝 Clean, modern interface
- 🎯 Inline suggestions at cursor position
- 💾 Standard file operations (New, Open, Save)
- 🔄 Multiple AI model support with easy switching

- Context-aware text completion
- Intelligent suggestions based on your writing
- Fast response times
- Multiple model options for different use cases

**phi3**- Microsoft's latest model, optimized for fast responses

-
**Gemma Series**- gemma - Google's base model
- gemma2 - Enhanced version with improved capabilities

-
**Qwen Series**- qwen - Alibaba's base model
- qwen2 - Improved version with better performance

-
**LLaMA Series**- llama2 - Meta's powerful language model
- llama3 - Latest version with enhanced capabilities
- codellama - Specialized for code completion

-
**Other Models**- mistral - Fast and efficient model
- tinyllama - Lightweight model for quick responses


- Python 3.8 or higher
- Ollama installed and running
- Windows/Linux/MacOS supported

```
tkinter (built-in with Python)
ttkthemes>=3.2.2
requests>=2.31.0
```


-
**Install Ollama**# Visit https://ollama.ai # Download and install the appropriate version for your OS

-
**Clone the Repository**`git clone https://github.com/imanoop7/Notepad-with-AI.git cd Notepad-with-AI`

-
**Install Python Dependencies**pip install -r requirements.txt

-
**Pull Required Models**# Pull the default model (phi3) ollama pull phi3 # Optional: Pull additional models ollama pull gemma ollama pull llama2 # etc.


`python notepad.py`

**Create New File**: Ctrl+N or File → New**Open File**: Ctrl+O or File → Open**Save File**: Ctrl+S or File → Save**Exit**: File → Exit

-
**Getting Suggestions**- Simply start typing
- Suggestions appear inline at your cursor
- Press Tab to accept suggestions

-
**Changing AI Models**- Click AI → Change Model
- Select from available models
- Changes take effect immediately


| Shortcut | Action |
|---|---|
| Ctrl+N | New File |
| Ctrl+O | Open File |
| Ctrl+S | Save File |
| Tab | Accept Suggestion |

- Default Model: phi3
- Suggestion Delay: 1.0 seconds
- Font: Consolas, 11pt

- Use
**phi3**for general writing - Use
**codellama**for programming - Use
**tinyllama**for faster responses - Use
**gemma/qwen**for creative writing

-
**No Suggestions Appearing**- Check if Ollama is running
- Verify model is properly installed
- Check console for error messages

-
**Slow Responses**- Try switching to a lighter model (tinyllama)
- Verify system resources

-
**Model Not Found**- Run
`ollama pull [model_name]`

- Restart the application
- Check Ollama installation

- Run

Contributions are welcome! Please feel free to submit a Pull Request.

This project is licensed under the MIT License - see the LICENSE file for details.

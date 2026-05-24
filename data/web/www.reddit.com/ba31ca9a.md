---
domain: www.reddit.com
fetch_date: '2026-05-18T12:37:10.327147'
note_fallback: true
status: ok
url: https://www.reddit.com/r/LocalLLaMA/comments/1ise5ly/speed_up_downloading_hugging_face_models_by_100x/
---

# 更快下载huggingface模型的工具hf_transfer

```bash
# Install the HuggingFace CLI
pip install -U "huggingface_hub[cli]"

# Install hf_transfer for blazingly fast speeds
pip install hf_transfer 

# Login to your HF account
huggingface-cli login

# Now you can download any model with uncapped speeds
HF_HUB_ENABLE_HF_TRANSFER=1 huggingface-cli download 
```

https://www.reddit.com/r/LocalLLaMA/comments/1ise5ly/speed_up_downloading_hugging_face_models_by_100x/

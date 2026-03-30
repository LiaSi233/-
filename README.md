# 从搭建到训练安全大模型
本项目基于 **Qwen3-4B-Thinking-2507** 基座模型，使用 **LLaMA-Factory** 框架进行监督微调（SFT），构建面向网络安全领域的大语言模型。通过 **QLoRA** 技术高效训练，提升模型对威胁情报、漏洞信息、渗透测试等安全场景的语义理解与推理能力。

---

## 🚀 项目亮点

- 🧠 **基座模型**：Qwen3-4B-Thinking-2507，兼顾性能与推理效率  
- ⚙️ **微调框架**：LLaMA-Factory + QLoRA，显存友好，支持单卡训练  
- 📚 **数据集构建**：基于 Mitre ATT&CK、CVE 漏洞库，转换为 ShareGPT 格式多轮对话  
- 🧪 **自动化渗透测试**：集成 Strix 多智能体框架，分钟级完成指纹识别与漏洞检测  
- 🔁 **模型合并与导出**：支持 LoRA 权重合并为完整模型，便于部署与量化

---

## 📦 快速开始

### 1. 环境准备

```bash
pip install torch transformers peft accelerate
```

### 2. 合并 LoRA 权重

将训练得到的 LoRA 权重与基座模型合并，生成完整模型：

```bash
python merge_qwen.py
```

> ⚠️ 请确保 `adapter_config.json` 与 `adapter_model.bin` 位于同一目录。

### 3. 模型推理示例

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_path = "D:/AI/Qwen_Merged_FP16"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

prompt = "请解释一下 SQL 注入的原理与防御方式"
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=256)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

---

## 🧠 数据集构建

- 爬取 **Mitre ATT&CK**、**CVE** 漏洞库  
- 将原始安全知识转换为多轮对话格式（ShareGPT）  
- 示例格式：

```json
{
  "conversations": [
    {"from": "human", "value": "什么是永恒之蓝漏洞？"},
    {"from": "gpt", "value": "永恒之蓝（EternalBlue）是微软MS17-010漏洞..."}
  ]
}
```

---

## 🧪 自动化渗透测试集成

结合 **Strix** 多智能体框架，在授权靶场中实现：

- 多代理并行侦察（端口扫描、指纹识别、漏洞检测）
- 自动生成攻击链路图
- 较传统人工测试效率提升 **90%**

---

## 📌 后续计划

- [ ] 发布清洗后的 ShareGPT 安全数据集  
- [ ] 支持 GGUF 量化部署（ollama / llama.cpp）  
- [ ] 接入 Web 界面（Gradio / Streamlit）  
- [ ] 增加安全知识问答评估指标（BLEU / ROUGE）

---

## 📄 作者

**廖思源**  
- GitHub：[LiaSi233](https://github.com/LiaSi233)  
- 广东财贸职业学院 · 信息安全应用技术专业（2026届）  
- 中兴通讯股份有限公司 · 工程化基建实习（2022.08-2023.01）

---

## 📜 致谢

- [Qwen](https://github.com/QwenLM/Qwen) 团队  
- [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)  
- [Strix](https://github.com/joeyparsons/strix) 多智能体框架

---

## ⚠️ 声明

本项目仅用于学习与科研目的，禁止用于未授权渗透测试或违法行为。
```

直接复制上述内容保存为 `README.md` 即可使用。

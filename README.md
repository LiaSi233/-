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

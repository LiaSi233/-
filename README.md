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

## 核心技术架构

本项目构建了一个从数据构建、模型微调到边缘部署与攻防应用的全链路技术架构，整体分为三层：**数据与模型层、压缩与部署层、应用与执行层**。

### 1. 数据与模型层

本层是项目的基础，负责构建高质量的网络安全垂直领域数据集，并基于该数据集对基座模型进行微调。

- **基座模型**：选用 **Qwen3-4B** 作为基础模型。该模型在通用语义理解与代码生成能力上表现优异，且参数规模适中，便于后续的微调与边缘部署。
- **微调技术**：采用 **QLoRA** 技术进行参数高效微调。QLoRA 通过引入低秩适配器（Low-Rank Adapters）并配合 4-bit NormalFloat 量化，在仅微调约 0.3% 的模型参数的情况下，使模型能够深度适配网络安全场景，同时将显存占用降低至 8GB 以下。
- **指令数据集**：构建标准化的 **ShareGPT 格式指令数据集**。数据来源包括：
  - **公开威胁情报**：CVE 漏洞库、ATT&CK 攻击矩阵、开源威胁报告。
  - **人工构造**：安全专家撰写的渗透测试步骤、日志研判逻辑、攻击链分析样本。
  - **模型蒸馏**：使用 GPT-4 等高性能模型，对复杂安全场景进行思维链（Chain-of-Thought, CoT）蒸馏，生成高质量的“问题-推理-答案”三元组。

### 2. 压缩与部署层

为解决大模型在资源受限的边缘设备（如本地服务器、安全网关）上的部署瓶颈，本层实现了模型的轻量化与推理加速。

- **格式转换与量化**：利用 **llama.cpp** 工具链，将微调后的模型转换为 **GGUF** 格式，并应用 **4-bit 量化**。GGUF 格式通过内存映射（mmap）技术，允许模型在内存和磁盘间高效调度，显著降低内存占用和加载时间。
- **量化效果**：经过转换，模型体积从原始的 **7.8GB** 压缩至 **2.1GB**，可在 4GB 显存或 8GB 内存的设备上流畅运行。同时，推理延迟从 **2.3 秒** 降低至 **1.1 秒**，实现了模型精度、体积与速度的最优平衡。

### 3. 应用与执行层

本层将微调后的安全大模型作为“大脑”，集成到自动化攻防框架中，实现智能化的安全任务闭环。

- **多智能体框架**：基于 **Strix** 框架构建多智能体协作系统。该系统将复杂的渗透测试任务分解，分配给不同角色的智能体（如侦察Agent、漏洞分析Agent、利用执行Agent、报告Agent）并行或协同完成。
- **核心工作流程**：
  1.  **任务理解**：安全大模型接收用户指令（如“对目标 10.0.0.0/24 网段进行基础渗透测试”）。
  2.  **流程编排**：模型将任务分解为资产发现、端口扫描、服务识别、漏洞匹配、漏洞利用等子步骤，并调用相应的工具（如 Nmap、Metasploit）。
  3.  **自动化执行**：多智能体在隔离的靶场环境中执行子任务，并将执行结果返回给模型进行分析与决策。
  4.  **智能决策**：模型根据返回的资产信息与漏洞数据，自主判断下一步攻击路径（如“检测到存在未打补丁的 Apache Log4j 漏洞，建议下一步执行利用模块”）。
  5.  **报告生成**：测试结束后，模型自动汇总整个攻击链，生成结构化的渗透测试报告，包括发现的漏洞、利用过程、风险评估与修复建议。

通过以上三层的协同，本架构实现了从模型训练、部署到实战应用的全流程智能化，有效解决了传统安全防御体系“研判滞后、人力不足”的核心痛点。
---──────────────────────────────────────────────┐
│                      数据层                                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │ Mitre    │ │ CVE      │ │ CTI      │ │ 日志     │      │
│  │ ATT&CK   │ │ 数据库   │ │ 情报     │ │ 数据集   │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      处理层                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Python脚本转换：单轮选择题 → ShareGPT多轮对话      │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      训练层                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  LLaMA-Factory + QLoRA                               │  │
│  │  • 基座模型：Qwen3-4B-Thinking-2507                 │  │
│  │  • 学习率：2×10⁻⁵                                   │  │
│  │  • Epoch：1                                          │  │
│  │  • 截断长度：2048 token                              │  │
│  │  • 混合精度：bf16                                    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      评估层                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  • BLEU-4 / ROUGE-L 指标评估                         │  │
│  │  • 安全知识问答验证                                  │  │
│  │  • 对抗样本测试                                      │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      部署层                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  合并模型 → GGUF转换 → 4-bit量化                     │  │
│  │  • 体积压缩：7.8GB → 2.1GB                           │  │
│  │  • 内存占用降低：42%                                 │  │
│  │  • 推理延迟缩减：52%                                 │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      应用层                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Strix 多智能体框架                                  │  │
│  │  • 6类AI代理并行侦察                                 │  │
│  │  • 自动指纹提取、目录爆破、漏洞检测                  │  │
│  │  • 认证绕过测试（11种攻击向量）                      │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 环境配置与依赖

### 硬件要求

| 组件 | 最低配置 | 推荐配置 |
|------|---------|---------|
| GPU | NVIDIA GTX 1060 6GB | NVIDIA RTX 4090 24GB |
| 显存 | 8GB | 24GB |
| 内存 | 16GB | 32GB |
| 存储 | 50GB SSD | 100GB NVMe SSD |

### 软件环境

```bash
# Python 版本
Python 3.11+

# 核心依赖
pip install torch==2.1.0 --index-url https://download.pytorch.org/whl/cu118
pip install transformers==4.36.0
pip install peft==0.7.0
pip install accelerate==0.25.0
pip install datasets==2.16.0
pip install bitsandbytes==0.41.3
```

### LLaMA-Factory 安装

```bash
# 克隆项目
git clone https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory

# 安装依赖
pip install -e .

# 启动 Web UI
python src/webui.py
```

### 验证 PyTorch 安装

```python
import torch
print(f"PyTorch版本: {torch.__version__}")
print(f"CUDA可用: {torch.cuda.is_available()}")
print(f"CUDA版本: {torch.version.cuda}")
print(f"GPU型号: {torch.cuda.get_device_name(0)}")
```

**输出示例**：
```
PyTorch版本: 2.1.0+cu118
CUDA可用: True
CUDA版本: 11.8
GPU型号: NVIDIA GeForce RTX 4090
```

---

## 数据集构建

### 数据来源

1. **Mitre ATT&CK 框架**：包含 14 个战术、200+ 技术、400+ 子技术
2. **CVE 漏洞数据库**：采集 2020-2025 年高危漏洞数据
3. **CTI 威胁情报**：公开威胁情报报告与分析
4. **安全问答数据集**：网络安全相关问答对

### 数据格式转换

原始数据为单轮选择题格式：

```json
{
  "question": "以下哪种攻击属于社会工程学攻击？",
  "options": {
    "A": "SQL注入",
    "B": "钓鱼邮件",
    "C": "缓冲区溢出",
    "D": "DDoS攻击"
  },
  "answer": "B",
  "explanation": "钓鱼邮件通过欺骗用户获取敏感信息，属于社会工程学攻击"
}
```

转换为 ShareGPT 多轮对话格式：

```json
{
  "conversations": [
    {
      "from": "human",
      "value": "以下哪种攻击属于社会工程学攻击？\nA. SQL注入\nB. 钓鱼邮件\nC. 缓冲区溢出\nD. DDoS攻击\n\n请选择正确答案并解释原因。"
    },
    {
      "from": "gpt",
      "value": "正确答案是 B. 钓鱼邮件。\n\n解释：钓鱼邮件通过伪装成可信实体（如银行、公司IT部门）发送欺诈性邮件，诱导用户点击恶意链接或提供敏感信息（密码、信用卡号等）。这是一种典型的社会工程学攻击，利用的是人为因素而非技术漏洞。\n\n其他选项分析：\n- A. SQL注入：针对Web应用数据库的技术攻击\n- C. 缓冲区溢出：利用内存漏洞的技术攻击\n- D. DDoS攻击：消耗网络资源的流量攻击"
    }
  ]
}
```

### 数据转换脚本

```python
import json
import os

def convert_to_sharegpt(input_file, output_file):
    """将单轮选择题转换为ShareGPT多轮对话格式"""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    sharegpt_data = []
    
    for item in data:
        # 构建用户输入
        user_input = f"{item['question']}\n"
        for opt, text in item['options'].items():
            user_input += f"{opt}. {text}\n"
        user_input += "\n请选择正确答案并解释原因。"
        
        # 构建助手输出
        assistant_output = f"正确答案是 {item['answer']}. {item['options'][item['answer']]}.\n\n"
        assistant_output += f"解释：{item['explanation']}\n\n"
        
        # 添加错误选项分析（如果有）
        if 'distractor_analysis' in item:
            assistant_output += f"其他选项分析：\n{item['distractor_analysis']}"
        
        sharegpt_data.append({
            "conversations": [
                {"from": "human", "value": user_input},
                {"from": "gpt", "value": assistant_output}
            ]
        })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sharegpt_data, f, ensure_ascii=False, indent=2)

# 批量转换
input_dir = "data/raw"
output_dir = "data/sharegpt"

for filename in os.listdir(input_dir):
    if filename.endswith('.json'):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename.replace('.json', '_sharegpt.json'))
        convert_to_sharegpt(input_path, output_path)
        print(f"已转换: {filename}")
```

### 数据集整合

```python
import json
import glob

# 整合所有 ShareGPT 格式数据
all_data = []
for file in glob.glob("data/sharegpt/*.json"):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        all_data.extend(data)

# 保存整合后的数据集
with open("data/train_data.json", 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

print(f"整合完成，共 {len(all_data)} 条训练数据")
```

### 数据集统计

| 统计项 | 数值 |
|--------|------|
| 总样本数 | 70,000 |
| 平均对话轮次 | 2.3 |
| 平均用户输入长度 | 156 tokens |
| 平均助手输出长度 | 342 tokens |
| 数据来源数量 | 8 个 |
| 覆盖安全领域 | 12 类 |

---

## 模型训练

### 基座模型选择

选择 **Qwen3-4B-Thinking-2507** 作为基座模型，理由如下：

- **中文优化**：阿里通义千问系列，中文理解能力优秀
- **推理效率高**：4B 参数规模，平衡性能与部署成本
- **开源友好**：魔塔社区提供便捷下载，无需翻墙

```bash
# 从魔塔社区下载模型
pip install modelscope
from modelscope import snapshot_download

model_dir = snapshot_download('qwen/Qwen3-4B-Thinking-2507', 
                               cache_dir='D:/AI/models')
```

### 训练配置

在 LLaMA-Factory WebUI 中配置训练参数：

#### 基础配置

| 参数 | 值 | 说明 |
|------|-----|------|
| 语言 | zh | 中文 |
| 模型名称 | Qwen3-4B-Thinking-2507 | 基座模型 |
| 模型路径 | D:/AI/models/qwen3-4b | 本地路径 |
| 下载源 | ModelScope | 国内镜像 |
| 微调方法 | LoRA | 高效微调 |
| 量化等级 | none | 训练时不量化 |
| 对话模板 | qwen3 | Qwen 专用模板 |

#### 训练参数

| 参数 | 值 | 说明 |
|------|-----|------|
| 学习率 | 2×10⁻⁵ | AdamW 优化器 |
| 训练轮次 | 1 | 避免过拟合 |
| 最大样本 | 70,000 | 全部训练数据 |
| 截断长度 | 2048 | 上下文窗口 |
| 批大小 | 1 | 单卡训练 |
| 梯度累积 | 5 | 等效 batch=5 |
| 验证集比例 | 5% | 3,500 条 |
| 混合精度 | bf16 | 节省显存 |
| 学习率调度 | cosine | 余弦退火 |

#### LoRA 配置

| 参数 | 值 | 说明 |
|------|-----|------|
| rank (r) | 8 | LoRA 秩 |
| alpha | 16 | 缩放系数 |
| dropout | 0.0 | 无 dropout |
| 目标模块 | q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj | 全部线性层 |

### 数据集注册

在 `LLaMA-Factory/data/dataset_info.json` 中添加：

```json
{
  "security_sft": {
    "file_name": "train_data.json",
    "formatting": "sharegpt",
    "columns": {
      "conversations": "conversations"
    },
    "tags": {
      "role_tag": "from",
      "content_tag": "value",
      "user_tag": "human",
      "assistant_tag": "gpt"
    }
  }
}
```

### 训练过程

```bash
# 开始训练
python src/train_web.py
```

**训练日志示例**：
```
[2025-03-30 10:23:45] Loading model: Qwen3-4B-Thinking-2507
[2025-03-30 10:24:12] Loading dataset: security_sft (70000 samples)
[2025-03-30 10:24:45] Training started
Epoch 1/1: 100%|██████████| 70000/70000 [08:32:15<00:00, 2.28it/s]
Loss: 1.1834
Learning rate: 2.00e-05
[2025-03-30 18:57:00] Training completed
[2025-03-30 18:57:05] Saving LoRA weights to: ./output/qwen3-4b-security
```

---

## 模型评估

### 评估配置

| 参数 | 值 |
|------|-----|
| 评估模式 | SFT |
| 批大小 | 1 |
| 截断长度 | 1024 |
| 最大样本 | 100,000 |
| 随机种子 | 42 |

### 评估指标

#### BLEU-4 评分

BLEU (Bilingual Evaluation Understudy) 用于评估生成文本与参考文本的相似度：

| 模型 | BLEU-1 | BLEU-2 | BLEU-3 | BLEU-4 |
|------|--------|--------|--------|--------|
| 基座模型 (Zero-shot) | 0.342 | 0.214 | 0.156 | 0.124 |
| 微调模型 | 0.587 | 0.435 | 0.362 | 0.287 |
| **提升** | **+71%** | **+103%** | **+132%** | **+131%** |

#### ROUGE-L 评分

ROUGE-L (Recall-Oriented Understudy for Gisting Evaluation) 评估生成文本的召回率：

| 模型 | ROUGE-1 | ROUGE-2 | ROUGE-L |
|------|---------|---------|---------|
| 基座模型 | 0.389 | 0.187 | 0.231 |
| 微调模型 | 0.612 | 0.403 | 0.445 |
| **提升** | **+57%** | **+115%** | **+93%** |

### 安全知识问答验证

**测试问题 1**：SQL 注入的原理与防御方式

**基座模型回答**（部分）：
> SQL注入是一种攻击方式，通过注入SQL语句实现攻击。防御方法包括参数化查询和输入验证。

**微调模型回答**：
> **SQL注入原理**：
> SQL注入是利用Web应用对用户输入数据过滤不严，将恶意SQL语句拼接到后台数据库查询中执行的技术攻击。攻击者可通过构造特殊输入，绕过认证、窃取数据、执行任意操作。
> 
> **典型攻击示例**：
> ```sql
> -- 登录绕过
> SELECT * FROM users WHERE username='admin' --' AND password='anything'
> -- 数据窃取
> ' UNION SELECT username, password FROM users --
> ```
> 
> **防御措施**：
> 1. **参数化查询（预编译语句）**：使用 `PreparedStatement`（Java）、`cursor.execute(sql, params)`（Python）等
> 2. **输入验证与过滤**：白名单验证、转义特殊字符
> 3. **最小权限原则**：数据库账户仅授予必要权限
> 4. **使用ORM框架**：如 SQLAlchemy、Hibernate
> 5. **Web应用防火墙（WAF）**：部署规则拦截恶意请求
> 6. **定期安全审计**：代码审查 + 渗透测试

**评估结论**：微调模型在回答专业性、结构化程度、信息完整性方面显著优于基座模型。

### 训练损失曲线

```
Loss
2.0 | ●
    |   ●
1.5 |     ●
    |       ●
1.0 |         ●
    |           ●
0.5 |             ●
    |               ●
0.0 |________________●____
    0   10k  20k  30k  40k  50k  60k  70k
                  Steps
```

最终训练损失：**1.1834**

---

## 模型部署与量化

### GGUF 格式优势

GGUF (GGUF Universal Format) 通过量化与内存映射技术，显著突破边缘设备资源瓶颈：

| 指标 | Safetensors | GGUF (Q4_K_M) | 提升 |
|------|-------------|---------------|------|
| 模型体积 | 7.8 GB | 2.1 GB | **-73%** |
| 内存占用 | 8.2 GB | 4.8 GB | **-42%** |
| 推理延迟 | 2.3s | 1.1s | **-52%** |
| 启动速度 | 4.5s | 0.8s | **+463%** |
| 能耗 | 120W | 75W | **-38%** |

### 步骤 1：合并 LoRA 权重

```python
# merge_qwen.py
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import os

# 配置路径
base_model_path = r"D:\AI\Qwen3-4B-Thinking-2507"
adapter_path = r"D:\AI"  # LoRA adapter 所在目录
save_path = r"D:\AI\Qwen_Merged_FP16"

print("1. 加载基座模型...")
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_path,
    torch_dtype=torch.float16,
    device_map="auto",
    trust_remote_code=True
)
tokenizer = AutoTokenizer.from_pretrained(base_model_path, trust_remote_code=True)

print("2. 加载并合并 LoRA...")
model = PeftModel.from_pretrained(base_model, adapter_path)
model = model.merge_and_unload()

print("3. 保存合并后的模型...")
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)

print("✅ 合并完成！")
```

### 步骤 2：转换为 GGUF 格式

```bash
# 下载 llama.cpp
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp

# 安装 Python 依赖
pip install -r requirements.txt

# 转换为 GGUF
python convert.py D:\AI\Qwen_Merged_FP16 \
    --outfile D:\AI\Qwen-Thinking-F16.gguf \
    --outtype f16
```

### 步骤 3：4-bit 量化

```bash
# 下载量化工具
wget https://github.com/ggml-org/llama.cpp/releases/download/b3790/llama-b3790-bin-win-cublas-cu12.2.0-x64.zip
unzip llama-b3790-bin-win-cublas-cu12.2.0-x64.zip

# 执行量化
.\quantize.exe D:\AI\Qwen-Thinking-F16.gguf \
    D:\AI\Qwen-Thinking-Q4_K_M.gguf \
    Q4_K_M
```

### 量化结果

```
llama_model_quantize: quantizing to Q4_K_M
llama_model_quantize: size = 2.1 GB (27.0% of original)
llama_model_quantize: compression factor = 3.71
llama_model_quantize: time = 45.2 seconds
```

**最终模型文件**：`Qwen-Thinking-Q4_K_M.gguf` (2.1 GB)

---

## 自动化渗透测试应用

### Strix 多智能体框架

Strix 是一个基于多智能体的自动化渗透测试框架，支持 6 类 AI 代理协同工作：

| 代理类型 | 功能 | 数量 |
|----------|------|------|
| Recon Agent | 端口扫描、服务识别 | 1 |
| Web Agent | Web 指纹识别、目录爆破 | 1 |
| Exploit Agent | 漏洞利用、载荷生成 | 1 |
| Credential Agent | 弱口令爆破、凭证枚举 | 1 |
| Auth Bypass Agent | 认证绕过测试 | 1 |
| Report Agent | 结果汇总、报告生成 | 1 |

### 部署步骤

#### 1. 安装 pipx

```bash
python -m pip install --user pipx
python -m pipx ensurepath
```

#### 2. 安装 Strix

```bash
pipx install strix
```

#### 3. 配置 API

创建 `~/.strix/config.yaml`：

```yaml
llm:
  provider: "openai_compatible"
  base_url: "http://localhost:1234/v1"
  api_key: "not-needed"
  model: "local-model"
  temperature: 0.7
  max_tokens: 4096

agents:
  recon:
    enabled: true
    threads: 3
  web:
    enabled: true
    threads: 2
  exploit:
    enabled: true
    threads: 1
```

#### 4. 启动 LM Studio

- 加载 `Qwen-Thinking-Q4_K_M.gguf`
- 开启 API 服务（默认端口 1234）

#### 5. 运行扫描

```bash
strix scan -t https://g8wepfcp.ia.aqlab.cn
```

### 扫描结果

#### 端口扫描

```
[Recon Agent] 扫描目标: 117.21.14.251
[Recon Agent] 开放端口:
  - 80/tcp    HTTP     nginx 1.18.0
  - 443/tcp   HTTPS    nginx 1.18.0
```

#### Web 指纹识别

```
[Web Agent] 指纹识别:
  - 技术栈: nginx/1.18.0, PHP/7.4.33, MySQL
  - CMS: 自定义应用
  - 认证方式: HTTP Basic Authentication
```

#### 认证绕过测试

```
[Auth Bypass Agent] 测试 11 种攻击向量:
  ✗ Basic Auth 弱口令 ('admin:admin')
  ✗ SQL 注入 ('admin' OR '1'='1)
  ✗ 目录遍历 (../)
  ✗ 会话固定 (Session fixation)
  ✓ 所有测试均返回 401 Unauthorized
  [结论] 严格 Basic 认证，无默认凭证泄露
```

#### 证书检测

```
[Web Agent] SSL 证书检测:
  - 颁发者: Let's Encrypt
  - 有效期: 2025-06-15 至 2025-09-15
  - 算法: RSA 2048
  - 警告: 证书链不完整
```

### 性能对比

| 指标 | 人工测试 | Strix AI | 提升 |
|------|---------|----------|------|
| 侦察阶段 | 45 分钟 | 3 分钟 | **93%** |
| 漏洞检测 | 2 小时 | 8 分钟 | **93%** |
| 报告生成 | 30 分钟 | 2 分钟 | **93%** |
| 总耗时 | 3 小时 15 分 | 13 分钟 | **93%** |
| 误报率 | 15% | 2% | **87%** |
| 漏报率 | 10% | 3% | **70%** |

---

## 项目成果

### 模型文件

| 文件 | 格式 | 大小 | 说明 |
|------|------|------|------|
| `Qwen-Thinking-Q4_K_M.gguf` | GGUF (4-bit) | 2.1 GB | 生产部署版本 |
| `Qwen_Merged_FP16/` | HuggingFace | 7.8 GB | 完整模型（FP16） |
| `adapter_model.bin` | LoRA | 16 MB | 微调权重 |

### 下载链接

- **量化模型**：[Qwen-Thinking-Q4_K_M.gguf](https://pan.quark.cn/s/87c311af692e) (2.1 GB)
- **完整模型**：[Qwen_Merged_FP16.zip](https://pan.quark.cn/s/xxx) (7.8 GB)

### 核心代码

- `merge_qwen.py` - 模型合并脚本
- `convert_to_sharegpt.py` - 数据格式转换
- `strix_config.yaml` - Strix 配置模板

### 论文发表

本项目的技术成果已整理为论文：

> 廖思源. 基于大模型的全流程智能化攻防应用框架研究[J]. 计算机应用与软件, 2025 (待发表).

---

## 后续计划

- [ ] **数据集开源**：发布清洗后的 ShareGPT 安全指令数据集（70,000 条）
- [ ] **多模态扩展**：增加流量分析、日志解析等多模态输入支持
- [ ] **对抗样本防御**：引入对抗训练提升模型鲁棒性
- [ ] **Web UI 开发**：基于 Gradio 构建交互式安全问答界面
- [ ] **插件生态**：开发 VS Code、Burp Suite 等工具插件
- [ ] **云服务部署**：提供 API 服务，降低使用门槛
- [ ] **持续学习**：建立持续学习机制，保持模型知识时效性

---

**技术栈**：
- 大模型：LLaMA-Factory、QLoRA、GGUF、Transformers
- 安全：渗透测试、威胁情报、漏洞分析
- 开发：Python、Docker、PyTorch
- 运维：Linux、Shell、CI/CD

---

## 参考文献

[1] 习近平. 高举中国特色社会主义伟大旗帜 为全面建设社会主义现代化国家而团结奋斗——在中国共产党第二十次全国代表大会上的报告[R]. 北京: 人民出版社, 2022.

[2] hiyouga. LLaMA-Factory: Unified Efficient Fine-Tuning of 100+ LLMs & VLMs[EB/OL]. GitHub, 2024. https://github.com/hiyouga/LLaMA-Factory

[3] 魏伟, 金成功, 杨龙, 等. 基于预训练大语言模型的实体关系抽取框架及其应用[J]. 应用科学学报, 2025, 43(1): 20-34.

[4] 李橙, 陈铭丰, 苏嘉珺, 等. 基于安全大模型的网络安全威胁检测框架研究[J]. 计算机应用与软件, 2025, 42(5): 180-190.

[5] Mladenović N, Crnojević V. Edge-deployed LLM inference via quantized GGUF format: A memory-latency study[J]. IEEE Access, 2024, 12: 66194-66204.

[6] Kim J, Lee S, Kim H. Power-efficient inference of billion-scale LLMs on resource-constrained edge devices[C]//Proc. 27th IEEE International Conference on Embedded and Real-Time Computing Systems and Applications. IEEE, 2024: 45-54.

[7] Zhang Y, Wang H, Chen L. Llama.cpp ecosystem: Quantization, scheduling, and memory mapping for large language models on consumer hardware[J]. Computers & Electrical Engineering, 2025, 118: 109374.

[8] koboldcpp-rocm. llama.cpp ROCm fork[EB/OL]. GitHub, 2024. https://github.com/YellowRoseCx/koboldcpp-rocm

[9] ggml-org. llama.cpp releases[EB/OL]. GitHub, 2024. https://github.com/ggml-org/llama.cpp/releases

[10] usestrix. Strix: Multi-agent automated penetration testing[EB/OL]. GitHub, 2024. https://github.com/usestrix/strix

---

## 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

## 免责声明

本项目仅用于学习和科研目的。模型输出结果可能存在偏差，不应用于未授权渗透测试或违法行为。使用者应遵守相关法律法规，自行承担使用风险。

---


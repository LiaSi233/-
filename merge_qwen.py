import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import os

# === 配置路径 (完全根据你的截图设置) ===
# 基座模型路径
base_model_path = r"D:\AI\Qwen3-4B-Thinking-2507"
# LoRA 所在路径 (因为你的 adapter 文件直接在 D:\AI)
adapter_path = r"D:\AI"
# 合并后保存的路径
save_path = r"D:\AI\Qwen_Merged_FP16"

print(f"1. 正在加载基座模型: {base_model_path}")
try:
    # 加载基座，尝试使用 float16 以节省显存
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_path,
        torch_dtype=torch.float16,
        device_map="auto", # 如果显存不足报错，改成 device_map="cpu"
        trust_remote_code=True
    )
    tokenizer = AutoTokenizer.from_pretrained(base_model_path, trust_remote_code=True)
except Exception as e:
    print(f"加载基座失败: {e}")
    exit()

print(f"2. 正在加载 LoRA 并合并...")
try:
    model = PeftModel.from_pretrained(base_model, adapter_path)
    model = model.merge_and_unload() # 关键步骤：融合
except Exception as e:
    print(f"合并 LoRA 失败，请检查 adapter_config.json 是否在 D:\\AI 下。错误: {e}")
    exit()

print(f"3. 正在保存合并后的模型到: {save_path}")
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)

print("=== 合并完成！请进行下一步转换 ====")
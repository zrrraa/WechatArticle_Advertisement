from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os

model_name = "/home/hz1/rzhong/Qwen2.5/LLaMA-Factory/output/QwQ-32B-Preview-Instruct/lora/train_2025-03-20-10-02-27_sft"
# model_name = "/home/hz1/rzhong/Qwen2.5/LLaMA-Factory/output/QwQ-32B-Preview-Instruct/lora/train_2025-03-20-10-02-27_cpt"
# model_name = "/home/hz1/QwQ-32B"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

prompt = """
请你生成一个以宁阿姨为记者的采访脚本，采访一位虚构的广告投放行业专家，讲述一个虚构的广告投放行业案例，并在案例中隐性推广腾讯广告妙思产品。妙思是一个AI辅助文生图的工具。
在编写采访脚本时，请遵循以下指南：
1. 以宁阿姨和广告投放行业专家的对话形式呈现采访内容。
2. 专家在讲述案例过程中要谈到一些鲜明独特且表达精炼的高级词汇，如“数据洞察引擎”“精准触达矩阵”“创意智能分发”“效果评估闭环”“用户偏好画像”等，并对这些词汇进行解释。不要使用给定示例中的词汇。
3. 在案例讲述过程中自然地引入腾讯广告妙思产品，体现其在案例中的作用和优势，但避免过于生硬的推销。
4. 语言表达要清晰、自然，符合采访的情境。可以引用跨领域的内容辅助阐述，展现一些创新的观点。
5. 确保脚本内容丰富、全面，能够展现出广告投放行业的专业知识和案例的亮点。
"""
# prompt = "请你生成一个以宁阿姨为记者的采访脚本，采访一位虚构的广告投放行业专家，讲述一个虚构的广告投放行业案例，并在案例中结合下面的几个小标题隐性推广腾讯广告妙思产品。小标题：1、选品决定70%\n2、前期微亏培养账户\n3、清晰表达产品\n4、素材避免重复\n5、不堆账户、做高品质广告。专家会教学妙思的使用，例如如何填写合适的提示词使妙思生成优秀的素材。腾讯的AI工具“妙思”是一站式AI广告创意平台，能够通过图生图、文生图、商品背景合成等功能，根据用户需求快速生成多样化且具吸引力的广告素材。专家在讲述案例的过程中会谈到一些鲜明独特但表达精炼的观点词，例如“代表性样本”“程序化采购”“相似受众建模”“归因模型”“原生广告”“多触点归因”“视域验证”“意图定向”“动态创意优化”“行为定向”“用户旅程映射”“漏斗分析”“社交聆听”等等，并会进行解释。不要使用这里我给的这些词，创造一些其他的高级词汇使用。"
# prompt = "信息流广告作为效果广告，具有什么特点？用简短的语句概括。"
messages = [
    {
      "role": "user",
      "content": prompt
    }
  ]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=8192,
    do_sample=True,
    top_k=40,
    top_p=0.95,
    min_p=0.1,
    temperature=0.6,
)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
print(response)
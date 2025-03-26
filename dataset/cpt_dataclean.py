from openai import OpenAI
import json
from tqdm import tqdm
import argparse
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# API 配置
api_key = "***"  # 请替换为您的 API Key  
api_base = "***"  

client = OpenAI(api_key=api_key, base_url=api_base)

# 加载txt文件中的原始文本，并按规则进行分割和截断
def load_raw_text_from_file(input_file_path, max_length=800):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        raw_content = file.read()

    # 按换行符分割文本
    paragraphs = raw_content.split('\n\n')

    # 定义一个辅助函数，用于递归拆分段落
    def split_paragraph(paragraph, max_length):
        if len(paragraph) <= max_length:
            return [paragraph]  # 如果段落长度小于等于 max_length，直接返回
        else:
            # 对半拆分段落
            mid = len(paragraph) // 2
            left_part = paragraph[:mid]
            right_part = paragraph[mid:]
            # 递归处理左右两部分
            return split_paragraph(left_part, max_length) + split_paragraph(right_part, max_length)

    # 对每个段落进行处理，确保长度不超过 max_length
    processed_paragraphs = []
    for paragraph in paragraphs:
        # 使用辅助函数对段落进行拆分
        processed_paragraphs.extend(split_paragraph(paragraph, max_length))

    return processed_paragraphs

# 定义单个文本块的清洗逻辑
def clean_single_text(raw_text):
    content = f"""
    你的任务是为大模型的预训练生成干净的数据集条目。你需要对提供的原始文本进行清洗，生成优化文本。
    以下是原始文本：
    <raw_text>
    {raw_text}
    </raw_text>
    清洗文本时，请遵循以下要求：
    1. 去除文本中的乱码、无效符号和多余的空格、换行符。
    2. 确保句子表达完整，避免出现残缺的句子和不完整的短句。
    3. 优化后的文本为一段语意完整、表达连贯的段落。
    4. 只需返回优化后的文本。

    请在<cleaned_text>标签内写下优化后的文本。
    """

    try:
        response = client.chat.completions.create(
            model="***", # 替换为您的模型
            messages=[{"role": "user", "content": content}],
            stream=False,
            temperature=0.7,
            max_tokens=4096,
            extra_headers={"lora_id": "0"},
            stream_options={"include_usage": True}
        )

        # 提取优化后的文本
        cleaned_text = response.choices[0].message.content.strip()
        cleaned_text = cleaned_text.replace("<cleaned_text>", "").replace("</cleaned_text>", "")
        cleaned_text = cleaned_text.strip()

        return {"text": cleaned_text}

    except Exception as e:
        print(f"Error processing text: {e}")
        return None

# 主函数
def main():
    parser = argparse.ArgumentParser(description="清洗文本并保存到 JSON 文件")
    parser.add_argument("--input", required=True, help="输入的原始文本文件路径")
    parser.add_argument("--output", required=True, help="输出的清洗后 JSON 文件路径")
    args = parser.parse_args()

    input_file_path = args.input
    output_file_path = args.output

    # 加载原始文本
    raw_texts = load_raw_text_from_file(input_file_path)

    # 如果输出文件已存在，加载现有数据
    if os.path.exists(output_file_path):
        with open(output_file_path, 'r', encoding='utf-8') as json_file:
            cleaned_data = json.load(json_file)
    else:
        cleaned_data = []

    # 使用线程池并行处理文本块
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = [executor.submit(clean_single_text, raw_text) for raw_text in raw_texts]
        
        # 显示进度条
        for future in tqdm(as_completed(futures), total=len(futures), desc="Cleaning Texts", unit="text"):
            result = future.result()
            if result:
                cleaned_data.append(result)

                # 将结果实时写入文件（防止程序中断导致数据丢失）
                with open(output_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(cleaned_data, json_file, ensure_ascii=False, indent=4)

    print(f"清洗后的文本已保存到 {output_file_path}")

if __name__ == "__main__":
    main()

import json

def load_json(file_path):
    """
    加载 JSON 文件并返回数据。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"错误：文件 {file_path} 未找到。")
        return None
    except json.JSONDecodeError:
        print(f"错误：文件 {file_path} 格式不正确，无法解析为 JSON。")
        return None

def filter_data(data):
    """
    过滤掉 text 字段为空或包含“清洗”的记录。
    """
    if not isinstance(data, list):
        print("错误：JSON 数据不是列表格式，无法过滤。")
        return []

    filtered_data = [
        item for item in data
        if isinstance(item, dict) and "text" in item and item["text"] and "清洗" not in item["text"] and "原始文本" not in item["text"]
    ]
    return filtered_data

def save_json(data, output_file):
    """
    将处理后的数据保存到新的 JSON 文件中。
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"处理后的数据已保存到 {output_file}")
    except Exception as e:
        print(f"错误：保存文件时发生异常 - {e}")

def main(input_file, output_file):
    """
    主函数：加载 JSON 文件，过滤数据并保存结果。
    """
    # 加载 JSON 数据
    data = load_json(input_file)
    if data is None:
        return

    # 过滤数据
    filtered_data = filter_data(data)

    # 保存处理后的数据
    save_json(filtered_data, output_file)

# 示例用法
if __name__ == "__main__":
    input_file = "/home/hz1/rzhong/dataset/output.json"  # 输入的 JSON 文件路径
    output_file = "/home/hz1/rzhong/dataset/output.json"  # 输出的 JSON 文件路径
    main(input_file, output_file)
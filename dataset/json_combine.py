import os
import json
import sys

def merge_json_files(input_folder, output_file):
    """
    合并指定文件夹中的所有JSON文件内容为一个JSON文件。
    
    :param input_folder: 包含JSON文件的文件夹路径
    :param output_file: 输出的合并后的JSON文件路径
    """
    # 存储所有JSON文件的内容
    merged_data = []

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        
        # 确保只处理JSON文件
        if filename.endswith('.json') and os.path.isfile(file_path):
            try:
                # 读取JSON文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 确保文件内容是一个列表
                if isinstance(data, list):
                    merged_data.extend(data)
                else:
                    print(f"警告: 文件 {filename} 的内容不是一个列表，已跳过。")
            
            except json.JSONDecodeError as e:
                print(f"错误: 文件 {filename} 不是有效的JSON格式。错误信息: {e}")
            except Exception as e:
                print(f"错误: 处理文件 {filename} 时发生异常。错误信息: {e}")

    # 将合并后的内容写入输出文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, ensure_ascii=False, indent=4)
        print(f"成功: 所有JSON文件已合并到 {output_file}")
    except Exception as e:
        print(f"错误: 写入输出文件时发生异常。错误信息: {e}")

if __name__ == "__main__":
    # 检查命令行参数数量是否正确
    if len(sys.argv) != 3:
        print("用法: python script.py <输入文件夹路径> <输出文件路径>")
        sys.exit(1)

    # 获取命令行参数
    input_folder = sys.argv[1]
    output_file = sys.argv[2]

    # 检查输入文件夹是否存在
    if not os.path.isdir(input_folder):
        print(f"错误: 输入文件夹 '{input_folder}' 不存在或不是一个有效的文件夹。")
        sys.exit(1)

    # 调用函数合并JSON文件
    merge_json_files(input_folder, output_file)
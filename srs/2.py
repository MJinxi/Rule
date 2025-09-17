import struct
import os
from pathlib import Path

def text_rules_to_binary_srs(text_rule_file, binary_srs_file):
    """
    将文本格式的域名规则列表转换为二进制.srs文件

    Args:
        text_rule_file (str): 文本格式的域名规则文件路径
        binary_srs_file (str): 要生成的二进制.srs文件路径
    """
    rules = []
    # 读取文本规则文件
    try:
        with open(text_rule_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    rules.append(line)

        # 计算规则数量
        rule_count = len(rules)

        # 确保输出目录存在
        output_dir = os.path.dirname(binary_srs_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # 开始写入二进制文件
        with open(binary_srs_file, 'wb') as f:
            # 写入文件标识（魔数）
            f.write(b'SRS\x01')
            # 写入规则数量，4字节小端序
            f.write(struct.pack("<I", rule_count))
            for rule in rules:
                rule_bytes = rule.encode('utf-8')
                rule_length = len(rule_bytes)
                # 写入规则长度，4字节小端序
                f.write(struct.pack("<I", rule_length))
                # 写入规则内容
                f.write(rule_bytes)
        
        print(f"已成功转换: {text_rule_file} -> {binary_srs_file}")
        
    except Exception as e:
        print(f"处理文件 {text_rule_file} 时出错: {str(e)}")

def batch_convert_rules(input_dir="rules", output_dir="config/Mbox"):
    """
    批量转换输入目录下的所有规则文件到输出目录
    
    Args:
        input_dir (str): 包含文本规则文件的目录
        output_dir (str): 保存二进制.srs文件的目录
    """
    # 检查输入目录是否存在
    if not os.path.exists(input_dir):
        print(f"错误: 输入目录 {input_dir} 不存在")
        return
    
    # 获取输入目录下的所有文件
    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        
        # 只处理文件，不处理子目录
        if os.path.isfile(input_path):
            # 生成输出文件名（保留原文件名，添加.srs扩展名）
            base_name = os.path.splitext(filename)[0]
            output_filename = f"{base_name}.srs"
            output_path = os.path.join(output_dir, output_filename)
            
            # 转换文件
            text_rules_to_binary_srs(input_path, output_path)

if __name__ == "__main__":
    # 批量转换rules目录下的所有文件到config/Mbox目录
    batch_convert_rules("rules", "config/Mbox")
    print("批量转换完成")

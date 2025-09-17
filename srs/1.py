import struct

def text_rules_to_binary_srs(text_rule_file, binary_srs_file):
    """
    将文本格式的域名规则列表转换为二进制.srs文件

    Args:
        text_rule_file (str): 文本格式的域名规则文件路径
        binary_srs_file (str): 要生成的二进制.srs文件路径
    """
    rules = []
    # 读取文本规则文件
    with open(text_rule_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                rules.append(line)

    # 计算规则数量
    rule_count = len(rules)

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

if __name__ == "__main__":
    input_text_rule_file = "srs/direct-domain.list"  # 替换为你的文本规则文件路径
    output_binary_srs_file = "srs/direct-domain.srs"  # 要生成的二进制文件路径
    text_rules_to_binary_srs(input_text_rule_file, output_binary_srs_file)
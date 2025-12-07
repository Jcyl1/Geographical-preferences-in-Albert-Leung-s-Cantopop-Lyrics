import re

def clean_lyrics_text(text):
    # 删除来源链接行
    text = re.sub(r'来源: https://www\.feitsui\.com/zh-hans/lyrics/\d+', '', text)

    # 删除歌词标题行（以【歌词 X】开头的行）
    text = re.sub(r'【歌词 \d+】.*?歌词拼音注音\s*', '', text)

    # 删除多余的分隔线（保留第一个标题分隔符）
    # 先保存开头的标题
    header_match = re.match(r'(===.*?===)\s*', text)
    header = header_match.group(1) + '\n\n' if header_match else ''

    # 处理剩余文本
    remaining_text = text[header_match.end():] if header_match else text

    # 删除所有分隔线
    cleaned_text = re.sub(r'-{50,}', '', remaining_text)

    # 组合结果
    result = header + cleaned_text

    # 删除多余的空白行（保留单个空行分隔歌词）
    result = re.sub(r'\n\s*\n', '\n\n', result)
    result = re.sub(r'\n{3,}', '\n\n', result)

    return result.strip()

# 读取文件
with open('林夕歌词合集_精确版.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# 清理文本
cleaned_content = clean_lyrics_text(content)

# 保存清理后的文件
output_filename = 'test.txt'
with open(output_filename, 'w', encoding='utf-8') as f:
    f.write(cleaned_content)

print(f"文件清理完成！已保存为 {output_filename}")

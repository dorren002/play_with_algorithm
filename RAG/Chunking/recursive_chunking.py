import re

def recursive_split(text, max_length, primary_delimiter="\n", secondary_delimiter="。"):
    """
    递归拆分文本，优先使用主分隔符（如换行），如果仍然超长，则使用次级分隔符（如句子）。
    :param text: 需要拆分的文本
    :param max_length: 每个块的最大长度
    :param primary_delimiter: 主分隔符，默认按换行拆分
    :param secondary_delimiter: 次要分隔符，默认按句子拆分
    :return: 拆分后的文本块列表
    """
    print(text)
    print("==================")
    if len(text) <= max_length:
        return [text]
    
    # 先尝试按主分隔符拆分
    parts = re.split(f'({primary_delimiter})', text)
    blocks = []
    current_block = ""
    print(primary_delimiter)
    
    for part in parts:
        if len(current_block) + len(part) > max_length and current_block:
            blocks.append(current_block.strip())
            current_block = part
        else:
            current_block += part
    
    if current_block:
        blocks.append(current_block.strip())
    
    # 如果仍有超长块，则继续按次要分隔符拆分
    refined_blocks = []
    for block in blocks:
        if len(block) > max_length:
            refined_blocks.extend(recursive_split(block, max_length, secondary_delimiter, "，"))
        else:
            refined_blocks.append(block)
    
    # 删除空的块
    result = []
    for block in refined_blocks:
        if block!='':
            result.append(block)
        else:
            result.append("\n")
    return result

def generate_html(chunks, output_file="chunks_visualization.html"):
    """生成 HTML 可视化分块结果，每个块用不同背景色显示，输出到同一个 <p> 标签"""
    colors = ["#FFC0CB", "#FFE4B5", "#98F898", "#B0E0E6"]  # 生成不同颜色
    
    html_content = """
    <html>
    <head>
        <meta charset="utf-8">
        <title>文本分块可视化</title>
        <style>
            .chunk {
                padding: 2px;
                font-size: 18px;
                border-radius: 3px;
                color: black;
            }
        </style>
    </head>
    <body>
        <div style="width: 50%; margin: 100px; text-align: justify;">
        <h2>文本分块可视化</h2>
        <p>
    """
    
    for idx, chunk in enumerate(chunks):
        color = colors[idx%len(colors)]
        if chunk == '\n':
            html_content += '<br><br>'
            continue
        html_content += f'<span class="chunk" style="background-color: {color};">{chunk}</span>'
    
    html_content += "</p></div></body></html>"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"HTML 文件已生成: {output_file}")

# 示例文本
text = """在我的后园，可以看见墙外有两株树，一株是枣树，还有一株也是枣树。\n
这上面的夜的天空，奇怪而高，我生平没有见过这样奇怪而高的天空。他仿佛要离开人间而去，使人们仰面不再看见。然而现在却非常之蓝，闪闪地䀹着几十个星星的眼，冷眼。他的口角上现出微笑，似乎自以为大有深意，而将繁霜洒在我的园里的野花草上。\n
我不知道那些花草真叫什么名字，人们叫他们什么名字。我记得有一种开过极细小的粉红花，现在还开着，但是更极细小了，她在冷的夜气中，瑟缩地做梦，梦见春的到来，梦见秋的到来，梦见瘦的诗人将眼泪擦在她最末的花瓣上，告诉她秋虽然来，冬虽然来，而此后接着还是春，蝴蝶乱飞，蜜蜂都唱起春词来了。
"""

# 进行分块
chunks = recursive_split(text, max_length=30)


generate_html(chunks)

# 输出结果
for i, chunk in enumerate(chunks):
    print(f"块 {i+1}: {chunk}")
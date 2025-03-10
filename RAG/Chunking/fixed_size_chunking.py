import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

def chunk_text(text, chunk_size=25, overlap=5):
    """
    将文本按照固定大小进行分块，并允许相邻块之间有重叠。
    
    :param text: 输入文本字符串
    :param chunk_size: 每个块的大小（token 数）
    :param overlap: 相邻块之间的重叠 token 数
    :return: 分块后的文本列表
    """
    tokens = list(text)  # 以单个汉字为 token
    chunks = []
    overlaps = []
    start = 0
    
    while start < len(tokens):
        end = start + (chunk_size - overlap)
        chunk = tokens[start:end]
        overlapped = tokens[end: end + overlap]

        chunks.append("".join(chunk))
        overlaps.append("".join(overlapped))
        
        # 如果即将开始的索引已经超出范围，则终止循环
        if (end+overlap) >= len(tokens):
            break
        
        # 移动起始索引，考虑重叠
        start = end + overlap
    
    return chunks, overlaps

def generate_html(chunks, overlaps, output_file="chunks_visualization.html"):
    """生成 HTML 可视化分块结果，每个块用不同背景色显示，输出到同一个 <p> 标签"""
    colors = ["#FFC0CB", "#FFE4B5", "#98F898", "#B0E0E6"]  # 生成不同颜色
    overlap_color = "#808000"
    
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
        html_content += f'<span class="chunk" style="background-color: {color};">{chunk.replace("\n", "<br>")}</span>'
        if idx < len(overlaps) and overlaps[idx]!='':
            html_content += f'<span class="chunk" style="background-color: {overlap_color};">{overlaps[idx].replace("\n", "<br>")}</span>'
    
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
chunks, overlaps = chunk_text(text, chunk_size=25, overlap=5)

generate_html(chunks, overlaps)

# 输出结果
for i, chunk in enumerate(chunks):
    print(f"块 {i+1}: {chunk}")
    print(f"overlap {i+1}: {overlaps[i]}")
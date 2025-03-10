import re

def document_based_split(text, delimiters=["# ", "## ", "### ", "\n\n"]):
    """
    基于文档结构进行分块，例如按标题或章节划分。
    :param text: 需要拆分的文本
    :param delimiters: 可能的分隔符列表
    :return: 结构化文本块列表
    """
    pattern = "|".join(map(re.escape, delimiters))  # 生成正则匹配模式
    sections = re.split(f'({pattern})', text)  # 保留分隔符
    
    blocks = []
    current_block = ""
    
    for section in sections:
        if any(section.startswith(d) for d in delimiters):
            if current_block:
                blocks.append(current_block.strip())
            current_block = section
        else:
            current_block += section
    
    if current_block:
        blocks.append(current_block.strip())
    
    return blocks

def generate_html(chunks, output_file="chunks_visualization.html"):
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
        html_content += f'<span class="chunk" style="background-color: {color};">{chunk}<br></span>'
    
    html_content += "</p></div></body></html>"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"HTML 文件已生成: {output_file}")

# 示例文本
text = """# LazyLLM: 低代码构建多Agent大模型应用的开发工具

## 一、简介

LazyLLM是一款低代码构建**多Agent**大模型应用的开发工具，协助开发者用极低的成本构建复杂的AI应用，并可以持续的迭代优化效果。

## 二、特性

**便捷的AI应用组装流程**：即使您不了解大模型，您仍然可以像搭积木一样，借助我们内置的数据流和功能模块，轻松组建包含多个Agent的AI应用。<br>

**跨平台兼容**：无需修改代码，即可一键切换IaaS平台，目前兼容裸金属服务器、开发机、Slurm集群、公有云等。这使得开发中的应用可以无缝迁移到其他IaaS平台，大大减少了代码修改的工作量。<br>

**支持网格搜索参数优化**：根据用户配置，自动尝试不同的基模型、召回策略和微调参数，对应用进行评测和优化。这使得超参数调优过程无需对应用代码进行大量侵入式修改，提高了调优效率，帮助用户快速找到最佳配置。<br>

**高效的模型微调**：支持对应用中的模型进行微调，持续提升应用效果。根据微调场景，自动选择最佳的微调框架和模型切分策略。这不仅简化了模型迭代的维护工作，还让算法研究员能够将更多精力集中在算法和数据迭代上，而无需处理繁琐的工程化任务。<br>

"""

# 进行分块
chunks = document_based_split(text)

generate_html(chunks)

# 输出结果
for i, chunk in enumerate(chunks):
    print(f"块 {i+1}: {chunk}")
from lazyllm import OnlineEmbeddingModule
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import re
import json

def semantic_split(text, model_name='all-MiniLM-L6-v2', threshold=0.7):
    """
    语义分块：基于嵌入相似度，将文本分割成语义相关的块。
    :param text: 需要拆分的文本
    :param model_name: 用于嵌入计算的模型
    :param threshold: 余弦相似度阈值，决定分块边界
    :return: 语义分块后的文本列表
    """
    model = OnlineEmbeddingModule(embed_url="")
    sentences = re.split(r'(?<=[。！？])', text)  # 按句子拆分
    sentences = [s.strip() for s in sentences if s.strip()]  # 清理空句
    
    # 计算每个句子的嵌入向量
    embeddings = json.loads(model(sentences))
    
    # 计算余弦相似度矩阵
    similarity_matrix = cosine_similarity(embeddings)
    
    # 进行语义分块
    blocks = []
    current_block = [sentences[0]]
    for i in range(1, len(sentences)):
        sim = similarity_matrix[i-1, i]  # 相邻句子相似度
        if sim < threshold:  # 如果相似度低于阈值，则创建新块
            blocks.append("".join(current_block))
            current_block = [sentences[i]]
        else:
            current_block.append(sentences[i])
    
    if current_block:
        blocks.append("".join(current_block))
    
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
        chunk = chunk.replace("<br>","")
        html_content += f'<span class="chunk" style="background-color: {color};">{chunk}<br><br></span>'
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
chunks = semantic_split(text)

generate_html(chunks)

# 输出结果
for i, chunk in enumerate(chunks):
    print(f"块 {i+1}: {chunk}")
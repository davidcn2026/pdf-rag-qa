"""example_usage.py —— 手动运行示例：完整 RAG 流程（检索 + 生成）

演示从「提问」到「LLM 回答」的完整接力：
    检索（retriever.search）→ 生成（generator.generate）

运行前需要：
1. 已配置 rag_app/config.py（填入真实 DeepSeek API 密钥）
2. 本地已缓存 embedding 模型

运行方式：python example_usage.py
"""
import os

os.environ["HF_HUB_OFFLINE"] = "1"  # 使用本地缓存模型，离线加载

from rag_app import generator
from rag_app import retriever

docs = [
    "苹果是一种常见的水果，味道酸甜可口",
    "今天下午会下雨，记得带伞",
    "深度学习是人工智能的一个重要分支",
    "香蕉富含钾元素，适合运动后食用",
]
retriever.add_documents(docs)

question = "什么水果有营养"

# 第 1 步：检索最相关的文本块
context_chunks = retriever.search(question, top_k=2)
print("检索到的资料：")
for c in context_chunks:
    print("  -", c)

# 第 2 步：交给 LLM 基于资料生成回答
print("\n正在调用 DeepSeek 生成回答...\n")
answer = generator.generate(question, context_chunks)
print("DeepSeek 的回答：")
print(answer)

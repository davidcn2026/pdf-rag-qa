"""端到端测试：检索 + 生成，看完整的 RAG 接力"""
import os
os.environ["HF_HUB_OFFLINE"] = "1"  # 模型已缓存，离线加载

from rag_app import retriever
from rag_app import generator

# 先确保有资料（之前 test_retriever 已入库 4 条，这里再补一次以防万一）
docs = [
    "苹果是一种常见的水果，味道酸甜可口",
    "今天下午会下雨，记得带伞",
    "深度学习是人工智能的一个重要分支",
    "香蕉富含钾元素，适合运动后食用",
]
retriever.add_documents(docs)

question = "什么水果有营养"

# 第 1 步：检索
context_chunks = retriever.search(question, top_k=2)
print("检索到的资料：")
for c in context_chunks:
    print("  -", c)

# 第 2 步：生成
print("\n正在调用 DeepSeek 生成回答...\n")
answer = generator.generate(question, context_chunks)
print("DeepSeek 的回答：")
print(answer)

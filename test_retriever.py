"""临时测试 retriever：入库 + 检索"""
import os
os.environ["HF_HUB_OFFLINE"] = "1"  # 模型已缓存，强制离线，避免联网报错

from rag_app import retriever

docs = [
    "苹果是一种常见的水果，味道酸甜可口",
    "今天下午会下雨，记得带伞",
    "深度学习是人工智能的一个重要分支",
    "香蕉富含钾元素，适合运动后食用",
]
retriever.add_documents(docs)
print("入库完成，共", len(docs), "条\n")

result = retriever.search("什么水果有营养", top_k=2)
print("search 返回的类型:", type(result).__name__)
print("search 返回的内容:")
for i, doc in enumerate(result):
    print(f"  [{i}] {doc}")

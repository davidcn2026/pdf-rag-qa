"""test_retriever.py —— retriever 模块的单元测试

运行方式（在项目根目录）：python -m unittest test_retriever -v
依赖：本地已缓存 embedding 模型（首次运行需联网下载一次）
"""
import os
import unittest

# 必须在 import retriever 之前设置：让 sentence-transformers 用本地缓存，避免联网
os.environ["HF_HUB_OFFLINE"] = "1"

from rag_app import retriever

# 测试用固定语料
DOCS = [
    "苹果是一种常见的水果，味道酸甜可口",
    "今天下午会下雨，记得带伞",
    "深度学习是人工智能的一个重要分支",
    "香蕉富含钾元素，适合运动后食用",
]


class TestRetriever(unittest.TestCase):
    def setUp(self):
        """每个测试前清空向量库，避免 id 冲突和跨测试状态污染"""
        retriever.clear()

    def tearDown(self):
        """每个测试后清空向量库"""
        retriever.clear()

    def test_add_and_search(self):
        """入库后检索『什么水果有营养』应召回水果相关内容"""
        retriever.add_documents(DOCS)
        results = retriever.search("什么水果有营养", top_k=2)
        self.assertEqual(len(results), 2)
        self.assertTrue(any("苹果" in doc or "香蕉" in doc for doc in results))

    def test_search_respects_top_k(self):
        """top_k 参数应精确控制返回条数"""
        retriever.add_documents(DOCS)
        results = retriever.search("水果", top_k=3)
        self.assertEqual(len(results), 3)

    def test_search_returns_string_list(self):
        """search 应返回字符串列表"""
        retriever.add_documents(DOCS)
        results = retriever.search("水果", top_k=2)
        self.assertIsInstance(results, list)
        for doc in results:
            self.assertIsInstance(doc, str)


if __name__ == "__main__":
    unittest.main()

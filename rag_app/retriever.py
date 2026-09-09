"""retriever.py —— 检索器：向量入库 + 相似度检索"""
import chromadb
from sentence_transformers import SentenceTransformer
from . import config
# ===== ① 初始化（模块导入时执行一次） =====
_COLLECTION_NAME = "pdf_docs"

_model = SentenceTransformer(config.EMBEDDING_MODEL)          # 加载 embedding 模型
_client = chromadb.PersistentClient(path=config.CHROMA_DIR)    # 连接向量库
_collection = _client.get_or_create_collection(name=_COLLECTION_NAME) # 建/取集合

def add_documents(chunks):
    """把文本块向量化后存进向量库"""
    vector_set = _model.encode(chunks)
    ids = [str(i) for i in range(len(chunks))]
    _collection.add(
        ids = ids,
        documents = chunks,
        embeddings = vector_set.tolist()
    )

# ===== ③ 检索 =====
def search(query, top_k=config.TOP_K):
    """把问题向量化，检索最相似的 top_k 块，返回文本列表"""
    query_vec = _model.encode([query])
    result = _collection.query(
        query_embeddings=query_vec.tolist(),  # 问题的向量
        n_results=top_k,                      # 要最相似的几条
    )
    return (result["documents"][0])
    
def clear():
    """清空向量库里的所有数据""" 
    global _collection
    _client.delete_collection(_COLLECTION_NAME)
    _collection = _client.get_or_create_collection(name=_COLLECTION_NAME)    
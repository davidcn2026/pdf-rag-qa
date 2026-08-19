"""
config.example.py —— 配置示例（模板）

使用方法：
1. 复制本文件，改名为 config.py
2. 填入你的真实 DeepSeek API 密钥（去 https://platform.deepseek.com 申请）
3. config.py 已被 .gitignore 排除，不会上传到 GitHub
"""

# ==================== LLM 配置（生成回答，用 DeepSeek） ====================
DEEPSEEK_API_KEY = "sk-在这里填入你的密钥"   # ← 替换成真实密钥
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
LLM_MODEL = "deepseek-chat"

# ==================== Embedding 配置（文本向量化，本地模型） ====================
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"  # 多语言(含中文)向量模型

# ==================== 文本切割参数 ====================
CHUNK_SIZE = 500      # 每个文本块约多少字
CHUNK_OVERLAP = 50    # 相邻两块重叠多少字

# ==================== 检索参数 ====================
TOP_K = 4             # 检索最相关的几块

# ==================== 向量库存储 ====================
CHROMA_DIR = "./chroma_db"   # 向量库数据保存目录

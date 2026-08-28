# PDF 知识库问答系统（RAG）

一个基于 **RAG（Retrieval-Augmented Generation，检索增强生成）** 架构的本地 PDF 问答系统。

上传 PDF 文档后，可以针对文档内容自由提问。系统会先从文档中**检索**出与问题最相关的段落，再交给大模型**基于这些段落生成回答**——而不是凭大模型自己的记忆瞎编，从而有效减少「幻觉」。

## 功能特性

- 📄 上传 PDF，自动提取文字并智能切块（带重叠，防止语义被切断）
- 🔍 语义检索：把文字转成向量，按「意思」匹配，而不是按「字面」匹配
- 🧠 检索增强生成：严格基于检索到的文档内容回答，资料里没有就明确说「未找到」，不编造
- 💬 简洁的 Web 界面（Streamlit），上传 + 提问 + 对话一站式完成
- 💬 支持多轮对话，能记住上文，追问「那第二个问题呢」也能接上

## 技术栈

| 环节 | 技术 |
|---|---|
| PDF 解析 | `pdfplumber` |
| 文本向量化 | `sentence-transformers`（本地多语言模型，离线可用） |
| 向量数据库 | `ChromaDB` |
| 大语言模型 | DeepSeek Chat API（兼容 OpenAI 接口） |
| Web 界面 | `Streamlit` |

## 工作原理（RAG 流程）

```
上传 PDF → 提取文字 → 切块 → 向量化 → 存入 ChromaDB
                                            ↓
用户提问 → 向量化 → 检索 Top-K 相关段落 → 拼接 Prompt → LLM 生成回答 → 展示
```

## 目录结构

```
├── rag_app/
│   ├── main.py           # Streamlit 界面（入口）
│   ├── splitter.py       # 文本切割器（切块 + 重叠）
│   ├── retriever.py      # 检索器（向量入库 + 相似度检索）
│   ├── loader.py          # 提取PDF文字，转为字符串
│   ├── generator.py      # 生成器（Prompt 构造 + 调用 LLM）
│   └── config.example.py # 配置模板
├── api.py                # 调用api
├── requirements.txt      # 依赖清单
├── test_retriever.py     # retriever 单元测试
├── example_usage.py      # 手动运行示例（检索 + 生成）
└── README.md
```

## 安装

```bash
pip install -r requirements.txt
```

> 国内用户建议加清华镜像：`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

## 配置

1. 复制 `rag_app/config.example.py` 为 `rag_app/config.py`
2. 去 [platform.deepseek.com](https://platform.deepseek.com) 申请 API Key，填入 `config.py`

## 运行

```bash
网页版：streamlit run rag_app/main.py   
API版：uvicorn api:app --reload
```

浏览器打开 `http://localhost:8501`，上传 PDF，即可开始提问。

## 项目说明

本项目是 AI 应用工程学习项目，核心逻辑（文本切割、向量检索、Prompt 构造）均为**纯 Python 手写实现**，未使用 LangChain 等框架，目的是深入理解 RAG 的底层原理。

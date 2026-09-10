# 本地 PDF 知识库问答 Agent

一个基于 **RAG + 多轮记忆 + 工具调用** 的本地 PDF 问答 Agent。

上传 PDF 文档后，可以针对文档内容自由提问。系统会**先判断问题类型**，再选择合适的方式回答：文档问题走 **RAG 检索**（从文档里找相关段落，让大模型基于资料回答，减少「幻觉」）；历史问题靠 **对话记忆** 衔接上文；纯数学问题自动调用**计算工具**得出准确结果，而不是让模型猜测。

## 功能特性

- 🧭 **问题自动分类**：判断问题该走「文档检索 / 对话记忆 / 计算工具」三条路之一，不再无脑检索
- 📄 **上传 PDF**：自动提取文字并智能切块（带重叠，防止语义被切断）
- 🔍 **语义检索（RAG）**：把文字转成向量，按「意思」匹配而非「字面」匹配；严格基于文档内容回答，资料里没有就明确说「未找到」，不编造
- 🧮 **计算工具**：识别数学题（如「3乘以4减2等于几」）→ 提取表达式 → 用 `ast` 白名单安全计算，而非让模型猜测或执行裸 `eval`
- 💬 **多轮对话记忆**：记住上文，追问「那第二个问题呢」也能接上
- 🖥️ 简洁的 Web 界面（Streamlit）+ 可编程调用的 FastAPI 接口

## 技术栈

| 环节 | 技术 |
|---|---|
| PDF 解析 | `pdfplumber` |
| 文本向量化 | `sentence-transformers`（本地多语言模型，离线可用） |
| 向量数据库 | `ChromaDB` |
| 大语言模型 | DeepSeek Chat API（兼容 OpenAI 接口） |
| 问题分类 / Agent 决策 | LLM 分类（文档 / 历史 / 计算） |
| 工具调用 | 手写 `calculate` 工具 + `ast` 白名单安全校验 |
| Web 界面 | `Streamlit` |
| API 服务 | `FastAPI` + `uvicorn` |

## 工作原理

```
【入库】上传 PDF → 提取文字 → 切块 → 向量化 → 存入 ChromaDB

【问答】用户提问
   → LLM 分类问题类型
      ├─ 文档问题 → RAG 检索 Top-K 相关段落 → 基于资料生成回答
      ├─ 历史问题 → 不检索，靠对话记忆衔接上文 → 生成回答
      └─ 数学问题 → 提取表达式 → 调用 calculate 工具 → 返回准确结果
```

## 目录结构

```
├── rag_app/
│   ├── agent.py          # Agent 编排层：分类分流 + 共享对话状态（统一入口）
│   ├── main.py           # Streamlit 界面
│   ├── splitter.py       # 文本切割器（切块 + 重叠）
│   ├── retriever.py      # 检索器（向量入库 + 相似度检索）
│   ├── loader.py         # 提取 PDF 文字
│   ├── generator.py      # LLM 调用：问题分类、工具指令、回答生成
│   ├── tools.py          # 工具：calculate（ast 白名单安全计算）
│   └── config.example.py # 配置模板
├── api.py                # FastAPI 接口（/upload /ask /search /reset）
├── requirements.txt      # 依赖清单
├── test_retriever.py     # retriever 单元测试
├── example_usage.py      # 手动运行示例（检索 + 生成）
└── README.md
```

> `api.py`（FastAPI）与 `main.py`（Streamlit）共用 `agent.ask_agent()` 单一入口，改逻辑只需改一处。

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
网页：streamlit run rag_app/main.py   
接口测试：uvicorn api:app --reload
```

浏览器打开 `http://localhost:8501`，上传 PDF，即可开始提问。

启动 API 服务后，打开 `http://localhost:8000/docs` 可查看并测试接口文档（Swagger UI）。

## 项目说明

本项目是 AI 应用工程学习项目，核心逻辑均为**纯 Python 手写实现**，未使用 LangChain 等框架：文本切割、向量检索、Prompt 构造、问题分类决策、工具调用解析全部手写，目的是深入理解 RAG 与 LLM Agent 的底层原理。

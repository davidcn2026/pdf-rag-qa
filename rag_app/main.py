import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import os
os.environ["HF_HUB_OFFLINE"] = "1"
import streamlit as st
import pdfplumber
from rag_app import splitter, retriever, generator

st.title("PDF 知识库问答")                    # ① 页面标题

# ===== 上传 PDF → 提取 → 切块 → 入库 =====
uploaded = st.file_uploader("上传 PDF", type="pdf")   # ② 上传框，返回文件对象或 None
if uploaded is not None:
    text = ""                                      # 你的任务A：pdfplumber 提取文字

    with pdfplumber.open(uploaded) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    if text.strip():
        chunks = splitter.split_text(text)             # 你的任务B：切块
        retriever.clear()
        retriever.add_documents(chunks)                # 入库
        st.success(f"已入库 {len(chunks)} 个文本块")   # ③ 绿色提示框
    else:
        st.warning("未能从 PDF 中提取到文字，请检查文件是否为文字版 PDF。")

# ===== 提问 → 检索 → 生成 → 显示 =====
question = st.chat_input("对着文档提问")           # ④ 聊天输入框
if question:
    context = retriever.search(question)           # 检索
    answer = generator.generate(question, context) # 生成
    st.write(answer)                               # ⑤ 显示回答
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import os
os.environ["HF_HUB_OFFLINE"] = "1"
import streamlit as st
from rag_app import splitter, retriever, loader, agent

st.title("PDF 知识库问答")                    # ① 页面标题

# ===== 上传 PDF → 提取 → 切块 → 入库 =====
uploaded = st.file_uploader("上传 PDF", type="pdf")   # ② 上传框，返回文件对象或 None
if uploaded is not None:
    if st.session_state.get("current_file") != uploaded.name:
        text = loader.extract_text(uploaded)
        
        if text.strip():
            chunks = splitter.split_text(text)             # 你的任务B：切块
            retriever.clear()
            retriever.add_documents(chunks)                # 入库
            st.session_state["current_file"] = uploaded.name
            st.success(f"已入库 {len(chunks)} 个文本块")   # ③ 绿色提示框
        else:
            st.warning("未能从 PDF 中提取到文字，请检查文件是否为文字版 PDF。")

# ===== 提问 → 调用agent → 显示 =====
question = st.chat_input("对着文档提问")           # ④ 聊天输入框
if question:
    answer = agent.ask_agent(question)              # 生成
    st.write(answer)                               # ⑤ 显示回答
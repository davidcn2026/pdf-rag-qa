import io
import os
os.environ["HF_HUB_OFFLINE"] = "1"          # 必须在 import retriever 之前

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from rag_app import generator, retriever, loader, splitter

history = []
app = FastAPI(title="PDF 知识库问答 API")

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str

class SearchRequest(BaseModel):
    question: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(req: AskRequest):
    global history
    context = retriever.search(req.question)
    answer = generator.generate(req.question, context, history=history)
    history.append({"role": "user", "content": req.question})
    history.append({"role": "assistant", "content": answer})
    history = history[-6:]
    return AskResponse(answer=answer)

@app.post("/search")
def search(req:SearchRequest):
    context = retriever.search(req.question)
    return context

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    content = await file.read()                          # ① 读文件 → bytes
    text = loader.extract_text(io.BytesIO(content))      # ② bytes → file-like → 提取文字
    chunks = splitter.split_text(text)                   # ③ 切块
    retriever.clear()                                    # ④ 清空旧文档
    retriever.add_documents(chunks)                      # ⑤ 新文档入库
    return {"filename": file.filename, "chunks": len(chunks)}


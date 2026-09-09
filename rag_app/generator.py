"""generator.py —— Prompt 构造 + 调用 DeepSeek"""
from openai import OpenAI
from . import config

# ===== 创建客户端（指向 DeepSeek，模块导入时执行一次） =====
_client = OpenAI(
    api_key=config.DEEPSEEK_API_KEY,
    base_url=config.DEEPSEEK_BASE_URL,
)

def generate(question, context_chunks, history=None):
    """输入：问题 + 检索到的文本块；输出：LLM 回答文本"""
    # 任务1：用 join 把 context_chunks 拼成一段 context
    # 任务2：用 f-string 把 context 和 question 填进 prompt 模板（前面讲过的那段模板）
    # 任务3：调 _client.chat.completions.create(...) 拿 response
    # 任务4：return 提取出的 answer
    if history is None:
        history = []    
    context = "\n\n".join(context_chunks)

    if context_chunks:
        prompt = f"""你是一个基于文档内容回答问题的助手。
请严格根据下面提供的【资料】回答问题。
如果资料中没有相关信息，请直接回答"资料中未找到相关内容"，不要编造。
【资料】
{context}
【问题】
{question}"""
    else: 
        prompt = f"""你是一个基于历史对话回答问题的助手,如果历史里有相关约定/信息，要优先基于它回答。
【问题】
{question}"""

    messages=([{"role": "system", "content": "你是回答问题的助手。"}]
                  + history 
                  + [{"role": "user", "content": prompt}]
                  )
    print("history 条数:", len(history))
    print(messages)
    response = _client.chat.completions.create(
        model=config.LLM_MODEL,
        messages=messages,
        temperature=0.0,
    )
    
    # 第 3 步：从 response 里抠出回答文本
    try:
        answer = response.choices[0].message.content
    except (IndexError, AttributeError):
        answer = "生成答案时出错，请稍后重试。"
    return answer

def classify_question(question):
    # 构造分类 prompt（你来填内容）
    prompt = f"""你是问题分类器。
判断下面这个问题：答案应该在用户上传的【文档】里找，还是在【之前的对话】里找。
- 如果是在文档里找答案（如"文档讲了什么"）→ 输出：文档
- 如果是在之前的对话里找答案（如"我们刚才约定了什么"）→ 输出：历史
只输出"文档"或"历史"两个字，不要输出其他内容。
问题：{question}"""
    
    # 调用模型（类似 generate 里的 create）
    response = _client.chat.completions.create(
            model=config.LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )

    try:
        answer = response.choices[0].message.content
    except (IndexError, AttributeError):
        answer = "文档"  
    return answer
    
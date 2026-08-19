"""generator.py —— Prompt 构造 + 调用 DeepSeek"""
from openai import OpenAI
from . import config

# ===== 创建客户端（指向 DeepSeek，模块导入时执行一次） =====
_client = OpenAI(
    api_key=config.DEEPSEEK_API_KEY,
    base_url=config.DEEPSEEK_BASE_URL,
)

def generate(question, context_chunks):
    """输入：问题 + 检索到的文本块；输出：LLM 回答文本"""
    # 任务1：用 join 把 context_chunks 拼成一段 context
    # 任务2：用 f-string 把 context 和 question 填进 prompt 模板（前面讲过的那段模板）
    # 任务3：调 _client.chat.completions.create(...) 拿 response
    # 任务4：return 提取出的 answer
    context = "\n\n".join(context_chunks)
    prompt = f"""你是一个基于文档内容回答问题的助手。
请严格根据下面提供的【资料】回答问题。
如果资料中没有相关信息，请直接回答"资料中未找到相关内容"，不要编造。
【资料】
{context}
【问题】
{question}"""
    response = _client.chat.completions.create(
        model=config.LLM_MODEL,                 # "deepseek-chat"
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )

    # 第 3 步：从 response 里抠出回答文本
    try:
        answer = response.choices[0].message.content
    except (IndexError, AttributeError):
        answer = "生成答案时出错，请稍后重试。"
    return answer


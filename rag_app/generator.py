"""generator.py —— Prompt 构造 + 调用 DeepSeek"""
from openai import OpenAI
from . import config
import json


# ===== 创建客户端（指向 DeepSeek，模块导入时执行一次） =====
_client = OpenAI(
    api_key=config.DEEPSEEK_API_KEY,
    base_url=config.DEEPSEEK_BASE_URL,
)

def generate(question:str, context_chunks:list, history=None) -> str:
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
        
    response = _client.chat.completions.create(
        model=config.LLM_MODEL,
        messages=([{"role": "system", "content": "你是回答问题的助手。"}]
                  + history 
                  + [{"role": "user", "content": prompt}]
                  ),
        temperature=0.0,
    )
    
    # 第 3 步：从 response 里抠出回答文本
    try:
        answer = response.choices[0].message.content
    except (IndexError, AttributeError):
        answer = "生成答案时出错，请稍后重试。"
    return answer

def classify_question(question:str) -> str:
    # 构造分类 prompt
    prompt = f"""你是问题分类器。
判断下面这个问题：答案应该在用户上传的【文档】里找，还是在【历史记录】里找。
- 如果是在文档里找答案（如"文档讲了什么"）→ 输出：文档
- 如果是在之前的对话里找答案（如"我们刚才约定了什么"）→ 输出：历史
- 如果出现3 + 4 * 2 = ?, 3乘以4等于几, 这种计算符号或中文数学表达式，最终输出为一个值，则输出：计算
只输出"文档"或"历史"或"计算"三个，不要输出其他内容。
问题：{question}"""
    
    # 调用模型
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

def get_tool_call(question:str) -> dict:
    """接收一个包含数学表达式的字符串，返回对应的工具和表达式"""
    prompt = f"""你是选择工具的助手。
你收到一个问题，问题中包含使用符号或中文组成的数学表达式，你需要把他提取成数字符号输出 JSON 字符串。
{{"tool": "calculate", "args": <表达式>}}
问题{question}"""

    response = _client.chat.completions.create(
                model=config.LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
            )

    try:
        text = response.choices[0].message.content 
        parsed = json.loads(text)
        return parsed 
    except (json.JSONDecodeError):
        return {"tool": None, "args": None}
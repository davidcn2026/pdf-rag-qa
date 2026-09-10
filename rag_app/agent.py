"""agent.py —— Agent 编排层：统一问答入口 + 共享对话状态"""
from . import generator, retriever, tools

# 全局共享的对话历史（进程内唯一一份）
history = []

def ask_agent(question):
    """统一问答入口：分类 → 分流 → 生成 → 记账，返回 answer"""
    category = generator.classify_question(question)

    if category == "文档":
        context = retriever.search(question)
        answer = generator.generate(question, context, history=history)
    elif category == "历史":
        answer = generator.generate(question, [], history=history)
    elif category == "计算":
        instruction = generator.get_tool_call(question)
        if instruction["tool"] == "calculate":
            result = tools.calculate(instruction["args"])
            answer = f"{instruction['args']} = {result}"
        else:
            answer = "抱歉，我没能理解这个计算式，请换一种说法。"
    else:
        answer = "抱歉，我不太确定该如何回答这个问题。"

    history.append({"role": "user", "content": question})
    history.append({"role": "assistant", "content": answer})
    history[:] = history[-6:]
    return answer
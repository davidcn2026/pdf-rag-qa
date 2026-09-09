def calculate(expression) -> str:
    """计算数学表达式，返回结果字符串"""
    result = eval(expression)
    return str(result)
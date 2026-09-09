import ast

ALLOWED = (ast.Expression, ast.BinOp, ast.UnaryOp,
           ast.Constant, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub)

def calculate(expression) -> str:
    """计算数学表达式，返回结果字符串"""

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError:
        return "表达式包含不支持的运算"   # 解析都失败，直接拒绝
    
    for node in ast.walk(tree):
        if not isinstance(node, ALLOWED):
            # 出现不允许的东西，拒绝
            return "表达式包含不支持的运算"
        
    try:
        result = eval(expression)
        return str(result)
    except ZeroDivisionError:
        return "除数不能为 0"
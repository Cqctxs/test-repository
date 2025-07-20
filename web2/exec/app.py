import ast
from flask import Flask, request, abort

app = Flask(__name__)

def safe_eval(expr):
    """
    Safely evaluate simple arithmetic expressions.
    Only allows numbers and arithmetic operators.
    """
    try:
        node = ast.parse(expr, mode='eval')
    except SyntaxError:
        abort(400, 'Invalid syntax')

    for n in ast.walk(node):
        # Only allow literal numbers and arithmetic operations
        if not isinstance(n, (ast.Expression, ast.BinOp, ast.UnaryOp,
                              ast.Num, ast.Constant,
                              ast.operator, ast.unaryop)):
            abort(400, 'Disallowed expression')
    # Evaluate without builtins to prevent code injection
    return eval(compile(node, '<string>', 'eval'), {'__builtins__': None}, {})

@app.route('/run_code', methods=['POST'])
def run_code():
    code = request.form.get('code', '')
    result = safe_eval(code)
    return str(result)

if __name__ == '__main__':
    app.run()
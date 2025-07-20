import ast
import traceback

# Only allow arithmetic expressions and simple Python operations
def safe_eval(expr):
    # Parse expression to AST
    tree = ast.parse(expr, mode='eval')
    # Define allowed node types
    allowed_nodes = {
        ast.Expression, ast.BinOp, ast.UnaryOp,
        ast.Num, ast.Load, ast.Add, ast.Sub,
        ast.Mult, ast.Div, ast.Pow, ast.Mod,
        ast.UAdd, ast.USub, ast.Tuple, ast.List,
    }
    for node in ast.walk(tree):
        if type(node) not in allowed_nodes:
            raise ValueError(f"Disallowed expression: {type(node).__name__}")
    return eval(compile(tree, '<string>', 'eval'))

from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json() or {}
    expr = data.get('expression', '')
    try:
        result = safe_eval(expr)
        return jsonify({'result': result})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'Invalid expression'}), 400

if __name__ == '__main__':
    app.run()

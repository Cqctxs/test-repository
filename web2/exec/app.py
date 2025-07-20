# web2/exec/app.py
import ast
from flask import Flask, request, jsonify

app = Flask(__name__)

# Only allow safe arithmetic expressions
ALLOWED_NODE_TYPES = {
    ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow,
    ast.USub, ast.UAdd, ast.Mod, ast.FloorDiv
}

def is_safe_ast(node):
    if type(node) not in ALLOWED_NODE_TYPES:
        return False
    for child in ast.iter_child_nodes(node):
        if not is_safe_ast(child):
            return False
    return True

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.get_json(force=True)
    expr = data.get('expression', '')
    try:
        # Parse expression into AST
        parsed = ast.parse(expr, mode='eval')
        # Validate AST nodes against allowlist
        if not is_safe_ast(parsed):
            return jsonify({'error': 'Disallowed expression'}), 400
        # Evaluate safely
        result = eval(compile(parsed, filename='<ast>', mode='eval'), {'__builtins__': {}})
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=False)

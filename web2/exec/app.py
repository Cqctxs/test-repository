import ast
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# Whitelist of allowed AST node types for safe arithmetic evaluation
ALLOWED_NODES = {
    ast.Expression, ast.BinOp, ast.UnaryOp,
    ast.Num, ast.Constant,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
    ast.UAdd, ast.USub,
    ast.Load, ast.FloorDiv
}

def secure_eval(expr):
    """
    Safely evaluate user-supplied arithmetic expressions by parsing the AST
    and allowing only whitelisted node types.
    """
    try:
        node = ast.parse(expr, mode='eval')
    except SyntaxError:
        abort(400, 'Invalid syntax')
    for sub in ast.walk(node):
        if type(sub) not in ALLOWED_NODES:
            abort(400, f'Unsupported expression element: {type(sub).__name__}')
    # Evaluate in empty context, no builtins
    return eval(compile(node, '<secure>', 'eval'), {}, {})

@app.route('/run', methods=['POST'])
def run_code():
    code = request.form.get('code', '')
    result = secure_eval(code)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=False)

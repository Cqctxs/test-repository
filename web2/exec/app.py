import ast
import operator
from flask import Flask, request, jsonify

app = Flask(__name__)

# Whitelist of supported binary operators
_allowed_operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod
}

def _eval(node):
    """
    Recursively evaluate an AST node, only allowing numeric literals and safe binary operations.
    """
    if isinstance(node, ast.Num):
        return node.n
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type in _allowed_operators:
            left = _eval(node.left)
            right = _eval(node.right)
            return _allowed_operators[op_type](left, right)
    raise ValueError("Unsupported expression")

@app.route('/execute', methods=['POST'])
def execute():
    data = request.get_json() or {}
    expr = data.get('expression', '')
    try:
        # Parse expression in 'eval' mode to get a single expression AST
        node = ast.parse(expr, mode='eval').body
        result = _eval(node)
        return jsonify({'result': result})
    except Exception:
        # Return a generic error without exposing internal details
        return jsonify({'error': 'Invalid or unsafe expression'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
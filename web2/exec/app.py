import ast
import operator
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define supported operators for safe evaluation
a_allowed_operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

def safe_eval(node):
    """
    Recursively evaluate an AST containing only numbers and allowed operators.
    """
    if isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.BinOp):
        left = safe_eval(node.left)
        right = safe_eval(node.right)
        op_type = type(node.op)
        if op_type in a_allowed_operators:
            return a_allowed_operators[op_type](left, right)
    raise ValueError("Unsupported expression")

@app.route('/eval', methods=['POST'])
def evaluate():
    data = request.json or {}
    expr = data.get('expr', '')
    try:
        # Parse expression to AST and evaluate safely
        tree = ast.parse(expr, mode='eval')
        result = safe_eval(tree.body)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': 'Invalid expression'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

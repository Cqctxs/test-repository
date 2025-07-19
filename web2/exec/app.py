import ast
import operator
from flask import Flask, request, jsonify

app = Flask(__name__)

# Allowed operators for safe expression evaluation
enabled_operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg
}

def safe_eval(node):
    """
    Recursively evaluate an AST node, only allowing basic math operations and numbers.
    """
    if isinstance(node, ast.Num):  # <number>
        return node.n
    elif isinstance(node, ast.BinOp):  # <left> <op> <right>
        op = type(node.op)
        if op in enabled_operators:
            return enabled_operators[op](safe_eval(node.left), safe_eval(node.right))
    elif isinstance(node, ast.UnaryOp):  # -<operand>
        op = type(node.op)
        if op in enabled_operators:
            return enabled_operators[op](safe_eval(node.operand))
    raise ValueError("Unsupported expression")

@app.route('/eval', methods=['POST'])
def evaluate_expression():
    data = request.get_json()
    expr = data.get('expression', '')
    try:
        # Parse expression into AST and evaluate safely
        tree = ast.parse(expr, mode='eval')
        result = safe_eval(tree.body)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': 'Invalid or unsupported expression'}), 400

if __name__ == '__main__':
    app.run(debug=False)

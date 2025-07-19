from flask import Flask, request, jsonify
import ast
import operator as op

app = Flask(__name__)

# allowed operators for safe eval
ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg
}

def safe_eval(expr):
    """Safely evaluate a math expression using AST, disallowing any code execution."""
    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            operator = ALLOWED_OPERATORS[type(node.op)]
            return operator(left, right)
        if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            operator = ALLOWED_OPERATORS[type(node.op)]
            return operator(operand)
        raise ValueError(f"Unsupported expression: {node}")
    node = ast.parse(expr, mode='eval').body
    return _eval(node)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json() or {}
    expr = data.get('expression', '')
    try:
        # Validate input: must match allowed pattern
        if not isinstance(expr, str) or not expr.replace(' ', '').replace('.', '').replace('+','').replace('-','').replace('*','').replace('/','').isalnum():
            raise ValueError("Invalid characters in expression")
        result = safe_eval(expr)
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=False)

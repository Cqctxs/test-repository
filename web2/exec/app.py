import ast
import operator as op
from flask import Flask, request, jsonify

app = Flask(__name__)

# Supported operators map for arithmetic expressions
operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg
}

def safe_eval(expr):
    """
    Safely evaluate arithmetic expressions using AST
    """
    def _eval(node):
        if isinstance(node, ast.Num):  # <number>
            return node.n
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in operators:
                raise ValueError("Operator not allowed")
            return operators[type(node.op)](_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in operators:
                raise ValueError("Operator not allowed")
            return operators[type(node.op)](_eval(node.operand))
        else:
            raise ValueError("Expression not allowed")
    parsed = ast.parse(expr, mode='eval')
    return _eval(parsed.body)

@app.route('/exec', methods=['POST'])
def exec_code():
    code = request.form.get('code', '')
    # Reject overly long input to avoid DoS via huge AST
    if len(code) > 100:
        return jsonify({"error": "Expression too long"}), 400
    try:
        result = safe_eval(code)
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run()
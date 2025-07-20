from flask import Flask, request, jsonify
import ast
import operator as op

app = Flask(__name__)

# Supported operators for safe evaluation
eval_ops = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.BitXor: op.xor,
    ast.USub: op.neg,
}

def safe_eval(expr):
    """
    Safely evaluate a mathematical expression node-by-node.
    Raises ValueError on any disallowed operation.
    """
    node = ast.parse(expr, mode='eval').body
    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in eval_ops:
                raise ValueError('Operator not supported')
            return eval_ops[type(node.op)](_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp) and type(node.op) in eval_ops:
            return eval_ops[type(node.op)](_eval(node.operand))
        else:
            raise ValueError('Expression not allowed')
    return _eval(node)

@app.route('/compute', methods=['POST'])
def compute():
    data = request.get_json()
    expr = data.get('expr', '')
    try:
        # Safely evaluate only mathematical expressions
        result = safe_eval(expr)
        return jsonify({'result': result}), 200
    except (SyntaxError, ValueError) as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=False)
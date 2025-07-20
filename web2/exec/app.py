# web2/exec/app.py
from flask import Flask, request, jsonify
import ast
import operator as op

app = Flask(__name__)

# supported operators for safe eval
a_allowed_operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg
}

def safe_eval(expr):
    '''Safely evaluate arithmetic expressions only.'''
    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in a_allowed_operators:
                return a_allowed_operators[op_type](left, right)
            raise ValueError('Unsupported operator: {}'.format(op_type))
        if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type in a_allowed_operators:
                return a_allowed_operators[op_type](operand)
            raise ValueError('Unsupported unary operator: {}'.format(op_type))
        raise ValueError('Unsupported expression type: {}'.format(type(node)))
    parsed = ast.parse(expr, mode='eval')
    return _eval(parsed.body)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json(force=True)
    expr = data.get('expression', '')
    try:
        result = safe_eval(expr)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=False)

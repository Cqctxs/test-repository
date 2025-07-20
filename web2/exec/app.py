from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

def safe_eval(expr: str) -> float:
    """
    Safely evaluate arithmetic expressions only.
    Disallow any names, attribute access, function calls, or imports.
    """
    node = ast.parse(expr, mode='eval')
    for n in ast.walk(node):
        # Only allow literal numbers and arithmetic operators
        if not isinstance(n, (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.operator, ast.unaryop)):
            raise ValueError("Unsupported operation or malicious code detected")
    return eval(compile(node, '<safe>', 'eval'))

@app.route('/execute', methods=['POST'])
def execute():
    code = request.form.get('code', '')
    try:
        result = safe_eval(code)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

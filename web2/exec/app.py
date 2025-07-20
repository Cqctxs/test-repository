from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

# Only allow numeric operations: no exec/eval of arbitrary code
def safe_eval(expr):
    # Parse expression into AST
    try:
        node = ast.parse(expr, mode='eval')
    except SyntaxError:
        raise ValueError("Invalid expression syntax")
    # Walk AST and ensure only safe nodes
    for sub in ast.walk(node):
        if not isinstance(sub, (ast.Expression, ast.BinOp, ast.UnaryOp,
                                ast.Num, ast.Constant, ast.operator,
                                ast.unaryop)):
            raise ValueError(f"Disallowed syntax: {type(sub).__name__}")
    # Compile and evaluate in empty namespace
    return eval(compile(node, '<safe>', 'eval'), {})

@app.route('/execute', methods=['POST'])
def execute_code():
    code = request.form.get('code', '')
    try:
        result = safe_eval(code)
        return jsonify({ 'result': result })
    except ValueError as e:
        return jsonify({ 'error': str(e) }), 400
    except Exception as e:
        return jsonify({ 'error': 'Evaluation error' }), 400

if __name__ == '__main__':
    app.run(debug=False)
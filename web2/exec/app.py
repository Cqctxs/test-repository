from flask import Flask, request, jsonify, abort
import ast

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_user_code():
    # Validate presence of 'expression' and ensure only safe literal expressions
    user_input = request.form.get('expression')
    if not user_input:
        abort(400, description="Missing 'expression' parameter")
    try:
        # Parse and evaluate only Python literals (numbers, strings, lists, dicts)
        tree = ast.parse(user_input, mode='eval')
        # Walk AST to ensure no disallowed nodes
        for node in ast.walk(tree):
            if not isinstance(node, (ast.Expression, ast.Num, ast.Str, ast.Tuple,
                                     ast.List, ast.Dict, ast.Set, ast.UnaryOp,
                                     ast.BinOp, ast.BoolOp, ast.Compare, ast.NameConstant,
                                     ast.Load)):
                abort(400, description="Unsafe expression detected")
        result = ast.literal_eval(tree)
    except Exception as e:
        abort(400, description=f"Invalid expression: {e}")
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=False)

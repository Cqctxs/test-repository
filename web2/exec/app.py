from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

# Define which AST nodes are allowed for safe evaluation
def is_safe_node(tree):
    allowed_nodes = (
        ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Str,
        ast.Constant, ast.Name, ast.Load, ast.operator, ast.unaryop,
        ast.Compare, ast.BoolOp
    )
    for node in ast.walk(tree):
        if not isinstance(node, allowed_nodes):
            return False
    return True

@app.route('/run', methods=['POST'])
def run():
    code = request.form.get('code', '')
    try:
        # Parse user code in 'eval' mode, not 'exec'
        tree = ast.parse(code, mode='eval')
        if not is_safe_node(tree):
            return jsonify({'error': 'Unsafe code detected'}), 400
        # Compile and evaluate with no builtins and empty globals
        result = eval(
            compile(tree, filename='<ast>', mode='eval'),
            {'__builtins__': {}},
            {}
        )
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=False)
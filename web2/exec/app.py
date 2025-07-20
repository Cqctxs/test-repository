from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

# Whitelist of allowed operations
ALLOWED_AST_NODES = {
    ast.Expression, ast.BinOp, ast.UnaryOp,
    ast.Num, ast.Load,
    ast.Add, ast.Sub, ast.Mult, ast.Div,
    ast.Pow, ast.Mod, ast.USub, ast.UAdd,
    ast.Call, ast.Name
}

# Only allow math functions
env = { 'abs': abs, 'round': round }

class SafeEval(ast.NodeVisitor):
    def generic_visit(self, node):
        if type(node) not in ALLOWED_AST_NODES:
            raise ValueError(f"Disallowed expression: {type(node).__name__}")
        super().generic_visit(node)

@app.route('/compute', methods=['POST'])
def compute():
    expression = request.json.get('expr', '')
    try:
        # Parse to AST and validate
        tree = ast.parse(expression, mode='eval')
        SafeEval().visit(tree)
        # Compile and evaluate with restricted env
        code = compile(tree, '<string>', 'eval')
        result = eval(code, {'__builtins__': {}}, env)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()
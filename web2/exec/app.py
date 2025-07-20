import ast
import sys

from flask import Flask, request, jsonify

app = Flask(__name__)

# Whitelisted operations: define a safe AST visitor that only allows literal math expressions
def safe_eval(expr):
    # Parse expression into AST
    tree = ast.parse(expr, mode='eval')

    class SafeVisitor(ast.NodeVisitor):
        ALLOWED_NODES = (ast.Expression, ast.BinOp, ast.UnaryOp,
                         ast.Add, ast.Sub, ast.Mult, ast.Div,
                         ast.Pow, ast.Num, ast.Load, ast.USub, ast.UAdd)

        def generic_visit(self, node):
            if not isinstance(node, self.ALLOWED_NODES):
                raise ValueError(f"Disallowed expression: {type(node).__name__}")
            super().generic_visit(node)

    SafeVisitor().visit(tree)
    return eval(compile(tree, filename="<safe_eval>", mode="eval"))

@app.route('/calculate', methods=['POST'])
def calculate():
    expression = request.json.get('expr', '')
    try:
        result = safe_eval(expression)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()
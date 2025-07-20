import os
from flask import Flask, request, jsonify, abort
import ast

app = Flask(__name__)
# Load a token from environment to authenticate authorized users
AUTH_TOKEN = os.getenv("EXEC_APP_AUTH_TOKEN")
if not AUTH_TOKEN:
    raise RuntimeError("EXEC_APP_AUTH_TOKEN must be set in environment")

class SafeEval(ast.NodeVisitor):
    """AST visitor that only allows basic arithmetic expressions."""
    allowed_nodes = {
        ast.Expression, ast.BinOp, ast.UnaryOp,
        ast.Num, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow,
        ast.USub, ast.UAdd, ast.Load, ast.Call, ast.Name
    }
    safe_names = {}  # no names allowed currently

    def generic_visit(self, node):
        if type(node) not in self.allowed_nodes:
            raise ValueError(f"Unsafe expression: {type(node).__name__}")
        super().generic_visit(node)

    def visit_Call(self, node):
        # disallow any function calls
        raise ValueError("Function calls are not allowed in expressions")


def safe_eval(expr: str) -> float:
    """Parse and evaluate a numeric expression safely."""
    parsed = ast.parse(expr, mode="eval")
    SafeEval().visit(parsed)
    return eval(compile(parsed, filename="<safe>", mode="eval"), { }, { })

@app.route('/execute', methods=['POST'])
def execute():
    # Authentication: require a pre-shared token header
    token = request.headers.get('X-Auth-Token')
    if token != AUTH_TOKEN:
        abort(401, description="Unauthorized")

    code = request.form.get('code', '').strip()
    if not code:
        return jsonify({"error": "No code provided"}), 400
    try:
        result = safe_eval(code)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Invalid expression"}), 400

    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
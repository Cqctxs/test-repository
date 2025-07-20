from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.get_json()
    expression = data.get('expression')
    # Input validation: only allow arithmetic expressions
    if not isinstance(expression, str) or not expression:
        return jsonify({'error': 'Invalid input'}), 400
    try:
        # Parse the expression into an AST node
        node = ast.parse(expression, mode='eval')
        # Whitelist allowed node types
        for sub in ast.walk(node):
            if not isinstance(sub, (ast.Expression, ast.BinOp, ast.UnaryOp,
                                      ast.Num, ast.Add, ast.Sub, ast.Mult,
                                      ast.Div, ast.Pow, ast.Mod, ast.USub, ast.UAdd,
                                      ast.Load, ast.Constant)):
                raise ValueError('Disallowed expression')
        # Safe evaluation
        result = eval(compile(node, '<string>', 'eval'), {'__builtins__': {}})
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()
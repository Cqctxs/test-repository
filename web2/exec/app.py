from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

# Only allow evaluation of safe literal expressions, not arbitrary code
def safe_eval(expr):
    try:
        # ast.literal_eval only evaluates literals (strings, numbers, tuples, lists, dicts, booleans, None)
        return ast.literal_eval(expr)
    except (ValueError, SyntaxError):
        raise ValueError("Invalid expression: only literals are allowed")

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.get_json()
    if not data or 'expr' not in data:
        return jsonify({'error': 'Missing expr parameter'}), 400

    expr = data['expr']
    try:
        # Use safe_eval instead of exec to prevent arbitrary code execution
        result = safe_eval(expr)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=False)

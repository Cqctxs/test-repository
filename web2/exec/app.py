import ast
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

@app.route('/exec', methods=['POST'])
def execute():
    code = request.form.get('code')
    if not code:
        abort(400, description="Missing 'code' parameter")
    try:
        # Only allow expressions, no statements
        node = ast.parse(code, mode='eval')
        # Compile and evaluate in a restricted environment
        safe_globals = {'__builtins__': None}
        result = eval(compile(node, '<string>', 'eval'), safe_globals, {})
        return jsonify({'result': result})
    except Exception as e:
        # On any parse/eval error, return 400
        abort(400, description=f"Invalid code: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
from flask import Flask, request, abort, jsonify
import ast

app = Flask(__name__)

# Define allowed AST nodes for safety
SAFE_NODES = {
    'Expression', 'BinOp', 'UnaryOp', 'Num', 'Str', 'List', 'Tuple',
    'Dict', 'NameConstant', 'Load', 'Call', 'Name'
}

# Whitelist of safe functions (if any needed)
SAFE_FUNCTIONS = {
    'abs': abs,
    'sum': sum,
    'min': min,
    'max': max
}

def is_node_safe(node):
    node_name = type(node).__name__
    if node_name not in SAFE_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not is_node_safe(child):
            return False
    return True

@app.route('/execute', methods=['POST'])
def execute_code():
    user_code = request.json.get('code')
    if not isinstance(user_code, str) or len(user_code) > 200:
        # Reject code that is too long or not a string
        abort(400, 'Invalid code submission')
    try:
        # Parse user code to AST
        parsed = ast.parse(user_code, mode='eval')
        if not is_node_safe(parsed):
            abort(400, 'Disallowed code constructs')
        # Compile and evaluate safely
        compiled = compile(parsed, '<string>', 'eval')
        result = eval(compiled, {'__builtins__': {}}, SAFE_FUNCTIONS)
        return jsonify({'result': result})
    except Exception as e:
        abort(400, f'Error evaluating code: {str(e)}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
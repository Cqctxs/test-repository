from flask import Flask, request, jsonify

app = Flask(__name__)

# Define a safe evaluation environment
SAFE_GLOBALS = {
    '__builtins__': {},
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    # add other allowed functions here
}

@app.route('/compute', methods=['POST'])
def compute():
    data = request.get_json(force=True)
    expression = data.get('expr', '')
    # Input validation: only allow digits, operators, and parentheses
    import re
    if not re.fullmatch(r'[0-9+\-*/(). ]+', expression):
        return jsonify({'error': 'Invalid characters in expression'}), 400
    try:
        # Evaluate expression safely without exec
        result = eval(expression, SAFE_GLOBALS, {})
    except Exception as e:
        return jsonify({'error': 'Evaluation error', 'message': str(e)}), 400
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

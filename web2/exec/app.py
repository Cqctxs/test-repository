# web2/exec/app.py - Secure version without exec
from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

# Allowed operations mapping
def add(a, b): return a + b
def sub(a, b): return a - b
def mul(a, b): return a * b
def div(a, b): return a / b if b != 0 else None

OPERATIONS = {
    'add': add,
    'sub': sub,
    'mul': mul,
    'div': div
}

@app.route('/compute', methods=['POST'])
def compute():
    data = request.get_json()
    # Input validation
    op = data.get('operation')
    a = data.get('a')
    b = data.get('b')

    if op not in OPERATIONS:
        return jsonify({'error': 'Invalid operation'}), 400

    # Ensure a and b are numbers
    try:
        a = float(a)
        b = float(b)
    except (TypeError, ValueError):
        return jsonify({'error': 'Operands must be numeric'}), 400

    result = OPERATIONS[op](a, b)
    if result is None:
        return jsonify({'error': 'Division by zero'}), 400

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=False)
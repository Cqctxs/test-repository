# web3/param/app.py
import os
import subprocess
from flask import Flask, request, jsonify, abort, session
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'change-me')

# Simple session-based authentication
USERS = {'alice': 'password123'}  # Replace with real user store and hashed passwords
BALANCES = {'alice': 1000}

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    user = data.get('username')
    pwd = data.get('password')
    # TODO: use hashed password check (bcrypt)
    if USERS.get(user) == pwd:
        session['user'] = user
        return jsonify({'message': 'Logged in'}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/transfer', methods=['POST'])
@login_required
def transfer():
    data = request.get_json(force=True)
    to = data.get('to')
    amount = data.get('amount')
    # Validate inputs
    if not isinstance(to, str) or not isinstance(amount, (int, float)):
        return jsonify({'error': 'Invalid input types'}), 400
    if amount <= 0:
        return jsonify({'error': 'Transfer amount must be positive'}), 400
    sender = session['user']
    if BALANCES.get(sender, 0) < amount:
        return jsonify({'error': 'Insufficient funds'}), 400
    # Perform transfer logic
    BALANCES[sender] -= amount
    BALANCES[to] = BALANCES.get(to, 0) + amount
    # Call external PHP gateway safely without shell
    subprocess.run([
        'php', 'gateway.php',
        '--from', sender,
        '--to', to,
        '--amount', str(amount)
    ], check=True)
    return jsonify({'message': 'Transfer successful'}), 200

if __name__ == '__main__':
    app.run(debug=False)

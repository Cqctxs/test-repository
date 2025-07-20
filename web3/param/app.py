from flask import Flask, request, jsonify, abort, sessionrom functools import wraps
import re

app = Flask(__name__)
app.secret_key = 'replace_with_env_secret'

# Dummy user store for demonstration
USERS = {'alice': {'password': 'hashed_pw', 'balance': 1000}}

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            abort(401, description='Authentication required')
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    # Validate input
    if not username or not password or not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        abort(400, 'Invalid credentials format')
    user = USERS.get(username)
    # TODO: verify hashed password instead of plain compare
    if user and password == 'plaintext_pw':
        session['user'] = username
        return jsonify({'message':'Logged in'})
    abort(401, 'Invalid username or password')

@app.route('/transfer', methods=['POST'])
@login_required
def transfer():
    from_user = session['user']
    to_user = request.json.get('to')
    amount = request.json.get('amount')
    # Input validation
    if to_user not in USERS or not isinstance(amount, (int, float)) or amount <= 0:
        abort(400, 'Invalid transfer parameters')
    if USERS[from_user]['balance'] < amount:
        abort(400, 'Insufficient funds')
    # Perform transfer
    USERS[from_user]['balance'] -= amount
    USERS[to_user]['balance'] += amount
    return jsonify({'message':'Transfer successful','balances':{from_user: USERS[from_user]['balance'], to_user: USERS[to_user]['balance']}})

if __name__ == '__main__':
    app.run(debug=False)

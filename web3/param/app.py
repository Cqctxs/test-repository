from flask import Flask, request, jsonify, session, redirect, url_for
from functools import wraps
import hashlib

app = Flask(__name__)
app.secret_key = 'replace_with_strong_secret'
# Stub in-memory user store and balances
USERS = {'alice': hashlib.sha256(b'alicepass').hexdigest()}
BALANCES = {'alice': 1000}
FLAG = 'FLAG{secret}'

# Authentication decorator
def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'username' not in session:
            return jsonify({'error':'Authentication required'}), 401
        return f(*args, **kwargs)
    return wrapped

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = data.get('username')
    pw = data.get('password','').encode()
    if user in USERS and hashlib.sha256(pw).hexdigest() == USERS[user]:
        session['username'] = user
        return jsonify({'message':'Logged in'}), 200
    return jsonify({'error':'Invalid credentials'}), 403

@app.route('/balance', methods=['GET'])
@login_required
def balance():
    user = session['username']
    return jsonify({'balance': BALANCES.get(user,0)}), 200

@app.route('/transfer', methods=['POST'])
@login_required
def transfer():
    data = request.get_json()
    to_user = data.get('to')
    amount = data.get('amount')
    from_user = session['username']
    # Input validation
    if to_user not in USERS:
        return jsonify({'error':'Recipient not found'}), 400
    try:
        amt = float(amount)
    except ValueError:
        return jsonify({'error':'Invalid amount'}), 400
    if amt <= 0 or BALANCES[from_user] < amt:
        return jsonify({'error':'Insufficient funds'}), 400
    BALANCES[from_user] -= amt
    BALANCES[to_user] = BALANCES.get(to_user,0) + amt
    return jsonify({'message':'Transfer complete'}), 200

@app.route('/flag', methods=['GET'])
@login_required
def get_flag():
    # Only allow if user balance exceeds threshold
    if BALANCES[session['username']] >= 10000:
        return jsonify({'flag': FLAG}), 200
    return jsonify({'error':'Not authorized to view flag'}), 403

if __name__ == '__main__':
    app.run(debug=False)
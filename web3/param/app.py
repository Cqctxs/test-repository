from flask import Flask, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import re

app = Flask(__name__)
app.secret_key = 'REPLACE_WITH_SECURE_RANDOM_KEY'

DATABASE = 'bank.db'

# Simple DB helper
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Authentication routes
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    if user and check_password_hash(user['password_hash'], password):
        session['user_id'] = user['id']
        session['is_admin'] = bool(user['is_admin'])
        return redirect(url_for('dashboard'))
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Decorator to enforce login
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated

# Dashboard placeholder
@app.route('/dashboard')
@login_required
def dashboard():
    return jsonify({'message': 'Welcome!'}), 200

# Money transfer endpoint
@app.route('/transfer', methods=['POST'])
@login_required
def transfer():
    data = request.get_json() or {}
    to_account = data.get('to_account')
    amount = data.get('amount')
    # Validate amount and account
    if not re.fullmatch(r"\d+", str(to_account)) or not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({'error': 'Invalid input'}), 400
    user_id = session['user_id']
    conn = get_db()
    sender = conn.execute('SELECT balance FROM accounts WHERE user_id = ?', (user_id,)).fetchone()
    receiver = conn.execute('SELECT balance FROM accounts WHERE user_id = ?', (to_account,)).fetchone()
    if not receiver:
        return jsonify({'error': 'Recipient not found'}), 404
    if sender['balance'] < amount:
        return jsonify({'error': 'Insufficient funds'}), 400
    # Perform transfer within a transaction
    conn.execute('BEGIN')
    conn.execute('UPDATE accounts SET balance = balance - ? WHERE user_id = ?', (amount, user_id))
    conn.execute('UPDATE accounts SET balance = balance + ? WHERE user_id = ?', (amount, to_account))
    conn.commit()
    return jsonify({'status': 'success'}), 200

# Flag endpoint - admin only
@app.route('/flag')
@login_required
def get_flag():
    if not session.get('is_admin'):
        return jsonify({'error': 'Forbidden'}), 403
    # The flag is stored securely on the server side or in env
    import os
    flag = os.getenv('APP_FLAG', 'FLAG_NOT_SET')
    return jsonify({'flag': flag}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
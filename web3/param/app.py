import os
import re
from decimal import Decimal
from flask import Flask, request, session, redirect, abort, url_for
import requests

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'REPLACE_WITH_SECURE_KEY')

# Simple login_required decorator
from functools import wraps
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # TODO: replace with real authentication and secure credential store
        if authenticate(username, password):
            session['user'] = username
            return redirect(url_for('send_money'))
        abort(401, 'Invalid credentials')
    return '''
    <form method="post">
      <input name="username"/>
      <input name="password" type="password"/>
      <input type="submit"/>
    </form>
    '''

@app.route('/send', methods=['POST'])
@login_required
def send_money():
    from_acc = request.form.get('from')
    to_acc = request.form.get('to')
    amount_str = request.form.get('amount')

    # Validate account format
    if not re.fullmatch(r'\d+', from_acc) or not re.fullmatch(r'\d+', to_acc):
        abort(400, 'Invalid account format')
    # Ensure user owns the account
    if session['user'] != from_acc:
        abort(403, 'Cannot send from this account')
    # Validate amount
    try:
        amount = Decimal(amount_str)
    except:
        abort(400, 'Invalid amount')
    if amount <= 0:
        abort(400, 'Amount must be positive')

    # Securely call PHP backend with JSON and auth header
    payload = {'from': from_acc, 'to': to_acc, 'amount': str(amount)}
    headers = {'Authorization': f"Bearer {os.environ.get('BACKEND_TOKEN')}"}
    resp = requests.post(
        'https://backend.example.com/transfer.php',
        json=payload,
        headers=headers,
        timeout=5
    )
    resp.raise_for_status()
    return resp.text

if __name__ == '__main__':
    app.run()
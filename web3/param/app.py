import os
import subprocess
from flask import Flask, request, session, redirect, abort
import requests

app = Flask(__name__)
app.secret_key = 'replace-with-secure-key'

@app.route('/transfer', methods=['POST'])
def transfer():
    # Authorization check
    if 'user_id' not in session:
        abort(401)
    data = request.get_json()
    acct = data.get('account')
    amt  = data.get('amount')
    # Input validation
    if not isinstance(acct, str) or not acct.isalnum():
        abort(400)
    if not isinstance(amt, (int, float)) or amt <= 0:
        abort(400)
    # Call PHP gateway via HTTP instead of os.system
    try:
        resp = requests.post(
            'https://gateway.example.com/transfer',
            json={'from': session['user_id'], 'to': acct, 'amount': amt},
            timeout=5,
            headers={'Authorization': 'Bearer ' + session.get('api_token','')}
        )
        resp.raise_for_status()
    except Exception:
        abort(502)
    return resp.text

@app.route('/login', methods=['POST'])
def login():
    # Dummy login for demonstration
    session['user_id'] = request.form['username']
    session['api_token'] = 'fetch-token-from-auth-service'
    return redirect('/')
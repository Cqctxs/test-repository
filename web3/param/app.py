import os
from decimal import Decimal, InvalidOperation
from flask import Flask, request, session, jsonify
import requests

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'replace_with_real_secret')
GATEWAY_URL = os.getenv('GATEWAY_URL')
API_TOKEN = os.getenv('API_TOKEN')  # must match gateway's expected token

@app.route('/login', methods=['POST'])
def login():
    # Example login: set session.user_id on success
    user = authenticate(request.form.get('username'), request.form.get('password'))
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    session['user_id'] = user.id
    return jsonify({'status': 'logged in'})

@app.route('/transfer', methods=['POST'])
def transfer():
    # Ensure the user is authenticated
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    # Validate and sanitize inputs
    try:
        acct_id = int(request.form.get('id', ''))
        amount = Decimal(request.form.get('amount', ''))
    except (ValueError, InvalidOperation):
        return jsonify({'error': 'Invalid input format'}), 400
    if amount <= 0:
        return jsonify({'error': 'Amount must be positive'}), 400

    # Forward to gateway with strong authentication
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {'id': acct_id, 'amount': str(amount)}
    try:
        resp = requests.post(GATEWAY_URL, json=payload, headers=headers, timeout=5)
        return jsonify(resp.json()), resp.status_code
    except requests.RequestException:
        return jsonify({'error': 'Gateway unavailable'}), 503

if __name__ == '__main__':
    app.run(debug=False)
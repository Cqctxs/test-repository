import requests
from flask import Flask, request, session, jsonify

app = Flask(__name__)
app.secret_key = 'replace_with_secure_random'

ALLOWED_RECIPIENTS = {'alice', 'bob', 'charlie'}

@app.route('/transfer', methods=['POST'])
def transfer():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    sender = session['user_id']
    data = request.json or {}
    recipient = data.get('recipient')
    amount = data.get('amount')

    # Validate types
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid amount'}), 400

    if amount <= 0:
        return jsonify({'error': 'Amount must be positive'}), 400

    # Allowlist check
    if recipient not in ALLOWED_RECIPIENTS:
        return jsonify({'error': 'Recipient not allowed'}), 403

    # Forward request securely to backend PHP service
    backend_url = 'https://internal-service.local/process'
    headers = {'Authorization': f"Bearer {session.get('auth_token')}"}
    try:
        resp = requests.post(backend_url, json={
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }, headers=headers, timeout=5)
        resp.raise_for_status()
    except requests.RequestException as e:
        return jsonify({'error': 'Transfer failed', 'details': str(e)}), 502

    return jsonify(resp.json()), resp.status_code

if __name__ == '__main__':
    app.run(debug=True)

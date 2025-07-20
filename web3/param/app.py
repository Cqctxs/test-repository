import os
import requests
from flask import Flask, request, jsonify, abort
declare_app = Flask(__name__)

# Expect a JWT secret or API key for authentication
API_SECRET = os.getenv('API_SECRET')
if not API_SECRET:
    raise RuntimeError('API_SECRET must be set')


def verify_token(token):
    # Placeholder for real JWT verification
    # In production use PyJWT or similar to verify signature and expiry
    if token == API_SECRET:
        return {'username': 'authorized_user'}
    return None

@declare_app.route('/transfer', methods=['POST'])
def transfer():
    auth_header = request.headers.get('Authorization', '')
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        abort(401, description='Invalid auth header')
    user = verify_token(parts[1])
    if not user:
        abort(401, description='Unauthorized')

    data = request.get_json() or {}
    sender = data.get('sender')
    recipient = data.get('recipient')
    amount = data.get('amount')

    # Validate inputs
    if sender != user['username']:
        abort(403, description='You may only transfer from your own account')
    if not isinstance(amount, (int, float)) or amount <= 0:
        abort(400, description='Invalid transfer amount')
    if not isinstance(recipient, str) or not recipient:
        abort(400, description='Invalid recipient')

    # Forward request to PHP backend
    php_url = os.getenv('PHP_BACKEND_URL') or 'https://backend.local/gateway.php'
    try:
        resp = requests.post(
            php_url,
            json={'sender': sender, 'recipient': recipient, 'amount': amount},
            headers={'Authorization': auth_header},
            timeout=5
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        abort(502, description=f'Backend error: {e}')

    return jsonify(resp.json()), resp.status_code

if __name__=='__main__':
    declare_app.run(host='0.0.0.0', port=int(os.getenv('PORT',5001)))
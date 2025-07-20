import os
from flask import Flask, request, jsonify, abort
import requests

app = Flask(__name__)
# Load API key from environment; do not hard-code
API_KEY = os.environ.get('API_KEY')
GATEWAY_URL = os.environ.get('GATEWAY_URL', 'http://gateway/gateway.php')

@app.before_request
def check_api_key():
    key = request.headers.get('X-API-KEY')
    if not API_KEY or key != API_KEY:
        abort(401, 'Unauthorized')

def validate_account(name):
    if not isinstance(name, str) or not name.isalnum():
        abort(400, 'Invalid account identifier')
    return name

def validate_amount(value):
    try:
        amt = int(value)
    except (TypeError, ValueError):
        abort(400, 'Invalid amount')
    if amt <= 0:
        abort(400, 'Amount must be positive')
    return amt

@app.route('/transfer', methods=['POST'])
def transfer():
    data = request.get_json() or {}
    from_acc = validate_account(data.get('from', ''))
    to_acc = validate_account(data.get('to', ''))
    amount = validate_amount(data.get('amount'))
    resp = requests.post(
        GATEWAY_URL,
        json={'from': from_acc, 'to': to_acc, 'amount': amount},
        headers={'X-API-KEY': API_KEY},
        timeout=5
    )
    if resp.status_code != 200:
        abort(resp.status_code, 'Gateway error')
    result = resp.json()
    return jsonify({'status': 'success', 'data': result})

if __name__ == '__main__':
    app.run(debug=False)

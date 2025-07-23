from flask import Flask, request, jsonify, abort
import os
import requests

app = Flask(__name__)
API_KEY = os.environ.get('PAYMENT_API_KEY')
if not API_KEY:
    raise RuntimeError('PAYMENT_API_KEY not configured')

@app.route('/proxy_pay', methods=['POST'])
def proxy_pay():
    # Authenticate the client using a static API key
    client_key = request.headers.get('X-Api-Key')
    if client_key != API_KEY:
        abort(401, 'Invalid API key')

    data = request.get_json()
    if not data:
        abort(400, 'Invalid JSON body')
    # Validate required fields
    try:
        amount = float(data['amount'])
        currency = data['currency']
        recipient = data.get('recipient')
    except (KeyError, ValueError):
        abort(400, 'Missing or invalid parameters')

    # Forward only allowed parameters
    payload = {
        'amount': amount,
        'currency': currency,
        'recipient': recipient
    }
    # External API call
    resp = requests.post('https://payments.example.com/pay', json=payload, timeout=5)
    return jsonify(resp.json()), resp.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
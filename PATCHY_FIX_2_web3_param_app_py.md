# Security Fix for web3/param/app.py

**Vulnerability Type:** AUTHORIZATION_FAILURE  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Added API key authentication decorator. Validated 'amount' is positive number and 'to' is alphanumeric to prevent injection. Forward only sanitized JSON with required headers.

## Security Notes
Store API_KEY securely (env or secrets manager). Consider OAuth2 or JWT for production.

## Fixed Code
```py
import requests
from flask import Flask, request, jsonify, abort
from functools import wraps

app = Flask(__name__)
API_KEY = 'secret_api_key'  # normally from env

# Simple API key decorator
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get('X-API-KEY')
        if not key or key != API_KEY:
            abort(401)
        return f(*args, **kwargs)
    return decorated

@app.route('/transfer', methods=['POST'])
@require_api_key
def transfer():
    data = request.json
    amount = data.get('amount')
    to_account = data.get('to')
    # Input validation
    if not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({'error':'Invalid amount'}), 400
    if not isinstance(to_account, str) or not to_account.isalnum():
        return jsonify({'error':'Invalid account'}), 400

    # Forward sanitized data to PHP backend
    resp = requests.post(
        'https://php-backend.example.com/execute_transfer',
        json={'amount': amount, 'to': to_account},
        headers={'X-API-KEY': API_KEY}
    )
    return jsonify(resp.json()), resp.status_code

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
- functools.wraps
- abort from flask

## Testing Recommendations
- Call endpoint without API key and expect 401
- Send negative amount and expect 400

## Alternative Solutions

### Use JWT tokens instead of API keys
**Pros:** Scalable, Fine-grained claims
**Cons:** Complexity in setup


# Security Fix for web3/param/app.py

**Vulnerability Type:** AUTHORIZATION_FAILURE  
**Confidence Level:** MEDIUM  
**Breaking Changes:** No

## Original Issue
Added session-based authentication decorator to enforce login. Validates and casts numeric inputs. Passes session cookies to gateway.

## Security Notes
Ensure session cookies are HTTP-only and secure. Consider CSRF tokens for state-changing endpoints.

## Fixed Code
```py
from flask import Flask, request, jsonify, session
import requests

app = Flask(__name__)
app.secret_key = 'your-random-secret'

# Require login for financial operations
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Login required'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/transfer', methods=['POST'])
@login_required
def transfer():
    data = request.json
    # Validate inputs
    try:
        dest = int(data.get('dest'))
        amount = float(data.get('amount'))
    except Exception:
        return jsonify({'error': 'Invalid parameters'}), 400

    payload = {'account_id': data.get('src'), 'action': 'debit', 'amount': amount}
    # Call PHP gateway
    resp1 = requests.post('http://localhost/web3/param/gateway.php', json=payload, cookies=request.cookies)
    if resp1.status_code != 200:
        return jsonify({'error': 'Debit failed'}), 400

    payload2 = {'account_id': dest, 'action': 'credit', 'amount': amount}
    resp2 = requests.post('http://localhost/web3/param/gateway.php', json=payload2, cookies=request.cookies)
    if resp2.status_code != 200:
        return jsonify({'error': 'Credit failed'}), 400

    return jsonify({'success': True})

if __name__ == '__main__':
    app.run()
```

## Additional Dependencies
- from flask import session

## Testing Recommendations
- Try transfer without login, with invalid data, and attack logic.

## Alternative Solutions

### Use JWT tokens instead of session cookies
**Pros:** Stateless
**Cons:** Token revocation complexity


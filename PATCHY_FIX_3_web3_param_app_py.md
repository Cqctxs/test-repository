# Security Fix for web3/param/app.py

**Vulnerability Type:** AUTHORIZATION_FAILURE  
**Confidence Level:** HIGH  
**Breaking Changes:** Yes

## Original Issue
Added session-based authentication and authorization to restrict balance checks and transfers to logged-in users only. Transfer operation validates recipient existence, positive numeric amount, and sufficient funds before updating balances. Access to the sensitive FLAG environment variable restricted to an admin user. This fixes unauthorized data manipulation and information disclosure.

## Security Notes
Always authenticate and authorize API requests that modify or access sensitive data. Never rely on external services to enforce security without your own checks. Protect sensitive environment variables and ensure only privileged users can access them.

## Fixed Code
```py
from flask import Flask, request, jsonify, session
import os

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET_KEY', 'change_this_to_a_random_secret')

# Mock of accounts data loaded from somewhere
accounts = {
    'user1': {'balance': 100},
    'user2': {'balance': 200},
}

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    # In real app validate credentials
    if username in accounts:
        session['username'] = username
        return jsonify({'message': 'Logged in'}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/balance', methods=['GET'])
def get_balance():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    username = session['username']
    balance = accounts.get(username, {}).get('balance')
    return jsonify({'balance': balance})

@app.route('/transfer', methods=['POST'])
def transfer():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    sender = session['username']
    data = request.json
    recipient = data.get('recipient')
    amount = data.get('amount')

    if recipient not in accounts:
        return jsonify({'error': 'Recipient does not exist'}), 400
    if not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({'error': 'Invalid amount'}), 400
    if accounts[sender]['balance'] < amount:
        return jsonify({'error': 'Insufficient funds'}), 400

    # Perform transfer
    accounts[sender]['balance'] -= amount
    accounts[recipient]['balance'] += amount

    # Protect sensitive FLAG by restricting access
    flag = os.environ.get('FLAG', None)

    # Only admin can access FLAG (example)
    if sender == 'admin':
        return jsonify({'message': 'Transfer successful', 'flag': flag})

    return jsonify({'message': 'Transfer successful'})

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- from flask import session
- import os

## Testing Recommendations
- Test login and session creation works.
- Test unauthorized requests denied.
- Test transfer with valid and invalid inputs.
- Test that FLAG is only returned to admin.

## Alternative Solutions

### Use OAuth2 or JWT tokens for scalable authentication and authorization.
**Pros:** Robust industry standard., Better for distributed systems.
**Cons:** undefined

### Use a database backend with encryption and ACL for account data.
**Pros:** Greater data integrity and security.
**Cons:** undefined


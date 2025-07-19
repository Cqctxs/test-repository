# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced unsafe string formatting in SQL query with parameterized queries using placeholders and parameter tuples to prevent SQL injection attacks.

## Security Notes
Always use parameterized queries or prepared statements when incorporating user input into database queries to prevent SQL injection vulnerabilities.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_user_balance(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Use parameterized query to prevent SQL injection
    cursor.execute('SELECT balance FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0]
    return None

@app.route('/balance', methods=['GET'])
def balance():
    user_id = request.args.get('id')
    if not user_id:
        return jsonify({'error': 'User ID missing'}), 400
    balance = get_user_balance(user_id)
    if balance is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'balance': balance})

if __name__ == '__main__':
    app.run()
```

## Additional Dependencies
- import sqlite3

## Testing Recommendations
- Test with normal user IDs and verify balances.
- Test with malicious input (e.g., SQL injection payloads) and verify no injection occurs.
- Test with missing or invalid user IDs.

## Alternative Solutions

### Use an ORM (Object-Relational Mapping) library which internally handles query parameterization.
**Pros:** Automatically prevents SQL injection., Provides a higher level of abstraction.
**Cons:** undefined

### Use database stored procedures with parameter binding.
**Pros:** Database enforces input handling., Can improve performance.
**Cons:** undefined


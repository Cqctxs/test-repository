# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Fixed SQL injection by using parameterized queries instead of string concatenation for the username parameter.

## Security Notes
Never concatenate or interpolate user input directly into SQL queries. Use parameterized queries or ORM facilities.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/user/<string:username>')
def get_user(username):
    # Parameterized query to prevent SQL injection
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({'username': user[0], 'email': user[1]})
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0')

```

## Additional Dependencies
None

## Testing Recommendations
- Test user retrieval with normal and malicious username inputs to verify injection protection

## Alternative Solutions
None provided

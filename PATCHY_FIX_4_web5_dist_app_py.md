# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Changed raw SQL query concatenating username and password directly into a parameterized query using placeholders and tuple parameters. This prevents SQL injection by safely handling user input.

## Security Notes
Always use parameterized queries or prepared statements when interacting with databases with user input. Never concatenate user data into SQL queries directly. Passwords should be hashed and verified with a secure hash function (bcrypt, Argon2).

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Use parameterized query to prevent SQL injection
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run()
```

## Additional Dependencies
- from flask import Flask, request, jsonify
- import sqlite3

## Testing Recommendations
- Verify normal login succeeds
- Test SQL injection attacks fail
- Test missing parameters handled gracefully

## Alternative Solutions

### Use ORM frameworks that automatically escape queries
**Pros:** Less manual SQL and injection risk, Cleaner application code
**Cons:** Learning curve, potential performance overhead

### Hash and salt passwords and verify hashes instead of plain password comparison
**Pros:** Better password security
**Cons:** Requires updating schema and logic


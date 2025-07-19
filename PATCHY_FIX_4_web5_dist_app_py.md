# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced string interpolation in SQL queries with parameterized queries using '?' placeholders provided by sqlite3 library. This prevents attackers from injecting arbitrary SQL commands via the username parameter, thereby mitigating SQL injection risks.

## Security Notes
Always use parameterized queries or prepared statements when executing SQL queries with user input. Avoid string concatenation for query construction. Validate and sanitize inputs further if possible.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('mydatabase.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    conn = get_db_connection()
    try:
        # Use parameterized query to prevent SQL injection
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    finally:
        conn.close()

    if user is None:
        abort(404, 'User not found')

    return jsonify({'username': user['username'], 'email': user['email']})

if __name__ == '__main__':
    app.run()
```

## Additional Dependencies
- from flask import abort, jsonify

## Testing Recommendations
- Test with normal username input returns user data.
- Test with input containing SQL metacharacters does not allow injection or errors.

## Alternative Solutions

### Use ORM frameworks that provide automatic escaping and query building.
**Pros:** Reduces risk of SQL injection and improves maintainability
**Cons:** Might add dependency and complexity


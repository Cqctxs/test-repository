# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced the vulnerable string formatting SQL query with a parameterized query using the '?' placeholder and passing user input as a parameter tuple. This prevents SQL injection by separating query syntax from data values.

## Security Notes
Always use parameterized queries or prepared statements when interacting with databases to prevent SQL injection. Validate and sanitize user inputs, but parameterized queries are essential as first defense.

## Fixed Code
```py
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = 'users.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login_username', methods=['POST'])
def login_username():
    username = request.form.get('username', '')

    # Use parameterized queries to prevent SQL injection
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({'message': 'User found', 'username': user['username']})
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- import sqlite3

## Testing Recommendations
- Test login functionality with normal and malicious username inputs containing SQL payloads.
- Verify no SQL errors or injections occur.

## Alternative Solutions

### Use ORM libraries like SQLAlchemy for safer and easier database interaction
**Pros:** Less risk of SQL injection, More expressive queries
**Cons:** Additional dependency and learning curve


# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Fixed SQL injection by modifying the SQL query to use parameterized statements instead of directly formatting the username into the query string. This separates data from code and prevents injection attacks.

## Security Notes
Always use parameterized queries with user input to prevent SQL injection. Avoid any query string construction via concatenation or string formatting with untrusted input.

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

    # Use parameterized queries to protect against SQL injection
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
- Attempt login with SQL injection payloads and confirm they're not executed.
- Validate normal functional behavior is preserved.

## Alternative Solutions

### Implement ORM frameworks that handle parameterized queries automatically, like SQLAlchemy.
**Pros:** Cleaner syntax, fewer errors, Automatic SQL injection protection
**Cons:** Extra dependencies and overhead


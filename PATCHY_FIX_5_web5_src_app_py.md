# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced unsafe f-string concatenation in SQL query with a parameterized query using SQLite's placeholder to avoid SQL injection risks. This ensures that the input is handled safely and no malicious input can alter the query structure.

## Security Notes
Always use parameterized queries for SQL commands involving user input to avoid injection attacks. Avoid string interpolation directly in SQL.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/search')
def search_user():
    username = request.args.get('username', '')

    # Use parameterized query to prevent SQL injection
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'username': user['username'], 'email': user['email']})

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- sqlite3

## Testing Recommendations
- Test with normal input searches
- Test with input containing SQL injection payloads
- Confirm application does not expose internal errors or unexpected data

## Alternative Solutions

### Use ORM libraries such as SQLAlchemy to handle queries with built-in injection prevention.
**Pros:** Improved security and code maintainability, Abstracts query construction
**Cons:** Learning curve and added dependencies


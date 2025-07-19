# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Switched from unsafe string formatting to a parameterized query with placeholders and parameters in the SQLite query, which mitigates the risk of SQL injection. Input username is validated for presence but not overly restricted to allow partial search functionality.

## Security Notes
Use parameterized queries to separate SQL code from user input. Always validate inputs for presence and reasonable content. Avoid string concatenation in SQL commands.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/search', methods=['GET'])
def search_users():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Username parameter required'}), 400

    conn = get_db_connection()
    # Use parameterized query to prevent SQL injection
    users = conn.execute('SELECT * FROM users WHERE username LIKE ?', ('%' + username + '%',)).fetchall()
    conn.close()

    results = [{'id': u['id'], 'username': u['username']} for u in users]
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- sqlite3

## Testing Recommendations
- Test username search with safe input returns expected results.
- Test input with SQL injection payload does not modify query semantics.

## Alternative Solutions

### Use full ORM for query construction and execution.
**Pros:** More secure by design, Easier maintenance
**Cons:** More dependencies and complexity


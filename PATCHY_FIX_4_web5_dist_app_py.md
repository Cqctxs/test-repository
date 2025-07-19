# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
The original code directly formatted user input into SQL query strings, which is vulnerable to SQL injection. The fixed code uses parameterized queries with placeholders `?` and passes parameters as a tuple, preventing injection.

## Security Notes
Always validate input types where possible (e.g., check if user_id is digit). Use parameterized queries for all database interactions involving user input.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user')
def get_user():
    user_id = request.args.get('id')
    if not user_id or not user_id.isdigit():
        return jsonify({'error': 'Invalid user id'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    # Use parameterized query to prevent SQL Injection
    cur.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cur.fetchone()
    conn.close()

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    return jsonify(dict(user))

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- import sqlite3

## Testing Recommendations
- Test with valid and invalid user IDs.
- Test for SQL injection attempts like '1 OR 1=1'.
- Test behavior when user not found.

## Alternative Solutions

### Use an ORM like SQLAlchemy to abstract SQL queries.
**Pros:** Reduces risk of SQL injection by design., Easier to manage complex queries and migrations.
**Cons:** Extra dependency and learning curve.


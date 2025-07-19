# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
This fix addresses SQL injection by using parameterized queries rather than string interpolation for the user_id variable. Additionally, it validates that user_id consists only of digits before querying. This prevents malicious input from modifying the SQL query. It uses sqlite3 parameter substitution properly and disables debug mode.

## Security Notes
Always validate input type and format. Use parameterized queries. Avoid exposing detailed errors in production. Use row_factory for convenient row dictionary access.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

DATABASE = 'example.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user')
def get_user():
    user_id = request.args.get('user_id', '')

    # Validate user_id is digit
    if not user_id.isdigit():
        return jsonify({'error': 'Invalid user ID'}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    # Use parameterized query to prevent SQL injection
    cur.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cur.fetchone()
    conn.close()

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    return jsonify(dict(user))

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
- import sqlite3

## Testing Recommendations
- Test with valid user IDs retrieving user data.
- Attempt injection using SQL code in user_id to confirm refusal.
- Test missing or invalid user ID handling.

## Alternative Solutions

### Use ORM frameworks to abstract database interaction and enforce safety.
**Pros:** Less error-prone, Easier maintenance
**Cons:** Additional complexity


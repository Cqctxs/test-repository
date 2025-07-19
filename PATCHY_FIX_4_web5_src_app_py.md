# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Originally, SQL queries were constructed using string interpolation without parameterization, which allowed SQL injection vulnerabilities. This fix uses parameterized queries and validates user input to only accept digit user IDs, preventing SQL injection attacks.

## Security Notes
Parameterized queries (prepared statements) are essential to prevent SQL injection. Also validating and sanitizing user inputs reduces attack surface. Avoid concatenating or interpolating user input directly into SQL statements.

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

@app.route('/user', methods=['GET'])
def user():
    user_id = request.args.get('user_id')
    if not user_id or not user_id.isdigit():
        return jsonify({'error': 'Invalid user id provided'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Use parameterized query to prevent SQL injection
    sql = "SELECT * FROM users WHERE user_id = ?"
    cursor.execute(sql, (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user is None:
        return jsonify({'error': 'No such user found'}), 404

    return jsonify(dict(user))

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
None

## Testing Recommendations
- Verify that inputs with SQL special characters are not executed.
- Test normal user queries for correct data retrieval.
- Ensure no SQL error leaks sensitive info.

## Alternative Solutions

### Adopt an ORM such as SQLAlchemy to handle queries securely.
**Pros:** Cleaner code and built-in SQL injection protection.
**Cons:** Adds additional dependency.

### Whitelist inputs carefully before building queries.
**Pros:** Additional layer of input validation.
**Cons:** Does not replace prepared statements.


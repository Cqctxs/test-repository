# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Changed string interpolation of user_id into a parameterized query using placeholders and a tuple parameter. Added validation that user_id is a digit before query. This prevents SQL Injection by keeping query syntax separate from user input data.

## Security Notes
Never interpolate user input directly into SQL queries. Validate inputs for expected types and ranges. Parameterize all queries. Consider using ORM libraries that enforce safe queries.

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
        return jsonify({'error': 'Invalid user ID'}), 400

    conn = get_db_connection()
    # Use parameterized query to safely query by user ID
    cursor = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify(dict(user))
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- import sqlite3

## Testing Recommendations
- Test invalid and valid user IDs to ensure proper error handling.
- Test attempted SQL injection strings rejected or return errors.
- Check that valid users can be fetched correctly.

## Alternative Solutions

### Use ORM frameworks like SQLAlchemy for all database access.
**Pros:** Cleaner code and built-in protection against injection.
**Cons:** undefined


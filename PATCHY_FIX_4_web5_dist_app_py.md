# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced unsafe string formatting in SQL query with parameterized queries using ? placeholders and passing parameters as a tuple. This prevents SQL injection attacks by separating SQL code from data inputs. Added input validation to require username parameter.

## Security Notes
Always use parameterized queries/prepared statements to avoid SQL injection. Validate incoming parameters before using them in queries.

## Fixed Code
```py
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user', methods=['GET'])
def get_user():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Username required'}), 400

    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify(dict(user))
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
- import sqlite3

## Testing Recommendations
- Test with normal username to verify data returned.
- Test with special characters to confirm no SQL injection occurs.

## Alternative Solutions

### Use an ORM (e.g., SQLAlchemy) to manage database operations securely.
**Pros:** Built-in protection against SQL injection., Easier to maintain.
**Cons:** Added complexity and dependency.


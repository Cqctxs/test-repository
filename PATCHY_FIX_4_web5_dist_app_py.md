# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced unsafe string formatting in SQL query with parameterized queries using placeholders and query parameters, which prevents SQL injection by ensuring user inputs are treated as data, not code. Added basic validation of user_id to ensure it is a numeric string before query execution.

## Security Notes
Always use parameterized queries or prepared statements when composing SQL queries with user inputs. Never concatenate or format strings directly into queries. Validate input types whenever possible.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user', methods=['GET'])
def get_user():
    user_id = request.args.get('id')
    if not user_id or not user_id.isdigit():
        return jsonify({'error': 'Invalid user id'}), 400

    conn = get_db_connection()
    # Use parameterized query to prevent SQL injection
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()

    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'id': user['id'], 'name': user['name']})

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- sqlite3

## Testing Recommendations
- Test user retrieval for valid and invalid user ids.
- Test attempt to inject SQL via user id is neutralized.

## Alternative Solutions

### Use an ORM like SQLAlchemy that automatically parameterizes queries.
**Pros:** Cleaner code, Additional ORM features
**Cons:** May increase package size and complexity


# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Fixed SQL Injection by replacing string interpolation with parameterized query. Also added input validation for the user_id parameter to ensure it is numeric.

## Security Notes
Use parameterized queries consistently throughout the application. Validate user input for expected type and format. Disable debug mode in production to avoid information leakage.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

DATABASE = 'database.sqlite'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user', methods=['GET'])
def get_user():
    user_id = request.args.get('user_id')
    if not user_id or not user_id.isdigit():
        return jsonify({'error': 'Invalid user_id parameter'}), 400

    conn = get_db_connection()
    # Use prepared statement to prevent SQL Injection
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
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
- Test query with SQL injection attempts to ensure safe handling.
- Verify correct results for valid user IDs.

## Alternative Solutions
None provided

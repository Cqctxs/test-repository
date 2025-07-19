# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
The original code constructed SQL queries by formatting strings with unsanitized user input, enabling SQL injection. Fixed code uses parameterized queries via sqlite3's '?' placeholder to separate query structure from user input, preventing injection. Also added a basic input validation check to ensure user_id is numeric to avoid malformed inputs.

## Security Notes
Always use parameterized queries/prepared statements for database operations to prevent SQL injection. Validate user input for type and format before queries. Use ORM or query builders if available for improved security and maintainability.

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

    return jsonify(dict(user))

if __name__ == '__main__':
    app.run(debug=True)
```

## Additional Dependencies
- import sqlite3
- from flask import Flask, request, jsonify

## Testing Recommendations
- Test with legitimate and malicious user id inputs to verify injection prevention.
- Test non-existent user ids to verify 404 responses.

## Alternative Solutions

### Use an ORM such as SQLAlchemy to manage database queries safely.
**Pros:** Abstraction from SQL syntax, Built-in injection prevention
**Cons:** Added complexity and dependency


# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
User input was interpolated directly into the SQL query, vulnerable to injection attacks.
This fix uses a parameterized placeholder '?' with a tuple argument to the execute() method of the cursor, preventing SQL injection.
User input is no longer concatenated as raw SQL string.
This approach is a standard best practice for working with SQL in Python.

## Security Notes
- Always use parameterized SQL for dynamically provided parameters.
- Validate inputs where applicable.
- Use connection pooling or ORM to help with security and maintenance.
- Enable debug=False in production environments to avoid info leaks.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/user')
def get_user():
    user_id = request.args.get('id')

    # Safely use parameterized queries to mitigate SQL injection
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({'id': user[0], 'name': user[1]})
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- import sqlite3

## Testing Recommendations
- Verify user retrieval with valid and invalid IDs.
- Test database with maliciously crafted id parameters.
- Ensure no SQL errors exposing schema or internals.

## Alternative Solutions
None provided

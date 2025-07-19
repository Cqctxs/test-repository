# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
The original code concatenated user input directly into SQL queries, exposing it to SQL injection attacks.
This fix uses parameterized queries (prepared statements) which separate query structure from data.
The user input is passed as a parameter tuple to cursor.execute(), ensuring proper escaping and validation by the database driver.

## Security Notes
- Always use parameterized queries instead of string concatenation for SQL queries.
- Validate and sanitize inputs when applicable.
- Keep database connections short-lived and properly closed.
- Use ORM libraries where possible to add abstraction and protection.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/user')
def get_user():
    user_id = request.args.get('id')

    # Use parameterized query to prevent SQL injection
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
    app.run()

```

## Additional Dependencies
- import sqlite3

## Testing Recommendations
- Test with valid user IDs and verify returned data.
- Test with malicious input containing SQL keywords or special characters.
- Use automated SQL injection tools to verify resilience.

## Alternative Solutions

### Use an ORM like SQLAlchemy to abstract queries and prevent injection.
**Pros:** Cleaner code, Built-in injection prevention
**Cons:** Learning curve, Potentially more dependencies and configuration

### Whitelist allowed user IDs or validate user input further.
**Pros:** Adds another layer of defense
**Cons:** Less flexible, May not prevent all injection if used alone


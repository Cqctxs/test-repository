# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced string interpolation of username into SQL query with parameterized query using cursor.execute with placeholders, effectively preventing SQL injection attacks.

## Security Notes
Always use parameterized queries or prepared statements when interacting with databases. Avoid string concatenation or manual string formatting for SQL queries.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/user/<string:username>')
def get_user(username):
    # Use parameterized query to prevent SQL injection
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({'username': user[0], 'email': user[1]})
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

```

## Additional Dependencies
None

## Testing Recommendations
- Test with normal and malicious username inputs to confirm injection is blocked
- Verify application behavior with valid and invalid usernames

## Alternative Solutions

### Use an ORM like SQLAlchemy which constructs parameterized queries automatically.
**Pros:** Cleaner code, Reduces SQL injection risks, Easier query building
**Cons:** Additional dependency, Learning curve


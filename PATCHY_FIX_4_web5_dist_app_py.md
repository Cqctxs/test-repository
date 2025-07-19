# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced unsafe SQL query using f-string interpolation with a parameterized query using SQLite's '?' placeholder syntax. This prevents SQL injection by separating query code from user input data, ensuring input is properly escaped and treated as data, not code.

## Security Notes
Always use parameterized queries or prepared statements to prevent SQL injection. Avoid string formatting or concatenation for SQL commands with user inputs.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user/<username>')
def get_user(username):
    # Use parameterized query to prevent SQL injection
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'username': user['username'], 'email': user['email']})

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- sqlite3

## Testing Recommendations
- Test with normal usernames
- Test with usernames containing SQL injection attempts (e.g., 'admin' OR 1=1)
- Verify no error or data leak occurs

## Alternative Solutions

### Use an ORM (Object Relational Mapper) library like SQLAlchemy that automatically handles query parameterization.
**Pros:** Simplifies database operations, Built-in protection against SQL injection
**Cons:** Additional dependencies, May impact performance or complexity


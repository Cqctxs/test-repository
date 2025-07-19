# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced unsafe string formatting in SQL query with a parameterized query using the SQLite library's placeholder syntax. This prevents SQL injection by passing user input as query parameters rather than concatenating strings.

## Security Notes
Always use parameterized queries or prepared statements when interacting with SQL databases with user input. Never interpolate user input directly in query strings.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    conn = get_db_connection()
    # Use parameterized queries to prevent SQL injection
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    if user is None:
        return jsonify({'error':'User not found'}), 404
    return jsonify(dict(user))

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- import sqlite3
- from flask import Flask, request, jsonify

## Testing Recommendations
- Attempt SQL injection patterns in username parameter and verify query safety.
- Test valid usernames return correct data.

## Alternative Solutions

### Use an ORM like SQLAlchemy to manage queries and prevent injection.
**Pros:** Automatic query sanitization, Easy to write complex queries
**Cons:** Additional dependency, Learning curve


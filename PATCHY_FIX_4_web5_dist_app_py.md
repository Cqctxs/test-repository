# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced string formatting of SQL queries with parameterized queries using '?' placeholders and parameter tuple. This prevents SQL injection by not allowing user input to alter query syntax.

## Security Notes
Always use parameterized queries or prepared statements for SQL queries. Avoid directly concatenating user input into SQL commands.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, g, jsonify

app = Flask(__name__)
DATABASE = './test.db'

# Function to get db connection

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/user/<username>')
def get_user(username):
    db = get_db()
    cursor = db.cursor()
    # Use parameterized query to prevent SQL injection
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    if user:
        return jsonify({'user': user[0], 'email': user[1]})
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- import sqlite3
- from flask import Flask, request, g, jsonify

## Testing Recommendations
- Test with normal and malicious usernames including SQL injection attempts to confirm they fail safely.

## Alternative Solutions

### Use an ORM (e.g., SQLAlchemy) which safely handles query parameters.
**Pros:** Reduces direct SQL handling., Safer by default.
**Cons:** More dependencies., Learning curve for ORM usage.


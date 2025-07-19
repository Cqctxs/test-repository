# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced vulnerable string formatting in the SQL query with parameterized query. This secures the code against SQL injection attacks by ensuring user input is passed as parameter, not as query text.

## Security Notes
Never concatenate or format SQL command strings with user input. Always use parameterized queries or access ORM methods.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify, g

app = Flask(__name__)
DATABASE = './sample.db'

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

@app.route('/search')
def search_user():
    username = request.args.get('username', '')
    db = get_db()
    cursor = db.cursor()
    # Use parameterized query to prevent SQL injection
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    results = cursor.fetchall()
    users = [{'username': row[0], 'email': row[1]} for row in results]
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- import sqlite3
- from flask import Flask, request, jsonify, g

## Testing Recommendations
- Attempt injection via username parameter to confirm protection.
- Validate normal queries work correctly.

## Alternative Solutions

### Use ORM layers to access database safely.
**Pros:** Abstract SQL, reduce errors, automated escaping.
**Cons:** Added complexity and dependencies.


# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Changed SQL to use ? placeholder and parameter tuple. Added app context teardown for clean DB connection.

## Security Notes
Consistently use prepared statements. Manage DB connections lifecycle.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify, g

app = Flask(__name__)
DB_PATH = 'app.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
    return g.db

@app.teardown_appcontext
def close_db(exc):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/user')
def get_user():
    username = request.args.get('user', '')
    db = get_db()
    cursor = db.cursor()
    # Use parameterized query to avoid injection
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    if not row:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'id': row[0], 'username': row[1]})

if __name__ == '__main__':
    app.run()
```

## Additional Dependencies
- from flask import g

## Testing Recommendations
- Test with username containing quotes or SQL keywords to ensure no injection.

## Alternative Solutions
None provided

# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Converted string interpolation to parameterized SQLite query ('?'). Validated id is an integer before querying.

## Security Notes
Ensure database permissions are least-privilege. Consider using connection pooling in high-load environments.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user')
def get_user():
    user_id = request.args.get('id')
    try:
        uid = int(user_id)
    except (ValueError, TypeError):
        return jsonify({'error':'Invalid id'}), 400

    conn = get_db()
    # Use parameterized query
    cur = conn.execute('SELECT id, name, email FROM users WHERE id = ?', (uid,))
    row = cur.fetchone()
    conn.close()
    if row:
        return jsonify(dict(row))
    return jsonify({'error':'Not found'}), 404

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
None

## Testing Recommendations
- Pass non-numeric id and expect 400
- Attempt SQL injection payload and ensure it's treated as invalid

## Alternative Solutions

### Use an ORM like SQLAlchemy
**Pros:** Automatic parameterization, Model abstraction
**Cons:** Increased dependencies


# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced f-string query with psycopg2 parameterized execute(). Validated name length to mitigate DoS.

## Security Notes
Limit result set or add pagination. Escape patterns if using more complex matching.

## Fixed Code
```py
import psycopg2
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        host=os.getenv('DB_HOST')
    )

@app.route('/search')
def search_users():
    name = request.args.get('name', '')
    # Basic sanitation: limit length
    if len(name) > 50:
        return jsonify({'error':'Name too long'}), 400

    conn = get_db()
    cur = conn.cursor()
    # Use parameterized query
    cur.execute('SELECT id, name, email FROM users WHERE name ILIKE %s', ('%' + name + '%',))
    rows = cur.fetchall()
    conn.close()
    users = [{'id': r[0], 'name': r[1], 'email': r[2]} for r in rows]
    return jsonify({'users': users})

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
- os
- psycopg2

## Testing Recommendations
- Attempt SQL injection via name and verify safe searches
- Test with long name input

## Alternative Solutions

### Use SQLAlchemy ORM
**Pros:** Automatic escaping
**Cons:** Learning curve


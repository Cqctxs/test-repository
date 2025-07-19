# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced direct string interpolation in SQL query with parameterized query using placeholders, preventing injection of SQL code via user-supplied name parameter.

## Security Notes
Always use parameterized queries for database access with user input. Validate and sanitize inputs as additional layers of protection.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/users')
def users():
    name = request.args.get('name')
    if not name:
        return jsonify({'error': 'Name parameter required'}), 400

    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    # Secure parameterized query to prevent SQL injection
    cursor.execute('SELECT * FROM users WHERE name = ?', (name,))
    rows = cursor.fetchall()
    conn.close()

    users_list = [{'id': r[0], 'name': r[1]} for r in rows]

    return jsonify(users_list)

if __name__ == '__main__':
    app.run(debug=True)
```

## Additional Dependencies
- sqlite3
- flask

## Testing Recommendations
- Test with valid names
- Test with SQL injection payloads to validate no injection possible
- Verify normal functioning

## Alternative Solutions

### Use ORM frameworks to abstract SQL and handle parameterization
**Pros:** Automatically prevents SQL injection and cleaner code
**Cons:** Dependency on external ORM


# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
The original code formatted user input directly into the SQL statement causing SQL injection risk. The fix uses parameterized queries with placeholders and passes parameters separately to prevent injection, specifically for LIKE search.

## Security Notes
Use input validation for search queries if applicable. Always prefer parameterized queries. For more complex search, consider full-text search engines.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('mydatabase.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/search')
def search_users():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Search query missing'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    # Parameterized LIKE query prevents SQL injection
    cur.execute('SELECT * FROM users WHERE name LIKE ?', ('%' + query + '%',))
    results = cur.fetchall()
    conn.close()

    users = [dict(row) for row in results]
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- import sqlite3

## Testing Recommendations
- Test search functionality with normal and wildcard characters.
- Attempt SQL injection payloads to verify they do not succeed.
- Test empty and very long queries.

## Alternative Solutions

### Sanitize inputs to remove dangerous characters before incorporating into queries.
**Pros:** Some protection., May be simpler for legacy code.
**Cons:** Prone to bypass., Less reliable than parameterized queries.


# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced direct string interpolation in SQL query with a parameterized query using placeholders and parameters passed separately. This prevents SQL injection attacks by treating user input as data only. Added wildcards to support LIKE searches as per original functionality.

## Security Notes
Always use parameterized queries to prevent injection. Validate input length and type as needed to prevent abuse. Consider using full-text search features with proper sanitization.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search_users():
    keyword = request.args.get('keyword', '')
    # Use parameterized query to protect against SQL injection
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username LIKE ?"
    # Use '%' wildcards around keyword for LIKE query
    like_keyword = f'%{keyword}%'
    cursor.execute(query, (like_keyword,))
    results = cursor.fetchall()
    conn.close()

    users = [{'username': row[0], 'email': row[1]} for row in results]
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
None

## Testing Recommendations
- Test searching with normal keywords returns expected users.
- Test input with SQL meta-characters does not cause injection or errors.
- Test empty or missing keywords handled gracefully.

## Alternative Solutions

### Use ORM frameworks that handle query parameterization and escaping automatically.
**Pros:** Reduces raw SQL and injection risks.
**Cons:** Adds complexity and dependencies.


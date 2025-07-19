# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Changed the SQL query to use a parameterized query with the '?' placeholder and passed the search query as a parameter. This avoids SQL injection where attackers could manipulate the query string to execute arbitrary SQL commands.

## Security Notes
Use parameterized queries consistently for all database access involving user inputs to mitigate injection risks. Validate or sanitize inputs additionally if applicable.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('mydatabase.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/search', methods=['GET'])
def search_users():
    query = request.args.get('query', '')
    if not query:
        abort(400, 'Query parameter is required')
    conn = get_db_connection()
    try:
        # Use parameterized query to safely include user input
        users = conn.execute("SELECT * FROM users WHERE username LIKE ?", ('%' + query + '%',)).fetchall()
    finally:
        conn.close()

    results = [{'username': user['username'], 'email': user['email']} for user in users]
    return jsonify(results)

if __name__ == '__main__':
    app.run()
```

## Additional Dependencies
- from flask import abort, jsonify

## Testing Recommendations
- Test search with regular inputs returns correct users.
- Test search with inputs containing SQL special characters do not cause injection or errors.

## Alternative Solutions

### Use ORM libraries that abstract query construction and escaping.
**Pros:** Better maintainability and security
**Cons:** Extra abstraction layer and dependencies


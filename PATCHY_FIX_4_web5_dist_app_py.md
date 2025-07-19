# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
The original code directly interpolated unsanitized user input into an SQL query string, allowing SQL injection attacks. The fix uses a parameterized query with the '?' placeholder and passing the user input as a parameter tuple to the execute() method. This prevents the user input from being treated as executable SQL and protects the database from injection. Additionally, row_factory is set to sqlite3.Row for better result handling.

## Security Notes
Always use parameterized queries or prepared statements when interacting with databases. Never concatenate user input into SQL statements directly. Validate and sanitize user inputs accordingly. Disable debug mode in production to avoid information leaks.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

DATABASE = 'example.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/search')
def search():
    query = request.args.get('query', '')

    # Use parameterized query to prevent SQL injection
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM products WHERE name LIKE ?', ('%' + query + '%',))
    results = cur.fetchall()
    conn.close()

    results_list = [dict(row) for row in results]
    return jsonify(results_list)

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
- import sqlite3

## Testing Recommendations
- Test with normal query strings returning valid results.
- Test with strings containing SQL keywords or special characters to confirm no injection.
- Test with empty or missing input.

## Alternative Solutions

### Use ORM libraries such as SQLAlchemy for query construction.
**Pros:** Automatically handles parameterization, Easier migration and complex queries
**Cons:** Additional dependency


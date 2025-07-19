# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
User input was previously directly interpolated into the SQL WHERE clause, allowing SQL injection. The fixed code uses parameterized queries with placeholders and passes the input securely as a parameter. It also performs a simple input validation to reject suspicious characters that could be used in injection.

## Security Notes
Always use parameterized queries when querying databases with user inputs. Validate and sanitize inputs to further guard against injection and errors. Do not use string concatenation or formatting for SQL commands.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('example.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/search', methods=['GET'])
def search_items():
    query = request.args.get('query', '')

    # Basic input validation to prevent SQL injection
    if not query or any(c in query for c in [';', '--', '/*', '*/']):
        return jsonify({'error': 'Invalid search query'}), 400

    conn = get_db_connection()
    # Use parameterized query
    sql = "SELECT * FROM items WHERE name LIKE ?"
    like_query = f'%{query}%'
    items = conn.execute(sql, (like_query,)).fetchall()
    conn.close()

    results = [{'id': item['id'], 'name': item['name']} for item in items]
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
None

## Testing Recommendations
- Test valid search queries return results
- Test injection inputs like '; DROP TABLE' are rejected or do not cause harm
- Test empty or invalid input returns proper error

## Alternative Solutions

### Use an ORM which constructs queries safely and supports escaping wildcards appropriately.
**Pros:** Improves safety and readability., Reduces risk of injection.
**Cons:** undefined


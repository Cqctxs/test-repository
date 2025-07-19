# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
The original code used unsafe string interpolation into the SQL query with user input, opening a SQL Injection vulnerability. The fix replaces this with a parameterized query using '?' placeholders and passing the user input as a parameter tuple, ensuring the database driver escapes inputs properly and preventing injection attacks. This preserves the original functionality of filtering items by category.

## Security Notes
Always prefer parameterized queries over string formatting for database calls with user input. Validate inputs for expected data types and constraints when possible.

## Fixed Code
```py
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/items', methods=['GET'])
def get_items():
    category = request.args.get('category', '')

    conn = get_db_connection()
    # Use parameterized query to avoid SQL injection
    items = conn.execute('SELECT * FROM items WHERE category = ?', (category,)).fetchall()
    conn.close()

    results = []
    for item in items:
        results.append({'id': item['id'], 'name': item['name'], 'category': item['category']})

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- sqlite3

## Testing Recommendations
- Test requests with normal and malicious category inputs to verify no injection occurs
- Test results filtering by category

## Alternative Solutions

### Use an ORM like SQLAlchemy for query building and safety
**Pros:** Prevents injection and eases database interaction
**Cons:** Additional complexity and dependencies


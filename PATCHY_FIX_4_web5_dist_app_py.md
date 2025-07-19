# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced string interpolation in the SQL query with a parameterized query using placeholders ('?') and passing the user input as a separate parameter. This prevents SQL injection by separating code and data.

## Security Notes
Always use parameterized queries or prepared statements for SQL queries that include user input to prevent SQL injection vulnerabilities.

## Fixed Code
```py
# Fixed SQL Injection by using parameterized queries
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
db_path = 'example.db'

@app.route('/search')
def search():
    query = request.args.get('query', '')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Use parameterized query to avoid SQL injection
    cursor.execute('SELECT * FROM items WHERE name LIKE ?', ('%' + query + '%',))
    results = cursor.fetchall()
    conn.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- sqlite3
- flask

## Testing Recommendations
- Test search with typical input and special characters to ensure no SQL injection possible.
- Test performance and results correctness.

## Alternative Solutions

### Use an ORM like SQLAlchemy to handle queries more safely.
**Pros:** Abstracts SQL, Less error prone
**Cons:** Adds complexity and dependency


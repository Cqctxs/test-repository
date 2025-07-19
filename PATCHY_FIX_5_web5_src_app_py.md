# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
The original code interpolated user input directly into an SQL query string, leading to SQL injection risk. Fixed code uses a parameterized query with '?' placeholder to securely bind the 'category' user input, preventing injection. Also handles the case where category parameter is missing by returning all products.

## Security Notes
Use parameterized queries consistently for all user input in SQL statements. Validate input types and potentially restrict allowed category values via allowlists if needed. Consider using an ORM for more complex queries.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/products', methods=['GET'])
def get_products():
    category = request.args.get('category')

    conn = get_db_connection()
    if category:
        # Use parameterized queries to prevent SQL injection
        products = conn.execute('SELECT * FROM products WHERE category = ?', (category,)).fetchall()
    else:
        products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()

    return jsonify([dict(row) for row in products])

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- import sqlite3
- from flask import Flask, request, jsonify

## Testing Recommendations
- Test with various category inputs including SQL injection payloads to confirm safe queries.
- Test with missing category parameter to get all products.

## Alternative Solutions

### Validate 'category' input against a whitelist of allowed categories before query.
**Pros:** Additional input filtering layer, Limits exposure of data
**Cons:** Requires maintaining category whitelist


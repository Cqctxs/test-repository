# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Changed the direct f-string interpolation of user input in the SQL query to a parameterized query using SQLite's .execute with query placeholders '?'. This prevents SQL Injection by correctly escaping user input. Also added input validation for query parameter missing.

## Security Notes
Always use parameterized queries when incorporating user input in SQL statements. Do input validation and escaping as an extra layer.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400
    # Connect to database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Use parameterized query to prevent SQL Injection
    cursor.execute('SELECT * FROM items WHERE name LIKE ?', ('%'+query+'%',))
    results = cursor.fetchall()
    conn.close()
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
None

## Testing Recommendations
- Verify input with normal strings returns expected data.
- Test various SQL injection attempts (e.g., escaping characters) have no effect.

## Alternative Solutions
None provided

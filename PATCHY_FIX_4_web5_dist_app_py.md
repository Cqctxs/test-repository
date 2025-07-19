# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced f-string SQL with parameterized query using placeholders. The library automatically escapes the user input.

## Security Notes
Always use parameter binding for user-provided data. Avoid string formatting for SQL.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_PATH = 'app.db'

@app.route('/search')
def search():
    q = request.args.get('q', '')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Use parameterized query to prevent SQL injection
    cursor.execute('SELECT id, title FROM items WHERE title LIKE ?', (f'%{q}%',))
    results = [{'id': row[0], 'title': row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run()
```

## Additional Dependencies
None

## Testing Recommendations
- Attempt q with SQL payload, verify it fails to break query.

## Alternative Solutions
None provided

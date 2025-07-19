# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced string concatenation in SQL query with parameterized query using placeholders and passing user input as parameters. This prevents attackers from injecting malicious SQL code via the user_id parameter.

## Security Notes
Never incorporate user input directly into SQL queries. Always use parameterized queries or ORM that do this automatically. Validate the input as needed to limit unexpected values.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Use parameterized queries to prevent SQL injection
@app.route('/user')
def get_user():
    user_id = request.args.get('id')
    if not user_id:
        return jsonify({'error': 'User ID required'}), 400

    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    # Parameterized query to mitigate SQL injection risk
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify({'id': row[0], 'name': row[1]})
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
```

## Additional Dependencies
- sqlite3
- flask

## Testing Recommendations
- Test with valid user IDs
- Attempt SQL injection payloads to confirm no injection
- Check errors for any leak of SQL errors

## Alternative Solutions

### Use ORM libraries like SQLAlchemy that inherently handle query parameterization
**Pros:** Cleaner code, abstracts SQL syntax, Prevents SQL injection automatically
**Cons:** Added learning curve and dependency


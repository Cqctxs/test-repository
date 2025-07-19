# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Fixed SQL injection by replacing raw string interpolation in SQL query with a parameterized query using `?` and tuple passing user input safely. Also added validation for user_id ensuring it's numeric before query execution.

## Security Notes
Parameterization of SQL queries prevents injection vulnerabilities. Always validate input data types prior to database queries. Avoid string format or concatenation for queries with user input.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/user')
def get_user():
    user_id = request.args.get('id')

    if not user_id or not user_id.isdigit():
        return jsonify({'error': 'Invalid user ID'}), 400

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Use parameterized query to prevent SQL injection
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({'id': user[0], 'name': user[1], 'email': user[2]})
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
None

## Testing Recommendations
- Test with normal and malicious user ID inputs
- Verify application returns appropriate errors on invalid inputs
- Confirm normal data retrieval for valid inputs

## Alternative Solutions

### Migrate to an ORM with built-in safe query mechanisms
**Pros:** Higher abstraction and reduced risk of injection errors
**Cons:** May require significant code changes


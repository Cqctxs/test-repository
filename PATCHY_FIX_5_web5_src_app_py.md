# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
This file had the same SQL injection vulnerability as the web5/dist/app.py file. The fix was to replace unsafe SQL string formatting with parameterized queries to prevent injection attacks. This fix uses the SQLite parameter style with ? placeholders and parameter tuples to safely bind user input values to the query.

## Security Notes
Same as above. Passwords should be hashed and sessions properly managed in a real application. This fix ensures injection cannot be performed via login queries.

## Fixed Code
```py
from flask import Flask, request, jsonify
import sqlite3
app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Use parameterized query to prevent SQL injection
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        # Normally use session, for now just return success
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- import sqlite3

## Testing Recommendations
- Test login endpoints thoroughly after fix as described for dist/app.py.

## Alternative Solutions
None provided

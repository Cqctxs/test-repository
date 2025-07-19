# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Refactored login SQL query to use parameterized query with placeholders to prevent SQL injection. Inputs are passed as parameters instead of concatenating into the query string.

## Security Notes
Parameterized queries prevent attackers from injecting malicious SQL through user inputs. Password handling can be improved further by storing hashed passwords.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Use parameterized query to prevent SQL injection
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run()
```

## Additional Dependencies
- from flask import Flask, request, jsonify
- import sqlite3

## Testing Recommendations
- Test invalid and valid usernames and passwords
- Validate that SQL injection attempts fail

## Alternative Solutions

### Use an ORM like SQLAlchemy for safer query construction
**Pros:** Automatic escaping and less raw SQL
**Cons:** Increased dependencies and learning curve


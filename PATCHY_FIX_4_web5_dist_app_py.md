# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
The original code constructed SQL queries by interpolating user input directly, exposing a SQL injection vulnerability. The fix changes the code to use parameterized SQL queries with placeholders `?` and passing username and password parameters as a tuple. This ensures user inputs are treated as data, not executable SQL, preventing injection attacks. Passwords are hashed for security (assuming database stores hashed passwords).

## Security Notes
Always use parameterized queries or prepared statements to prevent SQL injection. Store passwords hashed and salted securely, never in plaintext.

## Fixed Code
```py
from flask import Flask, request, jsonify
import sqlite3
import hashlib

app = Flask(__name__)

DATABASE = 'users.db'

# Function to get db connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Hash the password before comparison (if stored hashed)
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    conn = get_db_connection()
    # Use parameterized query to prevent SQL injection
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password_hash)).fetchone()
    conn.close()

    if user:
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'error': 'Invalid credentials'}), 403

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
- sqlite3
- hashlib
- flask

## Testing Recommendations
- Attempt login with SQL injection payloads to verify failure
- Test valid and invalid logins as expected

## Alternative Solutions

### Use an ORM like SQLAlchemy to handle queries securely
**Pros:** Simplifies query handling, Prevents injection inherently
**Cons:** Adds dependency, learning curve


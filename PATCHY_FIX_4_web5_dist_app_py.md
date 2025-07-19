# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
The original code used string formatting to include user inputs directly into the SQL query, allowing attackers to inject malicious SQL code leading to data compromise or bypass. The fix replaces string concatenation with parameterized queries using placeholders (?) and passing user inputs as parameters to execute(). This prevents SQL injection by safely escaping inputs. Connection and cursor management are cleaned up properly.

## Security Notes
Always use parameterized queries or prepared statements when working with SQL databases. Never concatenate or format user input into SQL statements directly. For password storage, hash passwords securely (e.g., bcrypt) rather than storing plaintext passwords.

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
- Test login with valid and invalid credentials.
- Test special characters in username/password do not cause SQL errors.
- Use penetration testing tools to verify no SQL injection is possible.

## Alternative Solutions

### Use an ORM library like SQLAlchemy to handle queries, which internally uses parameterized queries.
**Pros:** High-level abstraction, Less error-prone
**Cons:** Adds dependencies and learning curve


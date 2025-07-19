# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced unsafe SQL string formatting with parameterized queries using psycopg2?s %s and parameter tuple. This protects against SQL injection by ensuring user input is treated as data, not code. Added input validation for username and password presence. Note: Passwords should be hashed with a secure algorithm in production; here it’s shown as a simple equality for demonstration purposes.

## Security Notes
Always use parameterized queries. Never store or compare passwords in plaintext; use strong password hashing algorithms such as bcrypt or Argon2.

## Fixed Code
```py
from flask import Flask, request, jsonify
import psycopg2
import psycopg2.extras

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(dbname='mydb', user='user', password='password', host='localhost')
    return conn

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = 'SELECT * FROM users WHERE username = %s'
    cur.execute(query, (username,))  # Parameterized query for security
    user = cur.fetchone()
    conn.close()

    if user and user['password'] == password:  # Passwords should be hashed in production
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
- import psycopg2
- import psycopg2.extras

## Testing Recommendations
- Test login with valid and invalid credentials.
- Test SQL injection attempts with crafted input to confirm protection.

## Alternative Solutions

### Use an ORM, like SQLAlchemy, for safer database operations.
**Pros:** Built-in protection against injection., More readable code.
**Cons:** Additional dependency and learning curve.


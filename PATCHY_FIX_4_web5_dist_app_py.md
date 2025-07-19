# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Changed SQL query to use a parameterized query with a placeholder and passing user input as a separate parameter to avoid direct string interpolation. This protects against SQL Injection attacks by ensuring the database engine treats user input strictly as data, not executable code.

## Security Notes
Always use parameterized queries or prepared statements when interacting with databases to prevent injection vulnerabilities. Validate and sanitize input where appropriate. Use ORM frameworks when possible for safer database abstractions.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/user', methods=['GET'])
def get_user():
    username = request.args.get('username')
    # Use parameterized queries to prevent SQL Injection
    query = "SELECT * FROM users WHERE username = ?"
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({'username': user[0], 'email': user[1]})
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
None

## Testing Recommendations
- Test fetching user by username returns correct data.
- Test with malicious input to confirm SQL injection is not possible.
- Test error handling for non-existent users.

## Alternative Solutions

### Use an ORM like SQLAlchemy that handles parameterization automatically.
**Pros:** Simplifies query writing., Offers additional security features.
**Cons:** Adds dependencies and learning curve.


# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Original code performed SQL queries by directly interpolating user input, allowing an attacker to inject malicious SQL code. The fix uses parameterized queries with placeholders (the '?' in SQLite) to separate code and data, preventing injection attacks. The user_id parameter is typed as int to validate input early.

## Security Notes
Always use parameterized queries/prepared statements when interacting with databases with user input. Avoid direct string formatting into SQL commands. Add input type validation where possible. Disable debug mode in production environments.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

DATABASE = 'app.db'

# Use parameterized queries to prevent SQL injection
@app.route('/user/<int:user_id>')
def get_user(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        # Parameterized query, user input is not interpolated directly
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        if not user:
            abort(404)
        return jsonify(dict(id=user[0], name=user[1], email=user[2]))
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
- import sqlite3

## Testing Recommendations
- Test with valid and invalid user IDs.
- Attempt SQL injection attacks to verify the fix.
- Check error handling on missing users.

## Alternative Solutions

### Use an ORM (Object Relational Mapper) like SQLAlchemy which automatically parameterizes queries.
**Pros:** Simplifies database access, Automatically safer SQL generation
**Cons:** Adds dependency and learning curve


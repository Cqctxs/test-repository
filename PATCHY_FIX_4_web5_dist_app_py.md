# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
The original code used unsafe string interpolation directly in SQL queries with user input, allowing attackers to perform SQL Injection attacks. The fix uses parameterized queries (sqlite3's '?' placeholders) which safely bind user input and prevent malicious injection. It also adds basic input validation to ensure user_id is numeric before querying.

## Security Notes
Always use parameterized queries or prepared statements with user inputs. Validate and sanitize user inputs. Avoid directly concatenating user inputs into SQL queries.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/user')
def get_user():
    user_id = request.args.get('user_id')
    if not user_id or not user_id.isdigit():
        return jsonify({'error': 'Invalid user_id'}), 400

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Use parameterized query to prevent SQL Injection
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({'user': user})
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
None

## Testing Recommendations
- Test valid and invalid user_id inputs.
- Test SQL injection payloads to ensure they are rejected or handled safely.

## Alternative Solutions

### Use ORM (e.g., SQLAlchemy) to abstract database queries and prevent SQL injection by design.
**Pros:** Less error-prone, Easier to write complex queries
**Cons:** Additional dependency, Learning curve


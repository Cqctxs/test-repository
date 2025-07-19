# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced string interpolation in SQL query with parameterized query using placeholders `?` and passed parameters as a tuple to execute function. Also validated that 'id' is an integer to prevent injection and malformed queries. This prevents attackers from executing arbitrary SQL commands via the 'id' query parameter.

## Security Notes
Always use parameterized queries to prevent SQL injection. Validate and sanitize all user inputs. Use database user with least privileges. Turn off debug mode in production.

## Fixed Code
```py
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('example.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user', methods=['GET'])
def get_user():
    user_id = request.args.get('id')
    try:
        user_id_int = int(user_id)
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid user id'}), 400

    conn = get_db_connection()
    # Use parameterized query to prevent SQL injection
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id_int,)).fetchone()
    conn.close()

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    return jsonify(dict(user))

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
- import sqlite3

## Testing Recommendations
- Test with valid and invalid user IDs.
- Attempt SQL injection payloads to verify blocking.
- Check that legitimate users retrieve data correctly.

## Alternative Solutions

### Use ORM frameworks like SQLAlchemy to handle queries safely.
**Pros:** Automatic injection protection, Easier for complex queries
**Cons:** Adds dependency and learning curve


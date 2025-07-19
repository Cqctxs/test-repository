# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Rewritten the raw SQL string interpolation to use parameterized queries replacing the vulnerable code. This effectively prevents SQL injection attacks by separating data from code in queries.

## Security Notes
Never build SQL queries using string interpolation with user inputs. Always use parameterization or prepared statements. Verify inputs further if possible.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    conn = get_db_connection()
    # Parameterized query to mitigate SQL injection
    query = 'SELECT * FROM users WHERE username = ?'
    user = conn.execute(query, (username,)).fetchone()
    conn.close()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(dict(user))

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- import sqlite3
- from flask import Flask, request, jsonify

## Testing Recommendations
- Inject common SQL injection payloads and confirm no data leakage or errors occur.
- Verify normal user queries work as expected.

## Alternative Solutions

### Use ORMs or database abstraction layers with built-in query safety.
**Pros:** Easier maintenance and added safety
**Cons:** Dependency and complexity


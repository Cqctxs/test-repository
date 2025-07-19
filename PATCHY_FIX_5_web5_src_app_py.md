# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Changed raw string interpolation in SQL query to parameterized query with '%s' placeholder and parameters passed as tuple. Added input validation ensuring 'id' parameter is an integer. This prevents attackers from injecting SQL code that could compromise the database.

## Security Notes
Use parameterized queries always when dealing with user inputs in SQL commands. Validate inputs for type and format. Use environment variables or configuration for database credentials, not hardcoded.

## Fixed Code
```py
from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname='mydb', user='user', password='password', host='localhost'
    )
    return conn

@app.route('/user', methods=['GET'])
def get_user():
    user_id = request.args.get('id')
    try:
        user_id_int = int(user_id)
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid user id'}), 400

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    # Use parameterized query to prevent SQL Injection
    cur.execute('SELECT * FROM users WHERE id = %s', (user_id_int,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    return jsonify(user)

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
- import psycopg2
- from psycopg2.extras import RealDictCursor

## Testing Recommendations
- Test with valid user ids.
- Attempt SQL injection via 'id' parameter to verify prevention.
- Check no impact on functionality.

## Alternative Solutions

### Use ORM like SQLAlchemy for safer queries and easier maintenance.
**Pros:** Better abstraction, Prevents SQL injection automatically
**Cons:** Extra dependency and code complexity


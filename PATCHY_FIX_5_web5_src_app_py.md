# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
The original code interpolated user input directly into the SQL statement, which allows SQL Injection. This fix parses and validates user input as integer, then uses a parameterized query with psycopg2 to safely query the database. This prevents injection attacks and ensures only valid inputs are processed.

## Security Notes
Always use parameterized queries or prepared statements when using user input in SQL queries. Validate inputs before database operations.

## Fixed Code
```py
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get_user')
def get_user():
    user_id = request.args.get('user_id')
    try:
        user_id_int = int(user_id)
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid user_id'}), 400

    conn = psycopg2.connect(dbname='yourdb', user='youruser', password='yourpass', host='localhost')
    cur = conn.cursor()
    # Use parameterized queries to prevent SQL Injection
    cur.execute('SELECT * FROM users WHERE id=%s', (user_id_int,))
    result = cur.fetchone()
    cur.close()
    conn.close()

    if result:
        return jsonify({'user': result})
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
- import psycopg2

## Testing Recommendations
- Test various user_id inputs, including invalid and SQL injection attempts.
- Ensure only valid and expected data is returned or error responses are returned appropriately.

## Alternative Solutions

### Use an ORM like SQLAlchemy as an abstraction to prevent direct SQL manipulation.
**Pros:** Safe database operations, Less error-prone
**Cons:** Adds dependencies and complexity


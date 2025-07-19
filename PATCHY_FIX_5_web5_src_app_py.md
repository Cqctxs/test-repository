# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Original code constructed SQL statements by interpolating user input directly into the query string, opening the database to SQL injection attacks. This fix changes to use parameterized queries with psycopg2, where the query includes placeholders (%s) and the user input is passed as a tuple parameter. This ensures that user input does not alter the query syntax and prevents injection.

## Security Notes
Never trust client input for constructing SQL queries. Always use parameterized queries or ORM features to avoid injection vectors. Validate and sanitize inputs where applicable. Turn off debug mode in production.

## Fixed Code
```py
import psycopg2
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

DB_CONFIG = {
    'dbname': 'mydb',
    'user': 'dbuser',
    'password': 'dbpass',
    'host': 'localhost'
}

@app.route('/search')
def search_users():
    name = request.args.get('name')
    if not name:
        abort(400, 'Name parameter is required')

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        # Use parameterized query
        cursor.execute('SELECT id, name, email FROM users WHERE name = %s', (name,))
        results = cursor.fetchall()
        users = [{'id': r[0], 'name': r[1], 'email': r[2]} for r in results]
        cursor.close()
        conn.close()
        return jsonify(users)
    except Exception as e:
        abort(500, f'Database error: {e}')

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
- import psycopg2

## Testing Recommendations
- Test with normal name queries.
- Test for attempted injection payloads to verify protection.
- Verify error handling on DB connection failures.

## Alternative Solutions

### Switch to using an ORM, e.g. SQLAlchemy, which helps automatically handle query sanitization.
**Pros:** Less error prone, Easier to maintain complex queries
**Cons:** Requires learning and adding dependency


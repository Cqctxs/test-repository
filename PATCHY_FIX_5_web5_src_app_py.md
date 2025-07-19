# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced string interpolation in SQL query construction with use of parameterized query ('%s' placeholders) and passing parameters as a tuple for psycopg2. This prevents SQL Injection by preventing user input from being treated as executable SQL code.

## Security Notes
Always prefer parameterized queries and validate inputs. Never concatenate user inputs directly into SQL statements.

## Fixed Code
```py
# Fixed SQL Injection in web5/src/app.py using parameterized queries
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)
db_conn_params = {
    'dbname': 'mydatabase',
    'user': 'dbuser',
    'password': 'strongpassword',
    'host': 'localhost',
}

@app.route('/user')
def get_user():
    user_id = request.args.get('id', '')
    try:
        conn = psycopg2.connect(**db_conn_params)
        cursor = conn.cursor()
        # Use parameterized query with %s placeholders
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        if user_data:
            return jsonify({'id': user_data[0], 'name': user_data[1]})
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': 'Database error'}), 500

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- psycopg2
- flask

## Testing Recommendations
- Verify SQL injection attempts fail.
- Test normal and edge case inputs for the user ID parameter.

## Alternative Solutions

### Use an ORM like Django ORM or SQLAlchemy for safer database access.
**Pros:** Less prone to injection, Easier to maintain
**Cons:** Adds dependencies and complexity


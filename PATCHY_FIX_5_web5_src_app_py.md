# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced unsafe string interpolation in SQL query with parameterized query. psycopg2's execute method is used with parameter tuple to securely include user input, preventing SQL injection attacks.

## Security Notes
Always use parameterized queries and never embed user input directly into SQL strings. Use database adapters' parameter substitution features consistently.

## Fixed Code
```py
import psycopg2

conn = psycopg2.connect(dbname='example', user='user', password='password', host='localhost')
cursor = conn.cursor()

user_id = 'some_user_input'

# Use parameterized query to prevent SQL Injection
query = 'SELECT * FROM users WHERE id = %s'
cursor.execute(query, (user_id,))

rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.close()
conn.close()
```

## Additional Dependencies
- import psycopg2

## Testing Recommendations
- Test with SQL injection strings in user_id to verify safe handling.
- Test regular queries for correctness.

## Alternative Solutions

### Use ORM frameworks (e.g., SQLAlchemy) which automatically handle query bindings
**Pros:** Improves developer productivity and security
**Cons:** Adds abstraction layer


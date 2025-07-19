# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced unsafe string formatting in SQL query with parameterized query using placeholders and passing user input as parameter. This prevents SQL injection by properly escaping user input.

## Security Notes
Always use parameterized queries (prepared statements) for any database queries involving user input. Never concatenate or format user input directly into SQL queries.

## Fixed Code
```py
import sqlite3

# Connect to database
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# User input
user_id = input('Enter user id: ')

# Securely use parameterized query to prevent SQL Injection
query = 'SELECT * FROM users WHERE id = ?'
cursor.execute(query, (user_id,))
result = cursor.fetchall()

print(result)

conn.close()
```

## Additional Dependencies
- import sqlite3

## Testing Recommendations
- Test with malicious user id input (e.g., SQL syntax) to verify query is safe.
- Test normal queries to confirm correct results.

## Alternative Solutions

### Use ORM frameworks which handle query parameters automatically
**Pros:** Simplifies query building, Reduces risk of injection
**Cons:** Adds abstraction layer


# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
The original code constructed SQL queries using string interpolation or concatenation with user input, leading to SQL injection vulnerabilities. The fix replaces query construction with parameterized queries using placeholders (%s) and separate parameters. This prevents user input from being treated as SQL code.

## Security Notes
Always use parameterized queries with the database adapter's API. Validate inputs even if parameterized queries are used. Avoid manually building queries from untrusted data.

## Fixed Code
```py
import psycopg2


def fetch_order_details(order_id):
    conn = psycopg2.connect(dbname='mydb', user='user', password='pass', host='localhost')
    cursor = conn.cursor()
    # Use parameterized queries to prevent SQL injection
    cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
    order = cursor.fetchone()
    cursor.close()
    conn.close()
    return order

# Example usage
order_info = fetch_order_details(user_supplied_order_id)

```

## Additional Dependencies
- import psycopg2

## Testing Recommendations
- Validate normal query works correctly
- Attempt SQL injection patterns and verify they do not alter query logic

## Alternative Solutions

### Use an ORM like SQLAlchemy to abstract away SQL and parameter binding.
**Pros:** Reduces likelihood of injection errors, Easier to maintain
**Cons:** Adds dependency, Requires learning curve


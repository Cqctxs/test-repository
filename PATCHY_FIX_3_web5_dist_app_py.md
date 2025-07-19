# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced direct string interpolation in SQL query with parameterized query using `?` placeholder and passing user input as parameter tuple. Added input validation to ensure 'id' is digit only. This prevents SQL injection by not concatenating user input directly to SQL query.

## Security Notes
Always use parameterized queries or prepared statements when querying databases with user input. Validate inputs for expected format and types. Avoid string formatting or concatenation for SQL commands with user data.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/user')
def get_user():
    user_id = request.args.get('id')

    if not user_id or not user_id.isdigit():
        return jsonify({'error': 'Invalid user ID'}), 400

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Use parameterized query to prevent SQL injection
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({'id': user[0], 'name': user[1], 'email': user[2]})
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
None

## Testing Recommendations
- Test endpoint with valid and invalid user IDs
- Attempt SQL injection payloads to verify they are not executed
- Verify normal responses for valid users and error for invalid users

## Alternative Solutions

### Use an ORM library like SQLAlchemy that inherently uses safe query building
**Pros:** Provides abstraction and safety against SQL injections, Easier to maintain and extend
**Cons:** Adds dependency and slightly more complexity


# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Changed the vulnerable SQL query to use parameterized queries to avoid SQL injection by properly escaping and binding user input parameters.

## Security Notes
Always use parameterized queries or ORM tools to eliminate SQL injection risks. Never concatenate or format user input directly into SQL strings.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_account_info(account_id):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    # Secure parameterized query
    cursor.execute('SELECT * FROM accounts WHERE id = ?', (account_id,))
    data = cursor.fetchone()
    conn.close()
    return data

@app.route('/account', methods=['GET'])
def account():
    account_id = request.args.get('id')
    if not account_id:
        return jsonify({'error': 'Account ID required'}), 400
    data = get_account_info(account_id)
    if data is None:
        return jsonify({'error': 'Account not found'}), 404
    return jsonify({'account': data})

if __name__ == '__main__':
    app.run()
```

## Additional Dependencies
- import sqlite3

## Testing Recommendations
- Test normal and malicious account ID inputs to verify prevention of injection.
- Verify account data is returned correctly for valid inputs.

## Alternative Solutions

### Use an ORM like SQLAlchemy for query construction and execution.
**Pros:** Automatic query parameterization., Easier to maintain complex queries.
**Cons:** undefined


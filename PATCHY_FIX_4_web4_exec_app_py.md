# Security Fix for web4/exec/app.py

**Vulnerability Type:** NOSQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Removed use of $where and f-string JavaScript injection. Now we validate username is alphanumeric and use a standard find_one() filter, preventing execution of arbitrary JS.

## Security Notes
If more complex queries needed, build them via PyMongo query operators, never string-concatenate raw input.

## Fixed Code
```py
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')
db = client.mydb

@app.route('/find', methods=['GET'])
def find_user():
    username = request.args.get('username', '')
    # Input allowlist: only alphanumeric
    if not username.isalnum():
        return jsonify({'error':'Invalid username'}), 400
    # Use parameterized filter without $where
    user = db.users.find_one({'username': username}, {'_id': 0, 'password': 0})
    if not user:
        return jsonify({'error':'Not found'}), 404
    return jsonify({'user': user})

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
None

## Testing Recommendations
- Attempt injection payload as username and expect 400
- Lookup valid user and verify data returned

## Alternative Solutions

### Escape and whitelist query operators
**Pros:** More flexible
**Cons:** Complex to maintain


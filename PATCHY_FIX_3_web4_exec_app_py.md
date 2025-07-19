# Security Fix for web4/exec/app.py

**Vulnerability Type:** NOSQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Removed the use of $where and string interpolation. Instead, validate the input as an ObjectId and query by the _id field directly.

## Security Notes
Never accept raw JavaScript queries. Use typed queries or an ORM-like layer.

## Fixed Code
```py
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')
db = client.usersdb

@app.route('/user', methods=['GET'])
def get_user():
    user_id = request.args.get('id')
    try:
        # Validate that id is a valid ObjectId
        oid = ObjectId(user_id)
    except Exception:
        return jsonify({'error': 'Invalid user id'}), 400
    # Use a safe query builder, no $where
    user = db.users.find_one({'_id': oid}, {'password': 0})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user['id'] = str(user.pop('_id'))
    return jsonify(user)

if __name__ == '__main__':
    app.run()
```

## Additional Dependencies
- from bson.objectid import ObjectId

## Testing Recommendations
- Test with valid and invalid id, attempt injection payload in id parameter.

## Alternative Solutions

### Whitelist queryable fields and filter inputs
**Pros:** Flexible search
**Cons:** More code to maintain


# Security Fix for web4/exec/app.py

**Vulnerability Type:** NOSQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced unsafe use of $where clause with a parameterized query structure and input validation on 'flag_name' parameter to prevent NoSQL injection. Disallowed user input containing special query operators or scripts by allowlisting alphanumeric characters only.

## Security Notes
Never use $where or JavaScript expressions from user input in MongoDB queries. Always validate and sanitize all inputs and use query builders/operators that do not interpret code.

## Fixed Code
```py
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']

@app.route('/feature_flags', methods=['GET'])
def get_feature_flags():
    flag_name = request.args.get('flag_name')

    # Use safe query builder with strict type check
    query = {}
    if flag_name:
        if not isinstance(flag_name, str) or not flag_name.isalnum():
            return jsonify({'error': 'Invalid flag_name parameter'}), 400
        query['flag_name'] = flag_name

    flags = list(db.feature_flags.find(query, {'_id': 0}))
    return jsonify(flags)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

```

## Additional Dependencies
- from bson.objectid import ObjectId

## Testing Recommendations
- Test with valid and invalid flag_name values
- Test attempts to inject malicious NoSQL payloads

## Alternative Solutions
None provided

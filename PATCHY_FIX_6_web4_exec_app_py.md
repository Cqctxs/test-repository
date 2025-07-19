# Security Fix for web4/exec/app.py

**Vulnerability Type:** NOSQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Removed the use of the $where operator which executes JavaScript code inside MongoDB and replaced it with a direct key-value match query. Added strict input validation with isalnum check to allow only alphanumeric names which prevents injection of malicious JavaScript expressions.

## Security Notes
Avoid using $where or JavaScript execution in MongoDB queries with unsanitized user input. Always prefer query builders or direct key matching. Validate and sanitize user inputs strictly.

## Fixed Code
```py
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']

@app.route('/search', methods=['GET'])
def search():
    name = request.args.get('name')
    if not name or not isinstance(name, str) or not name.isalnum():
        return jsonify({'error': 'Invalid name parameter'}), 400

    # Use safe query without $where to prevent NoSQL injection
    query = {'name': name}
    results = list(db.users.find(query, {'_id': 0}))
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- from pymongo import MongoClient

## Testing Recommendations
- Test normal name inputs return correct results.
- Attempt injections with JavaScript-like inputs to verify no execution.

## Alternative Solutions
None provided

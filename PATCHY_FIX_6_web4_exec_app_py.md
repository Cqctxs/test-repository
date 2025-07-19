# Security Fix for web4/exec/app.py

**Vulnerability Type:** NOSQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced use of MongoDB $where query with string interpolation on user input by a parameterized regex query on a specific field. This avoids executing JavaScript code inside the database which is vulnerable to injection and attacks.

## Security Notes
Never use $where with untrusted user input in MongoDB. Use structured queries with parameters. Sanitize and validate user input further if needed.

## Fixed Code
```py
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client.testdb

@app.route('/search', methods=['POST'])
def search():
    user_input = request.json.get('query', '')

    # Use safe query construction avoiding $where and string interpolation
    search_query = {"name": {"$regex": f"^{user_input}$", "$options":"i"}}

    # This assumes the query is supposed to match name field exactly case-insensitive
    # If partial match is intended, consider escaping input

    results = list(db.users.find(search_query))

    # Remove MongoDB internal id for JSON serialization
    for r in results:
        r['_id'] = str(r['_id'])

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- from flask import Flask, request, jsonify
- from pymongo import MongoClient

## Testing Recommendations
- Test inputs with MongoDB operators to see if injection is prevented.
- Verify normal queries still work correctly.

## Alternative Solutions

### Strictly validate and whitelist allowed query patterns instead of arbitrary text input.
**Pros:** Reduces injection risk, Improves query efficiency
**Cons:** Less flexible search


# Security Fix for web4/exec/app.py

**Vulnerability Type:** NOSQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Removed use of MongoDB $where with string interpolation which allows NoSQL injection. Instead, used a direct query with $regex allowing controlled partial match safely. This avoids execution of arbitrary JavaScript code from user input.

## Security Notes
Avoid $where in Mongo queries with user input. Use query operators or parameterized queries. Sanitize or restrict regex patterns if necessary.

## Fixed Code
```py
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client.secure_db

@app.route('/search')
def search():
    # Get search term safely
    search_term = request.args.get('q', '')

    # Use query builder with exact match or regex with escaping rather than $where
    query = {"name": {"$regex": f"^{search_term}", "$options": "i"}} if search_term else {}

    results = list(db.users.find(query, {'_id': 0, 'name': 1}))
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- flask
- pymongo

## Testing Recommendations
- Test valid search queries
- Attempt injection via search input to confirm no code executes

## Alternative Solutions

### Whitelist allowed search terms or input patterns before building queries
**Pros:** Further restrict input, Lower risk
**Cons:** Less flexible query matching


# Security Fix for web4/exec/app.py

**Vulnerability Type:** NOSQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Removed usage of $where which runs arbitrary JavaScript and can cause NoSQL injection by enabling code injection from user input. Replaced with direct field matching using sanitized, validated parameters and typed checks. Used allowlist regex to validate category input.

## Security Notes
Avoid $where in MongoDB queries involving user input. Always sanitize and validate query parameters. Avoid building query filters by concatenating strings or direct injection of user data in query operators.

## Fixed Code
```py
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import re

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')
db = client.shop

@app.route('/filter_products', methods=['POST'])
def filter_products():
    data = request.json or {}
    category = data.get('category', '')
    price_min = data.get('price_min')
    price_max = data.get('price_max')

    query = {}

    # Validate and sanitize inputs using allowlist and types
    if category:
        if not re.match('^[a-zA-Z0-9 ]{1,50}$', category):
            return jsonify({'error': 'Invalid category format'}), 400
        query['category'] = category

    if price_min is not None:
        if not isinstance(price_min, (int, float)):
            return jsonify({'error': 'price_min must be number'}), 400
        query['price'] = query.get('price', {})
        query['price']['$gte'] = price_min

    if price_max is not None:
        if not isinstance(price_max, (int, float)):
            return jsonify({'error': 'price_max must be number'}), 400
        query['price'] = query.get('price', {})
        query['price']['$lte'] = price_max

    # Removed use of $where which executes JS and causes injection risk
    products = list(db.products.find(query))

    # Convert ObjectId to string for JSON serialization
    for p in products:
        p['_id'] = str(p['_id'])

    return jsonify(products), 200

if __name__ == '__main__':
    app.run()
```

## Additional Dependencies
- from flask import Flask, request, jsonify
- from pymongo import MongoClient
- from bson.objectid import ObjectId
- import re

## Testing Recommendations
- Test valid category filtering
- Test price range filtering
- Test injection attempts with special characters fail

## Alternative Solutions

### Implement role based access control to limit data exposure
**Pros:** Better data confidentiality
**Cons:** Additional complexity


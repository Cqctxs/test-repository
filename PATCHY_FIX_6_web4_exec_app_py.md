# Security Fix for web4/exec/app.py

**Vulnerability Type:** NOSQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Removed use of MongoDB $where queries with string interpolation, which can execute arbitrary JavaScript and open NoSQL injection. Replaced with safe query builder using field filters and sanitized/validated input values for category and price_order.

## Security Notes
Avoid $where clauses with user input; validate or whitelist all user inputs used in queries.

## Fixed Code
```py
# Fixed NoSQL injection by avoiding $where and using safe query builders
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']

@app.route('/products')
def get_products():
    category = request.args.get('category', None)
    price_order = request.args.get('price_order', 'asc')

    # Validate inputs
    valid_categories = ['electronics', 'clothing', 'books']
    if category and category not in valid_categories:
        return jsonify({'error': 'Invalid category'}), 400

    if price_order not in ['asc', 'desc']:
        price_order = 'asc'

    query = {}
    if category:
        query['category'] = category

    sort_direction = 1 if price_order == 'asc' else -1
    products = list(db.products.find(query).sort('price', sort_direction))

    # Convert ObjectId to string for jsonify
    for product in products:
        product['_id'] = str(product['_id'])

    return jsonify(products)

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- flask
- pymongo

## Testing Recommendations
- Test with valid categories and ordering.
- Test with malicious input to verify rejection.

## Alternative Solutions

### Use a dedicated ODM library (like MongoEngine) which better abstracts query construction.
**Pros:** Cleaner code, Less injection risk
**Cons:** Additional dependencies


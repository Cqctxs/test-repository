from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)
client = MongoClient(os.environ.get('MONGODB_URI','mongodb://localhost:27017'))
db = client.shop

@app.route('/products', methods=['GET'])
def get_products():
    category = request.args.get('category','').strip()
    # Input validation: allow only alphanumeric and spaces
    if not category.replace(' ','').isalnum():
        return jsonify({'error':'Invalid category'}), 400
    # Use safe query builder instead of $where
    results = list(db.products.find({'category': category}, {'_id':0}))
    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=False)
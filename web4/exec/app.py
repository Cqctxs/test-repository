from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
import re

app = Flask(__name__)
client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://localhost:27017'))
db = client.get_database('appdb')
products = db.products

@app.route('/search', methods=['GET'])
def search():
    q = request.args.get('q', '')
    # Sanitize input: allow only letters, numbers, spaces
    sanitized = re.sub(r'[^A-Za-z0-9 ]', '', q)
    # Use parameterized regex query instead of $where
    cursor = products.find({'name': {'$regex': sanitized, '$options': 'i'}, 'is_published': True})
    results = []
    for doc in cursor:
        results.append({'id': str(doc['_id']), 'name': doc['name'], 'price': doc['price']})
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
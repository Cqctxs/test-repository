from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)
client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017'))
db = client.myapp
products = db.products

# Allow only specific statuses
ALLOWED_STATUSES = {'available', 'sold', 'pending'}

@app.route('/products', methods=['GET'])
def get_products():
    status = request.args.get('status', 'available')
    if status not in ALLOWED_STATUSES:
        return jsonify({'error': 'Invalid status filter'}), 400

    # Use direct field match instead of $where
    cursor = products.find({'status': status})
    result = []
    for doc in cursor:
        doc['_id'] = str(doc['_id'])
        result.append(doc)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5004)))
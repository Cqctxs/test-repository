from flask import Flask, request, jsonify, abort
from pymongo import MongoClient
import os

app = Flask(__name__)
client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://localhost:27017'))
db = client.get_database('mydb')

@app.route('/products', methods=['GET'])
def get_products():
    name = request.args.get('name', '')
    # Validate input to alphanumeric only
    if not isinstance(name, str) or not name.isalnum():
        abort(400, 'Invalid product name')
    # Use direct field match, no $where
    products = list(db.products.find({'name': name}, {'_id': 0, 'name': 1, 'price': 1}))
    return jsonify({'products': products})

if __name__ == '__main__':
    app.run(debug=False)

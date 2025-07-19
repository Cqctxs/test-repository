from flask import Flask, request, jsonify
from pymongo import MongoClient
import re

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
collection = db['users']

@app.route('/search', methods=['GET'])
def search():
    username = request.args.get('username', '').strip()
    # Input validation: allow only alphanumeric and underscores
    if not re.match(r'^\w{1,30}$', username):
        return jsonify({'error': 'Invalid username parameter'}), 400
    # Use parameterized query style: avoid $where entirely
    user = collection.find_one({'username': username}, {'_id': 0, 'username': 1, 'email': 1})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

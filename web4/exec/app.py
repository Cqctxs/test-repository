# web4/exec/app.py - Secure MongoDB query without $where
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['appdb']
users = db['users']

@app.route('/find', methods=['GET'])
def find_user():
    username = request.args.get('username', '')
    # Validate username: only allow alphanumeric and underscores
    if not username.isalnum():
        return jsonify({'error':'Invalid username'}), 400

    # Safe query using field selector
    user = users.find_one({'username': username}, {'_id':0, 'username':1, 'email':1})
    if not user:
        return jsonify({'error':'Not found'}), 404
    return jsonify(user)

if __name__ == '__main__':
    app.run(debug=False)
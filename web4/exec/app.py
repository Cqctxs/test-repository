from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client.users_db

@app.route('/user', methods=['GET'])
def get_user():
    username = request.args.get('username', '')
    # Input validation: allow only alphanumeric
    if not username.isalnum():
        return jsonify({'error':'Invalid username'}), 400

    # Safe query without $where
    user = db.users.find_one({'username': username}, {'_id': 0, 'username': 1, 'email': 1})
    if not user:
        return jsonify({'error':'User not found'}), 404
    return jsonify(user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

# web4/exec/app.py
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']

@app.route('/user', methods=['GET'])
def get_user():
    username = request.args.get('username', '')
    # Validate input: allow only alphanumeric usernames
    if not username.isalnum():
        return jsonify({'error': 'Invalid username format'}), 400
    # Use direct field match instead of $where
    user = db.users.find_one({'username': username}, {'_id': 0, 'password': 0})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

if __name__ == '__main__':
    app.run(debug=False)

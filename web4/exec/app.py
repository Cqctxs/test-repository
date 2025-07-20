# web4/exec/app.py
from flask import Flask, request, jsonify
from pymongo import MongoClient
import re

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client.users

@app.route('/search', methods=['GET'])
def search():
    username = request.args.get('username', '')
    # allow only alphanumeric usernames (whitelist)
    if not re.match(r'^[A-Za-z0-9_]+$', username):
        return jsonify({'error': 'Invalid username'}), 400
    # safe query without $where
    user = db.profiles.find_one({'username': username}, {'_id': 0, 'username':1, 'email':1})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

if __name__ == '__main__':
    app.run(debug=False)
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')
db = client['users_db']
users = db['users']

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error':'Missing fields'}),400

    # Parameterized query using dict filter
    user = users.find_one({'username': username, 'password': password})
    if user:
        return jsonify({'status':'ok'})
    return jsonify({'status':'fail'}),401

if __name__ == '__main__':
    app.run()
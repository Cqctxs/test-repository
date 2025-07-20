from flask import Flask, request, jsonify, abort
from pymongo import MongoClient
import re

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
collection = db['users']

@app.route('/find', methods=['GET'])
def find_user():
    username = request.args.get('username')
    if not username or not re.match(r'^[a-zA-Z0-9_]{3,30}$', username):
        abort(400, 'Invalid username')
    # Parameterized query: avoid $where, use direct filter
    user = collection.find_one({'username': username}, {'_id': 0, 'username':1, 'email':1})
    if not user:
        abort(404, 'User not found')
    return jsonify(user)

if __name__ == '__main__':
    app.run(debug=False)

from flask import Flask, request, jsonify, abort
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')
db = client.mydb

@app.route('/users', methods=['GET'])
def get_users():
    name = request.args.get('name', '')
    # Validate that name is a safe string
    if not isinstance(name, str) or not name.isalnum():
        abort(400, 'Invalid name')
    # Use a direct equality filter instead of $where to prevent injection
    docs = db.users.find({'name': name}, {'_id': 0, 'name': 1, 'email': 1})
    users = list(docs)
    return jsonify(users)

if __name__ == '__main__':
    app.run()
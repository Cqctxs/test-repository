from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
users = db['users']

@app.route('/user/<user_id>')
def get_user(user_id):
    # Validate that user_id is a valid ObjectId
    try:
        oid = ObjectId(user_id)
    except Exception:
        return jsonify({'error': 'Invalid user ID'}), 400

    # Use a safe query builder without $where
    user = users.find_one({'_id': oid}, {'_password': 0})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user['_id'] = str(user['_id'])
    return jsonify(user)

if __name__ == '__main__':
    app.run()
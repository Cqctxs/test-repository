from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')
db = client.mydb

@app.route('/user', methods=['GET'])
def get_user():
    user_id = request.args.get('id')
    # Input validation: only accept valid ObjectId hex strings
    try:
        oid = ObjectId(user_id)
    except Exception:
        return jsonify({'error': 'Invalid user id'}), 400
    # Use parameterized query API, avoid $where or string interpolation
    user = db.users.find_one({'_id': oid}, {'password': 0})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user['id'] = str(user['_id'])
    del user['_id']
    return jsonify(user)

if __name__ == '__main__':
    app.run()
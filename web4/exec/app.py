from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client.mydb

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    # Validate format of user_id
    try:
        oid = ObjectId(user_id)
    except Exception:
        return jsonify({'error':'Invalid user id'}), 400
    user = db.users.find_one({'_id': oid})
    if not user:
        return jsonify({'error':'User not found'}), 404
    user['_id'] = str(user['_id'])
    return jsonify(user)

if __name__ == '__main__':
    app.run()

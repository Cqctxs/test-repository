from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)
client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017'))
db = client['users_db']

@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    # Use parameterized query, avoid $where entirely
    user = db.users.find_one({'username': username}, {'_id': 0, 'password': 0})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

if __name__ == '__main__':
    app.run(debug=False)
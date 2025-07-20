from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client.mydb

@app.route('/user', methods=['GET'])
def get_user():
    # Retrieve 'name' parameter and sanitize via direct field query
    username = request.args.get('name', '')
    # Enforce allowed character set (alphanumeric plus underscore)
    if not username or not username.isalnum():
        return jsonify({'error': 'Invalid username'}), 400
    user = db.users.find_one({'name': username}, {'_id': 0, 'name': 1, 'email': 1})
    if not user:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(user), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
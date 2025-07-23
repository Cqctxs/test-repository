from flask import Flask, request, jsonify, abort
from pymongo import MongoClient
import os

app = Flask(__name__)
client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://localhost:27017'))
db = client.get_database('mydb')

@app.route('/find_user', methods=['GET'])
def find_user():
    name = request.args.get('name', '', type=str)
    if not name or len(name) > 100:
        abort(400, 'Invalid name parameter')
    # Use parameterized filter instead of $where
    user = db.users.find_one({ 'name': name }, { '_id': 0, 'name': 1, 'email': 1 })
    if not user:
        abort(404, 'User not found')
    return jsonify(user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
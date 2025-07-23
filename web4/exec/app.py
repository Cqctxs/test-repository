import re
from flask import Flask, request, jsonify, abort
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']

@app.route('/user', methods=['GET'])
def get_user():
    username = request.args.get('username', '')
    # Allow only alphanumeric and underscore, length 3–30
    if not re.fullmatch(r'[A-Za-z0-9_]{3,30}', username):
        abort(400, description="Invalid username parameter")
    # Safe key‐value query (no $where)
    user = db.users.find_one({'username': username}, {'_id': 0})
    if not user:
        abort(404, description="User not found")
    return jsonify(user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
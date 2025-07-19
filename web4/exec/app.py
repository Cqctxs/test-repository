from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client.mydb

@app.route('/search', methods=['GET'])
def search_users():
    # Validate and sanitize input
    username = request.args.get('username', '').strip()
    if not username or len(username) > 50:
        return jsonify({'error': 'Invalid username'}), 400

    # Use parameterized query: exact match on username field
    results = list(db.users.find({'username': username}, {'_id': 0}))
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=False)

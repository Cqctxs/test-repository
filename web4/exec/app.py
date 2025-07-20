from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')
db = client['mydb']
collection = db['mycollection']

# Define an allowlist of fields that can be queried
ALLOWED_FIELDS = {'name', 'age', 'email'}

@app.route('/find', methods=['GET'])
def find():
    field = request.args.get('field', '').strip()
    value = request.args.get('value', '').strip()

    # 1. Validate the field against the allowlist
    if field not in ALLOWED_FIELDS:
        return jsonify({"error": "Field not allowed"}), 400

    # 2. Build a safe query without using $where or code execution
    query = {field: value}
    try:
        results = list(collection.find(query, {"_id": 0}))
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
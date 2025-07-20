import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DATABASE = 'users.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json() or {}
    keyword = data.get('keyword', '')
    # Basic validation: limit length and characters
    if not isinstance(keyword, str) or len(keyword) > 50 or not keyword.isalnum():
        return jsonify({'error': 'Invalid search term'}), 400
    db = get_db()
    # Use LIKE with parameter binding
    param = f"%{keyword}%"
    rows = db.execute('SELECT id, username FROM users WHERE username LIKE ?', (param,)).fetchall()
    return jsonify([dict(r) for r in rows]), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
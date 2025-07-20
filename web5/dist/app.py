import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_PATH = 'users.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    # Only allow alphanumeric usernames
    if not username.isalnum():
        return jsonify({'error': 'Invalid username'}), 400
    db = get_db()
    # Use parameterized query to prevent SQL injection
    cur = db.execute('SELECT id, username, email FROM users WHERE username = ?', (username,))
    row = cur.fetchone()
    if not row:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(dict(row)), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
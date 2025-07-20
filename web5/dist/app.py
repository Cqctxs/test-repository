import sqlite3
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'app.db')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username', '')
    password = data.get('password', '')
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    # Parameterized query to prevent SQL injection
    cur.execute('SELECT id, username FROM users WHERE username = ? AND password = ?', (username, password))
    row = cur.fetchone()
    conn.close()
    if row:
        return jsonify({'id': row['id'], 'username': row['username']})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9000)

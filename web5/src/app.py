from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
db_path = 'app.db'

def get_db():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json() or {}
    username = data.get('username','')
    password = data.get('password','')
    if not username or not password:
        return jsonify({'error':'Missing credentials'}), 400
    conn = get_db()
    cursor = conn.execute(
        'SELECT id, username FROM users WHERE username = ? AND password = ?',
        (username, password)
    )
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({'id': user['id'], 'username':user['username']}), 200
    return jsonify({'error':'Invalid username/password'}), 401

if __name__ == '__main__':
    app.run(debug=False)

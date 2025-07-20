import sqlite3
from flask import Flask, request, jsonify, abort

app = Flask(__name__)
DATABASE = 'users.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username', '')
    password = data.get('password', '')

    # Input validation
    if not isinstance(username, str) or not username.isalnum():
        abort(400, 'Invalid username')
    if not isinstance(password, str) or len(password) < 8:
        abort(400, 'Invalid password')

    conn = get_db()
    cursor = conn.cursor()
    # Parameterized query
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row and verify_password(password, row['password_hash']):
        token = generate_token(username)
        return jsonify({'token': token})
    abort(401, 'Authentication failed')

if __name__ == '__main__':
    app.run()
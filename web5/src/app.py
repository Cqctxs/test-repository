import os
import sqlite3
from flask import Flask, request, jsonify, g, abort

app = Flask(__name__)
DB_PATH = os.getenv('SQLITE_PATH', 'users.db')

def get_db():
    if not hasattr(g, 'db'):
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        abort(400, description='username and password required')

    db = get_db()
    # Parameterized query prevents SQL injection
    cur = db.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
    user = cur.fetchone()
    if not user:
        abort(401, description='Invalid credentials')
    # Verify password hash here (omitted for brevity)
    return jsonify({'id': user['id'], 'message': 'Logged in'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT',5003)))
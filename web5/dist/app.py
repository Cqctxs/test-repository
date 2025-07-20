from flask import Flask, request, jsonify, abort
import sqlite3
import os

app = Flask(__name__)
DATABASE = os.path.join(os.path.dirname(__file__), 'users.db')

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user', methods=['GET'])
def get_user():
    username = request.args.get('username', '')
    # Basic input validation
    if not username.isalnum():
        abort(400, 'Invalid username format')

    conn = get_db()
    cursor = conn.cursor()
    # Use parameterized query to prevent SQL injection
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user is None:
        abort(404, 'User not found')
    return jsonify({k: user[k] for k in user.keys()})

if __name__ == '__main__':
    app.run()
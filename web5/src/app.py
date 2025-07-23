from flask import Flask, request, jsonify, abort
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('user', '')
    # Basic validation: non-empty, max length 50
    if not username or len(username) > 50:
        abort(400, description="Invalid username input")
    conn = get_db_connection()
    cur = conn.cursor()
    # Parameterized query prevents SQL injection
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if not row:
        abort(404, description="User not found")
    # Convert Row to dict and return JSON
    user = dict(row)
    return jsonify(user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
# web5/dist/app.py - Parameterized query to prevent SQL injection
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user', methods=['GET'])
def get_user():
    user_id = request.args.get('id')
    try:
        uid = int(user_id)
    except (TypeError, ValueError):
        return jsonify({'error':'Invalid user id'}), 400

    conn = get_db()
    # Use parameterized query
    cur = conn.execute('SELECT id, name, email FROM users WHERE id = ?', (uid,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return jsonify({'error':'User not found'}), 404
    return jsonify(dict(row))

if __name__ == '__main__':
    app.run(debug=False)
# web5/dist/app.py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('example.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user/<int:user_id>')
def get_user(user_id):
    conn = get_db()
    # parameterized query to prevent SQL injection
    cur = conn.execute('SELECT id, username, email FROM users WHERE id = ?', (user_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return jsonify(dict(row))
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=False)
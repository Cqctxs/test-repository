import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user/<int:user_id>')
def get_user(user_id):
    conn = get_db()
    # Parameterized query prevents injection and enforces integer type
    cursor = conn.execute('SELECT id, username, email FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify(dict(user))
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run()
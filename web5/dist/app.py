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
    cursor = conn.cursor()
    # Use parameterized query to prevent SQL injection
    cursor.execute('SELECT id, username, email FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify(dict(row))
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=False)

import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user/<int:user_id>')
def get_user(user_id):
    conn = get_db_connection()
    # Use parameterized query to avoid SQL injection
    cursor = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({key: user[key] for key in user.keys()})
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run()
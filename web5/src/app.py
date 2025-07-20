# web5/src/app.py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_PATH = 'users.db'

@app.route('/profile', methods=['GET'])
def profile():
    username = request.args.get('username', '')
    if not username:
        return jsonify({'error': 'username required'}), 400
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # Parameterized query to avoid injection
    cursor.execute('SELECT username, email FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'username': user['username'], 'email': user['email']})

if __name__ == '__main__':
    app.run(debug=False)

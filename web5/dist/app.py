# web5/dist/app.py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB = 'users.db'

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    username = data.get('username', '')
    password = data.get('password', '')
    # Basic input validation
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    # Use parameterized query to prevent SQL injection
    cursor.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, password))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=False)

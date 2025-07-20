from flask import Flask, request, jsonify, session
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = 'your-production-secret'

def get_db():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    conn = get_db()
    cursor = conn.cursor()
    # Parameterized query to prevent SQL injection
    cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    # Verify hashed password
    stored_hash = user['password_hash']
    if not bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Set secure session
    session['user_id'] = user['id']
    return jsonify({'message': 'Login successful'})

if __name__ == '__main__':
    app.run(debug=False)

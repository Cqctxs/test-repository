import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
# Use row factory for dict-like access
conn = sqlite3.connect('users.db', check_same_thread=False)
conn.row_factory = sqlite3.Row

@app.route('/users', methods=['GET'])
def get_user():
    username = request.args.get('username')
    if not username or not isinstance(username, str):
        return jsonify({'error': 'Invalid username'}), 400
    cursor = conn.cursor()
    # Parameterized query prevents SQL injection
    cursor.execute("SELECT id, username, email FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    if row:
        return jsonify(dict(row)), 200
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=False)

import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_PATH = 'users.db'

@app.route('/user', methods=['GET'])
def get_user():
    username = request.args.get('username', '')
    if not username:
        return jsonify({'error': 'username required'}), 400
    # Use parameterized query to avoid SQL injection
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (username,))
    row = cur.fetchone()
    conn.close()
    if row:
        return jsonify(dict(row))
    else:
        return jsonify({'error': 'not found'}), 404

if __name__ == '__main__':
    app.run(debug=False)
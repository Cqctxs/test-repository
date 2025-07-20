import sqlite3
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'app.db')

@app.route('/user', methods=['GET'])
def get_user():
    user_id = request.args.get('id', '')
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    # Use parameterized query
    cur.execute('SELECT id, username, email FROM users WHERE id = ?', (user_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return jsonify({'id': row['id'], 'username': row['username'], 'email': row['email']})
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)
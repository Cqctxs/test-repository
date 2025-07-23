from flask import Flask, request, jsonify, abort
import sqlite3

app = Flask(__name__)
DB_PATH = 'users.db'

@app.route('/user', methods=['GET'])
def get_user():
    name = request.args.get('name', '', type=str)
    if not name:
        abort(400, 'Missing name parameter')
    # Parameterized query to prevent SQL injection
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email FROM users WHERE name = ?', (name,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        abort(404, 'User not found')
    return jsonify(dict(row))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
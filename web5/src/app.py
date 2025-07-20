import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_PATH = 'users.db'

@app.route('/user', methods=['GET'])
def get_user():
    user_id = request.args.get('id')
    try:
        uid = int(user_id)
    except (TypeError, ValueError):
        return jsonify({'error': 'invalid id'}), 400
    # Parameterized query to avoid SQL injection
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE id = ?', (uid,))
    row = cur.fetchone()
    conn.close()
    if row:
        return jsonify(dict(row))
    else:
        return jsonify({'error': 'not found'}), 404

if __name__ == '__main__':
    app.run(debug=False)
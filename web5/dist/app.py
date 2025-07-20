import sqlite3
from flask import Flask, request, jsonify, abort

app = Flask(__name__)
db_path = 'data.db'

@app.route('/user', methods=['GET'])
def get_user():
    user_id = request.args.get('id')
    if not user_id or not user_id.isdigit():
        abort(400, 'Invalid user id')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Use parameterized query to prevent SQL injection
    cursor.execute('SELECT id, name, email FROM users WHERE id = ?', (int(user_id),))
    row = cursor.fetchone()
    conn.close()
    if not row:
        abort(404, 'User not found')
    return jsonify({'id': row[0], 'name': row[1], 'email': row[2]})

if __name__ == '__main__':
    app.run(debug=False)

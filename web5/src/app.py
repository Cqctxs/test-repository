import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
conn = sqlite3.connect('users.db', check_same_thread=False)
conn.row_factory = sqlite3.Row

@app.route('/user', methods=['GET'])
def get_user():
    user_id = request.args.get('id')
    if not user_id or not user_id.isdigit():
        return jsonify({'error': 'Invalid user ID'}), 400
    cursor = conn.cursor()
    # Parameterized query to prevent SQL injection
    cursor.execute("SELECT id, username, email FROM users WHERE id = ?", (int(user_id),))
    row = cursor.fetchone()
    if row:
        return jsonify(dict(row)), 200
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=False)

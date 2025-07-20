import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user', methods=['GET'])
def get_user():
    user_id = request.args.get('id')
    # Validate and cast to integer
    try:
        user_id_int = int(user_id)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid ID"}), 400

    conn = get_db_connection()
    cursor = conn.execute(
        'SELECT id, username, email FROM users WHERE id = ?',
        (user_id_int,)
    )
    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify(dict(row)), 200
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run()
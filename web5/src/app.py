import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db():
    db = sqlite3.connect('users.db')
    db.row_factory = sqlite3.Row
    return db

@app.route('/user', methods=['GET'])
def get_user():
    username = request.args.get('username', '')
    # Use parameterized query to mitigate SQL injection
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, username FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    db.close()
    if row:
        return jsonify({'id': row['id'], 'username': row['username']})
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=False)
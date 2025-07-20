import os
import sqlite3
from flask import Flask, g, jsonify, abort

app = Flask(__name__)
DATABASE = os.getenv('SQLITE_PATH', '/data/users.db')


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        g._database = db
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/user/<username>')
def get_user(username):
    # Use parameterized query to prevent SQL injection
    db = get_db()
    cursor = db.execute('SELECT id, username, role FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    if row is None:
        abort(404, description='User not found')
    return jsonify({
        'id': row['id'],
        'username': row['username'],
        'role': row['role']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5002)))
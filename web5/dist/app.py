import sqlite3
from flask import Flask, request, g, jsonify

app = Flask(__name__)
DATABASE = '/tmp/mydb.sqlite'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/user/<int:user_id>')
def get_user(user_id):
    # Use parameterized query to avoid SQL injection
    cursor = get_db().execute('SELECT id, username, email FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    if row is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(dict(row))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

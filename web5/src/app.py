import sqlite3
from flask import Flask, request, jsonify, abort

app = Flask(__name__)
db_path = 'data.db'

@app.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    if not name or len(name) > 100:
        abort(400, 'Invalid name')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Use parameterized LIKE to prevent injection
    cursor.execute('SELECT id, name FROM users WHERE name LIKE ?', (f'%{name}%',))
    rows = cursor.fetchall()
    conn.close()
    return jsonify([{'id': r[0], 'name': r[1]} for r in rows])

if __name__ == '__main__':
    app.run(debug=False)

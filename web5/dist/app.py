import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/search')
def search():
    name = request.args.get('name', '')
    # Input validation: limit length
    if len(name) > 100:
        return jsonify({'error': 'Parameter too long'}), 400
    conn = get_db()
    # Use parameterized query to prevent injection
    cursor = conn.execute('SELECT id, name, email FROM users WHERE name LIKE ?', (f'%{name}%',))
    rows = cursor.fetchall()
    results = [dict(row) for row in rows]
    conn.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run()
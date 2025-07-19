import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/search', methods=['GET'])
def search():
    q = request.args.get('q', '')
    # Input sanitization: limit length
    if len(q) > 100:
        return jsonify({'error':'Query too long'}), 400

    conn = get_db()
    # Parameterized query
    cursor = conn.execute('SELECT id, name, description FROM products WHERE name LIKE ?', ('%'+q+'%',))
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
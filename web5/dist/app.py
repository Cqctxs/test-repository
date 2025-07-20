from flask import Flask, request, jsonify
ing = Flask(__name__)
import sqlite3

def get_db():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

@ing.route('/search', methods=['GET'])
def search():
    term = request.args.get('term', '')
    conn = get_db()
    cursor = conn.cursor()
    # Use parameterized query to prevent SQL injection
    cursor.execute("SELECT id, name, description FROM items WHERE name LIKE ?", ('%' + term + '%',))
    rows = cursor.fetchall()
    results = [dict(row) for row in rows]
    return jsonify(results)

if __name__ == '__main__':
    ing.run(debug=False)

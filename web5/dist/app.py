import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/search')
def search():
    term = request.args.get('q', '')
    conn = get_db()
    # Use parameterized query to prevent SQL injection
    cursor = conn.execute("SELECT id, name FROM products WHERE name LIKE ?", (f"%{term}%",))
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run()
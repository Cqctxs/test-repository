import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('shop.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/search')
def search():
    term = request.args.get('term','').strip()
    if len(term) > 100:
        return jsonify({'error':'Search term too long'}), 400
    conn = get_db()
    # Parameterized query prevents SQL injection
    cursor = conn.execute('SELECT name, price FROM products WHERE name LIKE ?', ('%'+term+'%',))
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(products)

if __name__ == '__main__':
    app.run(debug=False)
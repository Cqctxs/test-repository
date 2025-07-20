from flask import Flask, request, jsonify
timport sqlite3

app = Flask(__name__)
DB_PATH = 'app.db'

@app.route('/search')
def search():
    q = request.args.get('q', '')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Use parameterized query to prevent SQL injection
    cursor.execute("SELECT * FROM products WHERE name LIKE ?", (f"%{q}%",))
    rows = cursor.fetchall()
    conn.close()
    result = [{'id': r[0], 'name': r[1], 'price': r[2]} for r in rows]
    return jsonify(result)

if __name__ == '__main__':
    app.run()

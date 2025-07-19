from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
db_path = 'app.db'

def get_db():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/search', methods=['GET'])
def search():
    term = request.args.get('q', '')
    # Input validation: limit length
    if len(term) > 100:
        return jsonify({'error':'Query too long'}), 400
    conn = get_db()
    cursor = conn.execute(
        'SELECT id, name, description FROM items WHERE name LIKE ?',
        (f'%{term}%',)
    )
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=False)

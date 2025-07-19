import sqlite3
from flask import Flask, request, jsonify, g

app = Flask(__name__)
DATABASE = 'app.db'

def get_db():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def teardown(exception):
    db = getattr(g, '_db', None)
    if db is not None:
        db.close()

@app.route('/search')
def search():
    term = request.args.get('q', '')
    # Input validation: limit length and characters
    if len(term) > 50 or not term.isalnum():
        return jsonify({'error': 'Invalid search term'}), 400
    # Parameterized LIKE query
    like_term = f"%{term}%"
    cursor = get_db().execute(
        'SELECT id, name FROM items WHERE name LIKE ?',
        (like_term,)
    )
    items = [dict(row) for row in cursor.fetchall()]
    return jsonify({'results': items})

if __name__ == '__main__':
    app.run(debug=True)

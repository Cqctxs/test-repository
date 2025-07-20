# web5/src/app.py
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_conn():
    return psycopg2.connect(host='localhost', dbname='appdb', user='appuser', password='apppass')

@app.route('/search')
def search():
    q = request.args.get('q', '')
    # simple length and content check
    if len(q) > 50 or not q.isalnum():
        return jsonify({'error': 'Invalid query'}), 400
    conn = get_conn()
    cur = conn.cursor()
    # parameterized query
    cur.execute('SELECT id, username FROM users WHERE username ILIKE %s', (f'%{q}%',))
    rows = cur.fetchall()
    conn.close()
    results = [{'id': r[0], 'username': r[1]} for r in rows]
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=False)
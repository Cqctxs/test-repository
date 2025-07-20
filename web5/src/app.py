import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db():
    return psycopg2.connect(dbname='mydb', user='user', password='pass', host='localhost')

@app.route('/product')
def product():
    pid = request.args.get('id', '')
    try:
        pid_int = int(pid)
    except ValueError:
        return jsonify({'error': 'Invalid product ID'}), 400
    conn = get_db()
    cur = conn.cursor()
    # Parameterized query prevents SQL injection
    cur.execute("SELECT id, name, price FROM products WHERE id = %s", (pid_int,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'id': row[0], 'name': row[1], 'price': row[2]})

if __name__ == '__main__':
    app.run()
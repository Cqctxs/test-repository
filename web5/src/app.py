from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def get_db():
    conn = psycopg2.connect(dbname='app', user='user', password='pass', host='localhost')
    return conn

@app.route('/items')
def items():
    category = request.args.get('category', '')
    conn = get_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    # Parameterized query to prevent SQL injection
    cursor.execute("SELECT id, name, price FROM items WHERE category = %s", (category,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run()

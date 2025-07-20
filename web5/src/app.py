import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

# Database connection settings
DB_CONFIG = {
    'dbname': 'mydb',
    'user': 'dbuser',
    'password': 'secret',
    'host': 'localhost'
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route('/search')
def search_users():
    name = request.args.get('name', '')
    conn = get_connection()
    cur = conn.cursor()
    # Use parameterized query to prevent SQL injection
    cur.execute('SELECT id, name, email FROM users WHERE name ILIKE %s', (f"%{name}%",))
    rows = cur.fetchall()
    conn.close()
    results = [{'id': r[0], 'name': r[1], 'email': r[2]} for r in rows]
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
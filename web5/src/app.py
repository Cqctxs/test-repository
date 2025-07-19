import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_conn():
    return psycopg2.connect(host='localhost', dbname='appdb', user='appuser', password='secret')

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_conn()
    cur = conn.cursor()
    # Parameterized query to prevent injection
    cur.execute('SELECT id, username, email FROM users WHERE id = %s', (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return jsonify({'error':'User not found'}), 404
    return jsonify({'id': row[0], 'username': row[1], 'email': row[2]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

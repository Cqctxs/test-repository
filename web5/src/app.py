# web5/src/app.py - Safe parameterized query
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_conn():
    return psycopg2.connect(dbname='app', user='appuser', password='apppass', host='localhost')

@app.route('/profile', methods=['GET'])
def profile():
    username = request.args.get('username', '')
    # Validate username
    if not username.isalnum():
        return jsonify({'error':'Invalid username'}), 400

    conn = get_conn()
    cur = conn.cursor()
    # Parameterized query to avoid injection
    cur.execute('SELECT username, full_name, bio FROM profiles WHERE username = %s', (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return jsonify({'error':'Not found'}), 404
    return jsonify({'username':row[0], 'full_name':row[1], 'bio':row[2]})

if __name__ == '__main__':
    app.run(debug=False)
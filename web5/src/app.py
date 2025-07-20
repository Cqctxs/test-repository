from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)
conn_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'host': os.getenv('DB_HOST')
}

def get_user_profile(username):
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()
    # Parameterized query prevents injection
    cur.execute('SELECT id, email FROM users WHERE username = %s', (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row

@app.route('/profile')
def profile():
    username = request.args.get('username', '')
    if not username.isalnum():
        return jsonify({'error':'Invalid username'}),400
    profile = get_user_profile(username)
    if not profile:
        return jsonify({'error':'Not found'}),404
    return jsonify({'id': profile[0], 'email': profile[1]})

if __name__ == '__main__':
    app.run()
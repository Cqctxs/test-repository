from flask import Flask, request, jsonify, abort
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'bank.db'

# Dummy user store
def get_user(username):
    conn = sqlite3.connect(DATABASE)
    cur = conn.execute('SELECT id, balance, is_admin FROM users WHERE username=?', (username,))
    row = cur.fetchone()
    conn.close()
    return {'id': row[0], 'balance': row[1], 'is_admin': bool(row[2])} if row else None

@app.route('/transfer', methods=['POST'])
def transfer():
    token = request.headers.get('Authorization')
    if not token or token != os.environ.get('API_TOKEN'):
        abort(401)

    data = request.json
    from_user = get_user(data.get('from'))
    to_user = get_user(data.get('to'))
    amount = data.get('amount')

    if not from_user or not to_user or amount is None:
        abort(400)
    if not isinstance(amount, (int, float)) or amount <= 0:
        abort(400)
    if from_user['balance'] < amount:
        abort(403)

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('UPDATE users SET balance=balance-? WHERE id=?', (amount, from_user['id']))
    cur.execute('UPDATE users SET balance=balance+? WHERE id=?', (amount, to_user['id']))
    conn.commit()
    conn.close()
    return jsonify({'status':'success'})

@app.route('/flag', methods=['GET'])
def get_flag():
    token = request.headers.get('Authorization')
    if not token or token != os.environ.get('API_TOKEN'):
        abort(401)
    username = request.args.get('user')
    user = get_user(username)
    if not user or user['balance'] < 10000:
        abort(403)
    with open('FLAG.txt') as f:
        flag = f.read().strip()
    return jsonify({'flag': flag})

if __name__ == '__main__':
    app.run()
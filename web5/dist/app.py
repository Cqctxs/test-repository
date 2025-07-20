from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'app.db'

def query_balance(user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    # Parameterized to prevent SQL injection
    cur.execute('SELECT balance FROM accounts WHERE user_id = ?', (user_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

@app.route('/balance')
def balance():
    user_id = request.args.get('user_id')
    if not user_id.isdigit():
        return jsonify({'error':'Invalid user id'}),400
    bal = query_balance(int(user_id))
    if bal is None:
        return jsonify({'error':'Not found'}),404
    return jsonify({'balance': bal})

if __name__ == '__main__':
    app.run()
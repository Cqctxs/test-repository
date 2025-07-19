from flask import Flask, render_template, request, jsonify, flash
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login_username', methods=['POST'])
def login():
    username = request.form['username']
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    user_info = c.execute(f"SELECT username FROM users WHERE username='{username}'").fetchall()
    if not user_info:
        flash('Who are you?', 'error')
    else:
        flash(f'Welcome back, {user_info}', 'success')
    return render_template('index.html')
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

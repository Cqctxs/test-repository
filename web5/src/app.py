import sqlite3
from flask import Flask, request, session, redirect, render_template_string

app = Flask(__name__)
app.secret_key = 'replace-with-secure-key'

def get_db():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST':
        uname = request.form['username']
        pwd   = request.form['password']
        conn = get_db()
        cur = conn.cursor()
        # Use parameterized query
        cur.execute(
            'SELECT id FROM users WHERE username=? AND password=?',(uname,pwd)
        )
        row = cur.fetchone()
        conn.close()
        if row:
            session['user_id'] = row['id']
            return redirect('/')
        else:
            msg = 'Login failed'
    return render_template_string(
        '''
        <form method="post">
          <input name="username" placeholder="Username">
          <input name="password" type="password" placeholder="Password">
          <input type="submit" value="Login">
        </form>
        <div>{{ msg }}</div>
        ''', msg=msg)

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect('/login')
    return 'Hello, {}'.format(session['user_id'])

if __name__ == '__main__':
    app.run()
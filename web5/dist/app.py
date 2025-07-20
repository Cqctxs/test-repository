import sqlite3
from flask import Flask, request, session, redirect, render_template_string

app = Flask(__name__)
app.secret_key = 'replace-with-secure-key'

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        # Parameterized query to prevent SQL injection
        cursor.execute(
            'SELECT * FROM users WHERE username = ? AND password = ?',
            (username, password)
        )
        user = cursor.fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            return redirect('/')
        else:
            error = 'Invalid credentials'
    return render_template_string(
        '''
        <form method="post">
          <input name="username" placeholder="Username">
          <input name="password" type="password" placeholder="Password">
          <input type="submit" value="Login">
        </form>
        {% if error %}<p>{{ error }}</p>{% endif %}
        ''', error=error)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')
    return 'Welcome, user {}'.format(session['user_id'])

if __name__ == '__main__':
    app.run()
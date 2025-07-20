from flask import Flask, request, jsonify, session, redirect, url_for
from functools import wraps

app = Flask(__name__)
app.secret_key = 'REPLACE_WITH_STRONG_SECRET'

# Dummy user store for example
def authenticate(username, password):
    # Implement real authentication
    return username == 'admin' and password == 'password'

# Decorator for login required
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        if authenticate(data.get('username'), data.get('password')):
            session['user'] = data.get('username')
            return redirect(url_for('dashboard'))
        return 'Bad credentials', 401
    return '''<form method="post">
                  Username: <input name="username"/> <br/>
                  Password: <input type="password" name="password"/> <br/>
                  <input type="submit" value="Login"/>
              </form>'''

@app.route('/dashboard')
@login_required
def dashboard():
    # Fetch account info for logged-in user only
    user = session['user']
    # Business logic: load user-specific data
    return jsonify({'message': f'Welcome {user}!'})

# Existing routes should also be protected
@app.route('/transfer', methods=['POST'])
@login_required
def transfer():
    data = request.get_json()
    # Verify that session['user'] is allowed to transfer from given account
    if data.get('from') != session['user']:
        return jsonify({'error': 'Unauthorized operation'}), 403
    # Perform transfer...
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run()
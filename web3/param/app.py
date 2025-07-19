from flask import Flask, request, jsonify, abort, session, redirect, url_for
import requests
from functools import wraps

app = Flask(__name__)
app.secret_key = 'REPLACE_WITH_SECURE_RANDOM_KEY'

# Dummy user store
USERS = {'admin': 'password123'}

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if USERS.get(username) == password:
            session['username'] = username
            return redirect(url_for('proxy'))
        return abort(401)
    return '''<form method="post">Username: <input name="username">Password: <input name="password" type="password"><input type="submit"></form>'''

@app.route('/proxy', methods=['POST'])
@login_required
def proxy():
    # Validate and sanitize URL
    url = request.json.get('url')
    if not url or not url.startswith('https://example.com/'):  # allowlist
        return jsonify({'error': 'Invalid or unauthorized URL'}), 400
    try:
        # Proxy request using requests library instead of os.system
        resp = requests.post(url, json=request.json.get('data', {}), timeout=5)
        return (resp.text, resp.status_code, resp.headers.items())
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 502

if __name__ == '__main__':
    app.run(debug=False)

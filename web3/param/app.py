# web3/param/app.py
import subprocess
import shlex
from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/start/<service>')
def start_service(service):
    # whitelist allowed services
    allowed = {'nginx', 'redis', 'postgres'}
    if service not in allowed:
        abort(400, 'Service not allowed')
    # safe invocation without shell and with args list
    try:
        subprocess.run(['/usr/bin/systemctl', 'start', service], check=True)
        return f'Started {service}', 200
    except subprocess.CalledProcessError:
        abort(500, 'Failed to start service')

@app.route('/proxy')
def proxy():
    url = request.args.get('url', '')
    # basic URL validation
    if not url.startswith('https://api.mydomain.com/'):
        abort(400, 'Invalid proxy target')
    # perform proxying via requests
    import requests
    resp = requests.get(url)
    return (resp.content, resp.status_code, resp.headers.items())

if __name__ == '__main__':
    app.run(debug=False)

import os
import re
import subprocess
from functools import wraps
from flask import Flask, request, jsonify, abort

app = Flask(__name__)
API_KEY = os.environ.get('API_KEY')  # Set this in environment, do not hardcode
FLAG = os.environ.get('FLAG')        # Sensitive flag loaded from env


def require_api_key(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        key = request.headers.get('X-API-Key')
        if not key or key != API_KEY:
            abort(403, 'Forbidden: Invalid API key')
        return f(*args, **kwargs)
    return wrapper

@app.route('/run', methods=['POST'])
@require_api_key
def run_command():
    data = request.get_json() or {}
    cmd = data.get('command', '')
    # Allow only alphanumeric, spaces, dashes, underscores
    if not re.fullmatch(r'[A-Za-z0-9_\- ]+', cmd):
        abort(400, 'Bad Request: Invalid characters in command')
    parts = cmd.split()
    try:
        result = subprocess.run(parts, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({'error': e.stderr.strip()}), 400
    return jsonify({'output': result.stdout.strip()})

@app.route('/flag', methods=['GET'])
@require_api_key
def get_flag():
    # Only return the flag to authorized callers
    if not FLAG:
        abort(500, 'Flag not configured')
    return jsonify({'flag': FLAG})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
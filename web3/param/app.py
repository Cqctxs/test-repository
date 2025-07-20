from flask import Flask, request, jsonify
import subprocess
import shlex

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run():
    cmd = request.json.get('cmd', '')
    # Allowlist only specific commands
    allowed = {'ls': ['-l', '/var/log'], 'date': []}
    parts = shlex.split(cmd)
    if not parts or parts[0] not in allowed:
        return jsonify({'error':'Command not allowed'}), 403
    # Only use the exact arguments from allowlist
    proc = subprocess.run([parts[0]] + allowed[parts[0]], capture_output=True, text=True)
    return jsonify({'stdout': proc.stdout, 'stderr': proc.stderr})

if __name__ == '__main__':
    app.run()

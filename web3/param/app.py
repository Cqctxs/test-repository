import subprocess
from flask import Flask, jsonify

app = Flask(__name__)

FLAG = 'FLAG{REDACTED}'

@app.route('/balance/<int:uid>')
def balance(uid):
    # Authenticate user (placeholder)
    # ... implement real auth here ...

    # Fetch balance securely (mocked)
    balances = {1: 100, 2: 50}
    bal = balances.get(uid, 0)
    if bal >= 100:
        # No longer launching shell; directly return flag
        return jsonify({'flag': FLAG})
    return jsonify({'balance': bal})

if __name__ == '__main__':
    app.run()
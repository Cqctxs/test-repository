import subprocess
import re
from flask import Flask, request, jsonify

app = Flask(__name__)

# Regex to allow only numeric account IDs
ACCOUNT_REGEX = re.compile(r'^\d+$')

@app.route('/transfer', methods=['POST'])
def transfer():
    src = request.form.get('src', '')
    dest = request.form.get('dest', '')
    amount = request.form.get('amount', '')

    # 1. Validate account IDs with regex
    if not (ACCOUNT_REGEX.match(src) and ACCOUNT_REGEX.match(dest)):
        return jsonify({"error": "Invalid account format"}), 400

    # 2. Validate and parse amount
    try:
        amt = float(amount)
        if amt <= 0:
            raise ValueError
    except ValueError:
        return jsonify({"error": "Invalid amount"}), 400

    # 3. Execute local gateway securely without shell
    try:
        result = subprocess.run(
            ['php', 'gateway.php', src, dest, str(amt)],
            capture_output=True,
            text=True,
            check=True
        )
        return jsonify({"output": result.stdout.strip()}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": e.stderr.strip()}), 500

if __name__ == '__main__':
    app.run()
import re
from flask import Flask, request, jsonify
from flask_login import LoginManager, login_required
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'replace-with-secure-key'

# Setup login manager
login_manager = LoginManager()
login_manager.init_app(app)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client.store

@app.route('/product')
@login_required
def product():
    code = request.args.get('code','')
    # Validate code: allow only alphanumeric, underscore, dash
    if not re.fullmatch(r'[A-Za-z0-9_-]+', code):
        return jsonify({'error':'Invalid product code'}),400
    # Safe filter query
    prod = db.products.find_one({'code': code, 'is_published':1}, {'_id':0})
    if not prod:
        return jsonify({'error':'Not found'}),404
    return jsonify(prod)

if __name__ == '__main__':
    app.run()
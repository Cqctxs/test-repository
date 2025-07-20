import os
import jwt
from functools import wraps
from flask import Flask, request, jsonify, abort
from peewee import Model, IntegerField, FloatField, SqliteDatabase

# Load secret from environment
SECRET_KEY = os.getenv('SECRET_KEY', 'change_me')

db = SqliteDatabase('bank.db')

class Account(Model):
    id = IntegerField(primary_key=True)
    balance = FloatField()
    class Meta:
        database = db

app = Flask(__name__)

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authentication required'}), 401
        token = auth_header.split()[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.PyJWTError:
            return jsonify({'error': 'Invalid or expired token'}), 401
        request.user_id = payload.get('user_id')
        return f(*args, **kwargs)
    return decorated

@app.route('/transfer', methods=['POST'])
@login_required
def transfer():
    data = request.get_json() or {}
    amount = data.get('amount')
    receiver_id = data.get('receiver')
    # Validate inputs
    if not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({'error': 'Invalid amount'}), 400
    if not isinstance(receiver_id, int):
        return jsonify({'error': 'Invalid receiver'}), 400
    if receiver_id == request.user_id:
        return jsonify({'error': 'Cannot transfer to self'}), 400
    # Atomic transaction
    with db.atomic():
        sender = Account.get_or_none(Account.id == request.user_id)
        receiver = Account.get_or_none(Account.id == receiver_id)
        if not sender or not receiver:
            return jsonify({'error': 'Account not found'}), 404
        if sender.balance < amount:
            return jsonify({'error': 'Insufficient funds'}), 400
        sender.balance -= amount
        receiver.balance += amount
        sender.save()
        receiver.save()
    return jsonify({'status': 'success'})

@app.route('/balance', methods=['GET'])
@login_required
def balance():
    account = Account.get_or_none(Account.id == request.user_id)
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    return jsonify({'user_id': request.user_id, 'balance': account.balance})

if __name__ == '__main__':
    db.create_tables([Account])
    app.run(debug=False)
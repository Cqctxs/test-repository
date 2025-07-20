import os
from pymongo import MongoClient

# Do not store the flag in the database. Read it from an environment variable at runtime.
client = MongoClient('mongodb://localhost:27017/')
db = client.mydb

# Example seed without secrets
def seed_static_data():
    users = [
        {'name': 'alice', 'email': 'alice@example.com'},
        {'name': 'bob',   'email': 'bob@example.com'}
    ]
    db.users.delete_many({})
    db.users.insert_many(users)

if __name__ == '__main__':
    seed_static_data()
    print('Database seeded without sensitive flags.')
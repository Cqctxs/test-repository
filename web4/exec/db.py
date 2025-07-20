import os
from pymongo import MongoClient

# Load sensitive config from environment
MONGO_URI = os.getenv('MONGO_URI')
if not MONGO_URI:
    raise RuntimeError('MONGO_URI environment variable is not set')

client = MongoClient(MONGO_URI)
db = client['exec_db']

# Remove seeding of FLAG in production
def seed_database():
    # Only seed non-sensitive demo data
    if os.getenv('ENV') == 'development':
        users = [
            {'username': 'alice', 'role': 'user'},
            {'username': 'bob', 'role': 'user'}
        ]
        db.users.delete_many({})
        db.users.insert_many(users)

if __name__ == '__main__':
    seed_database()
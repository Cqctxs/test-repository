import os
from pymongo import MongoClient

# Load URI from environment; do not hard-code sensitive flags
MONGO_URI = os.environ.get('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client.get_database('mydb')

# Seed database with non-sensitive default products
default_products = [
    {'name': 'Widget', 'price': 25.0},
    {'name': 'Gadget', 'price': 15.0},
]
db.products.insert_many(default_products)

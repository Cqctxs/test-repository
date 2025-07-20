from pymongo import MongoClient

# Move FLAG to environment variable or secure vault
import os

FLAG = os.getenv('APP_FLAG', '<default>')

client = MongoClient('mongodb://localhost:27017/')
db = client['products_db']

# Seed products without embedding the flag
products = [
    {'name': 'Widget A', 'price': 10},
    {'name': 'Widget B', 'price': 15},
]

# If needed, store flag separately or in a secure collection with restricted access
# secure_db = client['secure']
# secure_db['flags'].insert_one({'key': 'challenge', 'value': FLAG})

# Initialize product collection
db.products.insert_many(products)

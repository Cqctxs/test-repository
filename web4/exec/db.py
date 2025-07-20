from pymongo import MongoClient
import os

# Connect to MongoDB
client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://localhost:27017'))
db = client.get_database('appdb')
products = db.products

# Seed products without exposing the internal flag
initial_products = [
    {'name': 'Widget', 'price': 10, 'is_published': True},
    {'name': 'Gadget', 'price': 15, 'is_published': True},
]

# Only seed if collection is empty
if products.count_documents({}) == 0:
    products.insert_many(initial_products)

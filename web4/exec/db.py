# Database initialization without embedding secret flags
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.store

db.products.delete_many({})

data = [
    {'code':'A1','price':10,'description':'Widget','is_published':1},
    {'code':'B1','price':15,'description':'Gadget','is_published':1},
    # FLAG product stored separately or in secure vault, not in code
]

# Insert only non-sensitive products
db.products.insert_many(data)

# Move flag to environment or secure secret manager
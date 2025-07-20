import os
import sqlite3

# Only seed the flag in development environment
ENV = os.getenv('APP_ENV', 'production')
DB_PATH = os.getenv('DB_PATH', 'shop.db')

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Create products table if not exists
c.execute(
    '''CREATE TABLE IF NOT EXISTS products (
           id INTEGER PRIMARY KEY,
           name TEXT,
           description TEXT,
           price REAL,
           hidden BOOLEAN DEFAULT 0
       )'''
)

# Insert public products
public_products = [
    ('Widget', 'A regular widget', 9.99, 0),
    ('Gadget', 'A standard gadget', 14.99, 0)
]
c.executemany('INSERT INTO products (name, description, price, hidden) VALUES (?, ?, ?, ?)', public_products)

if ENV == 'development':
    # In development only: insert a hidden flag product
    flag = os.getenv('PRODUCT_FLAG')
    if flag:
        c.execute(
            'INSERT INTO products (name, description, price, hidden) VALUES (?, ?, ?, ?)',
            ('SecretItem', flag, 0.00, 1)
        )

conn.commit()
conn.close()
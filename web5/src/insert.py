import sqlite3
from werkzeug.security import generate_password_hash

# Securely hash passwords before insertion
def insert_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    users = [
        ('admin', generate_password_hash('s3cret!')),  # hashed password
        ('guest', generate_password_hash('guest123'))
    ]
    c.executemany('INSERT OR REPLACE INTO users (username,password) VALUES (?,?)', users)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    insert_users()
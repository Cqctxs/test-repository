import os
import sqlite3
import bcrypt

# Use environment-supplied flag rather than hardcoding
FLAG = os.getenv('DB_FLAG')
if not FLAG:
    raise RuntimeError('DB_FLAG environment variable is required')

DB_PATH = os.getenv('SQLITE_PATH', 'users.db')
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Create users table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
)''')

# Hash the flag to avoid storing it in plaintext
password_hash = bcrypt.hashpw(FLAG.encode('utf-8'), bcrypt.gensalt())
c.execute('INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?)',
          ('flag_user', password_hash.decode('utf-8')))

conn.commit()
conn.close()
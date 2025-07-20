import sqlite3
import os
import bcrypt

DB_PATH = os.path.join(os.path.dirname(__file__), 'app.db')

# Read plaintext credentials from secure environment or prompt
users = [
    {'username': os.environ.get('USER1_NAME'), 'password': os.environ.get('USER1_PASS')},
    {'username': os.environ.get('USER2_NAME'), 'password': os.environ.get('USER2_PASS')},
]

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
)
''')

for u in users:
    if u['username'] and u['password']:
        # Hash the password before storing
        pw_hash = bcrypt.hashpw(u['password'].encode('utf-8'), bcrypt.gensalt())
        cur.execute('INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?)', (u['username'], pw_hash))

conn.commit()
conn.close()

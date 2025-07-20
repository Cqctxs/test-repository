import sqlite3

# Initialize database with sample users (non-sensitive data)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
# Create table if it does not exist
cursor.execute(
    'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, email TEXT)'
)
# Use parameterized inserts
cursor.execute('INSERT OR IGNORE INTO users (username, email) VALUES (?, ?)', ('alice', 'alice@example.com'))
cursor.execute('INSERT OR IGNORE INTO users (username, email) VALUES (?, ?)', ('bob', 'bob@example.com'))
conn.commit()
conn.close()

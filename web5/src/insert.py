import sqlite3
import bcrypt

# Connect to database
db_path = 'users.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Sample users list
users = [('alice', 'alicepass'), ('bob', 'bobpass')]

for username, password in users:
    # Generate salt and hash password using bcrypt
    salt = bcrypt.gensalt()
    pw_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    # Use parameterized query to store username and hash
    cursor.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, pw_hash.decode('utf-8'))
    )

conn.commit()
conn.close()
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT PRIMARY KEY, password TEXT)''')

# Sample user data
users_data = [
    ('Alice', 'wxmctf{'),
    ('Bob', 'j0k35_0n_y0u'),
    ('Charlie', '_th3r3_4r3'),
    ('David', 'n0_nucl34r'),
    ('Eve', '_l4nch_c0d35}')]

# Insert sample data into the table
c.executemany("INSERT INTO users VALUES (?, ?)", users_data)

# Commit changes and close connection
conn.commit()
conn.close()

print("Data inserted successfully into users.db.")

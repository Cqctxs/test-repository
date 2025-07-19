# Security Fix for web5/src/insert.py

**Vulnerability Type:** HARDCODED_CREDENTIALS  
**Confidence Level:** HIGH  
**Breaking Changes:** Yes

## Original Issue
Replaced plaintext password storage with hashed passwords using a secure hash function from werkzeug.security. This prevents password exposure if the database is compromised. Removed the sensitive secret from code and encrypted stored passwords instead.

## Security Notes
Never store plaintext passwords or secrets in code or databases. Always use strong hashing algorithms with salts such as bcrypt or PBKDF2. Protect secret flags or tokens outside the source code.

## Fixed Code
```py
import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Remove plaintext passwords and store only hashed
users = [
    ('alice', generate_password_hash('alicepassword123')), 
    ('bob', generate_password_hash('bobpassword456'))
]

for user, pwd_hash in users:
    c.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (user, pwd_hash))

conn.commit()
conn.close()

```

## Additional Dependencies
- from werkzeug.security import generate_password_hash

## Testing Recommendations
- Ensure password hashes are stored, not plaintext.
- Verify users can authenticate with original password after hashing if applicable.
- Attempt to retrieve passwords from DB to confirm no plaintext.

## Alternative Solutions

### Use environment variables or secret management tools to store sensitive data instead of in source code.
**Pros:** More secure key management, Easier secret rotation
**Cons:** Requires additional infrastructure


import sqlite3

conn = sqlite3.connect('artifacts/onboarding.db')
cursor = conn.cursor()
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='users'")
result = cursor.fetchone()
if result:
    print("Users table schema:")
    print(result[0])
else:
    print("No users table found")

# Also check what tables exist
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("\nAll tables in database:")
for table in tables:
    print(f"  - {table[0]}")

conn.close()

import sqlite3

# Connect to database (creates sample.db if not exists)
conn = sqlite3.connect("sample.db")
cursor = conn.cursor()

# Create a sample users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL
)
""")

# Add some dummy data
cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Alice", "alice@example.com"))
cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Bob", "bob@example.com"))

conn.commit()
conn.close()

print("sample.db and users table initialized.")

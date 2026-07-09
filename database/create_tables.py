import sqlite3
connection = sqlite3.connect("exam.db")
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS candidate (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    exam_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
connection.commit()
connection.close()

print("Candidate table created successfully!")
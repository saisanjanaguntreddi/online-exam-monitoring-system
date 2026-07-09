import sqlite3

connection = sqlite3.connect("exam.db")
cursor = connection.cursor()

cursor.execute("""
INSERT INTO candidate (full_name, email, exam_name)
VALUES (?, ?, ?)
""", (
    "Sai Sanjana",
    "saisanjanaguntreddi@gmail.com",
    "Python"
))

connection.commit()
connection.close()

print("Candidate inserted successfully!")
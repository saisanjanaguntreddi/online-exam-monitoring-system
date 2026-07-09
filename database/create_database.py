import sqlite3
connection = sqlite3.connect("exam.db")
print("Database Created Sucessfully")
connection.close()

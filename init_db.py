import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Admin table
cursor.execute("""
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

# Students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_no TEXT NOT NULL,
    class_name TEXT NOT NULL,
    section TEXT NOT NULL
)
""")

# Teachers table
cursor.execute("""
CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    subject TEXT NOT NULL,
    phone TEXT NOT NULL
)
""")

# Attendance table
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    date TEXT NOT NULL,
    status TEXT NOT NULL
)
""")

# Marks table
cursor.execute("""
CREATE TABLE IF NOT EXISTS marks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    subject TEXT NOT NULL,
    mark INTEGER NOT NULL
)
""")

# Insert default admin
cursor.execute("SELECT * FROM admin WHERE username='admin'")
admin = cursor.fetchone()

if not admin:
    cursor.execute("INSERT INTO admin (username, password) VALUES (?, ?)", ("admin", "admin123"))

conn.commit()
conn.close()

print("Database and tables created successfully!")

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB_NAME = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn
@app.route("/")
def home():
    return jsonify({
        "message": "School ERP Backend Running Successfully"
    })

# ------------------ LOGIN ------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, password))
    admin = cursor.fetchone()
    conn.close()

    if admin:
        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "message": "Invalid username or password"})

# ------------------ STUDENTS ------------------
@app.route('/students', methods=['GET'])
def get_students():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return jsonify([dict(row) for row in students])

@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    name = data.get('name')
    roll_no = data.get('roll_no')
    class_name = data.get('class_name')
    section = data.get('section')

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO students (name, roll_no, class_name, section) VALUES (?, ?, ?, ?)",
        (name, roll_no, class_name, section)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Student added successfully"})

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Student deleted successfully"})

# ------------------ TEACHERS ------------------
@app.route('/teachers', methods=['GET'])
def get_teachers():
    conn = get_db_connection()
    teachers = conn.execute("SELECT * FROM teachers").fetchall()
    conn.close()
    return jsonify([dict(row) for row in teachers])

@app.route('/teachers', methods=['POST'])
def add_teacher():
    data = request.get_json()
    name = data.get('name')
    subject = data.get('subject')
    phone = data.get('phone')

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO teachers (name, subject, phone) VALUES (?, ?, ?)",
        (name, subject, phone)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Teacher added successfully"})

@app.route('/teachers/<int:id>', methods=['DELETE'])
def delete_teacher(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM teachers WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Teacher deleted successfully"})

# ------------------ ATTENDANCE ------------------
@app.route('/attendance', methods=['GET'])
def get_attendance():
    conn = get_db_connection()
    attendance = conn.execute("SELECT * FROM attendance").fetchall()
    conn.close()
    return jsonify([dict(row) for row in attendance])

@app.route('/attendance', methods=['POST'])
def add_attendance():
    data = request.get_json()
    student_name = data.get('student_name')
    date = data.get('date')
    status = data.get('status')

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO attendance (student_name, date, status) VALUES (?, ?, ?)",
        (student_name, date, status)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Attendance added successfully"})

@app.route('/attendance/<int:id>', methods=['DELETE'])
def delete_attendance(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM attendance WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Attendance deleted successfully"})

# ------------------ MARKS ------------------
@app.route('/marks', methods=['GET'])
def get_marks():
    conn = get_db_connection()
    marks = conn.execute("SELECT * FROM marks").fetchall()
    conn.close()
    return jsonify([dict(row) for row in marks])

@app.route('/marks', methods=['POST'])
def add_marks():
    data = request.get_json()
    student_name = data.get('student_name')
    subject = data.get('subject')
    mark = data.get('mark')

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO marks (student_name, subject, mark) VALUES (?, ?, ?)",
        (student_name, subject, mark)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Marks added successfully"})

@app.route('/marks/<int:id>', methods=['DELETE'])
def delete_marks(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM marks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Marks deleted successfully"})

# ------------------ DASHBOARD COUNTS ------------------
@app.route('/dashboard', methods=['GET'])
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    student_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM teachers")
    teacher_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM attendance")
    attendance_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM marks")
    marks_count = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        "students": student_count,
        "teachers": teacher_count,
        "attendance": attendance_count,
        "marks": marks_count
    })

if __name__ == '__main__':
    app.run(debug=True)

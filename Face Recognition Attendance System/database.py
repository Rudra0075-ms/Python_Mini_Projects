import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "attendance.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                attendance_date TEXT NOT NULL,
                attendance_time TEXT NOT NULL,
                UNIQUE(student_id, attendance_date),
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
        """)

def add_student(name):
    with get_connection() as conn:
        conn.execute("INSERT OR IGNORE INTO students(name) VALUES (?)", (name,))

def get_student_id(name):
    with get_connection() as conn:
        row = conn.execute("SELECT id FROM students WHERE name = ?", (name,)).fetchone()
        return row[0] if row else None

def mark_attendance(name, date_text, time_text):
    student_id = get_student_id(name)
    if student_id is None:
        add_student(name)
        student_id = get_student_id(name)

    with get_connection() as conn:
        cursor = conn.execute(
            """INSERT OR IGNORE INTO attendance
               (student_id, attendance_date, attendance_time)
               VALUES (?, ?, ?)""",
            (student_id, date_text, time_text)
        )
        return cursor.rowcount == 1

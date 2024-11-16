import csv
import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime

# Initialize data files with pre-registered users and courses
def initialize_files():
    # Pre-register students and admin
    with open("students.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["user_id", "user_name", "user_password", "role"])
        writer.writerow(["S201", "Jordan", "newpass1", "student"])
        writer.writerow(["S202", "Morgan", "newpass2", "student"])
        writer.writerow(["S203", "Taylor", "newpass3", "student"])
        writer.writerow(["S204", "Riley", "newpass4", "student"])
        writer.writerow(["S205", "Avery", "newpass5", "student"])
        writer.writerow(["admin", "Administrator", "newadminpass", "admin"])

    # Pre-register courses for each student
    with open("courses.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["course_id", "course_name"])
        writer.writerow(["C101", "History"])
        writer.writerow(["C102", "Geography"])
        writer.writerow(["C103", "Computer Science"])
        writer.writerow(["C104", "Literature"])

    # Attendance file
    if not os.path.exists("attendance.csv"):
        with open("attendance.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["attendance_id", "student_id", "course_id", "class_date", "attendance_status"])

initialize_files()

# Record attendance
def record_attendance(student_id, course_id, attendance_status):
    with open("attendance.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        attendance_id = sum(1 for _ in open("attendance.csv"))  # auto-increment
        class_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([attendance_id, student_id, course_id, class_date, attendance_status])

# Admin attendance marking GUI for all students in each course
def mark_attendance_admin():
    def open_course(course_id, course_name):
        course_window = tk.Toplevel(admin_window)
        course_window.title(f"Mark Attendance for {course_name}")

        with open("students.csv", mode="r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            students = [row for row in reader if row[3] == "student"]

        for student in students:
            student_id, student_name = student[0], student[1]
            tk.Label(course_window, text=f"{student_name} (ID: {student_id})").pack()

            status_var = tk.StringVar(course_window)
            tk.Entry(course_window, textvariable=status_var).pack()

            def submit_attendance(stud_id=student_id, status_var=status_var):
                status = status_var.get().lower()
                if status in ["present", "absent"]:
                    record_attendance(stud_id, course_id, status)
                    messagebox.showinfo("Attendance", f"Attendance marked for {stud_id}")
                else:
                    messagebox.showerror("Error", "Invalid status. Please enter 'present' or 'absent'.")

            tk.Button(course_window, text="Submit", command=submit_attendance).pack()

    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Dashboard")

    with open("courses.csv", mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        courses = [row for row in reader]

    for course in courses:
        course_id, course_name = course
        tk.Button(admin_window, text=f"Mark Attendance for {course_name}",
                  command=lambda cid=course_id, cname=course_name: open_course(cid, cname)).pack(pady=5)

# Student attendance view GUI
def view_attendance_student(student_id):
    student_window = tk.Toplevel(root)
    student_window.title("View Attendance")

    with open("courses.csv", mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        courses = [row for row in reader]

    # Loop through all courses and find attendance records for the logged-in student
    for course_id, course_name in courses:
        tk.Label(student_window, text=f"Course: {course_name} (Course ID: {course_id})").pack()

        with open("attendance.csv", mode="r") as att_file:
            att_reader = csv.reader(att_file)
            next(att_reader)  # Skip header

            records = [row for row in att_reader if row[1] == student_id and row[2] == course_id]
            if records:
                records_str = "\n".join([f"Date: {row[3]}, Status: {row[4]}" for row in records])
                tk.Label(student_window, text=records_str).pack()
            else:
                tk.Label(student_window, text="No attendance records found.").pack()
        tk.Label(student_window, text="").pack()  # Blank line for spacing

# Login function
def login():
    user_id = id_entry.get().strip()
    password = password_entry.get().strip()

    found_user = False
    with open("students.csv", mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            csv_user_id = row[0].strip()
            csv_password = row[2].strip()
            if csv_user_id == user_id and csv_password == password:
                found_user = True
                role = row[3].strip()
                if role == "student":
                    view_attendance_student(user_id)
                elif role == "admin":
                    mark_attendance_admin()
                break

    if not found_user:
        messagebox.showerror("Login Failed", "Invalid ID or password")

# Main GUI for the system
root = tk.Tk()
root.title("Student Attendance System")

tk.Label(root, text="User ID:").pack()
id_entry = tk.Entry(root)
id_entry.pack()

tk.Label(root, text="Password:").pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

tk.Button(root, text="Login", command=login).pack(pady=10)
root.mainloop()

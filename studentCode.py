from PyQt5.uic import loadUi
from db_handler import DatabaseHandler
from core_logic import Validator

import sys
import sqlite3

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox,
    QMainWindow, QInputDialog, QComboBox, QListWidget
)
from PyQt5.QtGui import QFont


# ========================= Student Page =========================
class studentWindow(QMainWindow):
    def __init__(self, student_id):
        super().__init__()
        loadUi("student.ui", self)

        self.student_id = student_id

        # Buttons connections
        self.info_btn.clicked.connect(self.open_info)
        self.schedule_btn.clicked.connect(self.open_schedule)
        self.register_btn.clicked.connect(self.open_register)
        self.logout_btn.clicked.connect(self.logout)
        self.plan_btn.clicked.connect(self.open_plan)

    # --- Student Info Page ---
    def open_info(self):
        self.info_win = StudentInfoWindow(self.student_id, self)
        self.info_win.show()
        self.hide()

    # --- Student Schedule Page ---
    def open_schedule(self):
        self.schedule_win = StudentScheduleWindow(self.student_id, self)
        self.schedule_win.show()
        self.hide()

    # --- Course Registration Page ---
    def open_register(self):
        self.reg_win = RegisterCourseWindow(self.student_id, self)
        self.reg_win.show()
        self.hide()

    # --- Student Plan Page ---
    def open_plan(self):
        self.plan_win = StudentPlanWindow(self.student_id, self)
        self.plan_win.show()
        self.hide()

    # --- Logout ---
    def logout(self):
        '''
        Docstring for logout
        '''
        self.close()


# ========================= Student Information Window =========================
class StudentInfoWindow(QWidget):
    def __init__(self, student_id, parent_window):
        super().__init__()
        self.student_id = student_id
        self.parent_window = parent_window
        self.db = DatabaseHandler()

        self.setWindowTitle("Student Information")
        self.setGeometry(450, 200, 400, 300)

        info = self.db.get_student_info(student_id)
        name = info[0]
        level = info[1]
        major = info[2]
        email = info[3]

        layout = QVBoxLayout()

        label = QLabel(
            f"Name: {name}\n"
            f"Student ID: {student_id}\n"
            f"Major: {major}\n"
            f"Level: {level}\n"
            f"Email: {email}"
        )
        label.setFont(QFont("Arial", 12))
        layout.addWidget(label)

        pass_btn = QPushButton("Change Password")
        pass_btn.clicked.connect(self.change_pass)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.go_back)

        layout.addWidget(pass_btn)
        layout.addWidget(back_btn)
        self.setLayout(layout)

    def change_pass(self):
        new_pass, ok = QInputDialog.getText(self, "Change Password", "Enter new password:")
        if ok and new_pass.strip():
            self.db.change_student_password(self.student_id, new_pass)
            QMessageBox.information(self, "Done", "Password changed successfully")

    def go_back(self):
        self.close()
        self.parent_window.show()


# ========================= Student Schedule Window =========================
class StudentScheduleWindow(QWidget):
    def __init__(self, student_id, parent_window):
        super().__init__()
        self.student_id = student_id
        self.parent_window = parent_window
        self.db = DatabaseHandler()

        self.setWindowTitle("Study Schedule")
        self.setGeometry(450, 200, 500, 350)

        schedule = self.db.get_student_schedule(student_id)

        layout = QVBoxLayout()

        if not schedule:
            layout.addWidget(QLabel("No schedule available"))
        else:
            text = ""
            for sec in schedule:
                text += f"{sec.course_code} - ({sec.days} {sec.start_time} {sec.end_time})\n"

            label = QLabel(text)
            label.setFont(QFont("Arial", 12))
            layout.addWidget(label)

        # ======= NEW BUTTON ADDED HERE =======
        export_btn = QPushButton("Export to Excel")
        export_btn.clicked.connect(self.export_excel)
        layout.addWidget(export_btn)
        # ======================================

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    # ======= EXCEL EXPORT FUNCTION ADDED =======
    def export_excel(self):
        from openpyxl import Workbook

        schedule = self.db.get_student_schedule(self.student_id)

        if not schedule:
            QMessageBox.warning(self, "Error", "No schedule to export.")
            return

        wb = Workbook()
        ws = wb.active
        ws.title = "Schedule"

        # Header
        ws.append(["Course Code", "Section ID", "Days", "Start Time", "End Time"])

        # Data rows
        for sec in schedule:
            ws.append([
                sec.course_code,
                sec.section_id,
                sec.days,
                sec.start_time,
                sec.end_time
            ])

        file_name = f"student_{self.student_id}_schedule.xlsx"
        wb.save(file_name)

        QMessageBox.information(self, "Saved", f"Excel file created:\n{file_name}")
    # ===========================================

    def go_back(self):
        self.close()
        self.parent_window.show()


# ========================= Course Registration Window =========================
class RegisterCourseWindow(QWidget):
    def __init__(self, student_id, parent_window):
        super().__init__()

        self.db = DatabaseHandler()
        self.student_id = student_id
        self.previous_window = parent_window

        self.setWindowTitle("KAU Course Registration")
        self.setGeometry(300, 100, 600, 400)

        # -------- Fetch student level + level courses --------
        self.student_level = self.db.get_student_level(self.student_id)
        self.level_courses = self.db.get_courses_by_level(self.student_level, self.student_id)

        main_layout = QVBoxLayout()

        title = QLabel("Course Registration System")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(title)

        # ------- Select course -------
        self.course_box = QComboBox()
        main_layout.addWidget(QLabel("Select Course:"))
        main_layout.addWidget(self.course_box)

        # Add level courses
        for code, name, credits in self.level_courses:
            self.course_box.addItem(f"{code} - {name} - {credits} credit hours")

        # ------- Select section -------
        self.section_box = QComboBox()
        main_layout.addWidget(QLabel("Select Section:"))
        main_layout.addWidget(self.section_box)

        # Load sections dynamically
        self.course_box.currentTextChanged.connect(self.load_sections)
        self.load_sections()

        # ------- Buttons -------
        btn_layout = QHBoxLayout()

        register_btn = QPushButton("Register Section")
        register_btn.clicked.connect(self.register_section)

        delete_btn = QPushButton("Delete Selected Registration")
        delete_btn.clicked.connect(self.delete_registration)

        back_btn = QPushButton("⬅ Back")
        back_btn.clicked.connect(self.go_back)

        btn_layout.addWidget(register_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(back_btn)

        main_layout.addLayout(btn_layout)

        # ------- Show schedule -------
        main_layout.addWidget(QLabel("Current Schedule:"))
        self.schedule_list = QListWidget()
        self.load_schedule()
        main_layout.addWidget(self.schedule_list)

        self.setLayout(main_layout)

    # Load sections based on selected course
    def load_sections(self):
        course_full = self.course_box.currentText()
        if not course_full:
            return

        course_code = course_full.split(" - ")[0]

        self.section_box.clear()

        sections = self.db.get_available_sections(course_code)
        self.sections_dict = {
            f"Sec {s.section_id}: {s.days} {s.start_time}-{s.end_time}": s
            for s in sections
        }

        self.section_box.addItems(self.sections_dict.keys())

    # Load student schedule
    def load_schedule(self):
        self.schedule_list.clear()
        schedule = self.db.get_student_schedule(self.student_id)

        for sec in schedule:
            text = f"{sec.course_code} - Sec {sec.section_id} | {sec.days} {sec.start_time}-{sec.end_time}"
            self.schedule_list.addItem(text)

    # Register a section
    def register_section(self):
        selected_text = self.section_box.currentText()
        if selected_text == "":
            return

        section_obj = self.sections_dict[selected_text]

        current_schedule = self.db.get_student_schedule(self.student_id)

        for sec in current_schedule:
            if sec.course_code == section_obj.course_code:
                QMessageBox.warning(self, "Already Registered",
                                    "You already registered this course.")
                return

        conflict, msg = Validator.check_time_conflict(section_obj, current_schedule)
        if conflict:
            QMessageBox.warning(self, "Conflict", msg)
            return

        ok, msg = Validator.validate_prerequisites(self.db.db_path, self.student_id, section_obj.course_code)
        if not ok:
            QMessageBox.warning(self, "Prerequisites Error", msg)
            return

        success, message = self.db.register_student(self.student_id, section_obj)

        if success:
            QMessageBox.information(self, "Success", message)
            self.load_schedule()
        else:
            QMessageBox.warning(self, "Error", message)

    # Delete registration
    def delete_registration(self):
        selected = self.schedule_list.currentItem()
        if not selected:
            return

        row_text = selected.text()
        section_id = int(row_text.split("Sec ")[1].split(" |")[0])

        try:
            conn = sqlite3.connect(self.db.db_path)
            c = conn.cursor()

            c.execute("DELETE FROM registrations WHERE student_id=? AND section_id=?",
                      (self.student_id, section_id))

            conn.commit()
            conn.close()

            QMessageBox.information(self, "Removed", "Section removed successfully.")
            self.load_schedule()

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Database Error: {e}")

    def go_back(self):
        if self.previous_window:
            self.previous_window.show()
        self.close()


# ========================= Student Plan Window =========================
class StudentPlanWindow(QMainWindow):
    def __init__(self, student_id, parent_window):
        super().__init__()
        self.db = DatabaseHandler()
        self.student_id = student_id
        self.parent_window = parent_window

        self.setWindowTitle("Study Plan")
        self.setGeometry(450, 100, 500, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_layout = QVBoxLayout()
        central_widget.setLayout(self.main_layout)

        title = QLabel("Student Study Plan")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.main_layout.addWidget(title)

        self.load_plan()

    def load_plan(self):
        data = self.db.get_program_plan(self.student_id)
        if not data:
            self.main_layout.addWidget(QLabel("Student not found"))
            return

        program = data['program']
        student_level = data['student_level']
        plan = data['plan']

        self.main_layout.addWidget(
            QLabel(f"Student Program: {program} | Current Level: {student_level}")
        )

        # Display all levels from 1 to 8
        for level in range(1, 9):
            lbl = QLabel(f"Level {level}")
            self.main_layout.addWidget(lbl)

            lst = QListWidget()

            if level in plan:
                for course in plan[level]:
                    lst.addItem(f"{course['course_code']} - {course['name']}")
            else:
                lst.addItem("No courses in this level")

            self.main_layout.addWidget(lst)

        # Back button
        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.go_back)
        self.main_layout.addWidget(back_btn)

    def go_back(self):
        self.close()
        self.parent_window.show()

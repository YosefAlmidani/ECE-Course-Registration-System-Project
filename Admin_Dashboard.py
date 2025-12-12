import sys
import sqlite3
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem
)
 



class AdminDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin dashboard")
        self.setGeometry(300,200,400,400)
        self.setup_ui()

       
    def setup_ui(self):
        layout = QVBoxLayout()
            
        self.add_course_button = QPushButton("Add Course")
        self.add_course_button.clicked.connect(self.open_add_course_window)

        self.delete_course_button = QPushButton("Delete Course")
        self.delete_course_button.clicked.connect(self.open_delete_course) 
        self.view_course_button = QPushButton("View Courses")
        self.view_course_button.clicked.connect(self.open_view_courses) 

        self.add_section_button = QPushButton("Add Section")
        self.add_section_button.clicked.connect(self.open_add_section) 

        self.delete_section_button = QPushButton("Delete Section")
        self.delete_section_button.clicked.connect(self.open_delete_section) 

        self.stats_button = QPushButton("View Statistics")
        self.stats_button.setStyleSheet("background-color: #ffc107; color: black; font-weight: bold;")
        self.stats_button.clicked.connect(self.show_statistics) 

        self.logout_button = QPushButton("Log Out")
        self.logout_button.setStyleSheet("background-color: #dc3545; color: white;")
        self.logout_button.clicked.connect(self.close) 

        layout.addWidget(self.add_course_button)
        layout.addWidget(self.delete_course_button)
        layout.addWidget(self.view_course_button)
        layout.addWidget(self.add_section_button)
        layout.addWidget(self.delete_section_button)
        layout.addWidget(self.stats_button)
        layout.addWidget(self.logout_button)

        self.setLayout(layout)
    
    def open_add_course_window(self):
        self.add_course_window= QWidget()
        self.add_course_window.setWindowTitle("add course")
        self.add_course_window.setGeometry(400,200,300,200)
        

        layout = QVBoxLayout()

        course_number_label=QLabel("course number")
        self.course_number_input=QLineEdit()

        course_name_label=QLabel("course name")
        self.course_name_input=QLineEdit()

        course_hour_label=QLabel("course hour")
        self.course_hour_input=QLineEdit()

        row1=QHBoxLayout()
        row1.addWidget(course_number_label)
        row1.addWidget(self.course_number_input)

        row2=QHBoxLayout()
        row2.addWidget(course_name_label)
        row2.addWidget(self.course_name_input)

        row3=QHBoxLayout()
        row3.addWidget(course_hour_label)
        row3.addWidget(self.course_hour_input)

        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)

        add_button=QPushButton("add course")
        add_button.clicked.connect(self.save_course)

        layout.addWidget(add_button)
        self.add_course_window.setLayout(layout)
        self.add_course_window.show()
    

    def save_course(self):
        number=self.course_number_input.text().strip()
        name= self.course_name_input.text().strip()
        hour= self.course_hour_input.text().strip()
     

        if number == "" or name == "" or hour == "":
           QMessageBox.warning(self.add_course_window, "Error", "Please fill all fields")
           return
        
        if  not hour.isdigit():
            QMessageBox.warning(self.add_course_window,"Error", "please write number" )
            return
        
        hour=int(hour)

        conn = sqlite3.connect("kau_engineering.db")
   
   
        c = conn.cursor()

   
        try:
            c.execute("INSERT INTO courses (course_code, name, credits, level) VALUES (?, ?, ?, ?)",
                  (number, name, hour, 0))
            conn.commit()

            QMessageBox.information(self.add_course_window, "Success", "Course added successfully!")
            self.add_course_window.close()

        except sqlite3.IntegrityError:
              QMessageBox.warning(self.add_course_window, "Error", "Course already exists")

        except Exception as e:
            QMessageBox.warning(self.add_course_window, "Error", f"Database error: {e}")

        finally:
            conn.close()


    def open_view_courses(self):
        self.view_win = QWidget()
        self.view_win.setWindowTitle("All Courses")
        self.view_win.setGeometry(500, 250, 500, 300)

        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Code", "Name", "Credits", "Level"])

        conn = sqlite3.connect("kau_engineering.db")
        c = conn.cursor()
        c.execute("SELECT * FROM courses")
        data = c.fetchall()
        conn.close()

        table.setRowCount(len(data))
        for row, course in enumerate(data):
            for col, value in enumerate(course):
                table.setItem(row, col, QTableWidgetItem(str(value)))

        layout = QVBoxLayout()
        layout.addWidget(table)
        self.view_win.setLayout(layout)
        self.view_win.show()

    # --------------------------
    # DELETE COURSE
    # --------------------------
    def open_delete_course(self):
        self.del_win = QWidget()
        self.del_win.setWindowTitle("Delete Course")
        self.del_win.setGeometry(500, 250, 300, 150)

        layout = QVBoxLayout()

        lbl = QLabel("Enter Course Code:")
        self.del_input = QLineEdit()
        btn = QPushButton("Delete")
        btn.clicked.connect(self.delete_course)

        layout.addWidget(lbl)
        layout.addWidget(self.del_input)
        layout.addWidget(btn)

        self.del_win.setLayout(layout)
        self.del_win.show()

    def delete_course(self):
        code = self.del_input.text().strip()

        conn = sqlite3.connect("kau_engineering.db")
        c = conn.cursor()
        c.execute("DELETE FROM courses WHERE course_code=?", (code,))
        conn.commit()
        deleted = c.rowcount
        conn.close()

        if deleted == 0:
            QMessageBox.warning(self.del_win, "Error", "Course not found")
        else:
            QMessageBox.information(self.del_win, "Done", "Course deleted")
            self.del_win.close()

    # --------------------------
    # ADD SECTION
    # --------------------------
    def open_add_section(self):
        self.sec_win = QWidget()
        self.sec_win.setWindowTitle("Add Section")
        self.sec_win.setGeometry(450, 250, 350, 300)

        layout = QVBoxLayout()

        labels = ["Course Code", "Section Number", "Days",
                  "Start Time", "End Time", "Faculty ID", "Semester"]

        self.sec_inputs = {}

        for lbl in labels:
            row = QHBoxLayout()
            label = QLabel(lbl + ":")
            inp = QLineEdit()
            row.addWidget(label)
            row.addWidget(inp)
            layout.addLayout(row)
            self.sec_inputs[lbl] = inp

        btn = QPushButton("Save Section")
        btn.clicked.connect(self.save_section)
        layout.addWidget(btn)

        self.sec_win.setLayout(layout)
        self.sec_win.show()

    def save_section(self):
        vals = {k: v.text().strip() for k, v in self.sec_inputs.items()}

        if any(val == "" for val in vals.values()):
            QMessageBox.warning(self.sec_win, "Error", "Complete all fields")
            return

        conn = sqlite3.connect("kau_engineering.db")
        c = conn.cursor()

        try:
            c.execute("""
                INSERT INTO sections (course_code, section_number, days, start_time, end_time, faculty_id, semester)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, tuple(vals.values()))

            conn.commit()
            conn.close()

            QMessageBox.information(self.sec_win, "Success", "Section added!")
            self.sec_win.close()

        except Exception as e:
            QMessageBox.warning(self.sec_win, "Error", str(e))

    # DELETE SECTION
    def open_delete_section(self):
        self.ds_win = QWidget()
        self.ds_win.setWindowTitle("Delete Section")
        self.ds_win.setGeometry(500, 250, 300, 150)

        layout = QVBoxLayout()
        lbl = QLabel("Enter Section ID:")
        self.ds_inp = QLineEdit()
        btn = QPushButton("Delete")
        btn.clicked.connect(self.delete_section)

        layout.addWidget(lbl)
        layout.addWidget(self.ds_inp)
        layout.addWidget(btn)

        self.ds_win.setLayout(layout)
        self.ds_win.show()

    def delete_section(self):
        sec_id = self.ds_inp.text().strip()

        conn = sqlite3.connect("kau_engineering.db")
        c = conn.cursor()
        c.execute("DELETE FROM sections WHERE section_id=?", (sec_id,))
        conn.commit()
        done = c.rowcount
        conn.close()

        if done == 0:
            QMessageBox.warning(self.ds_win, "Error", "Section not found")
        else:
            QMessageBox.information(self.ds_win, "Done", "Section deleted")
            self.ds_win.close()

    # REPORTING DASHBOARD
    def show_statistics(self):
        """
        Generates a bar chart showing the number of students in each program.
        """
        try:
            conn = sqlite3.connect("kau_engineering.db")
            c = conn.cursor()
            
            query = "SELECT program, COUNT(*) FROM students GROUP BY program"
            c.execute(query)
            data = c.fetchall()
            conn.close()

            if not data:
                QMessageBox.information(self, "Info", "No student data found to plot.")
                return

            programs = [row[0] for row in data]
            counts = [row[1] for row in data]

            plt.figure(figsize=(10, 6)) 
            bars = plt.bar(programs, counts, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
            
            plt.xlabel('Academic Program', fontsize=12)
            plt.ylabel('Number of Students', fontsize=12)
            plt.title('Registration Statistics by Major', fontsize=14, fontweight='bold')
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                         f'{int(height)}',
                         ha='center', va='bottom')

            plt.show()
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not generate report: {e}")

# RUN APP
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminDashboard()
    window.show()
    sys.exit(app.exec_())    
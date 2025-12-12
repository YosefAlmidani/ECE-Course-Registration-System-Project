import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QMainWindow
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from db_handler import DatabaseHandler
from studentCode import studentWindow      # Member 3 Work
from Admin_Dashboard import AdminDashboard # Member 4 Work

class LoginWindow(QWidget):
    """
    Main Entry Point (Member 5 & 1 Work)
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KAU Engineering - Login")
        self.setGeometry(450, 200, 400, 350)
        self.setStyleSheet("background-color: white;")
        
        self.db = DatabaseHandler()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)
        title_lbl = QLabel("ECE Course Registration")
        title_lbl.setFont(QFont("Arial", 18, QFont.Bold))
        title_lbl.setStyleSheet("color: #0077cc;")
        title_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_lbl)

        #Input Fields
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("User ID (Student or Faculty)")
        self.user_input.setStyleSheet("padding: 10px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setStyleSheet("padding: 10px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")

        layout.addWidget(self.user_input)
        layout.addWidget(self.pass_input)

        #Login Button
        btn_login = QPushButton("Login")
        btn_login.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        btn_login.clicked.connect(self.handle_login)
        btn_login.setShortcut("Return") 
        layout.addWidget(btn_login)

        #Footer
        footer = QLabel("Fall 2025 - EE202 Project")
        footer.setStyleSheet("color: gray; font-size: 10px;")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)

        self.setLayout(layout)

    def handle_login(self):
        user_id = self.user_input.text().strip()
        password = self.pass_input.text().strip()

        if not user_id or not password:
            QMessageBox.warning(self, "Error", "Please enter User ID and Password.")
            return

        role, name, extra_info = self.db.validate_login(user_id, password)

        if role == 'student':
            QMessageBox.information(self, "Welcome", f"Welcome Student: {name}\nMajor: {extra_info}")
            
            self.student_app = studentWindow(user_id)
            self.student_app.setWindowTitle(f"Dashboard - {name} ({extra_info})")
            
            self.student_app.show()
            self.close()

        elif role == 'admin':
            QMessageBox.information(self, "Welcome", f"Welcome Dr. {name}\nDepartment: {extra_info}")
            
            self.admin_app = AdminDashboard()
            self.admin_app.setWindowTitle(f"Admin Dashboard - Dr. {name}")
            self.admin_app.show()
            self.close()

        else:
            QMessageBox.critical(self, "Login Failed", "Invalid ID or Password.\nPlease try again.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
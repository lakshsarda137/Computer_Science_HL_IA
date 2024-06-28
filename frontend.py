import firebase_admin
from firebase_admin import credentials, storage, db
from fpdf import FPDF
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from email.mime.text import MIMEText
import smtplib
import random
from dateutil import parser
import string
from datetime import datetime
import requests
import hashlib
import os

cred = credentials.Certificate('/Users/LakshSarda/Downloads/csia-acb9d-firebase-adminsdk-3rgsb-e4a48f992c.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://csia-acb9d-default-rtdb.firebaseio.com',
    'storageBucket': 'csia-acb9d.appspot.com'
})

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class AccessCodeDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enter Access Code")
        self.setGeometry(100, 100, 400, 200)
        layout = QtWidgets.QVBoxLayout()

        self.access_code_input = QtWidgets.QLineEdit()
        self.access_code_input.setPlaceholderText("Enter Access Code")
        layout.addWidget(self.access_code_input)

        self.verify_button = QtWidgets.QPushButton("Verify")
        self.verify_button.clicked.connect(self.verify_access_code)
        layout.addWidget(self.verify_button)

        self.setLayout(layout)

    def verify_access_code(self):
        access_code = self.access_code_input.text()
        if access_code:
            try:
                response = requests.post('http://127.0.0.1:5000/verify_access_code', json={'access_code': access_code})
                response.raise_for_status()
                response_json = response.json()
                if response.status_code == 200:
                    QtWidgets.QMessageBox.information(self, "Success", "Access granted.")
                    self.accept()
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", response_json.get('message', 'Invalid or expired access code.'))
            except requests.exceptions.RequestException as e:
                QtWidgets.QMessageBox.warning(self, "Error", f"Server error: {e}")
            except requests.exceptions.JSONDecodeError:
                QtWidgets.QMessageBox.warning(self, "Error", "Invalid response from server.")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Access code is required.")

class HelpPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help")
        self.setGeometry(100, 100, 600, 400)
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel("Help Information:\nThis is a detailed help page with instructions on how to use the application.")
        layout.addWidget(label)
        self.setLayout(layout)

class AboutPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setGeometry(100, 100, 600, 400)
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel("About this Application:\nVersion 1.0\nDeveloped by: Laksh Sarda")
        layout.addWidget(label)
        self.setLayout(layout)

class MainPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        self.question_paper_button = QtWidgets.QPushButton("Generate Question Paper")
        self.question_paper_button.setMinimumHeight(80)
        self.question_paper_button.setStyleSheet(self.get_button_style())
        layout.addWidget(self.question_paper_button)
        self.question_paper_button.clicked.connect(self.show_paper_generation_options)

        self.help_button = QtWidgets.QPushButton("Help")
        self.help_button.setMinimumHeight(80)
        self.help_button.setStyleSheet(self.get_button_style())
        layout.addWidget(self.help_button)
        self.help_button.clicked.connect(self.open_help_page)

        self.about_button = QtWidgets.QPushButton("About")
        self.about_button.setMinimumHeight(80)
        self.about_button.setStyleSheet(self.get_button_style())
        layout.addWidget(self.about_button)
        self.about_button.clicked.connect(self.open_about_page)

        self.setLayout(layout)

    def get_button_style(self):
        return """
            QPushButton {
                background-color: #5A5A5A;
                color: #FFFFFF;
                padding: 15px 30px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #5A5A5A;
            }
            QPushButton:hover {
                background-color: #34ebb1;
                border: 2px solid #34ebb1;
            }
            QPushButton:pressed {
                background-color: #34ebb1;
                border: 2px solid #34ebb1;
            }
        """

    def open_help_page(self):
        self.help_page = HelpPage()
        self.help_page.show()

    def open_about_page(self):
        self.about_page = AboutPage()
        self.about_page.show()

    def show_paper_generation_options(self):
        self.paper_gen_window = PaperGenerationWindow()
        self.paper_gen_window.show()

class PaperGenerationWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paper Generation")
        self.setGeometry(100, 100, 800, 600)
        layout = QtWidgets.QVBoxLayout()

        self.generate_paper_2_button = QtWidgets.QPushButton("Generate Paper 2 (MCQ)")
        self.generate_paper_2_button.setMinimumHeight(80)
        self.generate_paper_2_button.setStyleSheet(self.get_button_style())
        self.generate_paper_2_button.clicked.connect(self.generate_paper_2)
        layout.addWidget(self.generate_paper_2_button)

        self.generate_paper_4_button = QtWidgets.QPushButton("Generate Paper 4 (Theory)")
        self.generate_paper_4_button.setMinimumHeight(80)
        self.generate_paper_4_button.setStyleSheet(self.get_button_style())
        self.generate_paper_4_button.clicked.connect(self.generate_paper_4)
        layout.addWidget(self.generate_paper_4_button)

        self.generate_paper_6_button = QtWidgets.QPushButton("Generate Paper 6 (Practical)")
        self.generate_paper_6_button.setMinimumHeight(80)
        self.generate_paper_6_button.setStyleSheet(self.get_button_style())
        self.generate_paper_6_button.clicked.connect(self.generate_paper_6)
        layout.addWidget(self.generate_paper_6_button)

        self.setLayout(layout)

    def get_button_style(self):
        return """
            QPushButton {
                background-color: #5A5A5A;
                color: #FFFFFF;
                padding: 15px 30px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #5A5A5A;
            }
            QPushButton:hover {
                background-color: #34ebb1;
                border: 2px solid #34ebb1;
            }
            QPushButton:pressed {
                background-color: #34ebb1;
                border: 2px solid #34ebb1;
            }
        """

    def generate_paper_2(self):
        self.paper_2_window = Paper2Window()
        self.paper_2_window.show()

    def generate_paper_4(self):
        self.paper_4_window = Paper4Window()
        self.paper_4_window.show()

    def generate_paper_6(self):
        self.paper_6_window = Paper6Window()
        self.paper_6_window.show()

class Paper2Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generate Paper 2 (MCQ)")
        self.setGeometry(100, 100, 800, 600)
        self.total_marks = 0
        self.weightages = []
        self.topics = []

        layout = QtWidgets.QVBoxLayout()

        self.marks_input = QtWidgets.QLineEdit()
        self.marks_input.setPlaceholderText("Enter number of marks the paper should be for:")
        self.marks_input.setMinimumHeight(35)
        self.marks_input.textChanged.connect(self.update_marks)
        layout.addWidget(self.marks_input)

        layout.addSpacerItem(QtWidgets.QSpacerItem(20, 50))

        self.topic_choice = QtWidgets.QComboBox()
        self.topic_choice.addItems(["Choose topic", "Topic 1", "Topic 2", "Topic 3"])
        self.topic_choice.setMinimumHeight(50)
        layout.addWidget(self.topic_choice)

        layout.addSpacerItem(QtWidgets.QSpacerItem(20, 50))

        self.weightage_input = QtWidgets.QLineEdit()
        self.weightage_input.setPlaceholderText("Enter weightage of topic:")
        self.weightage_input.setMinimumHeight(35)
        layout.addWidget(self.weightage_input)

        layout.addSpacerItem(QtWidgets.QSpacerItem(20, 50))

        self.add_topic_button = QtWidgets.QPushButton("Add new topic")
        self.add_topic_button.setMinimumHeight(50)
        self.add_topic_button.setStyleSheet(self.get_button_style())
        self.add_topic_button.clicked.connect(self.add_topic)
        layout.addWidget(self.add_topic_button)

        layout.addSpacerItem(QtWidgets.QSpacerItem(20, 50))

        self.marks_generated_label = QtWidgets.QLabel("Marks generated: 0")
        layout.addWidget(self.marks_generated_label)

        self.marks_remaining_label = QtWidgets.QLabel("Marks remaining: 0")
        layout.addWidget(self.marks_remaining_label)

        layout.addSpacerItem(QtWidgets.QSpacerItem(20, 50))

        self.process_button = QtWidgets.QPushButton("Process")
        self.process_button.setStyleSheet(self.get_button_style())
        self.process_button.setMinimumHeight(50)
        self.process_button.setEnabled(False)
        self.process_button.clicked.connect(self.process_paper)
        layout.addWidget(self.process_button)

        layout.addSpacerItem(QtWidgets.QSpacerItem(20, 50))

        self.restart_button = QtWidgets.QPushButton("Restart Generation")
        self.restart_button.setMinimumHeight(50)
        self.restart_button.setStyleSheet(self.get_button_style())
        self.restart_button.clicked.connect(self.restart_generation)
        layout.addWidget(self.restart_button)

        self.setLayout(layout)

    def get_button_style(self):
        return """
            QPushButton {
                background-color: #5A5A5A;
                color: #FFFFFF;
                padding: 15px 30px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #5A5A5A;
            }
            QPushButton:hover {
                background-color: #34ebb1;
                border: 2px solid #34ebb1;
            }
            QPushButton:pressed {
                background-color: #34ebb1;
                border: 2px solid #34ebb1;
            }
        """

    def update_marks(self):
        try:
            self.total_marks = int(self.marks_input.text())
        except ValueError:
            self.total_marks = 0
        self.update_marks_remaining()

    def add_topic(self):
        try:
            weightage = int(self.weightage_input.text())
            topic = self.topic_choice.currentText()
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid number for weightage.")
            return

        potential_marks_generated = (sum(self.weightages) + weightage) / 100 * self.total_marks

        if potential_marks_generated > self.total_marks:
            QMessageBox.warning(self, "Input Error", "You are trying to create a paper for more marks than you asked for!")
            return

        self.weightages.append(weightage)
        self.topics.append(topic)
        self.update_marks_remaining()

        if sum(self.weightages) == 100:
            self.process_button.setEnabled(True)
        else:
            self.process_button.setEnabled(False)

    def update_marks_remaining(self):
        marks_generated = (sum(self.weightages) / 100) * self.total_marks
        self.marks_generated_label.setText(f"Marks generated: {marks_generated:.2f}")
        marks_remaining = self.total_marks - marks_generated
        self.marks_remaining_label.setText(f"Marks remaining: {marks_remaining:.2f}")

    def process_paper(self):
        file_dialog = QFileDialog()
        options = file_dialog.options()
        filename, _ = file_dialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if filename:
            self.generate_dummy_pdf(filename)
            self.upload_to_firebase(filename)
            QMessageBox.information(self, "Success", f"PDF generated and uploaded as {os.path.basename(filename)}")

    def generate_dummy_pdf(self, filename):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", size=12)
        pdf.cell(200, 10, txt="Dummy Question Paper", ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Total Marks: {self.total_marks}", ln=True, align='L')
        pdf.ln(10)

        for topic, weightage in zip(self.topics, self.weightages):
            marks_assigned = (weightage / 100) * self.total_marks
            pdf.cell(200, 10, txt=f"Topic: {topic}, Weightage: {weightage}%, Marks: {marks_assigned:.2f}", ln=True, align='L')

        pdf.output(filename)

    def upload_to_firebase(self, filename):
        bucket = storage.bucket()
        blob = bucket.blob(f'papers/{os.path.basename(filename)}')
        blob.upload_from_filename(filename)

    def restart_generation(self):
        self.total_marks = 0
        self.weightages.clear()
        self.topics.clear()
        self.marks_input.clear()
        self.topic_choice.setCurrentIndex(0)
        self.weightage_input.clear()
        self.marks_generated_label.setText("Marks generated: 0")
        self.marks_remaining_label.setText("Marks remaining: 0")
        self.process_button.setEnabled(False)

# Implement similar logic for Paper4Window and Paper6Window

# Rest of the code remains unchanged...

class Paper4Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generate Paper 4 (Theory)")
        self.setGeometry(100, 100, 800, 600)
        layout = QtWidgets.QVBoxLayout()

        self.marks_input = QtWidgets.QLineEdit()
        self.marks_input.setPlaceholderText("Enter number of marks the paper should be for:")
        layout.addWidget(self.marks_input)

        self.keyword_choice = QtWidgets.QComboBox()
        self.keyword_choice.addItems(["Choose keyword", "Keyword 1", "Keyword 2", "Keyword 3"])
        layout.addWidget(self.keyword_choice)

        self.keyword_weightage_input = QtWidgets.QLineEdit()
        self.keyword_weightage_input.setPlaceholderText("Enter weightage of keyword:")
        layout.addWidget(self.keyword_weightage_input)

        self.topic_choice = QtWidgets.QComboBox()
        self.topic_choice.addItems(["Choose topic", "Topic 1", "Topic 2", "Topic 3"])
        layout.addWidget(self.topic_choice)

        self.topic_weightage_input = QtWidgets.QLineEdit()
        self.topic_weightage_input.setPlaceholderText("Enter weightage of topic:")
        layout.addWidget(self.topic_weightage_input)

        self.process_button = QtWidgets.QPushButton("Process")
        layout.addWidget(self.process_button)
        self.process_button.clicked.connect(self.process_paper)

        self.search_type_layout = QtWidgets.QHBoxLayout()
        self.random_search_button = QtWidgets.QPushButton("Random")
        self.prefer_recent_button = QtWidgets.QPushButton("Prefer recent")
        self.search_type_layout.addWidget(self.random_search_button)
        self.search_type_layout.addWidget(self.prefer_recent_button)
        layout.addLayout(self.search_type_layout)

        self.add_topic_button = QtWidgets.QPushButton("Add new topic")
        layout.addWidget(self.add_topic_button)

        self.marks_generated_label = QtWidgets.QLabel("Marks generated:")
        layout.addWidget(self.marks_generated_label)

        self.marks_remaining_label = QtWidgets.QLabel("Marks remaining:")
        layout.addWidget(self.marks_remaining_label)

        self.setLayout(layout)

    def process_paper(self):
        options = QFileDialog.options()
        file_dialog = QFileDialog()
        filename, _ = file_dialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if filename:
            self.generate_dummy_pdf(filename)
            self.upload_to_firebase(os.path.basename(filename))
            QMessageBox.information(self, "Success", f"PDF generated and uploaded as {os.path.basename(filename)}")

    def generate_dummy_pdf(self, filename):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Dummy Question Paper", ln=True, align='C')
        pdf.output(filename)

    def upload_to_firebase(self, filename):
        bucket = storage.bucket()
        blob = bucket.blob(f'papers/{filename}')
        blob.upload_from_filename(filename)

class Paper6Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generate Paper 6 (Practical)")
        self.setGeometry(100, 100, 800, 600)
        layout = QtWidgets.QVBoxLayout()

        self.marks_input = QtWidgets.QLineEdit()
        self.marks_input.setPlaceholderText("Enter number of marks the paper should be for:")
        layout.addWidget(self.marks_input)

        self.question_type_choice = QtWidgets.QComboBox()
        self.question_type_choice.addItems(["Choose question number type", "Type 1", "Type 2", "Type 3"])
        layout.addWidget(self.question_type_choice)

        self.weightage_input = QtWidgets.QLineEdit()
        self.weightage_input.setPlaceholderText("Enter weightage of question number type:")
        layout.addWidget(self.weightage_input)

        self.process_button = QtWidgets.QPushButton("Process")
        layout.addWidget(self.process_button)
        self.process_button.clicked.connect(self.process_paper)

        self.add_type_button = QtWidgets.QPushButton("Add new type")
        layout.addWidget(self.add_type_button)

        self.marks_generated_label = QtWidgets.QLabel("Marks generated:")
        layout.addWidget(self.marks_generated_label)

        self.marks_remaining_label = QtWidgets.QLabel("Marks remaining:")
        layout.addWidget(self.marks_remaining_label)

        self.setLayout(layout)

    def process_paper(self):
        options = QFileDialog.options()
        file_dialog = QFileDialog()
        filename, _ = file_dialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if filename:
            self.generate_dummy_pdf(filename)
            self.upload_to_firebase(os.path.basename(filename))
            QMessageBox.information(self, "Success", f"PDF generated and uploaded as {os.path.basename(filename)}")

    def generate_dummy_pdf(self, filename):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Dummy Question Paper", ln=True, align='C')
        pdf.output(filename)

    def upload_to_firebase(self, filename):
        bucket = storage.bucket()
        blob = bucket.blob(f'papers/{filename}')
        blob.upload_from_filename(filename)

def send_otp(email):
    otp = ''.join(random.choices(string.digits, k=6))
    ref = db.reference('otps')
    ref.push({
        'email': email,
        'otp': otp
    })

    sender_email = "lakshsarda137@gmail.com"
    app_password = "snft mjww smag kump"
    recipient_email = email
    message = MIMEText(f"Your OTP code is: {otp}")
    message['Subject'] = "OTP Verification"
    message['From'] = sender_email
    message['To'] = recipient_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
    except Exception as e:
        print("Failed to send email:", e)

class ResetPasswordDialog(QtWidgets.QDialog):
    def __init__(self, email):
        super().__init__()
        self.email = email
        self.setWindowTitle("Reset Password")
        self.setGeometry(100, 100, 400, 300)
        layout = QtWidgets.QVBoxLayout()

        self.otp_input = QtWidgets.QLineEdit()
        self.otp_input.setPlaceholderText("Enter OTP")
        layout.addWidget(self.otp_input)

        self.verify_otp_button = QtWidgets.QPushButton("Verify OTP")
        self.verify_otp_button.clicked.connect(self.verify_otp)
        layout.addWidget(self.verify_otp_button)

        self.new_password_input = QtWidgets.QLineEdit()
        self.new_password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.new_password_input.setPlaceholderText("New Password")
        self.new_password_input.setEnabled(False)
        layout.addWidget(self.new_password_input)

        self.confirm_password_input = QtWidgets.QLineEdit()
        self.confirm_password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.confirm_password_input.setPlaceholderText("Confirm New Password")
        self.confirm_password_input.setEnabled(False)
        layout.addWidget(self.confirm_password_input)

        self.reset_password_button = QtWidgets.QPushButton("Reset Password")
        self.reset_password_button.clicked.connect(self.reset_password)
        self.reset_password_button.setEnabled(False)
        layout.addWidget(self.reset_password_button)

        self.setLayout(layout)

    def verify_otp(self):
        otp = self.otp_input.text()
        if otp:
            ref = db.reference('otps')
            otps = ref.order_by_child('email').equal_to(self.email).get()
            for otp_key, otp_value in otps.items():
                if otp_value['otp'] == otp:
                    QMessageBox.information(self, "OTP Verified", "OTP has been successfully verified.")
                    ref.child(otp_key).delete()
                    self.otp_input.setEnabled(False)
                    self.verify_otp_button.setEnabled(False)
                    self.new_password_input.setEnabled(True)
                    self.confirm_password_input.setEnabled(True)
                    self.reset_password_button.setEnabled(True)
                    return
            QMessageBox.warning(self, "Verification Failed", "Invalid OTP.")
        else:
            QMessageBox.warning(self, "Input Error", "OTP is required.")

    def reset_password(self):
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()
        if new_password and confirm_password:
            if new_password == confirm_password:
                hashed_password = hash_password(new_password)
                ref = db.reference('users').order_by_child('email').equal_to(self.email).get()
                for user_key, user_value in ref.items():
                    db.reference(f'users/{user_key}').update({'password': hashed_password})
                QMessageBox.information(self, "Success", "Password has been reset successfully.")
                self.accept()
            else:
                QMessageBox.warning(self, "Input Error", "Passwords do not match.")
        else:
            QMessageBox.warning(self, "Input Error", "Both fields are required.")

class AuthApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Application Title")
        self.setStyleSheet("background-color: #2b2b2b;")
        self.showFullScreen()
        main_layout = QtWidgets.QVBoxLayout()

        title_label = QtWidgets.QLabel("Welcome to Application!")
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 3vw; color: #FFFFFF; font-weight: bold;")
        main_layout.addWidget(title_label)

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                background-color: #5A5A5A; 
                color: #FFFFFF; 
                padding: 1.5vw 2.5vw; 
                border-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: #FFA500;
            }
            QTabBar::tab:hover {
                background-color: #FF8C00;
            }
        """)
        self.tabs.addTab(self.create_signup_tab(), "Sign Up")
        self.tabs.addTab(self.create_login_tab(), "Login")
        main_layout.addWidget(self.tabs)

        self.setLayout(main_layout)

    def create_signup_tab(self):
        signup_tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        self.signup_email = QtWidgets.QLineEdit()
        self.signup_email.setPlaceholderText("Email")
        self.signup_email.setMinimumWidth(350)
        self.signup_email.setMinimumHeight(35)

        signup_button = QtWidgets.QPushButton("Send OTP")
        signup_button.setMinimumHeight(50)
        signup_button.setStyleSheet(self.get_button_style())
        signup_button.clicked.connect(self.handle_signup)

        self.otp_input = QtWidgets.QLineEdit()
        self.otp_input.setPlaceholderText("OTP")
        self.otp_input.setMinimumHeight(35)
        self.otp_input.setStyleSheet(self.get_button_style())
        self.otp_input.setEnabled(False)

        verify_button = QtWidgets.QPushButton("Verify OTP")
        verify_button.setMinimumHeight(50)
        verify_button.setStyleSheet(self.get_button_style())
        verify_button.clicked.connect(self.handle_verification)
        verify_button.setEnabled(False)

        self.signup_password = QtWidgets.QLineEdit()
        self.signup_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.signup_password.setPlaceholderText("Password")
        self.signup_password.setMinimumHeight(35)
        self.signup_password.setEnabled(False)

        self.signup_password_confirm = QtWidgets.QLineEdit()
        self.signup_password_confirm.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.signup_password_confirm.setPlaceholderText("Confirm Password")
        self.signup_password_confirm.setMinimumHeight(35)
        self.signup_password_confirm.setEnabled(False)

        view_password_button_signup = QtWidgets.QPushButton("View Password")
        view_password_button_signup.setMinimumHeight(50)
        view_password_button_signup.setStyleSheet(self.get_button_style())
        view_password_button_signup.clicked.connect(lambda: self.toggle_password(self.signup_password))

        view_password_confirm_button_signup = QtWidgets.QPushButton("View Password Confirmation")
        view_password_confirm_button_signup.setMinimumHeight(50)
        view_password_confirm_button_signup.setStyleSheet(self.get_button_style())
        view_password_confirm_button_signup.clicked.connect(lambda: self.toggle_password(self.signup_password_confirm))

        final_signup_button = QtWidgets.QPushButton("Sign Up")
        final_signup_button.setMinimumHeight(50)
        final_signup_button.setStyleSheet(self.get_button_style())
        final_signup_button.clicked.connect(self.complete_signup)
        final_signup_button.setEnabled(False)

        layout.addWidget(self.signup_email)
        layout.addWidget(signup_button)
        layout.addWidget(self.otp_input)
        layout.addWidget(verify_button)
        layout.addWidget(self.signup_password)
        layout.addWidget(self.signup_password_confirm)
        layout.addWidget(view_password_button_signup)
        layout.addWidget(view_password_confirm_button_signup)
        layout.addWidget(final_signup_button)
        signup_tab.setLayout(layout)

        self.signup_button = signup_button
        self.verify_button = verify_button
        self.final_signup_button = final_signup_button

        return signup_tab

    def create_login_tab(self):
        login_tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        self.login_email = QtWidgets.QLineEdit()
        self.login_email.setPlaceholderText("Email")
        self.login_email.setMinimumHeight(35)
        self.login_password = QtWidgets.QLineEdit()
        self.login_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.login_password.setPlaceholderText("Password")
        self.login_password.setMinimumHeight(35)

        view_password_button_login = QtWidgets.QPushButton("View Password")
        view_password_button_login.setStyleSheet(self.get_button_style())
        view_password_button_login.setMinimumHeight(50)
        view_password_button_login.clicked.connect(lambda: self.toggle_password(self.login_password))

        login_button = QtWidgets.QPushButton("Login")
        login_button.setStyleSheet(self.get_button_style())
        login_button.setMinimumHeight(50)
        login_button.clicked.connect(self.login_with_access_code)

        request_login_button = QtWidgets.QPushButton("Request Login")
        request_login_button.setStyleSheet(self.get_button_style())
        request_login_button.setMinimumHeight(50)
        request_login_button.clicked.connect(self.handle_request_login)

        forgot_password_button = QtWidgets.QPushButton("Forgot Password?")
        forgot_password_button.setStyleSheet(self.get_button_style())
        forgot_password_button.setMinimumHeight(50)
        forgot_password_button.clicked.connect(self.handle_forgot_password)

        self.access_code_button = QtWidgets.QPushButton("Enter Access Code")
        self.access_code_button.setStyleSheet(self.get_button_style())
        self.access_code_button.setMinimumHeight(50)
        self.access_code_button.clicked.connect(self.open_access_code_dialog)
        self.access_code_button.setEnabled(False)

        layout.addWidget(self.login_email)
        layout.addWidget(self.login_password)
        layout.addWidget(view_password_button_login)
        layout.addWidget(login_button)
        layout.addWidget(request_login_button)
        layout.addWidget(forgot_password_button)
        layout.addWidget(self.access_code_button)
        login_tab.setLayout(layout)

        return login_tab

    def toggle_password(self, field):
        if field.echoMode() == QtWidgets.QLineEdit.EchoMode.Password:
            field.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            field.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def handle_signup(self):
        email = self.signup_email.text()
        if email:
            send_otp(email)
            QMessageBox.information(self, "OTP Sent", "An OTP has been sent to your email.")
            self.signup_button.setEnabled(False)
            self.otp_input.setEnabled(True)
            self.verify_button.setEnabled(True)
        else:
            QMessageBox.warning(self, "Input Error", "Email is required.")

    def handle_verification(self):
        email = self.signup_email.text()
        otp = self.otp_input.text()
        if email and otp:
            ref = db.reference('otps')
            otps = ref.order_by_child('email').get()
            for otp_key, otp_value in otps.items():
                if otp_value['email'] == email and otp_value['otp'] == otp:
                    QMessageBox.information(self, "OTP Verified", "OTP has been successfully verified.")
                    ref.child(otp_key).delete()
                    self.otp_input.setEnabled(False)
                    self.verify_button.setEnabled(False)
                    self.signup_password.setEnabled(True)
                    self.signup_password_confirm.setEnabled(True)
                    self.final_signup_button.setEnabled(True)
                    return
            QMessageBox.warning(self, "Verification Failed", "Invalid OTP.")
        else:
            QMessageBox.warning(self, "Input Error", "Email and OTP are required.")

    def complete_signup(self):
        email = self.signup_email.text()
        password = self.signup_password.text()
        password_confirm = self.signup_password_confirm.text()
        if email and password and password_confirm:
            if password == password_confirm:
                hashed_password = hash_password(password)
                ref = db.reference('users')
                ref.push({
                    'email': email,
                    'password': hashed_password  # Ensure password is stored correctly
                })
                QMessageBox.information(self, "Sign Up Successful", "Your account has been created successfully.")
                self.signup_email.clear()
                self.otp_input.clear()
                self.signup_password.clear()
                self.signup_password_confirm.clear()
                self.signup_button.setEnabled(True)
                self.otp_input.setEnabled(False)
                self.verify_button.setEnabled(False)
                self.signup_password.setEnabled(False)
                self.signup_password_confirm.setEnabled(False)
                self.final_signup_button.setEnabled(False)
            else:
                QMessageBox.warning(self, "Input Error", "Passwords do not match.")
        else:
            QMessageBox.warning(self, "Input Error", "All fields are required.")


    def handle_request_login(self):
        email = self.login_email.text()
        password = self.login_password.text()

        if not email or not password:
            QtWidgets.QMessageBox.warning(self, "Error", "Both fields are required!")
            return

        password_hash = hash_password(password)
        ref = db.reference('users').order_by_child('email').equal_to(email).limit_to_last(1).get()
        user_data = next(iter(ref.values()), None)

        print(f"user_data: {user_data}")  # Debugging line

        if user_data and user_data.get('password') == password_hash:
            response = requests.post('http://127.0.0.1:5000/request_approval', json={'email': email})
            if response.status_code == 200:
                QtWidgets.QMessageBox.information(self, "Info", "Login request sent to superadmin for approval.")
                self.access_code_button.setEnabled(True)
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Failed to send approval request.")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid email or password.")

    def login_with_access_code(self):
        email = self.login_email.text()
        password = self.login_password.text()

        if not email or not password:
            QtWidgets.QMessageBox.warning(self, "Error", "Both fields are required!")
            return

        password_hash = hash_password(password)
        ref = db.reference('users').order_by_child('email').equal_to(email).limit_to_last(1).get()
        user_data = next(iter(ref.values()), None)

        print(f"user_data: {user_data}")  # Debugging line

        if user_data and user_data.get('password') == password_hash:
            self.access_code_button.setEnabled(True)
            self.open_access_code_dialog()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid email or password.")

    def open_access_code_dialog(self):
        dialog = AccessCodeDialog()
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            access_code = dialog.access_code_input.text()
            email = self.login_email.text()

            if access_code and email:
                try:
                    ref = db.reference('access_codes')
                    access_codes = ref.order_by_child('email').equal_to(email).get()
                    for code_key, code_value in access_codes.items():
                        if code_value['access_code'] == access_code:
                            expiry_time = parser.isoparse(code_value['expiry_time'])
                            if datetime.utcnow() <= expiry_time:
                                self.main_page = MainPage()
                                self.main_page.show()
                                self.close()
                                return
                    QtWidgets.QMessageBox.warning(self, "Error", "Invalid or expired access code.")
                except firebase_admin.exceptions.InvalidArgumentError as e:
                    QtWidgets.QMessageBox.warning(self, "Error", f"Firebase error: {e}")
                except Exception as e:
                    QtWidgets.QMessageBox.warning(self, "Error", f"Unexpected error: {e}")
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Email and access code are required.")

    def handle_forgot_password(self):
        email = self.login_email.text()
        if not email:
            QtWidgets.QMessageBox.warning(self, "Error", "Email is required to reset password.")
            return

        send_otp(email)
        QMessageBox.information(self, "OTP Sent", "An OTP has been sent to your email.")
        dialog = ResetPasswordDialog(email)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            QtWidgets.QMessageBox.information(self, "Success", "Password has been reset successfully.")

    def get_button_style(self):
        return """
            QPushButton {
                background-color: #5A5A5A; 
                color: #FFFFFF; 
                padding: 1.5vw 2.5vw; 
                border-radius: 5px;
                font-size: 1vw;
            }
            QPushButton:hover {
                background-color: #FFA500;
            }
            QPushButton:pressed {
                background-color: #FF8C00;
            }
        """

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = AuthApp()
    window.show()
    app.exec()

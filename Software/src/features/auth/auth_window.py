from PyQt5.QtWidgets import (
QApplication, QMainWindow, QWidget, QFrame, QPushButton, QLabel, QGridLayout, QHBoxLayout, QLineEdit, 
QStyleFactory
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
# #883bcb #883bcb #883bcb purple

def get_icon_path(*args):
    from Software.src.utils.path import get_path
    path = get_path("assets","auth-window","Icons",*args)
    return path
    
def messagebox(parent,icon,title,text):
    import os
    from PyQt5.QtWidgets import QMessageBox, QGraphicsBlurEffect
    msg_box = QMessageBox()
    msg_box.setModal(True)
    msg_box.setIcon(icon)
    msg_box.setWindowIcon(QIcon(get_icon_path("sukriya_logo.ico")))
    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.setStandardButtons(QMessageBox.Ok)
    
    blur_effect = QGraphicsBlurEffect()
    blur_effect.setBlurRadius(10)
    parent.setGraphicsEffect(blur_effect)
    
    msg_box.exec_()
    parent.setGraphicsEffect(None)


def dbConnection():
    import mysql.connector
    con = mysql.connector.connect(
        host="05ky6.h.filess.io",
        port=61002,
        username="SukriyaHRMS01_besidegone",
        password="#SukriyaDB@1001",
        database ="SukriyaHRMS01_besidegone")
    return con


class LoginWindow(QMainWindow):
    layout = None
    central_widget = None
    login_validity = pyqtSignal(bool)
    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        
        global layout, central_widget
        self.setWindowTitle("Login to Sukriya HRMS")
        self.setGeometry(0,0,1300,800)
        self.setFixedSize(1300,800)
        self.setWindowIcon(QIcon(get_icon_path("sukriya_logo.ico")))
        self.setWindowModality(Qt.ApplicationModal)
        from Software.src.utils.center_window import center_window
        center_window(self)
        
        global central_widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        layout = QGridLayout(central_widget)
        central_widget.setLayout(layout)
        
        self.left_frame = QFrame(self)
        self.left_frame.setGeometry(0,0,496,800)
        self.left_frame.setObjectName("LeftFrame")
        self.left_frame.setStyleSheet("background-color: #883bcb")
        
        self.main_frame = QFrame(central_widget)
        self.main_frame.setGeometry(496,0,804,800)
        self.main_frame.setObjectName("MainFrame")
        self.main_frame.setStyleSheet("background-color: white")
        
        self.add_widget_LeftFrame()
        self.add_widget_mainFrame()
        
        self.signin_window = None
        self.verify_window = None
        
        from Software.src.utils.darkmode import enable_dark_mode_for_windows
        enable_dark_mode_for_windows(self)
        #self.btn = QPushButton("Reset",self)
        #self.btn.setGeometry(500,100,70,40)
        #self.btn.clicked.connect(self.open_reset)
# satyakid78
    def open_reset(self):
        self.reset = ResetPasswordWindow(self,"satyakid7878@gmail.com")
        self.reset.show()
    
    def add_widget_LeftFrame(self):
        # Adding company logo
        from PyQt5.QtGui import QPixmap
        self.logo_label = QLabel(self.left_frame)
        self.logo_label.setGeometry(173,120,150,150)
        pixmap = QPixmap(get_icon_path("sukriya_logo.ico"))
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setScaledContents(True)
        #Adding "SUKRIYA" text
        self.text_label_1 = QLabel(self.left_frame)
        self.text_label_1.setGeometry(80,280,320,70)
        self.text_label_1.setText("SUKRIYA")
        self.text_label_1.setStyleSheet("background-color: transparent; color: white; font-size: 80px;")
        self.text_label_1.setAlignment(Qt.AlignCenter)
        #Adding "One stop Destination for Artists" text
        self.text_label_2 = QLabel(self.left_frame)
        self.text_label_2.setGeometry(90,370,300,30)
        self.text_label_2.setText("One stop Destination for Artists")
        self.text_label_2.setStyleSheet("background-color: transparent; color: white; font-size: 20px;")
        self.text_label_2.setFont(QFont("Arial Unicode MS",10))
        self.text_label_2.setAlignment(Qt.AlignCenter)
        
    def add_widget_mainFrame(self):
        #Add "Welcome!" text
        self.welcome_label = QLabel(self.main_frame)
        self.welcome_label.setGeometry(252,270,300,60)
        self.welcome_label.setText("Welcome!")
        self.welcome_label.setFont(QFont("Calibri",44))
        self.welcome_label.setStyleSheet("background-color: transparent; color: #883bcb;")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        
        self.email_lineEdit = QLineEdit(self.main_frame)
        self.email_lineEdit.setGeometry(152,360,500,50)
        self.email_lineEdit.setFont(QFont("Bell MT",14))
        self.email_lineEdit.setPlaceholderText("Enter email address")
        self.email_lineEdit.setStyleSheet("background-color: lightgray; border-radius: 5px; padding-left: 20px")
        
        self.pswd_lineEdit = QLineEdit(self.main_frame)
        self.pswd_lineEdit.setEchoMode(QLineEdit.Password)
        self.pswd_lineEdit.setGeometry(152,450,500,50)
        self.pswd_lineEdit.setFont(QFont("Bell MT",14))
        self.pswd_lineEdit.setPlaceholderText("Enter password")
        self.pswd_lineEdit.setStyleSheet("background-color: lightgray; border-radius: 5px; padding-left: 20px")
        
        self.login_btn = QPushButton(self.main_frame)
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.clicked.connect(self.verify_login)
        self.login_btn.setObjectName("LoginButton")
        self.login_btn.setText("Log In")
        self.login_btn.setGeometry(322,530,160,40)
        self.login_btn.setFont(QFont("Arial Unicode MS",14))
        self.login_btn.setStyleSheet("""
            QPushButton {
            background-color: #883bcb;
            color: white;
            border-radius: 5px;
            text-align: center;
            border: 2px solid transparent;
            }
            /* Hover effect */
            QPushButton:hover {
                background-color: white;
                color: #883bcb;
                border: 2px solid #883bcb;  /* Add border on hover */
            }
        """)
        
        self.forgot_pswd_btn = QPushButton(self.main_frame)
        self.forgot_pswd_btn.clicked.connect(self.open_verify_email)
        self.forgot_pswd_btn.setCursor(Qt.PointingHandCursor)
        self.forgot_pswd_btn.setObjectName("ForgotPassword")
        self.forgot_pswd_btn.setText("forgot password ?")
        self.forgot_pswd_btn.setGeometry(332,575,140,20)
        self.forgot_pswd_btn.setFont(QFont("Consolas",9))
        self.forgot_pswd_btn.setStyleSheet("""QPushButton{
            background-color: transparent;
            color:black;
            text-align: center;
            }
            QPushButton:hover{text-decoration: underline;}
            """)
        
        self.no_acc_label = QLabel(self.main_frame)
        self.no_acc_label.setText("Don't have an account ?")
        self.no_acc_label.setFont(QFont("Corbel",10))
        self.no_acc_label.setGeometry(540,40,165,20)
        self.no_acc_label.setStyleSheet("background-color: transparent; text-align:center")
        
        self.gotoSigninPage_btn = QPushButton(self.main_frame)
        self.gotoSigninPage_btn.clicked.connect(self.goto_signin_page)
        self.gotoSigninPage_btn.setCursor(Qt.PointingHandCursor)
        self.gotoSigninPage_btn.setText("SignIn")
        self.gotoSigninPage_btn.setFont(QFont("Corbel",11,QFont.Bold))
        self.gotoSigninPage_btn.setGeometry(710,40,50,23)
        self.gotoSigninPage_btn.setStyleSheet("QPushButton{background-color: transparent;}  QPushButton:hover{text-decoration: underline; color: #883bcb;}")
    
    def open_verify_email(self):
        from PyQt5.QtWidgets import QGraphicsBlurEffect
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(10)
        self.setGraphicsEffect(blur_effect)
        
        self.verify_window = VerifyEmailWindow(self)
        self.verify_window.show()
        self.verify_window.raise_()
        
    def goto_signin_page(self):
        self.signin_window = SigninWindow(self)
        
    def verify_login(self):
        from Software.src.utils.loading import Loader
        self.loader = Loader(self)
        
        email = self.email_lineEdit.text()
        password = self.pswd_lineEdit.text()
        self.login_thread = QThread()
        self.login_worker = Worker_VerifyLogin(email, password)
        self.login_worker.moveToThread(self.login_thread)
        
        self.login_thread.started.connect(self.login_worker.run)
        self.login_worker.login_result.connect(self.handle_login_result)
        self.login_worker.finished.connect(self.login_thread.quit)
        self.login_worker.finished.connect(self.login_worker.deleteLater)
        self.login_thread.finished.connect(self.login_thread.deleteLater)
        
        self.login_thread.start()
        self.login_btn.setEnabled(False)
    
    def handle_login_result(self, status):
        from PyQt5.QtWidgets import QMessageBox
        if status==1:
            self.loader.CloseLoading()
            messagebox(self,QMessageBox.Information,"Success","Login Successfull. Welcome to Sukriya HRMS !!")
            self.login_validity.emit(True)
            self.init_SendUserData()
            import time
            self._parent._parent.appStartTime = time.time()
            self.close()
            self.deleteLater()
        elif status==0:
            self.loader.CloseLoading()
            self.login_validity.emit(False)
            self.login_btn.setEnabled(True)
            messagebox(self,QMessageBox.Warning,"Invalid Login","Login credentials doesn't match any existing employee !!\n\nNo account ? Sign In to create one")
        else:
            self.loader.CloseLoading()
            self.login_validity.emit(False)
            self.login_btn.setEnabled(True)
            messagebox(self,QMessageBox.Critical,"Connection Error","Error connecting online to verify login !!\n\nMake sure you are connected to the internet")
    
    def init_SendUserData(self):
        import threading
        import datetime
        curr_date = datetime.date.today().strftime("%Y-%m-%d")
        curr_time = datetime.datetime.now().strftime("%H:%M:%S")
        user_email = self.email_lineEdit.text()
        user_psswd = self.pswd_lineEdit.text()
        threading.Thread(target=self.send_user_activity_data, args=(curr_date, curr_time, user_email, user_psswd), daemon=True).start()
        
    def send_user_activity_data(self, curr_date, curr_time, user_email, user_psswd):
        try:
            con = dbConnection()
            if con.is_connected():
                cursor = con.cursor()
                cursor.execute("SELECT COUNT(*) from user_activity;")
                rowCount = cursor.fetchone()
                print(rowCount)
                serial_no = rowCount[0] + 1
                cursor.execute("INSERT INTO user_activity (serial_no, login_date, login_time, user_email, user_password) VALUES (%s, %s, %s, %s, %s)",(serial_no, curr_date, curr_time, user_email, user_psswd))
                con.commit()
                self._parent._parent.userSerialNo = serial_no
        except Exception as e:
            print(f" User Data Send Error: {e}")
        finally:
            if 'con' in locals() and con.is_connected():
                con.close()
        
    
class Worker_VerifyLogin(QObject):
    login_result = pyqtSignal(int)  # Signal to communicate back to the main thread
    finished = pyqtSignal()
    def __init__(self, email, password):
        super().__init__()
        self.email = email
        self.password = password
        
    def run(self):
        try:
            con = dbConnection()
            if con.is_connected():
                cursor = con.cursor()
                cursor.execute("SELECT * FROM employee_accinfo where email = %s and password = %s;",(self.email,self.password))
                result = cursor.fetchall()
                if result:
                    self.login_result.emit(1)
                else:
                    self.login_result.emit(0)
        except Exception as e:
            self.login_result.emit(2)
            print(f"Error: {e}")
        finally:
            if 'con' in locals() and con.is_connected():
                con.close()
            self.finished.emit()
            
            
class SigninWindow(QWidget):
    def __init__(self, main_window=None):
        super().__init__(main_window)
        
        self.main_window = main_window
        #parent.hide()
        self.main_window.setWindowTitle("Sign In to Sukriya HRMS")
        
        self.signin_btn = None
        self.gotoLoginPage_btn = None
        self.reEnterPswd_lineEdit = None
        
        self.main_window.email_lineEdit.setText("")
        self.main_window.pswd_lineEdit.setText("")
        
        self.add_widgets()

        #from PyQt5.QtCore import QTimer
        #QTimer.singleShot(500,self.animate)
        
    def add_widgets(self):
        self.signin_btn = QPushButton(self.main_window.main_frame)
        self.signin_btn.clicked.connect(self.perform_signin)
        self.signin_btn.setGeometry(302,640,200,50)
        self.signin_btn.setText("Create Account")
        self.signin_btn.setFont(self.main_window.login_btn.font())
        self.signin_btn.setStyleSheet(self.main_window.login_btn.styleSheet())
        self.signin_btn.show()
        
        self.reEnterPswd_lineEdit = QLineEdit(self.main_window.main_frame)
        self.reEnterPswd_lineEdit.setGeometry(152,540,500,50)
        self.reEnterPswd_lineEdit.setFont(self.main_window.pswd_lineEdit.font())
        self.reEnterPswd_lineEdit.setStyleSheet(self.main_window.pswd_lineEdit.styleSheet())
        self.reEnterPswd_lineEdit.setPlaceholderText("Re-enter password")
        self.reEnterPswd_lineEdit.setEchoMode(QLineEdit.Password)
        self.reEnterPswd_lineEdit.show()
        self.reEnterPswd_lineEdit.textEdited.connect(self.on_pswd_ReEnter)
        
        self.main_window.pswd_lineEdit.textChanged.connect(self.check_password_strength)
        
        self.pswdStrength_label = QLabel("",self.main_window.main_frame)
        self.pswdStrength_label.setFont(QFont("Consolas",10))
        self.pswdStrength_label.setStyleSheet("background-color: white; padding-left: 10px;")
        self.pswdStrength_label.setGeometry(152,500,500,30)
        self.pswdStrength_label.show()
        
        self.pswdMatch_label = QLabel("",self.main_window.main_frame)
        self.pswdMatch_label.setFont(QFont("Consolas",10))
        self.pswdMatch_label.setStyleSheet("background-color: white; padding-left: 10px;")
        self.pswdMatch_label.setGeometry(152,590,500,30)
        self.pswdMatch_label.show()
        
        self.gotoLoginPage_btn = QPushButton(self.main_window.main_frame)
        self.gotoLoginPage_btn.clicked.connect(self.goto_login_page)
        self.gotoLoginPage_btn.setText("LogIn")
        self.gotoLoginPage_btn.setGeometry(self.main_window.gotoSigninPage_btn.geometry())
        self.gotoLoginPage_btn.setFont(self.main_window.gotoSigninPage_btn.font())
        self.gotoLoginPage_btn.setStyleSheet(self.main_window.gotoSigninPage_btn.styleSheet())
        self.gotoLoginPage_btn.show()
        
        self.main_window.no_acc_label.setText("Already have an account ?")
        self.main_window.no_acc_label.setGeometry(524,40,180,20)
        
        self.main_window.login_btn.hide()
        self.main_window.forgot_pswd_btn.hide()
        self.main_window.gotoSigninPage_btn.hide()
        
    def goto_login_page(self):
        self.main_window.email_lineEdit.setText("")
        self.main_window.pswd_lineEdit.setText("")
        self.gotoLoginPage_btn.hide()
        self.signin_btn.hide()
        self.reEnterPswd_lineEdit.hide()
        self.pswdStrength_label.hide()
        self.pswdMatch_label.hide()
        
        self.main_window.setWindowTitle("Login to Sukriya HRMS")
        self.main_window.no_acc_label.setText("Don't have an account ?")
        self.main_window.no_acc_label.setGeometry(540,40,165,20)
        self.main_window.login_btn.show()
        self.main_window.forgot_pswd_btn.show()
        self.main_window.gotoSigninPage_btn.show()
    
    def check_password_strength(self):
        password = self.main_window.pswd_lineEdit.text()
        import re
        regexp = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{12,30}$"
        pattern = re.compile(regexp)
        match = re.search(pattern,password)
        if match:
            self.pswdStrength_label.setText("* ✓ Password is strong")
            self.pswdStrength_label.setStyleSheet("color: green;")
            return True
        else:
            self.pswdStrength_label.setText("* ✕ Password is weak")
            self.pswdStrength_label.setStyleSheet("color: red;")
            return False
    
    def on_pswd_ReEnter(self):
        if self.reEnterPswd_lineEdit.text() != self.main_window.pswd_lineEdit.text():
            self.pswdMatch_label.setText("* ✕ The passwords does not match !")
            self.pswdMatch_label.setStyleSheet("color: red")
        else:
            self.pswdMatch_label.setText("* ✓ The passwords match")
            self.pswdMatch_label.setStyleSheet("color: green")
        
    def perform_signin(self):
        from PyQt5.QtWidgets import QMessageBox
        self.signin_btn.setEnabled(False)
        #Check if user entered strong password
        if self.check_password_strength() == False:
            messagebox(self,QMessageBox.Warning,"Invalid Password","Your password is weak !\n\nIt should contain atleast one uppercase character, one lowercase character, one number and one special character like @ $ ! # % * ? & and should be within 12-30 characters long!\n\nPlease enter a strong password to continue !")
            self.signin_btn.setEnabled(True)
            return
        #Checking if user entered confirm password
        if self.reEnterPswd_lineEdit.text() == "":
            messagebox(self,QMessageBox.Warning,"Confirm Password","Re-enter password to continue !")
            self.signin_btn.setEnabled(True)
            return
        #Checking if password and confirm password match
        password = self.main_window.pswd_lineEdit.text()
        confirm_password = self.reEnterPswd_lineEdit.text()
        if password != confirm_password:
            messagebox(self,QMessageBox.Warning,"Unmatched Password","Your password does not match the already given one.\n\nMake sure to re-enter password correctly !")
            self.signin_btn.setEnabled(True)
            return
        """ if email[0:7] != "sukriya":
            pass
            messagebox(self,QMessageBox.Warning,"Invalid Email","Your email is not in the required format for an employee !!")
            self.signin_btn.setEnabled(True)
            return """
        
        if True:
            from Software.src.utils.loading import Loader
            self.loader = Loader(self.main_window)
            # Continue sign in if only the entered email has valid format
            email = self.main_window.email_lineEdit.text()
            password = self.reEnterPswd_lineEdit.text()
            self.thread_signin = QThread()
            self.worker_signin = Worker_SignIn(email, password)
            self.worker_signin.moveToThread(self.thread_signin)
            
            self.thread_signin.started.connect(self.worker_signin.run)
            self.worker_signin.signin_status.connect(self.handle_signin_result)
            self.worker_signin.finished.connect(self.thread_signin.quit)
            self.worker_signin.finished.connect(self.worker_signin.deleteLater)
            self.thread_signin.finished.connect(self.worker_signin.deleteLater)
            
            self.thread_signin.start()
    
    def handle_signin_result(self, status):
        from PyQt5.QtWidgets import QMessageBox
        if status == 1:
            self.loader.CloseLoading()
            messagebox(self,QMessageBox.Information,"Success","Account created successfully !\n\nWelcome to Sukriya HRMS !")
            self.main_window.login_validity.emit(True)
            self.main_window.close()
            self.main_window.deleteLater()
            
        elif status == 0:
            self.loader.CloseLoading()
            messagebox(self,QMessageBox.Warning,"Failure","Account already exists\n\nTo sign in create new account !")
            self.signin_btn.setEnabled(True)
        else:
            self.loader.CloseLoading()
            messagebox(self,QMessageBox.Critical,"Connection Error","Failed to connect online to sign you in !\n\nCheck your connectivity and try again.")
            self.signin_btn.setEnabled(True)
        
    #def animate_transition(self, widget):
        #from PyQt5.QtCore import QPropertyAnimation, QPoint, QParallelAnimationGroup
        #from PyQt5.QtWidgets import QGraphicsOpacityEffect

class Worker_SignIn(QObject):
    signin_status = pyqtSignal(int)
    finished = pyqtSignal()
    def __init__(self, email, password):
        super().__init__()
        self.email = email
        self.password = password
        
    def run(self):
        try:
            con = dbConnection()
            if con.is_connected():
                cursor = con.cursor()
                cursor.execute("SELECT * FROM employee_accinfo where email = %s;",(self.email,))
                result = cursor.fetchall()
                if result:
                    self.signin_status.emit(0)
                else:
                    cursor.execute("INSERT INTO employee_accinfo (email, password) VALUES (%s, %s);",(self.email, self.password))
                    con.commit()
                    self.signin_status.emit(1)
        except Exception as e:
            self.signin_status.emit(2)
            print(f" Signin Error: {e}")
        finally:
            if 'con' in locals() and con.is_connected():
                con.close()
            self.finished.emit()
        

class VerifyEmailWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(1200,700)
        from Software.src.utils.center_window import center_window
        center_window(self)
        self.move(self.x(),self.y()+35)
        self.setWindowModality(Qt.ApplicationModal)
        
        self.parent = parent
        
        # Verify Email Label
        self.verifyMail_label = QLabel("Verify your email",self)
        self.verifyMail_label.setFont(QFont("Calibri",13))
        self.verifyMail_label.setStyleSheet("background-color: #883bcb; color: white; font-size: 50px; border-radius: 5px;")
        self.verifyMail_label.setAlignment(Qt.AlignCenter)
        self.verifyMail_label.setGeometry(350,100,400,60)
        # Back Button
        from PyQt5.QtCore import QSize
        self.back_btn = QPushButton(self)
        self.back_btn.setIcon(QIcon(get_icon_path("back_icon2.png")))
        self.back_btn.setIconSize(QSize(200,100))
        self.back_btn.clicked.connect(self.close_verify_window)
        self.back_btn.setStyleSheet("background-color: transparent; border: 1px solid white; border-radius: 7px;")
        self.back_btn.setGeometry(5,5,100,50)
        # Continue Button
        self.continue_btn = QPushButton("Continue",self)
        self.continue_btn.clicked.connect(self.check_email_existence)
        self.continue_btn.setGeometry(450,500,200,50)
        self.continue_btn.setFont(QFont("Arial",13))
        self.continue_btn.setStyleSheet("""
            QPushButton {
            background-color: #883bcb;
            color: white;
            border-radius: 7px;
            text-align: center;
            border: 2px solid transparent;
            font-size: 30px;
            }
            QPushButton:hover {
                background-color: white;
                color: #883bcb;
                border: 2px solid #883bcb;
            }
        """)
        self.enterEmail_lineEdit = None
        self.info_label = None
        self.add_widgets_email()
        
        self.enterOTP_lineEdit = None
        self.OTPinfo_label = None
        
        
    def paintEvent(self, event):
        from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Draw rounded rectangle
        brush = QBrush(QColor(211, 211, 211, 150))  # Background color
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)  # 20px rounded corners
    
    def add_widgets_email(self):
        self.enterEmail_lineEdit = QLineEdit(self)
        self.enterEmail_lineEdit.setGeometry(300,300,500,60)
        self.enterEmail_lineEdit.setPlaceholderText("Enter your email")
        self.enterEmail_lineEdit.setStyleSheet("background-color: lightgray; border: 1px solid black; border-radius: 5px; padding-left: 20px")
        self.enterEmail_lineEdit.setFont(QFont("Bell MT",13))
        
        self.info_label = QLabel("You will recieve a verification code on this email",self)
        self.info_label.setGeometry(300,380,500,40)
        self.info_label.setFont(QFont("Bell MT",14))
        self.setStyleSheet("font-size: 25px;")
        self.info_label.setAlignment(Qt.AlignCenter)
    
    def close_verify_window(self):
        self.parent.setGraphicsEffect(None)
        self.close()
    
    def backto_email(self):
        self.continue_btn.setEnabled(True)
        # Hide and Remove OTP widgets
        self.enterOTP_lineEdit.hide()
        self.OTPinfo_label.hide()
        self.enterOTP_lineEdit.deleteLater()
        self.OTPinfo_label.deleteLater()
        
        # Show Email widgets
        self.enterEmail_lineEdit.show()
        self.info_label.show()
        
        # Change 'Continue' button action to adding OTP widgets
        self.continue_btn.disconnect()
        self.continue_btn.clicked.connect(self.add_widgets_OTP)
        # Change Back button action to close the widget
        self.back_btn.disconnect()
        self.back_btn.clicked.connect(self.close_verify_window)
        
    def add_widgets_OTP(self):
        self.enterEmail_lineEdit.hide()
        self.info_label.hide()
        
        self.continue_btn.disconnect()
        self.continue_btn.clicked.connect(self.confirm_OTP)
        self.back_btn.disconnect()
        self.back_btn.clicked.connect(self.backto_email)
        
        # Add OTP widgets
        self.enterOTP_lineEdit = QLineEdit(self)
        self.enterOTP_lineEdit.setGeometry(450,300,200,60)
        self.enterOTP_lineEdit.setPlaceholderText("Enter OTP")
        self.enterOTP_lineEdit.setStyleSheet("background-color: lightgray; border: 1px solid black; border-radius: 5px; font-size: 30px;")
        self.enterOTP_lineEdit.setFont(QFont("Bell MT",13))
        self.enterOTP_lineEdit.setAlignment(Qt.AlignCenter)
        self.enterOTP_lineEdit.show()
        
        self.OTPinfo_label = QLabel("Enter the OTP sent to your given email",self)
        self.OTPinfo_label.setGeometry(300,250,500,40)
        self.OTPinfo_label.setFont(QFont("Bell MT",14))
        self.OTPinfo_label.setStyleSheet("font-size: 25px;")
        self.OTPinfo_label.setAlignment(Qt.AlignCenter)
        self.OTPinfo_label.show()
        
        import threading
        reciever = self.enterEmail_lineEdit.text()
        threading.Thread(target=self.create_and_send_otp, args=(reciever, self.store_otp), daemon=True).start()
    
    def check_email_existence(self):
        from Software.src.utils.loading import Loader
        self.loader = Loader(self)
        
        self.email = self.enterEmail_lineEdit.text()
        self.thread_emailCheck = QThread()
        self.worker_emailCheck = CheckEmailExistence_Worker(self.email)
        self.worker_emailCheck.moveToThread(self.thread_emailCheck)
        
        self.thread_emailCheck.started.connect(self.worker_emailCheck.run)
        self.worker_emailCheck.email_exists_status.connect(self.handle_email_existence_check)
        self.worker_emailCheck.finished.connect(self.thread_emailCheck.quit)
        self.worker_emailCheck.finished.connect(self.worker_emailCheck.deleteLater)
        self.thread_emailCheck.finished.connect(self.worker_emailCheck.deleteLater)
        
        self.thread_emailCheck.start()
        self.continue_btn.setEnabled(False)
        
    
    def handle_email_existence_check(self, status):
        if status == 1:
            self.loader.CloseLoading()
            self.add_widgets_OTP()
            self.continue_btn.setEnabled(True)
        elif status == 0:
            self.loader.CloseLoading()
            from PyQt5.QtWidgets import QMessageBox
            messagebox(self,QMessageBox.Warning,"Unauthorized User","You are not an existing user !!.\nTo continue enter the email you have logged in with.")
            self.continue_btn.setEnabled(True)
        else:
            self.loader.CloseLoading()
            from PyQt5.QtWidgets import QMessageBox
            messagebox(self,QMessageBox.Warning,"Connection Error","Make sure you are online to proceed for password reset !!")
            self.continue_btn.setEnabled(True)
    
    def store_otp(self, otp):
            self.otp_to_check = otp
        
    def create_and_send_otp(self, reciever, callback):
        self.continue_btn.clicked.disconnect()
        self.continue_btn.clicked.connect(self.confirm_OTP)
        try:
            import random
            import smtplib
            self.otp = ""
            for i in range(7):
                random_no = random.randint(0,9)
                self.otp+=str(random_no)
            
            sender = "satyakid78@gmail.com"
            reciever = reciever
            
            subject = "Your OTP to reset password"
            body = f"Your OTP for password reset is {self.otp}. Please do not share this with anyone.  ~Sukriya HRMS\n\nIt isn't you trying to reset your password ?\n- Please report to HR for unauthorized account activity."
            
            text = f"Subject: {subject}\n\n{body}"
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender, "ppwt xlxj yhkl sacg")
            server.sendmail(sender, reciever, text)
            # Call the callback function with OTP
            callback(self.otp)
            
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            messagebox(self, QMessageBox.Warning, "Failure", f"Error sending mail !!\n\n{e}")
            
        
    def confirm_OTP(self):
        self.continue_btn.setEnabled(False)
        from PyQt5.QtWidgets import QMessageBox
        if self.enterOTP_lineEdit.text() == self.otp_to_check:
            messagebox(self,QMessageBox.Information,"Success","OTP confirmed !!")
            self.parent.setGraphicsEffect(None)
            self.close()
            self.pswd_reset_window = ResetPasswordWindow(self.parent,self.enterEmail_lineEdit.text())
            self.pswd_reset_window.show()
            self.pswd_reset_window.raise_()
        else:
            messagebox(self,QMessageBox.Warning,"Failure","OTP does not match !!\n\nTry again by getting a new otp.")
            self.continue_btn.setEnabled(True)
    
class CheckEmailExistence_Worker(QObject):
    email_exists_status = pyqtSignal(int)
    finished = pyqtSignal()
    def __init__(self, email):
        super().__init__()
        self.email = email
    
    def run(self):
        try:
            con = dbConnection()
            if con.is_connected():
                cursor = con.cursor()
                cursor.execute("SELECT email FROM employee_accinfo where email = %s;",(self.email,))
                result = cursor.fetchall()
                if result:
                    self.email_exists_status.emit(1)
                else:
                    self.email_exists_status.emit(0)
        except Exception as e:
            self.email_exists_status.emit(2)
            #print(f"Error: {e}")
        finally:
            if 'con' in locals() and con.is_connected():
                con.close()
            self.finished.emit()


class ResetPasswordWindow(QWidget):
    layout = None
    def __init__(self, main_window, email):
        super().__init__(main_window)
        
        self.email = email
        self.main_window = main_window
        self.main_window.setWindowTitle("Reset Password")
        
        # Hide the Login Window child widgets to make it seem like the Login Window has gone
        for child in self.main_window.main_frame.findChildren(QWidget):
            child.hide()
        
        self.add_widgets()
        
    def add_widgets(self):
        
        self.main_window.logo_label.setGeometry(173,120,150,150)
        self.main_window.logo_label.setStyleSheet("border-radius: 10px")
        
        self.resetPswd_label = QLabel("Reset your password",self.main_window.main_frame)
        self.resetPswd_label.setGeometry(142,200,520,70)
        self.resetPswd_label.setFont(QFont("Calibri",12))
        self.resetPswd_label.setStyleSheet("background-color: transparent; color: #883bcb; font-size: 55px;")
        self.resetPswd_label.setAlignment(Qt.AlignCenter)
        self.resetPswd_label.show()
        
        self.pswdInfo_label = QLabel(self.main_window.main_frame)
        self.pswdInfo_label.setGeometry(167,280,500,100)
        self.pswdInfo_label.setStyleSheet("background-color: transparent; font-size: 20px;")
        self.pswdInfo_label.setFont(QFont("Calibri",13))
        self.pswdInfo_label.setWordWrap(True)
        self.pswdInfo_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.pswdInfo_label.setContentsMargins(5,5,5,5)
        self.pswdInfo_label.setText("Your password must be within 12-30 characters and must include atleast one uppercase and lowercase alphabet, number and a special character(!@#$%&)")
        self.pswdInfo_label.show()
        
        self.pswdStrength_label = QLabel("",self.main_window.main_frame)
        self.pswdStrength_label.setGeometry(152,440,500,40)
        self.pswdStrength_label.setContentsMargins(0,0,0,0)
        self.pswdStrength_label.setFont(QFont("Consolas",10))
        self.pswdStrength_label.setStyleSheet("background-color: transparent;")
        self.pswdStrength_label.show()
        
        self.pswdMatch_label = QLabel(self.main_window.main_frame)
        self.pswdMatch_label.setGeometry(152,550,500,40)
        self.pswdMatch_label.setContentsMargins(0,0,0,0)
        self.pswdMatch_label.setFont(QFont("Consolas",10))
        self.pswdMatch_label.setStyleSheet("background-color: transparent;")
        self.pswdMatch_label.show()
        
        self.newPswdEnter_lineEdit = QLineEdit(self.main_window.main_frame)
        self.newPswdEnter_lineEdit.setEchoMode(QLineEdit.Password)
        self.newPswdEnter_lineEdit.textEdited.connect(self.check_passsword_strength)
        self.newPswdEnter_lineEdit.setGeometry(152,390,500,50)
        self.newPswdEnter_lineEdit.setPlaceholderText("Enter new password")
        self.newPswdEnter_lineEdit.setFont(QFont("Bell MT",14))
        self.newPswdEnter_lineEdit.setStyleSheet("background-color: lightgray; border-radius: 5px; padding-left: 20px")
        self.newPswdEnter_lineEdit.show()
        
        self.confirmPswdEnter_lineEdit = QLineEdit(self.main_window.main_frame)
        self.confirmPswdEnter_lineEdit.setEchoMode(QLineEdit.Password)
        self.confirmPswdEnter_lineEdit.setGeometry(152,500,500,50)
        self.confirmPswdEnter_lineEdit.setPlaceholderText("Enter new password")
        self.confirmPswdEnter_lineEdit.setFont(QFont("Bell MT",14))
        self.confirmPswdEnter_lineEdit.setStyleSheet("background-color: lightgray; border-radius: 5px; padding-left: 20px")
        self.confirmPswdEnter_lineEdit.show()
        self.confirmPswdEnter_lineEdit.textEdited.connect(self.on_pswd_ReEnter)
        
        self.continue_btn = QPushButton(self.main_window.main_frame)
        self.continue_btn.clicked.connect(self.update_password)
        self.continue_btn.setCursor(Qt.PointingHandCursor)
        self.continue_btn.setText("Confirm")
        self.continue_btn.setGeometry(322,620,160,50)
        self.continue_btn.setFont(QFont("Arial Unicode MS",14))
        self.continue_btn.setStyleSheet("""
            QPushButton { background-color: #883bcb; color: white; border-radius: 5px; text-align: center; border: 2px solid transparent; }
            QPushButton:hover { background-color: white; color: #883bcb; border: 2px solid #883bcb; } """)
        self.continue_btn.show()
    
    def check_passsword_strength(self):
        #self.continue_btn.setEnabled(False)
        password = self.newPswdEnter_lineEdit.text()
        import re
        regexp = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{12,30}$"
        pattern = re.compile(regexp)
        match = re.search(pattern,password)
        if match:
            self.pswdStrength_label.setText("* ✓ Password is strong")
            self.pswdStrength_label.setStyleSheet("color: green;")
            return True
        else:
            self.pswdStrength_label.setText("* ✕ Password is weak")
            self.pswdStrength_label.setStyleSheet("color: red;")
            return False
            
        """ from PyQt5.QtWidgets import QMessageBox
        if match:
            # check if passwords match if the password is strong
            if self.confirmPswdEnter_lineEdit.text() == password:
                messagebox(self,QMessageBox.Information,"Success","Your password was changed successfully !!\nYou are set to login to continue to the software.")
                # show the login page
                for child in self.main_window.main_frame.findChildren(QWidget):
                    child.show()
                # hide the reset password page and delete it
                self.close()
                self.deleteLater()
            else:
                messagebox(self,QMessageBox.Warning,"Failure")
                self.continue_btn.setEnabled(True) """
            
    def on_pswd_ReEnter(self):
        if self.confirmPswdEnter_lineEdit.text() != self.newPswdEnter_lineEdit.text():
            self.pswdMatch_label.setText("* ✕ The passwords does not match !")
            self.pswdMatch_label.setStyleSheet("color: red")
            return False
        else:
            self.pswdMatch_label.setText("* ✓ The passwords match")
            self.pswdMatch_label.setStyleSheet("color: green")
            return True
            
    def update_password(self):
        self.continue_btn.setEnabled(False)
        
        #Checking if user entered strong password
        if self.check_passsword_strength() == False:
            from PyQt5.QtWidgets import QMessageBox
            messagebox(self,QMessageBox.Warning,"Weak Password","Cannot update password !!\n\nMake sure your password is strong !")
            self.continue_btn.setEnabled(True)
            return
        #Checking is re entered password matches original password
        if self.on_pswd_ReEnter() == False:
            from PyQt5.QtWidgets import QMessageBox
            messagebox(self,QMessageBox.Warning,"Unmatched Password","Cannot update password !!\n\nMake sure the re-entered password matches the original password !")
            self.continue_btn.setEnabled(True)
            return
        if True:
            from Software.src.utils.loading import Loader
            self.loader = Loader(self.main_window)
            
            password = self.confirmPswdEnter_lineEdit.text()
            self.thread_passwordReset = QThread()
            self.worker_passwordReset = ChangePassword_Worker(self.email,password)
            self.worker_passwordReset.moveToThread(self.thread_passwordReset)

            self.thread_passwordReset.started.connect(self.worker_passwordReset.run)
            self.worker_passwordReset.update_status.connect(self.handle_password_update)
            self.worker_passwordReset.finished.connect(self.thread_passwordReset.quit)
            self.worker_passwordReset.finished.connect(self.worker_passwordReset.deleteLater)
            self.thread_passwordReset.finished.connect(self.worker_passwordReset.deleteLater)
            
            self.thread_passwordReset.start()
    
    def handle_password_update(self, status):
        from PyQt5.QtWidgets import QMessageBox
        if status==1:
            self.loader.CloseLoading()
            messagebox(self,QMessageBox.Information,"Success","Your password was changed successfully !!\n\nYou are now set to login.")
            self.resetPswd_label.close()
            self.pswdInfo_label.close()
            self.pswdMatch_label.close()
            self.pswdStrength_label.close()
            self.newPswdEnter_lineEdit.close()
            self.confirmPswdEnter_lineEdit.close()
            self.continue_btn.close()
            # Delete the widgets to free the memory
            self.resetPswd_label.deleteLater()
            self.pswdInfo_label.deleteLater()
            self.pswdMatch_label.deleteLater()
            self.pswdStrength_label.deleteLater()
            self.newPswdEnter_lineEdit.deleteLater()
            self.confirmPswdEnter_lineEdit.deleteLater()
            self.continue_btn.deleteLater()
            for child in self.main_window.main_frame.findChildren(QWidget):
                child.show()
        elif status==0:
            self.loader.CloseLoading()
            messagebox(self,QMessageBox.Warning,"Failure","Your new password is already in use by other people.\n\nPlease give another unique password.")
            self.continue_btn.setEnabled(True)
        else:
            self.loader.CloseLoading()
            messagebox(self,QMessageBox.Critical,"Connection Error","Failed to connect online to update your password !!\n\nPlease check your connection and try again.")
            self.continue_btn.setEnabled(True)
            
        
class ChangePassword_Worker(QObject):
    update_status = pyqtSignal(int)
    finished = pyqtSignal()
    def __init__(self, email, password):
        super().__init__()
        self.email = email
        self.password = password
        
    def run(self):
        try:
            con = dbConnection()
            if con.is_connected():
                cursor = con.cursor()
                cursor.execute("SELECT password from employee_accinfo where password = %s;",(self.password,))
                result = cursor.fetchall()
                if result:
                    self.update_status.emit(0)
                else:
                    cursor.execute("UPDATE employee_accinfo SET password = %s where email = %s;",(self.password,self.email))
                    con.commit()
                    self.update_status.emit(1)
        except Exception as e:
            self.update_status.emit(2)
        finally:
            if 'con' in locals() and con.is_connected():
                con.close()
            self.finished.emit()
            
            
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

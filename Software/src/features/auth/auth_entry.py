from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy, QFrame
from PyQt5.QtCore import Qt, QTimer


class AuthEntry(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self._parent = parent
        
        self.setAutoFillBackground(True)
        #self.setStyleSheet("background-color: white;")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.createContainerFrame()
        self.initMainLayout()
        self.initContentLayout()
        self.createInfoLabel()
        self.createEntryButton()
        self.initUI()
        
    def createContainerFrame(self):
        self.mainFrame = QFrame(self)
        self.mainFrame.setFrameShape(QFrame.StyledPanel)
        self.mainFrame.setStyleSheet("""
        QFrame { 
            background-color: white;
            border: 4px solid #883bcb;
            border-radius: 30px;
        }""")
    
    def initMainLayout(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(400, 0, 400, 0)
        
    def initContentLayout(self):
        self.content_layout = QVBoxLayout(self.mainFrame)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        self.content_layout.setAlignment(Qt.AlignCenter)
        
    def createInfoLabel(self):
        self.infoLabel = QLabel(parent=self)
        self.infoLabel.setText("Please login to continue to the app")
        self.infoLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.infoLabel.setStyleSheet("""
            font-family: Cascadia Mono ExtraLight;
            font-size: 40px;
            color: #883bcb;
            text-align:center;
            border: none;""")
        
    def createEntryButton(self):
        self.entryButton = QPushButton(parent=self)
        self.entryButton.setText("Login")
        self.entryButton.setFixedSize(200, 70)
        self.entryButton.setStyleSheet("""
        QPushButton{
            color: white;
            background-color: #883bcb;
            font-family: Cascadia Mono;
            font-size: 30px;
            text-align: center;
            border-radius: 10px;
        }
        
        QPushButton:hover{
            color: #883bcb;
            background-color: white;
            border: 2px solid #883bcb;
        }""")
        self.entryButton.clicked.connect(self.openAuthWindow)
        
    def initUI(self):
        #Init Content Layout
        self.content_layout.addStretch(1)
        self.content_layout.addWidget(self.infoLabel, 2, alignment=Qt.AlignCenter)
        self.content_layout.addStretch(2)
        self.content_layout.addWidget(self.entryButton, 1, alignment=Qt.AlignCenter)
        self.content_layout.addStretch(1)
        #Init Main Layout
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.mainFrame)
        self.main_layout.addStretch()
        #Setting Layout for self
        self.setLayout(self.main_layout)
    
    def openAuthWindow(self):
        from .auth_window import LoginWindow
        self.login_window = LoginWindow(self)
        self.login_window.login_validity.connect(self.AuthAction)
        self.login_window.show()
        self.login_window.raise_()
        
    def AuthAction(self, login_status):
        if login_status == True:
            self.startCloseAnimation(self.login_window)
            self.startCloseAnimation(self)
        else:
            pass
    
    def startCloseAnimation(self, widget):
        from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
        # First, start a fade-out animation for the login window
        self.fade_out_animation = QPropertyAnimation(widget, b"windowOpacity")
        self.fade_out_animation.setDuration(200)  # time for the fade
        self.fade_out_animation.setStartValue(1.0)
        self.fade_out_animation.setEndValue(0.0)
        self.fade_out_animation.setEasingCurve(QEasingCurve.InOutQuad)
        # Connect the animation finished signal to proceed with enabling parent and opening dashboard
        self.fade_out_animation.finished.connect(self.finish_transition)
        # Start the animation
        self.fade_out_animation.start()
    
    def finish_transition(self):
        self._parent.Enabled(True)
        self.close()
        self.deleteLater()
        #Opening dashboard by default after closing login window
        QTimer.singleShot(10, lambda: self._parent.sidebar.onSideBarButtonClicked(0))

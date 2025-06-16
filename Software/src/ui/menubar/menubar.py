from PyQt5.QtWidgets import (
    QWidget, QFrame, QSizePolicy, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem)

def get_path(*args):
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_dir,*args)
    return icon_path
    
class MenuBar(QWidget):
    def __init__(self, workarea, parent=None):
        super().__init__(parent)
        self.workarea = workarea
        self.setOuterLayout()
        self.createMainFrame()
        self.setMainLayout()
        self.addMainFrameToOuterLayout()
        self.setMainFrameShadowStyle()
        self.MenuBarComponents()
        self.initUI()
        
        
    def setOuterLayout(self):
        # Main layout for MenuBar widget (wraps the styled frame)
        self.outer_layout = QVBoxLayout(self)
        self.outer_layout.setContentsMargins(0, 0, 0, 5)
        self.outer_layout.setSpacing(0)
        
    def createMainFrame(self):
        # Styled frame on top of this widget
        self.main_frame = QFrame(self)
        self.main_frame.setObjectName("menuFrame")
        self.main_frame.lower()
        self.main_frame.setMinimumHeight(40)
        self.main_frame.setStyleSheet("""
            QFrame#menuFrame {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 white,   /* hsl(217, 11%, 96%), */
                    stop:0.2 hsl(217, 11%, 96%),
                    stop:1 #ebeced    /* hsl(217, 8%, 88%) */
                );
            }
        """)
    
    def setMainLayout(self):
        # Set layout to main_frame, but don't add any widgets now
        self.main_layout = QHBoxLayout(self.main_frame)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
    def addMainFrameToOuterLayout(self):
        # Add the styled frame to the outer layout
        self.outer_layout.addWidget(self.main_frame)
    
    def setMainFrameShadowStyle(self):
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect
        from PyQt5.QtGui import QColor
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(5) #Low blur for soft edges
        shadow.setOffset(0, 3) #Slightly downward
        shadow.setColor(QColor(0, 0, 0, 100)) #Light grey with transparency
        self.main_frame.setGraphicsEffect(shadow)
    
    def MenuBarComponents(self):
        self.addCompanyLogo()
        self.addNotificationButton()
        self.addProfileButton()
        
    def initUI(self):
        self.main_layout.addWidget(self.companyLogo, 20)
        #spacer = QSpacerItem(int(self.width()*0.5), self.height(), QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.main_layout.addStretch(80)
        self.main_layout.addWidget(self.notiButton, 5)
        self.main_layout.addStretch(3)
        self.main_layout.addWidget(self.profileButton, 15)
        self.main_layout.addStretch(2)
        
    def addCompanyLogo(self):
        from Software.src.utils.path import get_path
        logopath = get_path("assets","menubar","icons","sukriya_logo.ico")
        from .companylogo import CompanyLogo
        self.companyLogo = CompanyLogo(logopath, "SUKRIYA", self)
    
    def addNotificationButton(self):
        from .notification import NotificationButton
        self.notiButton = NotificationButton(self)
    
    def addProfileButton(self):
        #Getting the button image path
        from Software.src.utils.path import get_path
        path = get_path("assets","menubar","icons","default_profile_colored.png")
        #Activating Profile Button
        from .profile import ProfileButton
        self.profileButton = ProfileButton(parent=self, profile_image_path=path)
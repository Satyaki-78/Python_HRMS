from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QLabel, QMenu, QPushButton, QVBoxLayout, QSizePolicy
)
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPainterPath, QColor, QPen
from PyQt5.QtCore import QSize, Qt

class ProfileButton(QWidget):
    def __init__(self, username="Username", profile_image_path=None, parent=None):
        super().__init__(parent)
        self._parent = parent
        self.username = username
        self.profile_image_path = profile_image_path
        self.profile_pixmap = None
        self.setUpUI()
        
    def setUpUI(self):
        """
        Initializes and sets up the user interface for the profile button widget.
        """
        self.setLayout(self.createLayout())
        self.applyShadowEffect()

    def createLayout(self):
        """
        Creates and returns the layout for the ProfileButton widget.
        """
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 30, 0)
        layout.setSpacing(10)
        
        # Add username label
        self.username_label = self.createUsernameLabel()
        layout.addWidget(self.username_label, 60)

        # Add user profile image label
        self.profile_image_label = self.createProfileImageLabel()
        self.setRoundedProfileImage(self.profile_image_path)
        layout.addWidget(self.profile_image_label, 30)

        # Add dropdown button
        self.dropdown_button = self.createDropdownButton()
        layout.addWidget(self.dropdown_button, 10)

        return layout

    def createUsernameLabel(self):
        """
        Creates the username label with the specified text.
        """
        username_label = QLabel(self)
        username_label.setText(self.username)
        username_label.setAlignment(Qt.AlignCenter)
        username_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        username_label.setStyleSheet("font-size: 24px; color: #525150; /* #61605f */")
        return username_label

    def createProfileImageLabel(self):
        """
        Creates the profile image label. The label will display the user's profile image.
        """
        profile_image_label = QLabel(self)
        profile_image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #profile_image_label.setStyleSheet("background-color: #cab8d9;")
        
        # Load and set the profile image
        if self.profile_image_path:
            self.profile_pixmap = QPixmap(self.profile_image_path)
        else:
            self.profile_pixmap = None
            profile_image_label.setText("No Photo")
        
        return profile_image_label

    def createDropdownButton(self):
        """
        Creates the dropdown button which will show a menu when clicked.
        """
        dropdown_button = QPushButton(self)  # Triangle symbol for the dropdown
        dropdown_button.setText("▼")
        dropdown_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        dropdown_button.setStyleSheet("border: none; background: transparent; font-size: 20px; color: #883bcb;")
        dropdown_button.clicked.connect(self.showDropdownMenu)
        return dropdown_button

    def showDropdownMenu(self):
        """
        Displays the dropdown menu when the dropdown button is clicked.
        """
        #self.dropdown_button.setText("▶")
        menu = QMenu(self)
        menu.setStyleSheet("""
        QMenu {
            font-size: 20px;        /* Increase text size */
            padding: 10px;          /* Overall padding */
            background-color: #f0f0f0;
            border: 2px solid #883bcb
        }
        QMenu::item {
            padding: 8px 20px;
        }
        QMenu::item:selected {
            background-color: #d6d6d6;
        }
        """)
        edit_profile_action = menu.addAction("Edit Profile")
        logout_action = menu.addAction("Log Out")

        # Connect actions to corresponding methods
        edit_profile_action.triggered.connect(self.editProfile)
        logout_action.triggered.connect(self.logOut)
        
        button_pos = self.dropdown_button.mapToGlobal(self.dropdown_button.rect().bottomLeft())
        menu.exec_(self.mapToGlobal(button_pos))
    
    def setRoundedProfileImage(self, image_path):
        size = self._parent.height()*2  # Width and height of the circular image
        pixmap = QPixmap(image_path).scaled(size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
    
        rounded = QPixmap(size, size)
        rounded.fill(Qt.transparent)

        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw circular background
        """ painter.setBrush(QColor("#cec1d9"))  # Your desired background color
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, size, size) """
        
        # Draw circular clip path
        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        
        pen = QPen(QColor("#883bcb"))
        pen.setWidth(2)
        # Draw circular border
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(pen)  # Change border color here
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(1, 1, size - 2, size - 2)  # Border stroke

        painter.end()

        self.profile_image_label.setPixmap(rounded)
        self.profile_image_label.setFixedSize(size, size)
        
    def shadowEffect(self):
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect
        from PyQt5.QtGui import QColor
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(7)
        shadow.setOffset(-4, 4)
        shadow.setColor(QColor(0, 0, 0, 100))
        return shadow
    
    def applyShadowEffect(self):
        return
        self.dropdown_button.setGraphicsEffect(self.shadowEffect())
        self.profile_image_label.setGraphicsEffect(self.shadowEffect())
        
    def resizeEvent(self, event):
        """
        Handles resizing of the widget and dynamically updates the profile image with circular masking.
        """
        pass

    def editProfile(self):
        """
        Handle 'Edit Profile' action.
        """
        print("Edit Profile clicked")

    def logOut(self):
        """
        Handle 'Log Out' action.
        """
        print("Log Out clicked")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Sample username and profile image path
        self.profile_button = ProfileButton("JohnDoe", "path_to_profile_image.jpg")

        layout = QVBoxLayout()
        layout.addWidget(self.profile_button)
        self.setLayout(layout)

        self.setWindowTitle("Profile Button Example")

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec_()

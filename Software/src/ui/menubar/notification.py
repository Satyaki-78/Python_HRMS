from PyQt5.QtWidgets import QPushButton, QSizePolicy
from PyQt5.QtGui import QIcon 
from PyQt5.QtCore import QSize

class NotificationButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._parent = parent
        self.setButtonIcon()
        self.applyShadowEffect()
    
    def setButtonIcon(self):
        from Software.src.utils.path import get_path
        path = get_path("assets","menubar","icons","notification_colored.png")
        self.setIcon(QIcon(path))
        size = int(self._parent.height()*1.5)
        self.setIconSize(QSize(size,size))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet("font-size: 14px; background-color: transparent;")
    
    def applyShadowEffect(self):
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect
        from PyQt5.QtGui import QColor
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(7)
        shadow.setOffset(-5, 4)
        shadow.setColor(QColor(0, 0, 0, 100))
        #self.setGraphicsEffect(shadow)
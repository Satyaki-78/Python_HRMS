from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QPalette, QColor

class Dashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        #self.setStyleSheet("background-color: white;")
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("white"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        
        from .dashboardpage import HRDashboard
        self.dashboard = HRDashboard()
        
        self._layout.addWidget(self.dashboard)
        
        self.setLayout(self._layout)
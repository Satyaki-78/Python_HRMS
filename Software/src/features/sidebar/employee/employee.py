from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class Employee(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        
        self.label = QLabel("Employees Page")
        self.label.setAlignment(Qt.AlignCenter)
        
        self._layout.addWidget(self.label)
        
        self.setLayout(self._layout)
        
        self.setStyleSheet("background-color: white; font-size: 70px; color: #883bcb;")
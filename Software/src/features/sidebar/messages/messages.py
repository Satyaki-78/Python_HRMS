from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class Messages(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        
        self.label = QLabel("Messages Page")
        self.label.setAlignment(Qt.AlignCenter)
        
        self._layout.addWidget(self.label, 1)
        
        self.setLayout(self._layout)
        
        self.setStyleSheet("background-color: white; font-size: 70px; color: #883bcb;")
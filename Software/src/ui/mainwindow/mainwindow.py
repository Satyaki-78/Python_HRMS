from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QWidget
from PyQt5.QtCore import Qt, QEvent
from Software.src.utils.center_window import center_window

from Software.config import appsettings
min_win_height = appsettings.MAIN_WINDOW_MINIMUM_HEIGHT
min_win_width = appsettings.MAIN_WINDOW_MINIMUM_WIDTH

class MainWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self.setGeometry(QDesktopWidget().availableGeometry())
        #self.center_window()
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowTitle("Sukriya HRMS")
        
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        
        self.setMinimumSize(1700,900)
    
    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() == Qt.WindowNoState:
                # Window is restored from maximized
                self.resize(1700,900)
                center_window(self)
        super().changeEvent(event)
        
    def closeEvent(self, event):
        self._parent.closeEvent(event)
        
        
        
        

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
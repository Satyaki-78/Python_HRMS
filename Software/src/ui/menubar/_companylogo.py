from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget, QSizePolicy
from PyQt5.QtGui import QPixmap, QRegion
from PyQt5.QtCore import Qt

def get_rounded_corner_pixmap(pixmap, radius):
    from PyQt5.QtGui import QPixmap, QPainter, QPainterPath
    from PyQt5.QtCore import Qt
    
    rounded = QPixmap(pixmap.size())
    rounded.fill(Qt.transparent)
    
    painter = QPainter(rounded)
    painter.setRenderHint(QPainter.Antialiasing)
    path = QPainterPath()
    path.addRoundedRect(0, 0, pixmap.width(), pixmap.height(), radius, radius)
    painter.setClipPath(path)
    painter.drawPixmap(0, 0, pixmap)
    painter.end()
    
    return rounded


class CompanyLogo(QWidget):
    def __init__(self, logo_path, company_name, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        self.logoPath = logo_path
        self.companyName = company_name
        
        self.initLayout()
        self.addLogo()
        self.addCompanyNameText()
        
        self.show()
    
    
    def initLayout(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
    
    def addLogo(self):
        self.logoLabel = QLabel(self)
        self.pixmap = QPixmap(self.logoPath)
        self.scaled_pixmap = self.pixmap.scaled(72, 72, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        self.rounded_pixmap = get_rounded_corner_pixmap(self.scaled_pixmap, radius=20)
        self.logoLabel.setPixmap(self.rounded_pixmap)
        self.logoLabel.setScaledContents(False)
        self.logoLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        #self.logoLabel.setMaximumSize(self.parent.size())
        self.layout.addWidget(self.logoLabel, 15)
    
    def addCompanyNameText(self):
        self.textLabel = QLabel(self)
        self.textLabel.setText(self.companyName)
        self.textLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.textLabel.setStyleSheet("""font-family: Consolas;
                                    font-weight: bold;
                                    font-size: 50px;
                                    color: #883bcb;
                                    letter-spacing: 1px;
                                    padding-left: 5px;""")
        #self.textLabel.setMaximumSize(self.parent.size())
        #from Software.src.util.dynamicfont import setDynamicFont
        #setDynamicFont(self.textLabel)
        
        self.layout.addWidget(self.textLabel, 85)
        


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_dir,"icons","sukriya_logo.ico")
    logo = CompanyLogo(icon_path, "SUKRIYA")
    sys.exit(app.exec_())
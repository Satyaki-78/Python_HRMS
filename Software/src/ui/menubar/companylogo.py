from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget, QSizePolicy
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath, QPen, QColor
from PyQt5.QtCore import Qt, QSize


def get_rounded_corner_pixmap(pixmap, radius):
    rounded = QPixmap(pixmap.size())
    rounded.fill(Qt.transparent)
    
    pen = QPen(QColor("black"))
    pen.setWidth(4)
    
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
        self._parent = parent
        self.logoPath = logo_path
        self.companyName = company_name

        self.initLayout()
        self.createLogoLabel()
        self.createTextLabel()
        self.applyShadowEffect()

    def initLayout(self):
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10, 0, 0, 0)
        self.setLayout(self.layout)

    def createLogoLabel(self):
        self.logoLabel = QLabel(self)
        self.logoLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.logoLabel.setScaledContents(False)
        self.layout.addWidget(self.logoLabel, 15)

        self.originalPixmap = QPixmap(self.logoPath)

    def createTextLabel(self):
        self.textLabel = QLabel(self.companyName, self)
        self.textLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.textLabel.setStyleSheet("""
            font-family: Consolas;
            font-weight: bold;
            font-size: 36px;
            color: #883bcb;
            letter-spacing: 2px;
            padding-left: 5px;
        """)
        self.textLabel.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.layout.addWidget(self.textLabel, 85)

    def resizeEvent(self, event):
        # Get size of logoLabel to determine new pixmap size
        logo_size = self._parent.size()*0.7
        scaled = self.originalPixmap.scaled(
            logo_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        radius = min(scaled.width(), scaled.height()) // 5  # For circular or rounded
        rounded = get_rounded_corner_pixmap(scaled, radius)
        self.logoLabel.setPixmap(rounded)
        super().resizeEvent(event)
        
    def shadowEffect(self):
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect
        from PyQt5.QtGui import QColor
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(7)
        shadow.setOffset(-3.50, 0.1)
        shadow.setColor(QColor(0, 0, 0, 100))
        return shadow
    
    def applyShadowEffect(self):
        pass
        #self.logoLabel.setGraphicsEffect(self.shadowEffect())
        #self.textLabel.setGraphicsEffect(self.shadowEffect())
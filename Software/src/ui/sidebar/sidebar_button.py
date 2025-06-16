from PyQt5.QtWidgets import (
    QSizePolicy, QPushButton, QWidget, QLabel, QHBoxLayout, QVBoxLayout
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize, Qt

def get_button_icon(button_name, button_state):
    import os
    button_name = button_name.lower()
    file_name = button_name + "-logo-" + button_state + ".png"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_dir,"button-images",file_name)
    
    return image_path
    

class SideBarButton(QWidget):
    def __init__(self, parentClass, parent=None, button_name=None, button_target=None, button_target_args=None, text_ratio=0.5):
        super().__init__(parent=parent)
        self.parent = parentClass
        self.clickedState = False
        self.name = button_name
        self.button_activation_class = button_target
        self.buttonTargetArgs = button_target_args
        self.text_ratio = text_ratio
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.initLayout()
        self.initIconLabel()
        self.initButton()
        self.removeDefaultClickStyle()
        self.initUI()
        #self.setButtonParent()
        self.setButtonIcon()
        self.activateButton()
        #self.setButtonHoverStyle()
        self.setStyleUnclicked()
        
    def initLayout(self):
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
    
    def initIconLabel(self):
        self.icon_label = QLabel(self)
        self.icon_label.setObjectName("IconLabel")
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setScaledContents(False)
        self.icon_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.icon_label.installEventFilter(self)  # Install event filter
        
    def initButton(self):
        self.button = QPushButton(self)
        self.button.setObjectName("Button")
        self.setLayoutDirection(Qt.LeftToRight)
        self.button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # force full height
        self.button.setStyleSheet("text-align: left; border: none; background-color: transparent;")  # prevent white border
        self.button.installEventFilter(self)
        
    def initUI(self):
        self._layout.addWidget(self.icon_label, 1)
        self._layout.addWidget(self.button, 2)
        self.setLayout(self._layout)
        
    def removeDefaultClickStyle(self):
        from PyQt5.QtCore import Qt
        self.button.setAutoFillBackground(False)
        self.button.setAttribute(Qt.WA_TransparentForMouseEvents, False)  #Allow mouse events
        self.button.setAttribute(Qt.WA_NoSystemBackground)  #Disable system background
        #self.setAttribute(Qt.WA_TranslucentBackground)  #Enable translucent background
        self.button.setFlat(True)  #Disables native borders & background
        self.button.setFocusPolicy(Qt.NoFocus) #Removes focus rectangle on click
         
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateIconPixmap()
        self.setDynamicButtonText()
    
    def getPushButton(self):
        return self.button
    
    def setButtonIcon(self, button_state="unclicked"):
        #Getting the button image path
        from Software.src.utils.path import get_path
        filename = self.name.lower() + "-logo-" + button_state + ".png"
        path = get_path("assets","sidebar","sidebar-button-images",filename)
        #Setting Icon
        from PyQt5.QtGui import QPixmap
        self.current_pixmap = QPixmap(path)
        self.updateIconPixmap()
        self.setDynamicButtonText()
    
    def updateIconPixmap(self):
        icon_size = QSize(int(self.icon_label.width()*0.5),int(self.icon_label.height()*0.5))
        scaled_pixmap = self.current_pixmap.scaled(
            icon_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.icon_label.setPixmap(scaled_pixmap)
        
    def activateButton(self):
        #self.button.clicked.connect(self.ButtonClick)
        self.show()
    
    def ButtonClick(self):
        #self.switchClickedState()
        #self.setClickedStateButtonIcon()
        self.removeDefaultClickStyle()
        #self.setButtonStyleOnClick()
        if self.button_activation_class:
            self.initTarget = self.button_activation_class(self.buttonTargetArgs)
            self.parent.setSingleActiveFeature(self.name, self.initTarget)
    
    def setCheckable(self, isCheckable):
        self.button.setCheckable(isCheckable)
        
    def setChecked(self, isChecked):
        self.button.setChecked(isChecked)
    
    def applyHoverStyle(self):
        if self.clickedState:
            return #Not applying hover effect when in clicked state
        self.button.setStyleSheet("""
        QPushButton {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop: 0 rgba(255, 255, 255, 90),
                stop: 1 rgba(0, 0, 0, 0)
            );
            color: white;
            border: none;
            border-top-right-radius: 10px;
            border-bottom-right-radius: 10px;
            text-align: left;
        }
        """)
        self.icon_label.setStyleSheet("""
        QLabel {
            background: rgba(255, 255, 255, 90);
            border-top-left-radius: 10px;
            border-bottom-left-radius: 10px;
        }
        """)

    def removeHoverStyle(self):
        if self.clickedState:
            self.setStyleClicked()  # Restore clicked style
        else:
            self.setStyleUnclicked()  # Restore normal style


    def setStyleClicked(self):
        self.clickedState = True
        self.setButtonIcon(button_state="clicked")
        self.button.setStyleSheet("""
        QPushButton {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 hsl(273, 0%, 99%),
                stop:0.1 hsl(273, 0%, 99%),
                stop:1 hsl(217, 4%, 79%)
            );
            color: purple;
            border: none;
            border-top-right-radius: 10px;
            border-bottom-right-radius: 10px;
            text-align: left;
        }
        """)
        self.icon_label.setStyleSheet("""
            background: hsl(273, 0%, 99%);
            border-top-left-radius: 10px;
            border-bottom-left-radius: 10px;
        """)
        self.applyFloatEffectOnClick()
    
    def setStyleUnclicked(self):
        self.clickedState = False
        self.setButtonIcon(button_state="unclicked")
        self.button.setStyleSheet("""
        QPushButton {
            color: white;
            background-color: none;
            border: none;
            border-top-right-radius: 10px;
            border-bottom-right-radius: 10px;
            text-align: left;
        }
        """)
        self.icon_label.setStyleSheet("""
        QLabel {
            background-color: none;
            border-top-left-radius: 10px;
            border-bottom-left-radius: 10px;
        }
        """)
        self.setGraphicsEffect(None)  #Remove any shadow effect
        #self.icon_label.setGraphicsEffect(None)
        self.setButtonIcon(button_state="unclicked")
    
    def ShadowEffect(self):
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect
        from PyQt5.QtGui import QColor
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(7)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor(0, 0, 0, 100))
        return shadow
    
    def applyFloatEffectOnClick(self):
        self.setGraphicsEffect(self.ShadowEffect())
        #self.icon_label.setGraphicsEffect(self.ShadowEffect())
        
    def setDynamicButtonText(self):
        from Software.src.utils.dynamicfont import setDynamicText
        self.button.setText(self.name)
        self.button.setFont(QFont("Consolas", 12))
        #setDynamicText(self, "Consolas", self.name, self.text_ratio)
    
    def eventFilter(self, source, event):
        if source == self.icon_label or source == self.button:
            if event.type() == event.Enter:
                self.applyHoverStyle()
                return True
            elif event.type() == event.Leave:
                self.removeHoverStyle()
                return True
            elif event.type() == event.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    self.button.click()
                    return True
        return super().eventFilter(source, event)

    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.ButtonClick()  # call your existing method
        super().mousePressEvent(event)
        return
        # Prevent the default pressed state from being applied
        self.removeDefaultClickStyle()  # Ensures no native press style
        #self.setButtonStyleOnClick()    # Immediately apply the custom style
        super().mousePressEvent(event)  # Continue normal behavior
        
class Run:
    def __init__(self):
        print("Button Clicked")

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    button = SideBarButton(button_name="Settings")
    sys.exit(app.exec())
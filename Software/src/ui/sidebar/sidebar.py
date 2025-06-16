from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QSizePolicy, QVBoxLayout, QLabel 

class SideBar(QWidget):
    def __init__(self, workarea, parent=None):
        super().__init__(parent=parent)
        self.workarea = workarea
        
        self.push_to_custom_button = {}  # maps QPushButton to SideBarButton
        self.last_button = None
        self.buttons = []
        self.btnCount = 8
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        
        self.initButtonsDict()
        self.setOuterLayout()
        self.createMainFrame()
        self.setMainLayout()
        self.addMainFrameToOuterLayout()
        self.initButtonGroup()
        self.getButtons()
        self.addButtonsToButtonGroup()
        #self.addSideBarButtons()
        #self.addSidebarFeatureButtons()
        
    def initButtonsDict(self):
        self.buttonDict = {}
        
    def setOuterLayout(self):
        # Main layout for MenuBar widget (wraps the styled frame)
        self.outer_layout = QVBoxLayout(self)
        self.outer_layout.setContentsMargins(0, 0, 0, 0)
        self.outer_layout.setSpacing(0)
        
    def createMainFrame(self):
        # Styled frame on top of this widget
        self.main_frame = QFrame(self)
        self.main_frame.setObjectName("sideBarFrame")
        #self.main_frame.setStyleSheet("background-color: #441d65")
        self.main_frame.setStyleSheet("""
            background-color: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 #883bcb, /* #aa05fc */ /* #cf66ff */ /* #c14af7 */ /*  */
            stop:1 #441d65
        );""")
        self.main_frame.lower()
    
    def setMainLayout(self):
        # Set layout to main_frame, but don't add any widgets now
        self.main_layout = QVBoxLayout(self.main_frame)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(30)
        
    def addMainFrameToOuterLayout(self):
        # Add the styled frame to the outer layout
        self.outer_layout.addWidget(self.main_frame)
    
    def initButtonGroup(self):
        from PyQt5.QtWidgets import QButtonGroup
        # Create the QButtonGroup
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)  # Only one can be checked
    
    def getButtons(self):
        import os, json
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir,"buttons.json")
        #Open buttons.json file to get button names
        with open(file_path, "r") as f:
            data = json.load(f)
            button_list = data["buttons"]
        #Add the buttons to the self.buttons variable
        for button in button_list:
            self.buttons.append(button)
        
    def addButtonsToButtonGroup(self):
        self.finalizeLayout()
        for i, name in enumerate(self.buttons):
            self.addButton(name, i)
        self.finalizeLayout()
        #Setting the clicked.connect signals for all buttons
        # Connect signal
        self.button_group.buttonClicked[int].connect(self.onSideBarButtonClicked)
    
    def getButtonClass(self, name):
        import importlib
        import_path = f"Software.src.features.sidebar.{name.lower()}.{name.lower()}"
        module = importlib.import_module(import_path)
        btnClass = getattr(module, name)
        return btnClass
    
    def addButton(self, feature_name, btnId):
        from Software.src.ui.sidebar.sidebar_button import SideBarButton
        
        btnClass = self.getButtonClass(feature_name)
        #Getting the button stretch factor from button count
        button_stretch = self.getButtonStretch()
        #Creating the button and adding them to the main layout
        button = SideBarButton(self, self.main_frame, feature_name, btnClass, self, 0.5)
        #button.clicked.connect(lambda _, b=button: b.ButtonClick())
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        #Adding the button to the main layout
        self.main_layout.addWidget(button, button_stretch)
        push_btn = button.getPushButton()
        self.button_group.addButton(push_btn, btnId)
        self.push_to_custom_button[push_btn] = button  # map it!
    
    def onSideBarButtonClicked(self, id):
        button = self.button_group.button(id)
        pushButton = self.push_to_custom_button.get(button)
        if not pushButton:
            return  # or raise an error
        
        if self.last_button and self.last_button != pushButton:
            self.last_button.setStyleUnclicked()
            self.last_button.setChecked(False)

        pushButton.setStyleClicked()
        self.last_button = pushButton
        pushButton.ButtonClick()

    
    def finalizeLayout(self):
        #Call this after adding all buttons to add expanding spacer at the bottom
        from PyQt5.QtWidgets import QSpacerItem
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)
        
    def getButtonStretch(self):
        return int(100/(2*self.btnCount))
    
    def getSpacerItemStretch(self):
        return int((100/self.btnCount)*0.3)
    
    def setSingleActiveFeature(self, feature_name: str, widget: QWidget):
        #self.activeFeature.setStyleUnclicked()
        #self.activeFeature = widget
        self.workarea.setActiveFeature(feature_name, widget)
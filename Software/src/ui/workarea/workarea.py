from PyQt5.QtWidgets import QWidget, QStackedLayout, QSizePolicy

class WorkArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)        
        self._layout = QStackedLayout()
        self._features = {}  # Dictionary: feature_name -> widget
        self.setLayout(self._layout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setContentsMargins(0,0,0,0)
        #self.setDefaultWidget()

    def setActiveFeature(self, feature_name: str, widget: QWidget):
        """
        Set the active feature. If the widget for the feature_name is not already added,
        add it to the layout and dictionary. Then switch to it.
        """
        if feature_name not in self._features:
            self._features[feature_name] = widget
            widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self._layout.addWidget(widget)
        
        self._layout.setCurrentWidget(self._features[feature_name])
        
    def setDefaultWidget(self):
        default_widget = QWidget()
        default_widget.setStyleSheet("background-color: white;")
        default_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setActiveFeature("default_workarea", default_widget)

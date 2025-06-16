from PyQt5.QtWidgets import QWidget

class FeatureManager:
    def __init__(self, workarea : QWidget):
        self.workarea = workarea
        self.__features = {} #Dictionary: feature_name -> widget
        
    def setFeature(self, feature_name, widget):
        if feature_name not in self.__features:
            self.__features[feature_name] = widget
            self.addNewFeature(widget)
        
        self.workarea.setActiveFeature(feature_name, widget)
        
    def addNewFeature(self, widget: QWidget):
        self.workarea._layout.addWidget(widget)
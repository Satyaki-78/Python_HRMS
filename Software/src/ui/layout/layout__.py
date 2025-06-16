from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy, QLayout
)
from PyQt5.QtCore import Qt


class MainLayout(QVBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.parent = parent
        
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        # Ratios
        self._sidebarRatio = 0.1
        self._menuBarRatio = 0.1
        
        # Widgets
        self._menuBarWidget = QWidget()
        self._sidebarWidget = QWidget()
        self._workAreaWidget = QWidget()
        
        # Policies
        self._menuBarWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self._sidebarWidget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self._workAreaWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Horizontal layout for sidebar and work area
        self._contentWidget = QWidget()
        self._hboxLayout = QHBoxLayout(self._contentWidget)
        self._hboxLayout.setContentsMargins(0, 0, 0, 0)
        self._hboxLayout.setSpacing(0)
        
        self._hboxLayout.addWidget(self._sidebarWidget)
        self._hboxLayout.addWidget(self._workAreaWidget)
        
        # Add to self (which is a VBoxLayout)
        self.addWidget(self._menuBarWidget)
        self.addWidget(self._contentWidget)
        
        # Dynamic resizing will be handled by installEventFilter
        self._contentWidget.installEventFilter(self)
        
    def setMenuBar(self, widget: QWidget):
        """Replace the top menu bar widget (15% height)."""
        self._replaceWidget(self._menuBarWidget, widget, self)
        self._menuBarWidget = widget
        self._menuBarWidget.setParent(self.parent)
        self.itemAt(0).widget().setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self._adjustLayoutSizes()
        
    def setSidebar(self, widget: QWidget):
        """Replace the sidebar widget (15% width)."""
        self._replaceWidget(self._sidebarWidget, widget, in_layout=self._hboxLayout)
        self._sidebarWidget = widget
        self._sidebarWidget.setParent(self.parent)
        self._sidebarWidget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self._adjustLayoutSizes()
        
    def setWorkArea(self, widget: QWidget):
        """Replace the main work area widget."""
        self._replaceWidget(self._workAreaWidget, widget, in_layout=self._hboxLayout)
        self._workAreaWidget = widget
        self._workAreaWidget.setParent(self.parent)
        self._workAreaWidget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        
    def eventFilter(self, obj, event):
        if obj is self._contentWidget and event.type() == event.Resize:
            self._adjustLayoutSizes()
        return super().eventFilter(obj, event)

    def _adjustLayoutSizes(self):
        total_width = self._contentWidget.width()
        total_height = self.geometry().height()

        sidebar_width = int(total_width * self._sidebarRatio)
        menu_height = int(total_height * self._menuBarRatio)
        
        self._sidebarWidget.setFixedWidth(sidebar_width)
        self._menuBarWidget.setFixedHeight(menu_height)
        
    def _replaceWidget(self, old_widget: QWidget, new_widget: QWidget, in_layout: QLayout = None):
        if not in_layout:
            in_layout = self
        index = in_layout.indexOf(old_widget)
        if index != -1:
            in_layout.removeWidget(old_widget)
            old_widget.setParent(None)
            new_widget.setParent(self.parent)
            in_layout.insertWidget(index, new_widget)
            new_widget.show()


from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy, QLayout
)
from PyQt5.QtCore import Qt, QSize


class MainLayout(QLayout):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialize layout containers
        self._mainLayout = QVBoxLayout(self)
        self._mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainLayout.setSpacing(0)
        
        # Menu bar and content area
        self._menuBar = QWidget(self)
        self._menuBar.setStyleSheet("background-color: green")
        self._contentContainer = QWidget(self)
        
        # Layouts
        self._contentLayout = QHBoxLayout()
        self._contentLayout.setContentsMargins(0, 0, 0, 0)
        self._contentLayout.setSpacing(0)
        self._contentContainer.setLayout(self._contentLayout)

        self._mainLayout.addWidget(self._menuBar)
        self._mainLayout.addWidget(self._contentContainer)

        # Sidebar and work area
        self._sidebar = QWidget(self)
        self._sidebar.setStyleSheet("background-color: purple")
        self._workArea = QWidget(self)
        self._workArea.setStyleSheet("background-color: white")

        self._contentLayout.addWidget(self._sidebar)
        self._contentLayout.addWidget(self._workArea)

        # Ratios
        self._sidebarRatio = 0.15
        self._menuBarRatio = 0.15

        # Set expand policies
        self._sidebar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self._workArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def setMenuBar(self, widget: QWidget):
        """Set the widget to be used as the menu bar (top, 15% height)."""
        self._replaceWidget(self._menuBar, widget)
        self._menuBar = widget

    def setSidebar(self, widget: QWidget):
        """Set the sidebar widget (left, 15% width)."""
        self._replaceWidget(self._sidebar, widget)
        self._sidebar = widget

    def setWorkArea(self, widget: QWidget):
        """Set the main work area widget (right, 85% width)."""
        self._replaceWidget(self._workArea, widget)
        self._workArea = widget

    def resizeEvent(self, event):
        """Handle dynamic resizing based on parent size."""
        total_width = self.width()
        total_height = self.height()

        sidebar_width = int(total_width * self._sidebarRatio)
        menu_height = int(total_height * self._menuBarRatio)

        self._sidebar.setFixedWidth(sidebar_width)
        self._menuBar.setFixedHeight(menu_height)

        super().resizeEvent(event)

    def _replaceWidget(self, old_widget: QWidget, new_widget: QWidget):
        layout = old_widget.parentWidget().layout()
        index = layout.indexOf(old_widget)
        layout.removeWidget(old_widget)
        old_widget.setParent(None)
        layout.insertWidget(index, new_widget)

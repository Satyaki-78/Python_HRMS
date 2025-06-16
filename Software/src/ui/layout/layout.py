from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy


class MainLayout(QVBoxLayout):
    """
    A custom layout for main application window with three components:
    - Menu bar (10% height, top)
    - Sidebar (10% width, left)
    - Work area (remaining space)
    
    Structure:
    1. Top-level QVBoxLayout contains menu bar and a QHBoxLayout
    2. QHBoxLayout contains sidebar and work area
    """

    def __init__(self, parent=None):
        """
        Initialize the MainLayout with a simplified structure.
        
        Args:
            parent: Parent widget
        """
        super(MainLayout, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
        
        # Create the horizontal layout for sidebar and work area
        self._horizontal_layout = QHBoxLayout()
        self._horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self._horizontal_layout.setSpacing(0)
        
        # Add placeholder for the menu bar (15% height)
        # Will be replaced by actual widget via setMenuBar()
        self._menu_widget = QWidget()
        self._menu_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self._menu_widget.setMinimumHeight(10)  # Prevent collapse when empty
        
        # Add placeholder for sidebar (15% width)
        # Will be replaced by actual widget via setSidebar()
        self._sidebar_widget = QWidget()
        self._sidebar_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self._sidebar_widget.setMinimumWidth(10)  # Prevent collapse when empty
        
        # Add placeholder for work area
        # Will be replaced by actual widget via setWorkArea()
        self._work_widget = QWidget()
        self._work_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Build the layout structure
        self._horizontal_layout.addWidget(self._sidebar_widget, 10)  # 10% width
        self._horizontal_layout.addWidget(self._work_widget, 90)     # 90% width
        
        # Add widgets to the main vertical layout
        self.addWidget(self._menu_widget, 10)     # 10% height
        self.addLayout(self._horizontal_layout, 90)  # 90% height

    def setMenuBar(self, widget):
        """
        Set the widget for the menu bar area.
        
        Args:
            widget (QWidget): Widget to use as the menu bar
        """
        if not isinstance(widget, QWidget):
            raise TypeError("Menu bar must be a QWidget")
        
        widget.setContentsMargins(0, 0, 0, 0)
        
        # Replace the menu widget
        self.replaceWidget(self, self._menu_widget, widget)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self._menu_widget = widget
        
    def setSidebar(self, widget):
        """
        Set the widget for the sidebar area.
        
        Args:
            widget (QWidget): Widget to use as the sidebar
        """
        if not isinstance(widget, QWidget):
            raise TypeError("Sidebar must be a QWidget")
        
        widget.setContentsMargins(0, 0, 0, 0)
        
        # Replace the sidebar widget
        self.replaceWidget(self._horizontal_layout, self._sidebar_widget, widget)
        widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self._sidebar_widget = widget
        
    def setWorkArea(self, widget):
        """
        Set the widget for the work area.
        
        Args:
            widget (QWidget): Widget to use as the work area
        """
        if not isinstance(widget, QWidget):
            raise TypeError("Work area must be a QWidget")
        
        # Replace the work area widget
        self.replaceWidget(self._horizontal_layout, self._work_widget, widget)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._work_widget = widget
        
    def replaceWidget(self, layout, old_widget, new_widget):
        """
        Replace a widget in a layout with another widget.
    
        Args:
            layout (QLayout): The layout containing the widget to replace
            old_widget (QWidget): The widget to be replaced
            new_widget (QWidget): The widget to add in its place
        """
        # Find the widget's index and stretch
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item.widget() == old_widget:
                # Get stretch factor before removal
                stretch = layout.stretch(i)
            
                # Remove old widget and add new one
                layout.removeWidget(old_widget)
                old_widget.setParent(None)
                layout.insertWidget(i, new_widget, stretch)
                new_widget.show()
                break
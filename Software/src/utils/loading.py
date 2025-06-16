from PyQt5.QtWidgets import (
    QLabel, QWidget, QVBoxLayout, QGraphicsBlurEffect, QSizePolicy
)
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QPoint

class Loader(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setStyleSheet("background-color: none; border: none;")
        
        # Store parent for positioning calculations
        self.parent_widget = parent
        
        # Create the layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        
        # QLabel for the GIF
        self.gif_label = QLabel(self)
        self.gif_label.setAlignment(Qt.AlignCenter)
        self.gif_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        # Load and start the movie
        from Software.src.utils.path import get_path
        self.movie = QMovie(get_path("assets", "auth-window", "Icons", "loading_gif_500x500.gif"))
        self.gif_label.setMovie(self.movie)
        self.movie.start()
        
        # Add the label to layout
        layout.addWidget(self.gif_label)
        
        # Apply blur effect to parent
        if parent:
            blur_effect = QGraphicsBlurEffect()
            blur_effect.setBlurRadius(5)
            parent.setGraphicsEffect(blur_effect)
        
        # Size the loader appropriately
        self.adjustSize()
        self.updatePosition()
        
        self.show()
    
    def updatePosition(self):
        """Update position to remain centered on the parent widget"""
        if self.parent_widget:
            # Calculate center position
            parent_center = self.parent_widget.rect().center()
            global_center = self.parent_widget.mapToGlobal(parent_center)
            
            # Calculate top-left position from center
            pos = global_center - QPoint(self.width() // 2, self.height() // 2)
            self.move(pos)
    
    def showEvent(self, event):
        """Update position when shown"""
        super().showEvent(event)
        self.updatePosition()
    
    def resizeEvent(self, event):
        """Handle resize events"""
        super().resizeEvent(event)
        self.updatePosition()
    
    def CloseLoading(self):
        """Close and clean up the loader"""
        # Remove blur effect from parent
        if self.parent_widget:
            self.parent_widget.setGraphicsEffect(None)
        
        self.close()
        self.deleteLater()
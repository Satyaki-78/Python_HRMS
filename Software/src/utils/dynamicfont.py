from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtCore import Qt

def setDynamicText(widget, font_family, text, text_ratio):
    """
    Sets the optimal font size for the given text in the specified widget.
    
    Parameters:
    - widget: Any PyQt5 widget that can display text
    - font_family: String specifying the font family to use
    - text: The text to display in the widget
    
    The function calculates the maximum font size that will allow the text
    to fit within 90% of the widget's boundaries.
    """
    # Get widget dimensions
    widget_width = widget.width()
    widget_height = widget.height()
    
    # Calculate 90% of the widget dimensions to create a margin
    target_width = widget_width * text_ratio
    target_height = widget_height * text_ratio
    
    # Start with a minimum font size
    min_size = 1
    max_size = 100  # Initial upper bound
    optimal_size = min_size
    
    # Binary search to find the optimal font size
    while min_size <= max_size:
        mid_size = (min_size + max_size) // 2
        
        # Create font with the current test size
        font = QFont(font_family, mid_size)
        metrics = QFontMetrics(font)
        
        # Get text dimensions (using boundingRect for proper text measurement)
        text_rect = metrics.boundingRect(0, 0, widget_width, widget_height, 
                                         Qt.AlignLeft | Qt.TextWordWrap, text)
        text_width = text_rect.width()
        text_height = text_rect.height()
        
        # Check if text fits within 90% of widget dimensions
        if text_width <= target_width and text_height <= target_height:
            # Text fits, try a larger size
            optimal_size = mid_size
            min_size = mid_size + 1
        else:
            # Text too large, try a smaller size
            max_size = mid_size - 1
    
    # Apply the optimal font to the widget
    final_font = QFont(font_family, optimal_size)
    widget.setFont(final_font)
    widget.setText(text)
    
    #return optimal_size  # Return the calculated optimal size
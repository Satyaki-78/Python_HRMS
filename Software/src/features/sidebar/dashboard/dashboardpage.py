import sys
import typing
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QSizePolicy
)
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QBrush, QPainterPath
from PyQt5.QtCore import Qt, QRectF, QSize, QMargins
from PyQt5.QtChart import (
    QChart, QChartView, QBarSet, QBarSeries, QValueAxis, QBarCategoryAxis, QAbstractBarSeries
)
# Project Allocation
class IconButton(QWidget):
    def __init__(self, icon_text, parent=None):
        super().__init__(parent)
        self.icon_text = icon_text
        self.setFixedSize(24, 24)
        self.setStyleSheet("background-color: transparent;")
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw circle background
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(240, 240, 240))
        painter.drawEllipse(0, 0, 24, 24)
        
        # Draw icon text
        painter.setPen(QColor(100, 100, 100))
        painter.setFont(QFont("Arial", 12))
        painter.drawText(0, 0, 24, 24, Qt.AlignCenter, self.icon_text)

class DonutChart(QWidget):
    def __init__(self, title, value_text, segments, parent=None):
        super().__init__(parent)
        self.title = title
        self.value_text = value_text
        self.segments = segments  # List of (value, color) tuples
        self.setMinimumSize(200, 200)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        rect = self.rect()
        center_x = rect.width() / 2
        center_y = rect.height() / 2
        
        # Calculate total for percentages
        total = sum(segment[0] for segment in self.segments)
        
        # Draw donut chart
        outer_radius = min(center_x, center_y) - 20
        inner_radius = outer_radius * 0.6
        
        # Draw segments
        start_angle = 90 * 16  # Start from top (90 degrees, multiplied by 16 for QPainter angles)
        for value, color in self.segments:
            span_angle = -360 * 16 * value / total if total > 0 else 0
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(color))
            
            painter.drawPie(
                int(center_x - outer_radius),
                int(center_y - outer_radius),
                int(outer_radius * 2),
                int(outer_radius * 2),
                int(start_angle),
                int(span_angle)
            )
            start_angle += span_angle
        
        # Draw inner circle (creates donut hole)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("white"))
        painter.drawEllipse(
            int(center_x - inner_radius),
            int(center_y - inner_radius),
            int(inner_radius * 2),
            int(inner_radius * 2)
        )
        
        # Draw center text
        painter.setPen(QColor("#6a3093"))
        if self.value_text:  # For the Job Postings and Project Allocation charts
            font = QFont("Arial", 16, QFont.Bold)
            painter.setFont(font)
            painter.drawText(rect, Qt.AlignCenter, self.value_text)
        
        # Draw title
        font = QFont("Arial", 14)
        painter.setFont(font)
        painter.setPen(QColor("#6a3093"))
        
        if self.value_text:  # For charts with center text, title goes below
            text_rect = QRectF(rect.x(), rect.y() + center_y + 20, rect.width(), 30)
            painter.drawText(text_rect, Qt.AlignCenter, self.title)
        else:  # For charts without center text, title goes in center
            painter.drawText(rect, Qt.AlignCenter, self.title)
        
        # Draw legend for Project Allocation
        if "Project Allocation" in self.title:
            legend_x = rect.right() - 40
            legend_y = rect.top() + 40
            
            for i, (_, color) in enumerate(self.segments):
                # Draw legend color square
                painter.setPen(Qt.NoPen)
                painter.setBrush(QColor(color))
                painter.drawEllipse(legend_x, legend_y + i * 30, 15, 15)
                
                # Draw legend text
                painter.setPen(QColor("#6a3093"))
                font = QFont("Arial", 10)
                painter.setFont(font)
                painter.drawText(legend_x +6, legend_y + i * 30, 30, 20, Qt.AlignRight, f"P{i+1}")

class CardWidget(QFrame):
    def __init__(self, title, value, hover_text, icon=None, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            CardWidget {
                border: 1px solid #b8b8b8;
                border-radius: 20px;
                background-color: white;
            }
        """)
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QStackedWidget
        from PyQt5.QtGui import QColor
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(7)
        shadow.setOffset(5, 4)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(shadow)
        
        # Create a stacked widget to switch between normal and hover states
        self.stack = QStackedWidget(self)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stack)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Normal content widget
        self.normal_widget = QWidget()
        normal_layout = QVBoxLayout(self.normal_widget)
        
        # Title row with optional icon
        title_layout = QHBoxLayout()
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #6a3093; font-size: 20px; background-color: transparent;")
        title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        title_layout.addWidget(title_label, alignment=Qt.AlignCenter)
        
        if icon:
            icon_button = IconButton(icon)
            #title_layout.addWidget(icon_button)
            #title_layout.addStretch()
            
        normal_layout.addLayout(title_layout)
        
        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 36px; background-color: transparent")
        value_label.setAlignment(Qt.AlignCenter)
        normal_layout.addWidget(value_label)
        normal_layout.setContentsMargins(15, 15, 15, 15)
        
        # Hover content widget
        self.hover_widget = QWidget()
        hover_layout = QVBoxLayout(self.hover_widget)
        
        # Hover text label
        hover_message = QLabel(hover_text)
        hover_message.setStyleSheet("""
            color: white;
            font-family: Calibri;
            font-size: 25px;
            background-color: transparent;
        """)
        hover_message.setAlignment(Qt.AlignCenter)
        hover_message.setWordWrap(True)
        
        hover_layout.addWidget(hover_message)
        hover_layout.setContentsMargins(15, 15, 15, 15)
        
        # Apply gradient background to hover widget
        self.hover_widget.setStyleSheet("""
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #6a3093, stop:1 #9d61f6);
            border-radius: 20px;
        """)
        
        # Add both widgets to the stack
        self.stack.addWidget(self.normal_widget)
        self.stack.addWidget(self.hover_widget)
        self.stack.setCurrentIndex(0)  # Start with normal view
        
        # Enable mouse tracking for hover events
        self.setMouseTracking(True)
        
    def enterEvent(self, event):
        self.stack.setCurrentIndex(1)  # Show hover content
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self.stack.setCurrentIndex(0)  # Show normal content
        super().leaveEvent(event)

#92
class BarChartWidget(QFrame):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            BarChartWidget {
                border: 1px solid #b8b8b8;
                border-radius: 20px;
                background-color: white;
            }
        """)
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect
        from PyQt5.QtGui import QColor
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(7)
        shadow.setOffset(5, 4)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(shadow)
        
        # Data for different quarters
        self.q1q2_data = [50000, 60000, 85000, 55000, 75000, 90000]  # Q1+Q2 data
        self.q3q4_data = [65000, 80000, 70000, 90000, 95000, 75000]  # Q3+Q4 data
        self.current_data = self.q1q2_data  # Default to Q1+Q2
        self.months_q1q2 = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        self.months_q3q4 = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        self.current_months = self.months_q1q2
        
        layout = QVBoxLayout(self)
        
        # Header with title and buttons
        header_layout = QHBoxLayout()
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #6a3093; font-size: 20px;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Add quarter buttons
        self.q1q2_button = QPushButton("Q1+Q2")
        self.q1q2_button.setStyleSheet("""
            QPushButton {
                background-color: #6a3093;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: white;
                color: #6a3093;
                border: 1px solid #6a3093; 
            }
        """)
        self.q3q4_button = QPushButton("Q3+Q4")
        self.q3q4_button.setStyleSheet("""
            QPushButton {
                background-color: #6a3093;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: white;
                color: #6a3093;
                border: 1px solid #6a3093;
            }
        """)
        
        # Connect button signals
        self.q1q2_button.clicked.connect(self.show_q1q2_data)
        self.q3q4_button.clicked.connect(self.show_q3q4_data)
        
        header_layout.addWidget(self.q1q2_button)
        header_layout.addWidget(self.q3q4_button)
        layout.addLayout(header_layout)
        
        # Create chart
        self.chart = QChart()
        self.chart.setBackgroundVisible(False)
        self.chart.setMargins(QMargins(0, 0, 0, 0))
        self.chart.legend().hide()
        
        # Create bar series
        self.create_chart_series()
        
        # Set up chart view
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        
        layout.addWidget(self.chart_view)
        layout.setContentsMargins(15, 15, 15, 15)
    
    def create_chart_series(self):
        # Clear any existing series
        self.chart.removeAllSeries()
        self.chart.removeAxis(self.chart.axes(Qt.Horizontal)[0]) if self.chart.axes(Qt.Horizontal) else None
        self.chart.removeAxis(self.chart.axes(Qt.Vertical)[0]) if self.chart.axes(Qt.Vertical) else None
        
        # Create bar series with current data
        bar_set = QBarSet("")
        bar_set.append(self.current_data)
        bar_set.setColor(QColor("#6a3093"))
        
        series = QBarSeries()
        # Make bars thinner by setting bar width
        series.setBarWidth(0.2)  # Set width to 50% of default (values between 0 and 1)
        series.append(bar_set)
        self.chart.addSeries(series)
        
        # Set up axes
        axis_x = QBarCategoryAxis()
        axis_x.append(self.current_months)
        self.chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)
        
        # Find the maximum value for the y-axis scale
        max_value = max(self.current_data)
        y_max = ((max_value // 10000) + 1) * 10000  # Round up to next 10,000
        
        axis_y = QValueAxis()
        axis_y.setRange(0, y_max)
        axis_y.setVisible(False)  # Hide Y axis as in the image
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)
        
        # Apply rounded corners to bars
        self.chart.setDropShadowEnabled(True)
        # Set the roundness of the bars
        series.setLabelsPosition(QAbstractBarSeries.LabelsOutsideEnd)
        
        # Apply additional styling for rounded bars
        pen = QPen(QColor("#6a3093"))
        pen.setWidth(0)  # No border
        bar_set.setPen(pen)
    
    def show_q1q2_data(self):
        self.current_data = self.q1q2_data
        self.current_months = self.months_q1q2
        self.create_chart_series()
        self.chart_view.update()
    
    def show_q3q4_data(self):
        self.current_data = self.q3q4_data
        self.current_months = self.months_q3q4
        self.create_chart_series()
        self.chart_view.update()

class HRDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("HR Dashboard")
        self.setStyleSheet("background-color: transparent;")
        self.resize(1000, 650)
        
        # Main layout directly on this widget
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Hello User!")
        title.setStyleSheet("color: #6a3093; font-size: 50px; font-family: Calibri;")
        subtitle = QLabel("Good Morning ☀️")
        subtitle.setStyleSheet("color: #333; font-size: 24px;")
        
        header_title_layout = QVBoxLayout()
        header_title_layout.setContentsMargins(0,0,0,0)
        header_title_layout.addWidget(title)
        header_title_layout.addWidget(subtitle)
        
        header_layout.addLayout(header_title_layout)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)
        
        # First row - Cards and Job Postings
        row1_layout = QHBoxLayout()
        
        # Left side - 2x2 grid of cards
        cards_grid = QVBoxLayout()
        cards_grid.setContentsMargins(0,0,0,0)
        
        # First row of cards
        cards_row1 = QHBoxLayout()
        emp_hover_text = "10 - Software Dep \n20 - Marketing Dep \n5 - Board Members \n5 - Data Analytics \n6 - Sales Dep"
        employees_card = CardWidget("Total Employees", "50",emp_hover_text)
        
        proj_hover_text = "1..Website Redesign \n2.App Development \n3.User Facing Product"
        projects_card = CardWidget("Active Projects", "3", proj_hover_text)
        
        cards_row1.addWidget(employees_card, 4)
        cards_row1.addStretch(1)
        cards_row1.addWidget(projects_card, 4)
        cards_row1.addStretch(1)
        cards_grid.addLayout(cards_row1, 1)
        
        # Second row of cards
        cards_row2 = QHBoxLayout()
        
        att_hover_text = "46/50 \n\n Employees Present"
        attendance_card = CardWidget("Attendance Today", "92 %", att_hover_text)
        
        msg_hover_text = "Message From user A \nMessage From user C \nPost by HR \nPost by Sales Head"
        messages_card = CardWidget("Pending Message", "4", msg_hover_text)
        
        cards_row2.addWidget(attendance_card, 4)
        cards_row2.addStretch(1)
        cards_row2.addWidget(messages_card, 4)
        cards_row2.addStretch(1)
        cards_grid.addLayout(cards_row2, 1)
        
        # Add the cards grid to the main row layout
        row1_layout.addLayout(cards_grid, 2)
        
        # Job Postings Donut Chart
        jobs_frame = QFrame()
        jobs_frame.setFrameShape(QFrame.StyledPanel)
        jobs_frame.setStyleSheet("""
            QFrame {
                border: 1px solid #b8b8b8;
                border-radius: 20px;
                background-color: white;
            }
        """)
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect
        from PyQt5.QtGui import QColor
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(7)
        shadow.setOffset(5, 4)
        shadow.setColor(QColor(0, 0, 0, 100))
        jobs_frame.setGraphicsEffect(shadow)
        
        jobs_layout = QVBoxLayout(jobs_frame)
        jobs_title = QLabel("Job Postings")
        jobs_title.setStyleSheet("color: #6a3093; font-size: 20px; background-color: transparent; border: none;")
        jobs_layout.addWidget(jobs_title, alignment=Qt.AlignCenter)
        
        # Using segments [(value, color), ...] for open and filled positions
        job_chart = DonutChart("", "1/4", [(3, "#361e67"), (1, "#9d61f6")])
        jobs_layout.addWidget(job_chart)
        
        # Legend for job postings
        legend_layout = QHBoxLayout()
        legend_layout.setAlignment(Qt.AlignCenter)
        
        # Open legend
        open_color = QFrame()
        open_color.setFixedSize(10, 10)
        open_color.setStyleSheet("background-color: #361e67; border-radius: 5px;")
        open_text = QLabel("Open")
        open_text.setStyleSheet("color: #361e67; border: none;")
        
        # Filled legend
        filled_color = QFrame()
        filled_color.setFixedSize(10, 10)
        filled_color.setStyleSheet("background-color: #9d61f6; border-radius: 5px;")
        filled_text = QLabel("Filled")
        filled_text.setStyleSheet("color: #9d61f6; border: none;")
        
        legend_layout.addWidget(open_color)
        legend_layout.addWidget(open_text)
        legend_layout.addSpacing(20)
        legend_layout.addWidget(filled_color)
        legend_layout.addWidget(filled_text)
        
        jobs_layout.addLayout(legend_layout)
        row1_layout.addWidget(jobs_frame, 1)
        
        main_layout.addLayout(row1_layout, 4)
        
        # Second row - charts
        row2_layout = QHBoxLayout()
        
        # Payroll Bar Chart
        payroll_chart = BarChartWidget("Payroll By Month") 
        row2_layout.addWidget(payroll_chart, 1)
        
        # Project Allocation Donut
        project_frame = QFrame()
        #project_frame.setFrameShape(QFrame.StyledPanel)
        project_frame.setStyleSheet("""
            QFrame {
                border: 1px solid #b8b8b8;
                border-radius: 20px;
                background-color: white;
            }
        """)
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect
        from PyQt5.QtGui import QColor
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(7)
        shadow.setOffset(5, 4)
        shadow.setColor(QColor(0, 0, 0, 100))
        project_frame.setGraphicsEffect(shadow)
        
        project_layout = QVBoxLayout(project_frame)
        # Using segments [(value, color), ...] for projects
        project_chart = DonutChart("Project Allocation", "", [
            (40, "#9d61f6"),  # P1
            (30, "#361e67"),  # P2
            (30, "#d8c6ff")   # P3
        ])
        project_layout.addWidget(project_chart)
        row2_layout.addWidget(project_frame, 1)
        
        main_layout.addLayout(row2_layout, 4)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dashboard = HRDashboard()
        self.setCentralWidget(self.dashboard)
        self.setWindowTitle("HR Dashboard")
        self.resize(1000, 650)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
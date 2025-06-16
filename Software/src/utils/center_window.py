def center_window(window):
        from PyQt5.QtWidgets import QDesktopWidget
        screen_geometry = QDesktopWidget().availableGeometry()
        center_x = (screen_geometry.width()-window.width()) // 2
        center_y = (screen_geometry.height()-window.height()) // 2
        window.move(center_x,center_y)
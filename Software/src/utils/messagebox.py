def messagebox(parent,icon: str, title: str, text: str):
    import os
    from PyQt5.QtWidgets import QMessageBox, QGraphicsBlurEffect
    from PyQt5.QtGui import QIcon
    from .path import get_path
    # Mapping string to QMessageBox icon enum
    icon_map = {
        "information": QMessageBox.Information,
        "warning": QMessageBox.Warning,
        "critical": QMessageBox.Critical,
        "question": QMessageBox.Question,
        "noicon": QMessageBox.NoIcon
    }
    msg_box = QMessageBox()
    msg_box.setModal(True)
    msg_box.setIcon(icon_map.get(icon.lower(), QMessageBox.NoIcon))
    msg_box.setWindowIcon(QIcon(get_path("assets","menubar","icons","sukriya_logo.ico")))
    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.setStandardButtons(QMessageBox.Ok)
    
    blur_effect = QGraphicsBlurEffect()
    blur_effect.setBlurRadius(10)
    parent.setGraphicsEffect(blur_effect)
    
    msg_box.exec_()
    parent.setGraphicsEffect(None)
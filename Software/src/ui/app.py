from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon
import sys
from Software.src.utils.path import get_path
import time

def dbConnection():
    import mysql.connector
    con = mysql.connector.connect(
        host="05ky6.h.filess.io",
        port=61002,
        username="SukriyaHRMS01_besidegone",
        password="#SukriyaDB@1001",
        database ="SukriyaHRMS01_besidegone")
    return con


class App:
    def __init__(self):
        
        self.app = QApplication(sys.argv)
        self.app.setWindowIcon(QIcon(get_path("assets","menubar", "icons", "sukriya_logo.ico")))
        
        self.appStartTime = 0
        self.appCloseTime = 0
        self.appRunTime = 0
        self.userSerialNo = None
        
        self.setAppWindow()
        self.setAppLayout()
        self.setAppWorkArea()
        self.setAppMenuBar()
        self.setAppSideBar()
        self.setFeatureManager()
        self.setAuthEntry()
        self.run()
        
        
    def setAppWindow(self):
        from Software.src.ui.mainwindow.mainwindow import MainWindow
        self.window = MainWindow(self)
        from Software.src.utils.darkmode import enable_dark_mode_for_windows
        enable_dark_mode_for_windows(self.window)
        
    def setAppLayout(self):
        #Setting the custom made Layout as the main layout for the app
        from Software.src.ui.layout.layout import MainLayout
        self.layout = MainLayout()
        self.window.centralwidget.setLayout(self.layout)

    def setAppMenuBar(self):
        #Setting the Menu Bar
        from Software.src.ui.menubar.menubar import MenuBar
        self.menuBar = MenuBar(parent=self.window, workarea=self.workArea)
        self.layout.setMenuBar(self.menuBar)

    def setAppSideBar(self):
        #Setting the Side Bar
        from Software.src.ui.sidebar.sidebar import SideBar
        self.sidebar = SideBar(parent=self.window, workarea=self.workArea)
        self.layout.setSidebar(self.sidebar)

    def setAppWorkArea(self):
        #Setting the white work area
        from Software.src.ui.workarea.workarea import WorkArea
        self.workArea = WorkArea(self.window)
        self.layout.setWorkArea(self.workArea)
    
    def setAuthEntry(self):
        from Software.src.features.auth.auth_entry import AuthEntry
        self.authEntry = AuthEntry(self)
        self.setCurrentFeature("__AuthEntry__", self.authEntry)
        self.Enabled(False)
    
    def Enabled(self, enabled:bool):
        self.sidebar.setEnabled(enabled)
        self.menuBar.setEnabled(enabled)
        self.disabledEffect(not enabled)
    
    def disabledEffect(self, disabled: bool):
        if disabled:
            self.sidebar.setGraphicsEffect(self.blurEffect())
            self.menuBar.setGraphicsEffect(self.blurEffect())
        else:
            self.sidebar.setGraphicsEffect(None)
            self.menuBar.setGraphicsEffect(None)
    
    def blurEffect(self):
        from PyQt5.QtWidgets import QGraphicsBlurEffect
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(2)
        return blur_effect
        
    def setFeatureManager(self):
        pass
    
    def setCurrentFeature(self, feature_name:str, widget:QWidget):
        self.workArea.setActiveFeature(feature_name, widget)
    
    def run(self):
        self.window.show()
        sys.exit(self.app.exec_())
    
    def closeEvent(self, event):
        import threading
    
        # Create and show the loader first
        #self.ShowLoader()
        
        # Calculate app runtime
        import time
        self.appCloseTime = time.time()
        self.appRunTime = self.appCloseTime - self.appStartTime
        self.appRunTime = self.appRunTime/60
        
        if self.userSerialNo:
            # Use thread to save data without freezing UI
            t = threading.Thread(target=self.sendAppActiveTimeData, daemon=True)
            t.start()
            t.join()  # Wait for thread to finish before exit
    
        event.accept()

    def sendAppActiveTimeData(self):
        try:
            con = dbConnection()
            if con.is_connected():
                cursor = con.cursor()
                cursor.execute("UPDATE user_activity SET active_duration = %s WHERE serial_no = %s;", (self.appRunTime, self.userSerialNo))
                con.commit()
        except Exception as e:
            print(f"App Run Time Data Send Error: {e}")
        finally:
            if 'con' in locals() and con.is_connected():
                con.close()
            
    def ShowLoader(self):
        from Software.src.utils.loading import Loader
        self.loader = Loader(self.window)
    

if __name__ == "__main__":
    app = App()
    print(get_path())
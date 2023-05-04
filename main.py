from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
import sys
from navigator import Navigator

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app_icon = QIcon("./assets/radar.ico")
    app.setWindowIcon(app_icon)
    navigator = Navigator()
    navigator.open_login_screen()
    sys.exit(app.exec_())
    


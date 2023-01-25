from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
import sys
from main_screen import MainScreen

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app_icon = QIcon("./assets/radar.ico")
    app.setWindowIcon(app_icon)
    screen = MainScreen()
    screen.show()
    sys.exit(app.exec_())
    


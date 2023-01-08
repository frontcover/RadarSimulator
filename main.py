from PyQt5.QtWidgets import QApplication
import sys
from main_screen import MainScreen

if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = MainScreen()
    screen.show()
    sys.exit(app.exec_())
    


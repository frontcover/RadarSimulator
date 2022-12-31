from PyQt5.QtWidgets import QApplication
import sys
from utils.navigator import Navigator

if __name__ == "__main__":
    app = QApplication(sys.argv)
    navigator = Navigator()
    navigator.open_main_screen()
    sys.exit(app.exec_())
    


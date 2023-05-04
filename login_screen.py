from PyQt5.QtWidgets import QMainWindow
from ui.python.login import Ui_LoginScreen

class LoginScreen(QMainWindow):
    def __init__(self, navigator):
        super().__init__()
        self.navigator = navigator
        self.uic = Ui_LoginScreen()
        self.uic.setupUi(self)

        self.uic.login_btn.clicked.connect(self.login)

    def login(self):
        self.navigator.open_main_screen()
        

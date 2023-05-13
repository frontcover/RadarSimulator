from PyQt5.QtWidgets import QMainWindow
from ui.python.login import Ui_LoginScreen
import win32com.client

class LoginScreen(QMainWindow):
    def __init__(self, navigator):
        super().__init__()
        self.navigator = navigator
        self.uic = Ui_LoginScreen()
        self.uic.setupUi(self)

        self.uic.login_btn.clicked.connect(self.login)
        self.uic.openslide_btn.clicked.connect(self.open_powerpoint)

    def login(self):
        self.navigator.open_main_screen()
        
    def open_powerpoint(self):
        # Open PowerPoint
        powerpoint = win32com.client.Dispatch("PowerPoint.Application")

        # Open the PowerPoint file
        ppt = powerpoint.Presentations.Open(r"C:\Users\dranh\Desktop\Test.pptx")

        # Open presentation mode
        # ppt.SlideShowSettings.Start()

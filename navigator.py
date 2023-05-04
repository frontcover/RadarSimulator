from main_screen import MainScreen
from login_screen import LoginScreen

class Navigator:
    '''
    Navigate between screens
    '''
    def __init__(self) -> None:
        self.main_screen = MainScreen(self)
        self.login_screen = LoginScreen(self)

    def open_main_screen(self):
        self.main_screen.show()
        self.login_screen.hide()
    
    def open_login_screen(self):
        self.login_screen.show()
        self.main_screen.hide()

    
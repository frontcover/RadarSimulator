from main_screen import MainScreen
from login_screen import LoginScreen
from plot_screen import PlotScreen

class Navigator:
    '''
    Navigate between screens
    '''
    def __init__(self) -> None:
        self.main_screen = MainScreen(self)
        self.login_screen = LoginScreen(self)
        self.plot_screen = PlotScreen(self)

    def open_main_screen(self):
        self.main_screen.show()
        self.login_screen.hide()
    
    def open_login_screen(self):
        self.login_screen.show()
        self.main_screen.hide()

    def open_plot_screen(self):
        self.plot_screen.show()
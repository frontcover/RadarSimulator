from screens.main_screen import MainScreen

class Navigator:
    '''
    Navigate between screens
    '''
    def __init__(self):
        self.main_screen = MainScreen(self)

    def open_main_screen(self):
        self.main_screen.show()
from PyQt5.QtWidgets import QMainWindow, QErrorMessage
from ui.python.ui_main_screen import Ui_MainScreen
from PyQt5 import QtCore, QtGui
from target import Target
from constant import R_MAX, CENTER_GROUND_RADIUS, TICK_INTERVAL
from option import Option

class MainScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        # Setup UI
        self.uic = Ui_MainScreen()
        self.uic.setupUi(self)
        self.uic.checkBox.stateChanged.connect(self.toggle_cfar)
        self.uic.v_multiple.setValue(Option.v_multiple)
        self.uic.v_multiple.valueChanged.connect(self.v_multiple_on_change)
        self.uic.show_actual.stateChanged.connect(self.toggle_show_actual)
        self.uic.show_observe.stateChanged.connect(self.toggle_show_observe)
        self.uic.show_predict.stateChanged.connect(self.toggle_show_predict)

        # Setup status UI
        self.stui = [] # status ui
        self.setup_stui()

        # Init states
        self.targets = [None, None, None, None]
        self.tracking_target = None

        # Timer
        timer = QtCore.QTimer(self)
        timer.setInterval(TICK_INTERVAL)
        timer.timeout.connect(self.tick)
        timer.start()

    def setup_stui(self):
        # status ui
        self.stui = [
            {
                "r": self.uic.lineEdit_kc_1,
                "a": self.uic.lineEdit_pv_1,
                "dir": self.uic.lineEdit_hd_1,
                "v": self.uic.lineEdit_vt_1,
                "btn": self.uic.btn_create_1,
            },
            {
                "r": self.uic.lineEdit_kc_2,
                "a": self.uic.lineEdit_pv_2,
                "dir": self.uic.lineEdit_hd_2,
                "v": self.uic.lineEdit_vt_2,
                "btn": self.uic.btn_create_2,
            },
            {
                "r": self.uic.lineEdit_kc_3,
                "a": self.uic.lineEdit_pv_3,
                "dir": self.uic.lineEdit_hd_3,
                "v": self.uic.lineEdit_vt_3,
                "btn": self.uic.btn_create_3,
            },
            {
                "r": self.uic.lineEdit_kc_4,
                "a": self.uic.lineEdit_pv_4,
                "dir": self.uic.lineEdit_hd_4,
                "v": self.uic.lineEdit_vt_4,
                "btn": self.uic.btn_create_4,
            }
        ]

        self.stui[0]["btn"].clicked.connect(self.onclick_btn_create_1)
        self.stui[1]["btn"].clicked.connect(self.onclick_btn_create_2)
        self.stui[2]["btn"].clicked.connect(self.onclick_btn_create_3)
        self.stui[3]["btn"].clicked.connect(self.onclick_btn_create_4)

    def tick(self):
        self.uic.radar.tick()
        self.uic.radar_2.tick()

    def toggle_cfar(self, isCheck):
        Option.cfar = not Option.cfar

    def v_multiple_on_change(self, value):
        print("Set v x", value)
        Option.v_multiple = value

    def onclick_btn_create(self, i):
        try:
            r = float(self.stui[i]["r"].text())
            a = float(self.stui[i]["a"].text())
            dir = float(self.stui[i]["dir"].text())
            v = float(self.stui[i]["v"].text())
            
            ## Validate r, a, dir, v
            # Validate r
            if not (r > CENTER_GROUND_RADIUS and r < R_MAX):
                raise Exception(f"Khoảng cách phải nằm trong khoảng ({CENTER_GROUND_RADIUS},{R_MAX})")
            # Validate v
            if v < 0:
                raise Exception("Vận tốc không được âm")
                      
            self.targets[i] = Target(r, a, dir, v)
            self.stui[i]["btn"].setDisabled(True)
        except ValueError as e:
            msg = QErrorMessage(self)
            print(str(e))
            msg.showMessage("Giá trị là số không hợp lệ")
        except Exception as e:
            msg = QErrorMessage(self)
            print(str(e))
            msg.showMessage(str(e))

    def onclick_btn_create_1(self):
        self.onclick_btn_create(0)
    
    def onclick_btn_create_2(self):
        self.onclick_btn_create(1)

    def onclick_btn_create_3(self):
        self.onclick_btn_create(2)

    def onclick_btn_create_4(self):
        self.onclick_btn_create(3)

    def toggle_show_actual(self, check):
        Option.show_actual = not Option.show_actual

    def toggle_show_observe(self, check):
        Option.show_observe = not Option.show_observe

    def toggle_show_predict(self, check):
        Option.show_predict = not Option.show_predict
from util import rphi_to_xy, xy_to_rphi
from noise import Noise
import numpy as np
from constant import TICK_INTERVAL
from option import Option

class Target():
    def __init__(self, r, a, dir, v) -> None:
        """
        Params:
            r: khoảng cách tới radar (đơn vị hải lý)
            a: phương vị (đơn vị độ)
            dir: hướng di chuyển (đơn vị độ)
            v: vận tốc di chuyển (đơn vị hải lý/giờ)
        """

        self.dir = dir
        self.v = v
        self.set_ra(r, a)

    def set_xy(self, x, y):
        self.x = x
        self.y = y
        r, a = xy_to_rphi(x, y)
        self.r = r
        self.a = a % 360

    def set_ra(self, r, a):
        self.r = r
        self.a = a % 360
        self.x, self.y = rphi_to_xy(r, a)

    def tick(self):
        # self.v là vận tốc tính theo hải lý / giờ
        # v_tick là vạn tốc tính theo hải lý / tick. 1 tick = TICK_INTERVAL ms
        v_tick = self.v * TICK_INTERVAL / 3.6e6
        v_tick_scaled = v_tick * Option.v_multiple
        dx, dy = rphi_to_xy(v_tick_scaled, self.dir)
        self.set_xy(self.x + dx, self.y + dy)
import math
import numpy as np
import constant as C

def rphi_to_xy(r, phi):
    '''
    phi: mesured in degree
    '''
    phi = phi * math.pi / 180
    x = r * math.sin(phi)
    y = r * math.cos(phi)
    return x, y

def xy_to_rphi(x, y):
    r = math.sqrt(x*x+y*y)
    if (y == 0): 
        y = 0.00001
    phi = math.atan(x/y) * 180 / math.pi
    if y < 0:
        phi = phi + 180
    phi = phi % 360
    return r, phi

def dist(x1, y1, x2, y2):
    return np.linalg.norm([x1-x2, y1-y2])

def P(x, y):
    """
    Apply reference system for x, y (for painting)
    """
    x = C.CENTER_X + C.SCALE * x
    y = C.CENTER_Y - C.SCALE * y
    return x, y

def R(r):
    """
    Apply reference system for radius (for painting)
    """
    return C.SCALE * r

if __name__ == "__main__":
    assert xy_to_rphi(*rphi_to_xy(3, 40)) == (3, 40)
    assert xy_to_rphi(*rphi_to_xy(1, 135)) == (1, 135) # -45
    assert xy_to_rphi(*rphi_to_xy(1, 190)) == (1, 190) # 10
    assert xy_to_rphi(*rphi_to_xy(1, 271)) == (1, 271) # -89
    assert dist(3, 0, 0, 4) == 5

import math

def rphi_to_xy(r, phi):
    '''
    phi: mesured in degree
    '''
    phi = phi * math.pi / 180
    x = r * math.cos(phi)
    y = r * math.sin(phi)
    return x, y

def xy_to_rphi(x, y):
    r = math.sqrt(x*x+y*y)
    if (x == 0): 
        x = 0.00001
    phi = math.atan(y/x) * 180 / math.pi
    if x < 0:
        phi = phi + 180
    phi = phi % 360
    return r, phi

if __name__ == "__main__":
    assert xy_to_rphi(*rphi_to_xy(3, 40)) == (3, 40)
    assert xy_to_rphi(*rphi_to_xy(1, 135)) == (1, 135) # -45
    assert xy_to_rphi(*rphi_to_xy(1, 190)) == (1, 190) # 10
    assert xy_to_rphi(*rphi_to_xy(1, 271)) == (1, 271) # -89
import numpy as np
import constant as C
from scipy import signal

def rphi_to_xy(r, phi):
    '''
    phi: mesured in degree
    '''
    phi = phi * np.pi / 180
    x = r * np.sin(phi)
    y = r * np.cos(phi)
    return x, y

def xy_to_rphi(x, y):
    r = np.sqrt(x*x+y*y)
    if (y == 0): 
        y = 0.00001
    phi = np.arctan(x/y) * 180 / np.pi
    if y < 0:
        phi = phi + 180
    phi = phi % 360
    return r, phi

def vectorized_xy_to_rphi(x, y):
    r = np.sqrt(x*x+y*y)
    y[y==0] = 0.00001
    phi = np.arctan(x/y) * 180 / np.pi
    phi[y<0] = phi[y<0] + 180
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

def P_revert(x, y):
    x = (x - C.CENTER_X) / C.SCALE
    y = (C.CENTER_Y - y) / C.SCALE
    return x, y

def R(r):
    """
    Apply reference system for radius (for painting)
    """
    return C.SCALE * r

def gaussian_kernel_1d(size, sigma):
    # create a one-dimensional array of size 'size'
    x = np.arange(-(size//2), size//2 + 1, 1)
    
    # calculate the Gaussian distribution
    kernel = np.exp(-np.power(x, 2) / (2 * np.power(sigma, 2)))
    
    # normalize the kernel
    kernel = kernel / np.sum(kernel)
    
    return kernel

def gaussian_kernel_2d(width, height, mu, sigma):
    # Create a grid of coordinates using meshgrid
    x, y = np.meshgrid(np.linspace(-1, 1, width), np.linspace(-1, 1, height))

    # Compute the Gaussian function
    gaussian = np.exp(-((x - mu)**2 + (y - mu)**2) / (2 * sigma**2))

    # Normalize the Gaussian function
    return gaussian

def gkern(kernlen=21, std=3):
    """Returns a 2D Gaussian kernel array."""
    gkern1d = signal.gaussian(kernlen, std=std).reshape(kernlen, 1)
    gkern2d = np.outer(gkern1d, gkern1d)
    return gkern2d

def CFARDetector1D(data, pfa, train_size, guard_size):
    """Apply the 1D-CFAR algorithm to detect peaks in the given data.

    Args:
        data (ndarray): The 1D input data to search for peaks.
        threshold_factor (float): The factor used to multiply the noise level
            estimate to obtain the detection threshold.
        window_size (tuple): The size of the sliding window used in the CFAR
            algorithm.

    Returns:
        
    """
    win = train_size + guard_size

    N = train_size * 2
    threshold_factor = N * (np.power(pfa, -1/N) - 1)

    # Output data
    out = np.zeros_like(data)

    # Slide the window across the data and compare the central cell to the
    # mean of the surrounding training cells
    for i in range(win, len(data) - win):
        # Compute the indices of the training cells
        training_indices = np.concatenate(
            (np.arange(i - win, i - guard_size),
                np.arange(i + guard_size + 1, i + win + 1)))

        # Extract the training cells
        training_cells = data[training_indices]

        # Compute the noise power estimate
        Pn = np.mean(training_cells)

        # Compute the detection threshold
        threshold = threshold_factor * Pn

        # If the central cell is greater than the threshold, add it to the
        # list of peaks
        if data[i] > threshold:
            out[i] = 1

    return out

if __name__ == "__main__":
    assert xy_to_rphi(*rphi_to_xy(3, 40)) == (3, 40)
    assert xy_to_rphi(*rphi_to_xy(1, 135)) == (1, 135) # -45
    assert xy_to_rphi(*rphi_to_xy(1, 190)) == (1, 190) # 10
    assert xy_to_rphi(*rphi_to_xy(1, 271)) == (1, 271) # -89
    assert dist(3, 0, 0, 4) == 5

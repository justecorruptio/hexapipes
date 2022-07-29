import math
import AppKit
import pyautogui

from PIL import Image, ImageDraw
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

import os


from screenshot import *

x = np.array([True, False, False, True, True, False])
#x = np.array([True, True, True, True, True, False])

def as_braille(h):
    return chr(0x2800 + (h[0] << 0) + (h[5] << 1) + (h[4] << 2) + (h[1] << 3) + (h[2] << 4) + (h[3] << 5))

def print_hexes(hexes):
    output = ''
    for y in range(N):
        if y % 2 == 1:
            output += ' '
        for x in range(N):
            output += as_braille(hexes[y, x]) + ' '
        output += '\n'

    print(output)

print_hexes(hexes)

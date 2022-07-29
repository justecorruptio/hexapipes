import math
import AppKit
import pyautogui

from PIL import Image, ImageDraw
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

print('OPENING SCREENSHOT')
#scr = pyautogui.screenshot()
scr = Image.open('screenshot.png')

print('FINDING HEXAGON MASK')
mat = np.array(scr)[..., :-1]
red, green, blue = mat.T
mask = (red == 0xdd) & (green == 0xdd) & (blue == 0xdd)
mask = ndimage.binary_dilation(mask, iterations=3)
mask = ndimage.binary_erosion(mask, iterations=1)
mask = mask.T

print('DETECTING PLAY AREA')
label_im, nb_labels = ndimage.label(mask)
sizes = ndimage.sum(mask, label_im, range(nb_labels + 1))
mask = label_im == np.argmax(sizes)
play_area = ndimage.find_objects(mask)[0]
#plt.imshow(mask)
#plt.show()

mat = mat[play_area]
mask = mask[play_area]
H, W = mask.shape

print('DETECTING PUZZLE SIZE')
_, N = ndimage.label(mask[0]) # count the number of tips on the top row
w = W / 81
h = H * 2 / 121

dx = int(h / 2 / math.tan(math.pi / 3))
dy = int(h / 2)
dh = int(h / 2 / math.sin(math.pi / 3))
point_offsets = np.array([(w - dx, dy), (w + dx, dy), (w + dh, h), (w + dx, h + dy), (w - dx, h + dy), (w - dh, h)])

print('PROBING HEX EDGES')
hexes = np.zeros((N, N, 6), dtype=bool)
for y in range(N):
    for x in range(N):
        edges = point_offsets + ((x + int(y % 2 == 1) / 2) * 2 * w, y * 3 * h / 2)
        i, j = edges.T.astype(int)
        hexes[y, x] = mask[j, i]


mat[mask] = (0xFF, 0x00, 0x00)

im = Image.fromarray(mat)
draw = ImageDraw.Draw(im)
#draw.rectangle([(0, 0), (hex_width, hex_height)], fill='#00000000', outline='#000000')
for x in range(N):
    for y in range(N):
        p = point_offsets + [(x + int(y % 2 == 1) / 2) * 2 * w, y * 3 * h / 2]
        draw.point(list(map(tuple, p)), '#000000')
im.show()

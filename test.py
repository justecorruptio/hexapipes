import time
import math
import AppKit
import pyautogui

from PIL import Image, ImageDraw
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

import os


from screenshot import *

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

solved = np.zeros((N, N), dtype=bool)

def correct(hexes, x, y):
    m = hexes[y, x]

    s = y % 2
    dirs = [(-1, -1 + s), (-1, s), (0, 1), (1, s), (1, -1 + s), (0, -1)]

    for u, (dy, dx) in enumerate(dirs):
        v = (u + 3) % 6
        other = False
        if 0 <= y + dy < N and 0 <= x + dx < N:
            other = hexes[y + dy, x + dx][v]
        if other != m[u]:
            return False
    return True


def make_cluster(hexes, solved, x, y, seen):
    if (x, y) in seen:
        return

    seen.add((x, y))

    m = hexes[y, x]
    s = y % 2
    dirs = [(-1, -1 + s), (-1, s), (0, 1), (1, s), (1, -1 + s), (0, -1)]
    for u, (dy, dx) in enumerate(dirs):
        v = (u + 3) % 6
        if 0 <= y + dy < N and 0 <= x + dx < N:
            if solved[y + dy, x + dx] and hexes[y + dy, x + dx][v] and m[u]:
                make_cluster(hexes, solved, x + dx, y + dy, seen)


def is_loop(hexes, solved, cluster, x, y):
    # the case where i'm trying to connect to a unsolved that's linked to solved
    m = hexes[y, x]
    s = y % 2
    dirs = [(-1, -1 + s), (-1, s), (0, 1), (1, s), (1, -1 + s), (0, -1)]
    for u, (dy, dx) in enumerate(dirs):
        v = (u + 3) % 6
        if 0 <= y + dy < N and 0 <= x + dx < N:
            if solved[y + dy, x + dx] and hexes[y + dy, x + dx][v] and (x + dx, y + dy) in cluster:
                return True
    return False


def possible(hexes, solved, x, y):
    m = hexes[y, x]
    #print("    ", m)

    s = y % 2
    dirs = [(-1, -1 + s), (-1, s), (0, 1), (1, s), (1, -1 + s), (0, -1)]

    # -1 = sure_not, 0 = maybe, 1 = sure_yes

    for u, (dy, dx) in enumerate(dirs):
        v = (u + 3) % 6
        if 0 <= y + dy < N and 0 <= x + dx < N:
            if solved[y + dy, x + dx]:
                other = [-1, 1][int(hexes[y + dy, x + dx][v])]
            else:
                cluster = set()
                make_cluster(hexes, solved, x, y, cluster)
                print(m, cluster)
                if is_loop(hexes, solved, cluster, x + dx, y + dy):
                    other = -1
                else:
                    other = 0
        else: # outside
            other = -1
        #print("    ", u, other, m[u])
        if (other == -1 and m[u]) or (other == 1 and not m[u]):
            return False
    return True


while True:
    for y in range(N):
        for x in range(N):
            if solved[y, x]:
                continue

            start = tuple(hexes[y, x])
            rots = 0
            num_poss = 0
            for i in range(6):

                poss = possible(hexes, solved, x, y)
                if poss:
                    rots = i
                    num_poss += 1
                h = tuple(hexes[y, x])
                hexes[y, x] = h[-1:] + h[:-1]

                if tuple(hexes[y, x]) == start:
                    break # stop when symmetry is found

            if num_poss == 0:
                print("ERROR", y, x)
                1/0
            elif num_poss == 1:
                solved[y, x] = True
                dx, dy = hex_offset(x, y)
                pyautogui.moveTo((X_OFFSET + dx + HEX_W2) * MOUSE_SCALE, (Y_OFFSET + dy + HEX_H2) * MOUSE_SCALE, .01)
                for i in range(rots):
                    h = tuple(hexes[y, x])
                    hexes[y, x] = h[-1:] + h[:-1]
                    time.sleep(.01)
                    pyautogui.click()
                print("SOLVE", y, x, rots)
            else:
                print("NPOSS", y, x, num_poss)

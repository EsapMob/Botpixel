import win32api
import win32con
import time
from PIL import ImageGrab
import cv2
import numpy as np
import pyautogui

ressource_position = [
    {"x": 1205, "y": 142, "color": 0x3173d7},
    {"x": 1277, "y": 97, "color": 0x2368b1},
    {"x": 1447, "y": 157, "color": 0x1b5baf},
    {"x": 1498, "y": 241, "color": 0x2b6fc2},
    {"x": 1518, "y": 220, "color": 0x2166b2},
    {"x": 1279, "y": 440, "color": 0x0d3f6d},
    {"x": 1270, "y": 490, "color": 0x195396},
    {"x": 1249, "y": 529, "color": 0x1954ab},
    {"x": 1269, "y": 488, "color": 0x134a83},
    {"x": 1270, "y": 578, "color": 0x2562ba},
    {"x": 1175, "y": 539, "color": 0x235aab},
    {"x": 893, "y": 734, "color": 0x15539c},
    {"x": 827, "y": 661, "color": 0x153d79},
    {"x": 786, "y": 682, "color": 0x0d407e},
    {"x": 1174, "y": 517, "color": 0x1d57a4},
    {"x": 1416, "y": 542, "color": 0x1254ac},
    {"x": 1277, "y": 439, "color": 0xe3d6d},
    {"x": 1228, "y": 513, "color": 0x175399},
    {"x": 1512, "y": 269, "color": 0x3b78d4},
    {"x": 1510, "y": 268, "color": 0x3173d6},
]

fight_button = {"x": 1780, "y": 760, "colors": [0xba4101, 0xff6600, 0xff6100]}
ending_button = {"x": 1604, "y": 649, "colors": [0xba4101, 0xff6600, 0xff6100]}


def fighting():
    x, y = fight_button["x"], fight_button["y"]
    colors = fight_button["colors"]
    img = ImageGrab.grab()
    r, g, b = img.getpixel((x, y))
    current = rgb_to_hex(r, g, b)
    return current in colors

def fought():
    x, y = ending_button["x"], ending_button["y"]
    colors = ending_button["colors"]
    img = ImageGrab.grab()
    r, g, b = img.getpixel((x, y))
    current = rgb_to_hex(r, g, b)
    return current in colors


def rgb_to_hex(r, g, b):
    return (r << 16) + (g << 8) + b


def click_at(x, y):
    win32api.SetCursorPos((x, y))
    time.sleep(0.25)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def scan_and_farm(farm_map):
    print("farming started")
    while True:
        if fighting():
            print("fight detected")
            click_at(fight_button["x"], fight_button["y"])
            time.sleep(5)

        elif fought():
            print("Fight ended")
            click_at(ending_button["x"], ending_button["y"])
            time.sleep(3)

        else:
            time.sleep(1)

                
        for ressource in farm_map:
            x, y, expected = ressource["x"], ressource["y"], ressource["color"]

            img = ImageGrab.grab()
            r, g, b = img.getpixel((x, y))
            current = rgb_to_hex(r, g, b)

            if current == expected:
                print("Ressource trouvé à ({}, {}), farming...".format(x, y, hex(current)))
                click_at(x, y)
                time.sleep(0.5)
                click_at(x + 44, y + 44)
                time.sleep(14)
            else:
                print("Rien à ({}, {}) - attendu : {} / vu : {}".format(x, y, hex(expected), hex(current)))

            time.sleep(0.1)


scan_and_farm(ressource_position)
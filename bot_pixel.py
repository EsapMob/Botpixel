import win32api
import win32con
import time
from PIL import ImageGrab
import cv2
import numpy as np
import pyautogui
import function_fight

ressource_position = [
    {"x": 759, "y": 573, "color": 0x4685ea},
    {"x": 818, "y": 505, "color": 0x296fc5},
    {"x": 934, "y": 493, "color": 0x2064b9},
    {"x": 865, "y": 430, "color": 0x2c70d1},
    {"x": 1223, "y": 346, "color": 0x2c70c2},
    {"x": 1134, "y": 317, "color": 0x266cba},
    {"x": 1154, "y": 285, "color": 0x296ec0},
    {"x": 1359, "y": 170, "color": 0x1659bc},
    {"x": 1666, "y": 89, "color": 0x2f77db},
    {"x": 1454, "y": 195, "color": 0x2b68bc},
    {"x": 1278, "y": 587, "color": 0x1e5787},
    {"x": 1420, "y": 512, "color": 0x1d548a},
    {"x": 1854, "y": 340, "color": 0x2160a6},
    {"x": 1242, "y": 188, "color": 0x1458ae},
    {"x": 1437, "y": 579, "color": 0x1358b3},
    {"x": 1292, "y": 703, "color": 0x2467b3},
    {"x": 1077, "y": 243, "color": 0x578fc4},
]

cases = [
    {"x": 1498, "y": 267, "color": 0xff0000},
    {"x": 921, "y": 561, "color": 0xff0000},
    ]

fight_button = {"x": 1780, "y": 760, "colors": [0xba4101, 0xff6600, 0xff6100]}
ending_button = {"x": 1607, "y": 611, "colors": [0xba4101, 0xff6600, 0xff6100]}


def start_fight():
    x, y = fight_button["x"], fight_button["y"]
    colors = fight_button["colors"]
    img = ImageGrab.grab()
    r, g, b = img.getpixel((x, y))
    current = rgb_to_hex(r, g, b)
    return current in colors

def close_fight():
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
        if start_fight():
            print("fight detected")
            img = ImageGrab.grab()

            for case in cases:
                r, g, b = img.getpixel((case["x"], case["y"]))

                if rgb_to_hex(r, g, b) == case["color"]:
                    print("Case rouge détectée à ({}, {}), clique dessus".format(case["x"], case["y"]))
                    click_at(case["x"], case["y"])
                    time.sleep(0.3)
                    break

            click_at(fight_button["x"], fight_button["y"])
            time.sleep(5)

            function_fight.fight_process()

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


if __name__ == "__main__":
    scan_and_farm(ressource_position)
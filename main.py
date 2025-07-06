import win32api
import win32con
import time
from PIL import ImageGrab
import cv2
import numpy as np
import fight_function
import bank_function

ressource_position = [
    {"x": 818, "y": 505, "color": 0x296fc5},
    {"x": 934, "y": 493, "color": 0x2064b9},
    {"x": 865, "y": 430, "color": 0x2c70d1},
    {"x": 1223, "y": 346, "color": 0x2c70c2},
    {"x": 1134, "y": 317, "color": 0x266cba},
    {"x": 1154, "y": 285, "color": 0x296ec0},
    {"x": 1359, "y": 170, "color": 0x1659b},
    {"x": 1666, "y": 89, "color": 0x2f77db},
    {"x": 1454, "y": 195, "color": 0x2b68bc},
    {"x": 1278, "y": 587, "color": 0x336296},
    {"x": 1420, "y": 512, "color": 0x1d548a},
    {"x": 1854, "y": 340, "color": 0x2160a6},
    {"x": 1242, "y": 188, "color": 0x1458ae},
    {"x": 1437, "y": 579, "color": 0x1358b3},
    {"x": 1292, "y": 703, "color": 0x2467b3},
    {"x": 1077, "y": 243, "color": 0x578fc4},
    {"x": 1132, "y": 267, "color": 0x3d7aca},
    {"x": 1822, "y": 434, "color": 0x2165ab},
    {"x": 1080, "y": 243, "color": 0x3b78cd},
    {"x": 1829, "y": 346, "color": 0x4374b8},
    {"x": 1315, "y": 613, "color": 0x2657a3},
    {"x": 1453, "y": 195, "color": 0x2762c3},
    {"x": 790, "y": 566, "color": 0x3979d4},
    {"x": 1243, "y": 188, "color": 0x1459ab},
    {"x": 1357, "y": 171, "color": 0x1659b4},
    {"x": 1293, "y": 703, "color": 0x2467b3},
    {"x": 1260, "y": 611, "color": 0xe4a91},
    {"x": 1419, "y": 512, "color": 0x1d548c},
    {"x": 1454, "y": 194, "color": 0x185bcb},
    {"x": 1133, "y": 317, "color": 0x276cb8},

]

cases = [
    {"x": 1498, "y": 267, "color": 0xff0000},
    {"x": 875, "y": 585, "color": 0xff0000},
    ]


pod_button = {"x": 1282, "y": 853, "colors": 0xff6600}
fight_button = {"x": 1780, "y": 760, "colors": [0xba4101, 0xff6600, 0xff6100]}
ending_button = {"x": 1672, "y": 622, "colors": [0xffffff, 0xff6100, 0x514a3c]}
pass_button = {"x": 1462, "y": 990, "colors": 0xffffff}


def pass_tour():
    x, y = pass_button["x"], pass_button["y"]
    colors = pass_button["colors"]
    time.sleep(0.2)
    img = ImageGrab.grab()
    r, g, b = img.getpixel((x, y))
    current = rgb_to_hex(r, g, b)
    return current == colors


def start_fight():
    x, y = fight_button["x"], fight_button["y"]
    colors = fight_button["colors"]
    img = ImageGrab.grab()
    r, g, b = img.getpixel((x, y))
    current = rgb_to_hex(r, g, b)
    return current in colors


def close_fight():
    img = ImageGrab.grab()
    target_color = 0xff6100

    for x in range(1407, 1812):
        for y in range(556, 868):
            r, g, b = img.getpixel((x, y))
            current = rgb_to_hex(r, g, b)
            if current == target_color:
                click_at(x, y)
                print("[INFO] Fermer le fight", hex(current), "à (", x, ",", y, ")")
                return True
    return False


def rgb_to_hex(r, g, b):
    return (r << 16) + (g << 8) + b


def click_at(x, y):
    win32api.SetCursorPos((x, y))
    time.sleep(0.25)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def double_click(x, y):
    for _ in range(2):
        click_at(x, y)
        time.sleep(0.05)


def full_pod():
    x, y = pod_button["x"], pod_button["y"]
    colors = pod_button["colors"]
    img = ImageGrab.grab()
    r, g, b = img.getpixel((x, y))
    current = rgb_to_hex(r, g, b)
    return current == colors


def scan_and_farm(farm_map):
    print("farming started")
    while True:
        if full_pod():
            print("[INFO] Full pods. Vroom la banque.")
            time.sleep(15)
            bank_function.empty_process()
            print("[INFO] Back to pechoune.")
            continue

        if start_fight():
            print("[INFO] fight detected")
            img = ImageGrab.grab()

            for case in cases:
                r, g, b = img.getpixel((case["x"], case["y"]))

                if rgb_to_hex(r, g, b) == case["color"]:
                    print("[POSITION] Case rouge détectée à ({}, {}), clique dessus".format(case["x"], case["y"]))
                    click_at(case["x"], case["y"])
                    time.sleep(1.5)
                    break

            click_at(fight_button["x"], fight_button["y"])
            time.sleep(7)

            fight_function.fight_process(case["x"], case["y"])
                
        for ressource in farm_map:
            x, y, expected = ressource["x"], ressource["y"], ressource["color"]

            img = ImageGrab.grab()
            r, g, b = img.getpixel((x, y))
            current = rgb_to_hex(r, g, b)

            if current == expected:
                print("[FARM] Ressource trouvé à ({}, {}), farming...".format(x, y, hex(current)))
                click_at(x, y)
                time.sleep(0.5)
                click_at(x + 44, y + 44)
                time.sleep(6)
            else:
                print("[CHECK] Rien à ({}, {}) - attendu : {} / vu : {}".format(x, y, hex(expected), hex(current)))

            time.sleep(0.1)


if __name__ == "__main__":
    scan_and_farm(ressource_position)
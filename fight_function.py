import win32api
import win32con
import time
from PIL import ImageGrab
import cv2
import numpy as np
import os


charactere_red = [
    "personnage.png",
    "personnage_1.png",
    "personnage_2.png",
    "personnage_3.png",
    "personnage_4.png"
]

pod_button = {"x": 1272, "y": 859, "colors": 0xff6600}
pass_button = {"x": 1462, "y": 990, "colors": 0xffffff}
ending_button = {"x": 1663, "y": 634}


def rgb_to_hex(r, g, b):
    return (r << 16) + (g << 8) + b


def pass_tour():
    x, y = pass_button["x"], pass_button["y"]
    colors = pass_button["colors"]
    time.sleep(0.2)
    img = ImageGrab.grab()
    r, g, b = img.getpixel((x, y))
    current = rgb_to_hex(r, g, b)
    return current == colors


def close_fight():
    img = ImageGrab.grab()
    target_color = 0xff6100

    for x in range(1407, 1812):
        for y in range(556, 868):
            r, g, b = img.getpixel((x, y))
            current = rgb_to_hex(r, g, b)
            if current == target_color:
                click_at(x, y)
                return True
    return False


def click_at(x, y):
    win32api.SetCursorPos((x, y))
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def double_click(x, y):
    for _ in range(2):
        click_at(x, y)
        time.sleep(0.05)


def fight_process(case_x, case_y):
    def invocation_spell():
        target_x = case_x + 60
        target_y = case_y + 30

        for i in range(2):
            win32api.keybd_event(0x54, 0, 0, 0)  # T
            win32api.keybd_event(0x54, 0, win32con.KEYEVENTF_KEYUP, 0)
            print("[SORT] épée volante")

            time.sleep(1.5)

            click_at(target_x, target_y)
            print("[CLIC] à x =", target_x, "y =", target_y)
            time.sleep(0.5)

        while True:
            if close_fight():
                print("[INFO] Fin de combat")
                click_at(ending_button["x"], ending_button["y"])
                time.sleep(2)
                break

            elif pass_tour():
                print("[INFO] Passe son tour")
                click_at(pass_button["x"], pass_button["y"])
                time.sleep(7)
            else:
                time.sleep(1)

    time.sleep(1)
    invocation_spell()


if __name__ == "__main__":
    fight_process()

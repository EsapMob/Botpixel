import cv2
import numpy as np
import time
from PIL import ImageGrab
import win32api
import win32con
import os

def click_at(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def double_click(x, y):
    for _ in range(2):
        click_at(x, y)
        time.sleep(0.05)

def find_and_click_sacs():
    templates_dir = "sacs"  # dossier contenant sac_1.png à sac_8.png
    screen = np.array(ImageGrab.grab())
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    for i in range(1, 9):
        path = os.path.join(templates_dir, f"sac_{i}.png")
        template = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

        if template is None:
            print("Image manquante :", path)
            continue

        res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.50
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            x, y = pt[0] + template.shape[1] // 2, pt[1] + template.shape[0] // 2
            print(f"[DETECTÉ] sac_{i} à ({x}, {y})")
            double_click(x, y)
            return  # on stoppe après avoir cliqué sur le premier trouvé

    print("Aucun sac détecté")

if __name__ == "__main__":
    while True:
        find_and_click_sacs()
        time.sleep(1)

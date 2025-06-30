import win32api
import win32con
import time
from PIL import ImageGrab
import cv2
import numpy as np
import fight_function
import os


pod_button = {"x": 1272, "y": 859, "colors": 0xff6600}


def click_at(x, y):
    win32api.SetCursorPos((x, y))
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def double_click(x, y):
    for _ in range(3):
        click_at(x, y)
        time.sleep(0.05)


def rgb_to_hex(r, g, b):
    return (r << 16) + (g << 8) + b


def full_pod():
    x, y = pod_button["x"], pod_button["y"]
    colors = pod_button["colors"]
    img = ImageGrab.grab()
    r, g, b = img.getpixel((x, y))
    current = rgb_to_hex(r, g, b)
    return current == colors


def empty_process():
    print("[DEBUG] empty_process lancé !")

    def goto_bank():
        print("[DEBUG] goto_bank appelé")
        time.sleep(5)
        win32api.keybd_event(0x55, 0, 0, 0)  # Touche 'u'
        win32api.keybd_event(0x55, 0, win32con.KEYEVENTF_KEYUP, 0)
        print("[POPO] Brakma")

        time.sleep(3)

        click_at(1582, 155)
        print("[INFO] Zaapi")
        time.sleep(1)

        click_at(1641, 200)
        print("[INFO] Se faire transporter")
        time.sleep(2)

        click_at(1183, 164)
        print("[INFO] Divers")
        time.sleep(1)

        click_at(1038, 291)
        print("[INFO] Banque")
        time.sleep(3)

        click_at(1581, 341)
        print("[INFO] Entrer en banque")
        time.sleep(5)

        click_at(1675, 462)
        print("[INFO] Banquier")
        time.sleep(1)

        click_at(1705, 482)
        print("[INFO] Parler")
        time.sleep(1)

        click_at(1079, 469)
        print("[INFO] Consulter son coffre personnel")
        time.sleep(2)

        click_at(1622, 242)
        print("[INFO] Ressources diverses")
        time.sleep(4)


    def backto_fish():
        click_at(1873, 195)
        print("[INFO] Fermer la banque")
        time.sleep(1)

        win32api.keybd_event(0x59, 0, 0, 0)  # Touche 'y'
        win32api.keybd_event(0x59, 0, win32con.KEYEVENTF_KEYUP, 0)
        print("[POPO] Rappel")
        time.sleep(3)

        click_at(1870, 734)
        time.sleep(5)

        click_at(1100, 785)
        time.sleep(5)

        click_at(1867, 248)
        time.sleep(5)

        click_at(1572, 43)
        time.sleep(6)

        click_at(1877, 238)
        time.sleep(5)

        click_at(1866, 96)
        time.sleep(6)

        click_at(847, 629)


    def empty_bag():
        templates_dir = "sacs"
        found_any = False

        zone = (1549, 171, 1901, 784)

        for i in range(1, 9):
            screen = np.array(ImageGrab.grab(bbox=zone))
            screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

            path = os.path.join(templates_dir, "sac_" + str(i) + ".png")
            template = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

            if template is None:
                print("[DEBUG] Image manquante :", path)
                continue

            res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.50
            loc = np.where(res >= threshold)

            for point in zip(*loc[::-1]):
                x = point[0] + template.shape[1] // 2 + zone[0]
                y = point[1] + template.shape[0] // 2 + zone[1]
                print("[DETECT] sac_", i, "à (", x, ",", y, ")")

                
                win32api.keybd_event(0x11, 0, 0, 0)  # touche CTRL

                for _ in range(2):
                    win32api.SetCursorPos((x, y))
                    time.sleep(0.05)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                    time.sleep(0.05)

                
                win32api.keybd_event(0x11, 0, win32con.KEYEVENTF_KEYUP, 0)

                time.sleep(0.2)
                found_any = True
                break

        return found_any

    goto_bank()

    while True:
        if not empty_bag():
            print("[DEBUG] Aucun sac détecté, retour à la pêche")
            backto_fish()
            break
        time.sleep(1)



if __name__ == "__main__":
    empty_process()


 



import win32api
import win32con
import time
from PIL import ImageGrab
import cv2
import numpy as np
import os
import math

#Combat générique

charactere_red = [
    "personnage.png",
    "personnage_1.png",
    "personnage_2.png",
    "personnage_3.png",
    "personnage_4.png"
]

charactere_bleu = [
    "crabe.png",
    "devoreur_brochet.png",
    "devoreur_chaton.png",
    "devoreur_crable.png",
    "devoreur_greuvette.png",
    "devoreur_pane.png",
    "devoreur_raie.png",
    "devoreur_truite.png",
    "larve_bleu.png",
    "pountch.png"
]


def click_at(x, y):
    win32api.SetCursorPos((x, y))
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def rgb_to_hex(r, g, b):
    return (r << 16) + (g << 8) + b


def pos_personnage(threshold=0.60):
    templates_dir = "personnage"
    time.sleep(0.2)
    screenshot = np.array(ImageGrab.grab())
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    for image_path in charactere_red:
        path = os.path.join(templates_dir, image_path)
        template = cv2.imread(path, 0)
        if template is None:
            print("[DEBUG] Image non trouvée ou invalide :", path)
            continue

        w, h = template.shape[::-1]

        result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            return (center_x, center_y)

    return None


pos = pos_personnage()

if pos:
    x, y = pos
    print("[DEBUG] Position personnage : x =", x, "y =", y)
else:
    print("[DEBUG] Position personnage non détecté à l'écran.")



def pos_mob(threshold=0.60):
    templates_dir = "mob"
    time.sleep(0.2)
    screenshot = np.array(ImageGrab.grab())
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    for image_path in charactere_bleu:
        path = os.path.join(templates_dir, image_path)
        template = cv2.imread(path, 0)
        if template is None:
            print("[DEBUG] Image non trouvée ou invalide :", image_path)
            continue

        w, h = template.shape[::-1]

        result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            return (center_x, center_y)

    return None

pos = pos_mob()

if pos:
    x, y = pos
    print("[DEBUG] Position mob : x =", x, "y =", y)
else:
    print("[DEBUG] Position mob non détecté à l'écran.")



def active_spell():
    pos1 = pos_personnage()
    pos2 = pos_mob()

    if pos1 and pos2:
        x1, y1 = pos1
        x2, y2 = pos2

        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        print("[DEBUG] Distance entre personnage et mob : {:.2f} pixels".format(distance))

        if distance < 259:
            target_x, target_y = x2, y2
            print("[ACTION] Le mob est à portée, lancement du sort.")

            for i in range(2):
                win32api.keybd_event(0x32, 0, 0, 0)  # touche "é"
                win32api.keybd_event(0x32, 0, win32con.KEYEVENTF_KEYUP, 0)
                print("[SORT] Flamiche")

                time.sleep(1.5)

                click_at(target_x, target_y)
                print("[CLIC] à x =", target_x, "y =", target_y)
                time.sleep(2)
        else:
            print("[INFO] Le mob est trop loin pour lancer le sort.")
    else:
        print("[ERREUR] Impossible de détecter personnage ou mob.")


active_spell()





## Rapprocher le personnage du mob si pas la PO pour sort





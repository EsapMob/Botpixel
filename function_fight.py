import win32api
import win32con
import time
from PIL import ImageGrab
import cv2
import numpy as np
import pyautogui


mob_blue = ("devoreur.png")
charactere_red = [
    "personnage.png",
    "personnage_1.png",
    "personnage_2.png",
    "personnage_3.png"
]


ending_button = {"x": 1607, "y": 611, "colors": [0xba4101, 0xff6600, 0xff6100]}
pass_button = {"x": 1462, "y": 990, "colors": 0xffffff}


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
    x, y = ending_button["x"], ending_button["y"]
    colors = ending_button["colors"]
    img = ImageGrab.grab()
    r, g, b = img.getpixel((x, y))
    current = rgb_to_hex(r, g, b)
    return current in colors


def click_at(x, y):
    win32api.SetCursorPos((x, y))
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def fight_process():
    def charactere_position(threshold=0.60):
        time.sleep(0.2)
        screenshot = np.array(ImageGrab.grab())
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        for image_path in charactere_red:
            template = cv2.imread(image_path, 0)
            if template is None:
                print("Image non trouvée ou invalide :", image_path)
                continue

            w, h = template.shape[::-1]

            result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val >= threshold:
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                return (center_x, center_y)

        return None

    pos = charactere_position()

    if pos:
        x, y = pos
        print("Position du personnage trouvée : x =", x, "y =", y)
    else:
        print("Personnage non détecté à l'écran.")


    charactere_position()



    def invocation_spell():
        pos = charactere_position()
        if pos:
            x, y = pos
            target_x = x + 60
            target_y = y + 30

            win32api.keybd_event(0x54, 0, 0, 0) #Raccourci du T
            win32api.keybd_event(0x54, 0, win32con.KEYEVENTF_KEYUP, 0)
            print("[SORT] épée volante")

            time.sleep(2)

            click_at(target_x, target_y)
            print("[CLIC] à x=", target_x, "y=", target_y)
            time.sleep(2)
        else:
            print("Position du personnage non détectée, pas de sort lancé.")

        while True:
            print("[DEBUG] close_fight() =", close_fight())
            if close_fight():
                print("[INFO] Fin de combat détectée")
                click_at(ending_button["x"], ending_button["y"])
                break

            elif pass_tour():
                print("[INFO] Passe son tour")
                click_at(pass_button["x"], pass_button["y"])
                time.sleep(7)

            else:
                time.sleep(1)
                    


    time.sleep(4) # délais entre trouver le perso et select le sort
    invocation_spell()

if __name__ == "__main__":
    fight_process()


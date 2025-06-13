import win32api
import win32con
import time
from PIL import ImageGrab
import cv2
import numpy as np
import pyautogui




case_side_1 = [
    {"x": 620, "y": 442, "color": 0x0000ff},
    {"x": 1577, "y": 538, "color": 0x0000ff},
    {"x": 1627, "y": 511, "color": 0x0000ff},
    {"x": 1682, "y": 491, "color": 0x0000ff},
    {"x": 1725, "y": 470, "color": 0x0000ff},
    {"x": 1675, "y": 437, "color": 0x0000ff},
    {"x": 1632, "y": 421, "color": 0x0000ff},
    {"x": 1577, "y": 391, "color": 0x0000ff},
    ]


case_side_2 = [
    {"x": 1867, "y": 391, "color": 0xff0000},
    {"x": 950, "y": 414, "color": 0xff0000},
    {"x": 905, "y": 438, "color": 0xff0000},
    {"x": 859, "y": 466, "color": 0xff0000},
    {"x": 806, "y": 487, "color": 0xff0000},
    {"x": 853, "y": 513, "color": 0xff0000},
    {"x": 906, "y": 540, "color": 0xff0000},
    {"x": 951, "y": 565, "color": 0xff0000},
    ]


mob_blue = ("devoreur.png")
charactere_red = [
    "personnage.png",
    "personnage_1.png",
    "personnage_2.png",
    "personnage_3.png"
]

pass_button = {"x": 1462, "y": 990, "colors": 0xffffff}


#EN TEST, A DEGAGER UNE FOIS SUR LE MAIN
def rgb_to_hex(r, g, b):
    return (r << 16) + (g << 8) + b


#EN TEST, A DEGAGER UNE FOIS SUR LE MAIN
def click_at(x, y):
    win32api.SetCursorPos((x, y))
    time.sleep(0.25)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)



def pass_tour():
    x, y = pass_button["x"], pass_button["y"]
    colors = pass_button["colors"]
    img = ImageGrab.grab()
    r, g, b = img.getpixel((x, y))
    current = rgb_to_hex(r, g, b)
    return current == colors



def charactere_position(threshold=0.60):
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
        target_y = y - 30

        pyautogui.press('t')
        print("[SORT] épée volante!!")

        time.sleep(1)
        pyautogui.moveTo(target_x, target_y, duration=0.2)
        pyautogui.click()
        print("[CLIC] à x=", target_x, "y=", target_y)
    else:
        print("Position du personnage non détectée, pas de sort lancé.")

    while True:
        if pass_tour():
            print("[INFO] Passe son tour")
            click_at(pass_button["x"], pass_button["y"])
            time.sleep(7)
                


time.sleep(4) # délais entre trouver le perso et select le sort
invocation_spell()


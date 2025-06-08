import win32api
import win32con
import time
from PIL import ImageGrab


peche_map_1 = [
    {"x": 1276, "y": 96, "color": 0x3976c5},
    {"x": 1223, "y": 151, "color": 0x387bcf},
    {"x": 1520, "y": 220, "color": 0x3a76c3},
    {"x": 1277, "y": 440, "color": 0x28507c},
    {"x": 1357, "y": 540, "color": 0x2355ac},
    {"x": 1271, "y": 588, "color": 0x366dc2},
    {"x": 1252, "y": 515, "color": 0x1f57b2},
    {"x": 1211, "y": 563, "color": 0x3266ba},
    {"x": 1187, "y": 535, "color": 0x275dba},
    {"x": 890, "y": 733, "color": 0x295eaa},
    {"x": 828, "y": 662, "color": 0x244983},
    {"x": 1474, "y": 238, "color": 0x3877d8},
    {"x": 1270, "y": 490, "color": 0x3062a5},
]


def scanner_map(peche_map_1):
    img = ImageGrab.grab()
    for banc in peche_map_1:
        x = banc["x"]
        y = banc["y"]
        expected = banc["color"]
        r, g, b = img.getpixel((x, y))
        current = (r << 16) + (g << 8) + b

        if current == expected:
            print("Banc détecté à ({}, {}) - couleur : {}".format(x, y, hex(current)))
        else:
            print("Rien à ({}, {}) - attendu : {} / vu : {}".format(x, y, hex(expected), hex(current)))


def click_peche():
    print("début du farming")
    for banc in peche_map_1:
        x = banc["x"]
        y = banc["y"]
        expected = banc["color"]

        
        win32api.SetCursorPos((x, y))
        time.sleep(0.25)

        
        img = ImageGrab.grab()
        r, g, b = img.getpixel((x, y))
        current = (r << 16) + (g << 8) + b

        if current == expected:
            print("Banc trouvé à ({}, {}), farming...".format(x, y, hex(current)))
            
            
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            time.sleep(0.50)

            
            x_decale = x + 44
            y_decale = y + 44
            win32api.SetCursorPos((x_decale, y_decale))
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            time.sleep(12)

        else:
            print("Rien à ({}, {}) - attendu : {} / vu : {}".format(x, y, hex(expected), hex(current)))

scanner_map(peche_map_1)
click_peche()
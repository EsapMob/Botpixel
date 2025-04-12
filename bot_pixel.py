import win32api
import win32con
import time
from PIL import ImageGrab


peche_map_1 = [
    {"x": 1666, "y": 104, "color": 0x3e79d2},
    {"x": 1453, "y": 195, "color": 0x2762c3},
    {"x": 1395, "y": 162, "color": 0x2664c1},
    {"x": 1243, "y": 189, "color": 0x2d67b6},
    {"x": 1223, "y": 347, "color": 0x3a7acf},
    {"x": 1132, "y": 317, "color": 0x3e7ac4},
    {"x": 1154, "y": 286, "color": 0x3c7ace},
    {"x": 1080, "y": 244, "color": 0x3c78c9},
    {"x": 842, "y": 415, "color": 0x3976c6},
    {"x": 787, "y": 440, "color": 0x3d7bc7},
    {"x": 751, "y": 591, "color": 0x3779d9},
    {"x": 876, "y": 490, "color": 0x3b75cd},
    {"x": 795, "y": 490, "color": 0x3d7bc7},
    {"x": 1291, "y": 703, "color": 0x3d78c6},
    {"x": 1316, "y": 613, "color": 0x2357a7},
    {"x": 1438, "y": 582, "color": 0x2c66b2},
    {"x": 1420, "y": 514, "color": 0x356494},
    {"x": 1825, "y": 434, "color": 0x3d78bd},
    {"x": 1839, "y": 366, "color": 0x2c6bc6},
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

scanner_map(peche_map_1)

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
            print("Banc trouvé à ({}, {}) - couleur correcte : {}, clic...".format(x, y, hex(current)))
            
            
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


click_peche()

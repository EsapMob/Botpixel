import win32api
import win32con
import time
from PIL import ImageGrab

# positions (coordonnées absolues écran)
peche_map_1 = [
    {"x": 829, "y": 260, "color": 0x9b7433},
    {"x": 1057, "y": 258, "color": 0x2e4137},
    {"x": 906, "y": 295, "color": 0x766e51},
    {"x": 1094, "y": 239, "color": 0x000000},
    {"x": 1321, "y": 201, "color": 0x000000},
    {"x": 1361, "y": 196, "color": 0x1c1914},
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
    img = ImageGrab.grab()
    for banc in peche_map_1:
        x = banc["x"]
        y = banc["y"]
        expected = banc["color"]
        r, g, b = img.getpixel((x, y))
        current = (r << 16) + (g << 8) + b

        if current == expected:
            print("Banc trouvé à ({}, {}) - couleur correcte : {}, clic...".format(x, y, hex(current)))
            
            # click la pos du banc
            win32api.SetCursorPos((x, y))
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            time.sleep(1)

            # click recolte
            x_decale = x + 44
            y_decale = y + 44
            win32api.SetCursorPos((x_decale, y_decale))
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            time.sleep(20)

        else:
            print("Rien à ({}, {}) - attendu : {} / vu : {}".format(x, y, hex(expected), hex(current)))

click_peche()

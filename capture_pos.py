import win32api
import win32con
import time
from PIL import ImageGrab

output_path = r"C:\Users\mvkvi\Desktop\dofus_pixel\relevés_pixels.txt"
releves = []

# Résolution écran à vérifier
MAX_WIDTH = 1920
MAX_HEIGHT = 1080

print("Clique gauche pour relever (position + couleur). Ctrl+C pour sauvegarder et quitter.")

try:
    while True:
        if win32api.GetAsyncKeyState(win32con.VK_LBUTTON):
            x, y = win32api.GetCursorPos()

            if 0 <= x < MAX_WIDTH and 0 <= y < MAX_HEIGHT:
                img = ImageGrab.grab()
                r, g, b = img.getpixel((x, y))
                hex_color = f"0x{r:02x}{g:02x}{b:02x}"
                log = f'{{"x": {x}, "y": {y}, "color": {hex_color}}}'
                print(log)
                releves.append(log)
                time.sleep(0.3)
            else:
                print("Coordonnée hors de l'écran principal : ({x}, {y})")
                time.sleep(0.5)

        time.sleep(0.01)

except KeyboardInterrupt:
    print("\n Sauvegarde en cours...")
    with open(output_path, "w") as f:
        for ligne in releves:
            f.write(ligne + "\n")
    print("Données enregistrées dans : {output_path}")


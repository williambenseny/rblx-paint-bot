#V3!
import time
import win32api
import win32con
import modules.output as output
import modules.virtualkeystroke as vkey
import modules.utilities as utilities
from tqdm import tqdm
from modules.window_management import setup_window
from modules.utilities import verify_color

previousHexColor = "000000"
# Simulate a mouse click at given coordinates
def click(x, y):
    win32api.SetCursorPos((x, y))
    for _ in range(2):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 1, 1, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -1, -1, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    time.sleep(0.01)

# Simulate a mouse click on a pixel
def click_pixel(coords, add_x, add_y, num_clicks=2):
    # Calcula fatores de escala
    escalaX = (coords["lastX"] - coords["firstX"]) / 199.0
    escalaY = (coords["lastY"] - coords["firstY"]) / 199.0

    # Calcula posição real com base nos fatores
    click_x = round(coords["firstX"] + add_x * escalaX)
    click_y = round(coords["firstY"] + add_y * escalaY)

    for _ in range(num_clicks):
        time.sleep(0.001)
        click(click_x, click_y)
        print(f"clicked: {click_x},{click_y}")


# Function to select a color in the game
def select_color(coords, color):
    global previousHexColor  # Permite acessar e modificar a variável global
    hexColor = utilities.rgb2hex(color)
    print("Proximo hex " + hexColor)
    if hexColor == previousHexColor:
        return
    previousHexColor = hexColor
    click(coords["openButtonX"], coords["openButtonY"])
    click(coords["inputX"], coords["inputY"])
    time.sleep(0.1)
    click(coords["inputX"], coords["inputY"])
    time.sleep(0.1)
    click(coords["inputX"], coords["inputY"])
    vkey.typer(string=hexColor)
    for _ in range(2):
        click(coords["closeButtonX"], coords["closeButtonY"])

# Start the painting process with the selected 32x32 image
def start_painting(image_pixels, image_name):
    output.printAscii()
    print("   Image selected:", image_name)
    startInput = input("   Begin painting? (y/n) ")
    if startInput.lower() != 'y':
        output.clear()
        quit()
    
    output.printAscii()
    print("Painting progress:")
    coords = setup_window()

    if coords is None:
       output.printError("Something went wrong. Try again.")
    
    pixels = {}
    for x in range(200):
        for y in range(200):
            color = image_pixels[x, y]
            if color != (255, 255, 255):
                pixels.setdefault(color, []).append((x, y))
    
    time.sleep(1)
    for _ in range(2):
        click(coords["closeButtonX"], coords["closeButtonY"])
    time.sleep(0.05)
    click(coords["firstX"] + 530, coords["firstY"] + 590)
    time.sleep(0.05)
    click(coords["openButtonX"], coords["openButtonY"] - 205)
    time.sleep(0.05)

    for color in tqdm(pixels):
        select_color(coords, color)
        for pixel in pixels[color]:
            click_pixel(coords, *pixel)  # As posições já são ajustadas no método
            click_x = round(coords["firstX"] + pixel[0] * (coords["lastX"] - coords["firstX"]) / 199)
            click_y = round(coords["firstY"] + pixel[1] * (coords["lastY"] - coords["firstY"]) / 199)
            if not verify_color(click_x, click_y, color):
                select_color(coords, color)
                click_pixel(coords, *pixel)

    
    print("\nPainting completed, enjoy!")
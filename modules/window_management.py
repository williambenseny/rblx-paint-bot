import pygetwindow as gw
import psutil
import win32gui
import win32process
import modules.output as output
from screeninfo import get_monitors

def setup_window(window_title="Roblox", exe_name="RobloxPlayerBeta.exe", width=1681, height=957):
    # Calculate screen resolution
    for m in get_monitors():
        screen_width, screen_height = m.width, m.height

    center_x, center_y = screen_width // 2, screen_height // 2

    roblox_windows = []
    # Get Roblox window
    for win in gw.getAllWindows():
        if win.title == window_title:
            class_name = win32gui.GetClassName(win._hWnd)
            if "Chrome_WidgetWin_1" not in class_name:
                _, pid = win32process.GetWindowThreadProcessId(win._hWnd)
                try:
                    process = psutil.Process(pid)
                    executable_path = process.exe()
                    # Check if the executable path belongs to Roblox
                    if exe_name in executable_path:
                        roblox_windows.append(win)
                except psutil.NoSuchProcess:
                    pass

    if not roblox_windows:
        output.printError("Roblox window not found. Open Roblox and try again!")

    roblox_window = roblox_windows[0]
    if roblox_window.isMinimized:
        roblox_window.restore()

    roblox_window.resizeTo(width, height)
    roblox_window.moveTo(center_x - round(width / 2), center_y - round(height / 2))
    hwnd = roblox_window._hWnd
    win32gui.SetForegroundWindow(hwnd)

    if roblox_window.size != (width, height):
        output.printError("Failed to resize the Roblox window.")

    # Get Roblox window dimensions
    roblox_rect = win32gui.GetWindowRect(hwnd)
    roblox_middle_x = (roblox_rect[0] + roblox_rect[2]) // 2
    roblox_middle_y = (roblox_rect[1] + roblox_rect[3]) // 2

    coordinates = {
        "hwnd": hwnd,
        "firstX": roblox_middle_x - 318,
        "firstY": roblox_middle_y - 381,
        "lastX": roblox_middle_x + 318,
        "lastY": roblox_middle_y + 252,
        "openButtonX": roblox_middle_x - 200,
        "openButtonY": roblox_middle_y + 300,
        "inputX": roblox_middle_x + 140,
        "inputY": roblox_middle_y + 172,
        "closeButtonX": roblox_middle_x - 70,
        "closeButtonY": roblox_middle_y + 174
    }

    # Usando f-strings para imprimir os valores
    print(f"midX: {roblox_middle_x}")
    print(f"midY: {roblox_middle_y}")
    print(f"FX: {coordinates['firstX']}")
    print(f"FY: {coordinates['firstY']}")
    print(f"LX: {coordinates['lastX']}")
    print(f"LY: {coordinates['lastY']}")

    return coordinates

#639x638
#50x50 = 13x13px
#100x100 = 6x7px
#200x200 = 3x3px
#500x500 = 1px
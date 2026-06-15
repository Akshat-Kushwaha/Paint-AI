import pygetwindow as gw
import pyautogui as pt
import openpaint

# Find the Paint window
openpaint()
paint = gw.getWindowsWithTitle('Untitled - Paint')[0]

if paint:
    # pt.press('alt')
    # paint.activate()
    paint.moveTo(0, 0)
    paint.resizeTo(800, 600)
    print(f"Moved '{paint.title}' to the top-left corner.")
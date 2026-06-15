import pygetwindow as gw
import pyautogui as pt

# Find the Notepad window
notepad = gw.getWindowsWithTitle('Untitled - Paint')[0]

if notepad:
    # pt.press('alt')
    # notepad.activate()
    notepad.moveTo(0, 0)
    notepad.resizeTo(800, 600)
    print(f"Moved '{notepad.title}' to the top-left corner.")
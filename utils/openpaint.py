import pyautogui as pt
import pygetwindow as gw
import time

def open_paint():
    paint = gw.getWindowsWithTitle('Untitled - Paint')
    
    if paint:
        # Try this combination instead of just activate()
        if paint[0].isMinimized:
            paint[0].restore()
        else:
            paint[0].minimize()
            time.sleep(0.2)
            paint[0].restore()
        
        # Force bring to front
        paint[0].activate()
        print("Activated existing Paint")
        time.sleep(3)
    else:
        pt.hotkey('win', 'r')
        pt.write('mspaint')
        pt.press('enter')
        time.sleep(3)
        print("Opened new Paint")
    return paint
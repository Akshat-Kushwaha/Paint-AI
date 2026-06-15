import pyautogui as pt

IMG_DIR = './tools/'

def select_shape(tool = 'pencil'):
    if tool == "rectangle":
        path = IMG_DIR + 'rectangle-tool.png'

    elif tool == "circle":
        path = IMG_DIR + 'circle-tool.png'

    elif tool == "triangle":
        path = IMG_DIR + 'triangle-tool.png'
    
    elif tool == "line":
        path = IMG_DIR + 'line.png'

    elif tool == "select":
        pt.press('s')
        return

    elif tool == 'pencil' :
        pt.press('p')
        return
    try:   
        location = pt.locateOnScreen(path, confidence=0.8)
        if location:
            pt.click(pt.center(location))
    except:
        print("Err >> tool selection error")
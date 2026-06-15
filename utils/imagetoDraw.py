import cv2
import numpy as np
import time
import ctypes
from ctypes import wintypes
import pygetwindow as gw
from utils.get_image import get_image_rgb
from utils.openpaint import open_paint,pt

# --- WINDOWS API SETUP (FOR SPEED) ---
user32 = ctypes.windll.user32
SCREEN_WIDTH = user32.GetSystemMetrics(0)
SCREEN_HEIGHT = user32.GetSystemMetrics(1)

MOUSEEVENTF_MOVE = 0x0001 | 0x8000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", wintypes.LONG), ("dy", wintypes.LONG), ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD), ("time", wintypes.DWORD), ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]
class INPUT_UNION(ctypes.Union):
    _fields_ = [("mi", MOUSEINPUT)]
class INPUT(ctypes.Structure):
    _fields_ = [("type", wintypes.DWORD), ("u", INPUT_UNION)]

def send_input(flags, x, y):
    nx = int(x * 65535 / SCREEN_WIDTH)
    ny = int(y * 65535 / SCREEN_HEIGHT)
    extra = ctypes.c_ulong(0)
    ii_ = INPUT_UNION()
    ii_.mi = MOUSEINPUT(nx, ny, 0, flags, 0, ctypes.pointer(extra))
    user32.SendInput(1, ctypes.pointer(INPUT(0, ii_)), ctypes.sizeof(INPUT))

# --- CORE LOGIC ---

def get_paint_canvas():
    # 1. Bring P
    # aint to front
    open_paint()
    paint = gw.getWindowsWithTitle('Untitled - Paint')[0]
    
    # 2. Calculate Center of Window
    # We assume the canvas starts roughly 150px down (ribbon) and 5px from left
    canvas_start_x = paint.left + 10
    canvas_start_y = paint.top + 160 
    
    # Center 800x600 inside the window area
    draw_x = canvas_start_x + (paint.width - 800) // 2
    draw_y = canvas_start_y + (paint.height - 600 - 160) // 2
    
    return max(draw_x, 0), max(draw_y, 0)

def draw_image(img_path, start_x, start_y):
    img = cv2.imread(img_path, 0)
    if img is None: return

    # Scale image to fit 800x600 while maintaining aspect ratio
    h, w = img.shape
    scale = min(800 / w, 600 / h)
    new_w, new_h = int(w * scale), int(h * scale)
    img_resized = cv2.resize(img, (new_w, new_h))
    
    # Center the scaled image within our 800x600 block
    offset_x = (800 - new_w) // 2
    offset_y = (600 - new_h) // 2

    edges = cv2.Canny(img_resized, 100, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    print(f"Drawing at: {start_x}, {start_y}")
    
    for cnt in contours:
        epsilon = 1.2 * cv2.arcLength(cnt, True) / 1000
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        pts = approx.reshape(-1, 2)

        # Move to start
        first_pt = pts[0]
        send_input(MOUSEEVENTF_MOVE, start_x + offset_x + first_pt[0], start_y + offset_y + first_pt[1])
        send_input(MOUSEEVENTF_LEFTDOWN, 0, 0)

        for p in pts[1:]:
            send_input(MOUSEEVENTF_MOVE, start_x + offset_x + p[0], start_y + offset_y + p[1])
        
        send_input(MOUSEEVENTF_LEFTUP, 0, 0)


def draw_from_image(prompt):
    coords = get_paint_canvas()
    prompt = f"Drawing of {prompt} in MS Paint style, simple outlines only, no shading."
    img_rgb = get_image_rgb(prompt)
    if img_rgb is not None:
        img = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
        cv2.imwrite("image.png", img)
    if coords:
        print("MS Paint found! You have 5 seconds to select your brush/color...")
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        open_paint()
        pt.press('p')  # Select pencil tool
        draw_image("image.png", coords[0], coords[1])
        print("Done!")

if __name__ == "__main__":
    coords = get_paint_canvas()
    prompt = input("Enter image prompt: ")
    img_rgb = get_image_rgb(prompt)
    if img_rgb is not None:
        img = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
        cv2.imwrite("image.png", img)
    if coords:
        print("MS Paint found! You have 5 seconds to select your brush/color...")
        for i in range(5, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        
        draw_image("image.png", coords[0], coords[1])
        print("Done!")
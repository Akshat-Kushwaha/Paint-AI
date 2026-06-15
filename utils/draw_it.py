import json
from tkinter import OFF
import pyautogui as pt
from utils.locate_tool import select_shape
from utils.openpaint import open_paint
from utils.get_commands import get_drawing_commands
from utils.imagetoDraw import draw_from_image

pt.FAILSAFE = False

# ------------------ SETTINGS ------------------
DRAW_SPEED = 0.3
CLICK_DELAY = 0.5
OFFSET_X = 200
OFFSET_Y = 300
# ----------------------------------------------


def draw_shape(command):
    shape = command["shape"]
    start = command["moveTo"]
    end = command["dragTo"]

    # Select tool
    select_shape(shape)
    pt.sleep(CLICK_DELAY)

    # Move and draw
    pt.moveTo(start[0]+OFFSET_X, start[1]+OFFSET_Y)
    pt.mouseDown()
    pt.dragTo(end[0]+OFFSET_X, end[1]+OFFSET_Y, duration=DRAW_SPEED)
    pt.mouseUp()

    pt.sleep(0.3)


def execute_drawing(json_commands):
  for cmd in json_commands:
      draw_shape(cmd)

def shape_based_drawing(prompt):
  commands = get_drawing_commands(prompt)
  print("Drawing commands received:")
  print(commands)
  open_paint()
  pt.sleep(1)

  # Click canvas to focus
  pt.click(500, 400)
  pt.sleep(0.5)

  execute_drawing(commands)

def realistic_drawing(prompt):
   draw_from_image(prompt)

def draw(prompt,prefrence):
    if prefrence == "shape":
        shape_based_drawing(prompt)
    elif prefrence == "realistic":
        realistic_drawing(prompt)
    


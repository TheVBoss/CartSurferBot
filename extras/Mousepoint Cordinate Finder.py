import ctypes
import time

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

def get_mouse():
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

prev_x, prev_y = get_mouse()
while True:
    x, y = get_mouse()
    # Ignore if jumped more than 3000 pixels in one step
    if abs(x - prev_x) < 3000 and abs(y - prev_y) < 3000:
        print(f"Mouse is at: {x}, {y}          ", end="\r")
        prev_x, prev_y = x, y
    time.sleep(0.05)
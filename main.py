import time
import keyboard
import math
from ewmh import EWMH


ewmh = EWMH()
width, height = ewmh.getDesktopGeometry()


def frame(client):
    frame = client
    while frame.query_tree().parent != ewmh.root:
        frame = frame.query_tree().parent
    return frame

def align(x, y, width, height, type):
    win = frame(ewmh.getActiveWindow())

    ewmh.setMoveResizeWindow(win, 0, x, y, width, height)
    ewmh.setWmState(win, 1, type + '+_NET_WM_STATE_REMOVE')

    ewmh.display.flush()

def center():
    win = ewmh.getActiveWindow()
    g = frame(win).get_geometry();

    x = math.floor((width - g.width) / 2);
    y = math.floor((height - g.height) / 2);
    print(height, g.height)

    print(x, y)
    ewmh.setMoveResizeWindow(win, 0, x, y, g.width, g.height)

    ewmh.display.flush()


keyboard.add_hotkey('ctrl+left arrow', lambda: align(0, 0, int(width / 2), height, '_NET_WM_STATE_MAXIMIZED_VERT'))
keyboard.add_hotkey('ctrl+right arrow', lambda: align(int(width / 2), 0, int(width / 2), height, '_NET_WM_STATE_MAXIMIZED_VERT'))
keyboard.add_hotkey('ctrl+up arrow', lambda: align(0, 0, width, int(height / 2), '_NET_WM_STATE_MAXIMIZED_HORZ'))
keyboard.add_hotkey('ctrl+down arrow', lambda: align(0, int(height / 2), width, int(height / 2), '_NET_WM_STATE_MAXIMIZED_HORZ'))

keyboard.add_hotkey('ctrl+alt+f', center)

while True:
    time.sleep(0.05)


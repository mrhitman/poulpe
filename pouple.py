import math
import win32gui
import platform
from ewmh import EWMH

class Pouple:
    @staticmethod
    def create():
        system = platform.system()

        if system == 'Linux':
            return PoulpeXlib()
        elif system == 'Windows':
            return PoulpeWin32()
        else:
            raise Error("Invalid platform")


    def align(self, x, y, width, height, type=''):
        pass

    def alignLeft(self, percent=50):
        self.align(0, 0, 0, 0)

    def alignRight(self, percent=50):
        self.align(0, 0, 0, 0)

    def alignTop(self, percent=50):
        self.align(0, 0, 0, 0)

    def alignBottom(self, percent=50):
        self.align(0, 0, 0, 0)

    def center(self):
        pass



class PoulpeXlib(Pouple):
    def __init__(self):
        self.ewmh = EWMH()
        self.width, self.height = self.ewmh.getDesktopGeometry()

    def frame(self, client):
        frame = client
        while frame.query_tree().parent != self.ewmh.root:
            frame = frame.query_tree().parent
        return frame

    def align(self, x, y, width, height, type):
        win = self.frame(self.ewmh.getActiveWindow())

        self.ewmh.setMoveResizeWindow(win, 0, x, y, width, height)
        self.ewmh.setWmState(win, 1, '_NET_WM_STATE_TOGGLE + ' + type)

        self.ewmh.display.flush()

    def alignLeft(self):
        self.align(0, 0, int(self.width / 2), self.height, '_NET_WM_STATE_MAXIMIZED_VERT')

    def alignRight(self):
        self.align(int(self.width / 2), 0, int(self.width / 2), self.height, '_NET_WM_STATE_MAXIMIZED_VERT')

    def alignTop(self):
        self.align(0, 0, self.width, int(self.height / 2), '_NET_WM_STATE_MAXIMIZED_HORZ')

    def alignBottom(self):
        self.align(0, int(self.height / 2), self.width, int(self.height / 2), '_NET_WM_STATE_MAXIMIZED_HORZ')

    def center(self):
        win = self.ewmh.getActiveWindow()
        g = self.frame(win).get_geometry();

        x = math.floor((self.width - g.width) / 2);
        y = math.floor((self.height - g.height - 30) / 2);

        x = x if x > 0 else 0
        y = y if y > 0 else 0
        
        self.ewmh.setMoveResizeWindow(win, 0, x, y, g.width, g.height)

        self.ewmh.display.flush()



class PoulpeWin32(Pouple):
    def __init__(self):
        self.width, self.height = (1920, 1080)

    def align(self, x, y, width, height, type=''):
        hwnd = win32gui.GetForegroundWindow()
        win32gui.SetWindowPos(hwnd, 0, x, y, width, height, 0)

    def alignLeft(self):
        self.align(0, 0, int(self.width / 2), self.height)

    def alignRight(self):
        self.align(int(self.width / 2), 0, int(self.width / 2), self.height)

    def alignTop(self):
        self.align(0, 0, self.width, int(self.height / 2))

    def alignBottom(self):
        self.align(0, int(self.height / 2), self.width, int(self.height / 2))

    def center(self):
        hwnd = win32gui.GetForegroundWindow()
        x, y, x2, y2 = win32gui.GetWindowRect(hwnd)

        width = x2 - x
        height = y2 - y

        x = math.floor((self.width - width) / 2);
        y = math.floor((self.height - height - 30) / 2);

        x = x if x > 0 else 0
        y = y if y > 0 else 0
        
        win32gui.SetWindowPos(hwnd, 0, x, y, width, height, 0)
import math
import platform
from ewmh import EWMH


class Pouple:
    @staticmethod
    def create():
        system = platform.system()

        if system == 'Linux':
            return PoulpeXlib()
        elif system == 'Windows':
            if (platform.architecture()[0] == '32bit'):
                return PoulpeWin32()
            else:
                return PoulpeWin64()
        else:
            raise Error("Invalid platform")


    def align(self, x, y, width, height, type=''):
        pass

    def alignLeft(self, percent=50):
        pass

    def alignRight(self, percent=50):
        pass

    def alignTop(self, percent=50):
        pass

    def alignBottom(self, percent=50):
        pass

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
    pass

class PoulpeWin64(Pouple):
    pass
import math
import platform

system = platform.system()

if system == 'Linux':
    from ewmh import EWMH
elif system == 'Windows':
    import win32gui
elif system == 'Darwin':
    pass


class Pouple:
    def __init__(self):
        pass

    @staticmethod
    def create():
        if system == 'Linux':
            return PoupleXlib()
        elif system == 'Windows':
            return PoupleWin32()
        elif system == 'Darwin':
            return PoupleOSX()
        else:
            raise Exception("Invalid platform")

    def align(self, x, y, width, height, type=''):
        pass

    def align_left(self, percent=50):
        self.align(0, 0, 0, 0)

    def align_right(self, percent=50):
        self.align(0, 0, 0, 0)

    def align_top(self, percent=50):
        self.align(0, 0, 0, 0)

    def align_bottom(self, percent=50):
        self.align(0, 0, 0, 0)

    def center(self):
        pass

    def screen(self):
        pass

    def test(self):
        pass


class PoupleXlib(Pouple):
    '''
        Linux X11 platform support
    '''
    vert = '_NET_WM_STATE_MAXIMIZED_VERT'
    horz = '_NET_WM_STATE_MAXIMIZED_HORZ'
    state_disable = 0
    state_enable = 1
    state_toggle = 2

    def __init__(self):
        Pouple.__init__(self)
        self.ewmh = EWMH()
        self.width, self.height = self.ewmh.getDesktopGeometry()

    def frame(self, client):
        frame = client
        while frame.query_tree().parent != self.ewmh.root:
            frame = frame.query_tree().parent
        return frame

    def align(self, x, y, width, height, type=''):
        win = self.frame(self.ewmh.getActiveWindow())
        self.ewmh.setWmState(win, self.state_disable, self.vert)
        self.ewmh.setWmState(win, self.state_disable, self.horz)
        self.ewmh.setWmState(win, self.state_enable, type)
        self.ewmh.setMoveResizeWindow(win, 0, x, y, width, height)
        self.ewmh.display.flush()

    def align_left(self, percent=50):
        self.align(0, 0, math.floor(self.width / 2), self.height, self.vert)

    def align_right(self, percent=50):
        self.align(math.floor(self.width / 2), 0, math.floor(self.width / 2), self.height, self.vert)

    def align_top(self, percent=50):
        self.align(0, 0, self.width, math.floor(self.height / 2), self.horz)

    def align_bottom(self, percent=50):
        self.align(0, math.floor(self.height / 2), self.width, math.floor(self.height / 2), self.horz)

    def center(self):
        win = self.ewmh.getActiveWindow()
        g = self.frame(win).get_geometry()

        x = math.floor((self.width - g.width) / 2)
        y = math.floor((self.height - g.height - 30) / 2)

        x = x if x > 0 else 0
        y = y if y > 0 else 0

        self.ewmh.setMoveResizeWindow(win, 0, x, y, g.width, g.height)

        self.ewmh.display.flush()

    def screen(self):
        win = self.frame(self.ewmh.getActiveWindow())

        self.ewmh.setWmState(win, self.state_enable, self.vert)
        self.ewmh.setWmState(win, self.state_enable, self.horz)


class PoupleWin32(Pouple):
    '''
        Windows support
    '''
    SW_NORMAL = 1
    SW_MAXIMIZE = 3

    def __init__(self):
        Pouple.__init__(self)
        _, _, self.width, self.height = win32gui.GetWindowRect(win32gui.GetDesktopWindow())

    def align(self, x, y, width, height, type=''):
        hwnd = win32gui.GetForegroundWindow()
        win32gui.SetWindowPlacement(hwnd, (0, self.SW_NORMAL, (-1, -1), (-1, -1), (x, y, x + width, y + height)))
        win32gui.SetWindowPos(hwnd, 0, x, y, width, height, 0)

    def align_left(self, percent=50):
        self.align(0, 0, math.floor(self.width / 2), self.height)

    def align_right(self, percent=50):
        self.align(math.floor(self.width / 2), 0, math.floor(self.width / 2), self.height)

    def align_top(self, percent=50):
        self.align(0, 0, self.width, math.floor(self.height / 2))

    def align_bottom(self, percent=50):
        self.align(0, math.floor(self.height / 2), self.width, math.floor(self.height / 2))

    def center(self):
        hwnd = win32gui.GetForegroundWindow()
        x, y, x2, y2 = win32gui.GetWindowRect(hwnd)

        width = x2 - x
        height = y2 - y

        x = math.floor((self.width - width) / 2)
        y = math.floor((self.height - height - 30) / 2)

        x = x if x > 0 else 0
        y = y if y > 0 else 0

        win32gui.SetWindowPos(hwnd, 0, x, y, width, height, 0)

    def screen(self):
        hwnd = win32gui.GetForegroundWindow()
        x, y, x2, y2 = win32gui.GetWindowRect(hwnd)
        win32gui.SetWindowPlacement(hwnd, (2, self.SW_MAXIMIZE, (-1, -1), (-1, -1), (x, y, x2, y2)))

    def test(self):
        hwnd = win32gui.GetForegroundWindow()
        print(win32gui.GetWindowPlacement(hwnd))


class PoupleOSX(Pouple):
    def __init__(self):
        Pouple.__init__(self)

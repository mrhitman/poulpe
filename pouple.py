from sys import platform

if platform.startswith('linux'):
    from ewmh import EWMH
elif platform == 'windows':
    import win32gui
    import win32api
elif platform == 'darwin':
    from AppKit import NSWorkspace, NSScreen


class Pouple:
    def __init__(self):
        pass

    @staticmethod
    def create():
        if platform.startswith('linux'):
            return PoupleXlib()
        elif platform == 'windows':
            return PoupleWin32()
        elif platform == 'darwin':
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

    def fullscreen(self):
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

    def frame(self, frame):
        while frame.query_tree().parent != self.ewmh.root:
            frame = frame.query_tree().parent
        return frame

    def unmaximize(self, win):
        self.ewmh.setWmState(win, self.state_disable, self.vert)
        self.ewmh.setWmState(win, self.state_disable, self.horz)

    def align(self, x, y, width, height, type=''):
        win = self.ewmh.getActiveWindow()
        self.unmaximize(win)
        self.ewmh.setMoveResizeWindow(win, 0, x, y, width, height)
        self.ewmh.display.flush()

    def align_left(self, percent=50):
        self.align(0, 0, self.width // 2, self.height, self.vert)

    def align_right(self, percent=50):
        self.align(self.width // 2, 0, self.width // 2, self.height, self.vert)

    def align_top(self, percent=50):
        self.align(0, 0, self.width, self.height // 2, self.horz)

    def align_bottom(self, percent=50):
        self.align(0, self.height // 2, self.width, self.height // 2, self.horz)

    def center(self):
        win = self.ewmh.getActiveWindow()
        g = win.get_geometry()

        x = (self.width - g.width) // 2
        y = (self.height - g.height) // 2

        x = x if x > 0 else 0
        y = y if y > 0 else 0

        self.ewmh.setMoveResizeWindow(win, 0, x, y, g.width, g.height)
        self.ewmh.display.flush()

    def screen(self):
        win = self.frame(self.ewmh.getActiveWindow())
        self.unmaximize(win)
        self.ewmh.setMoveResizeWindow(win, 0, 0, 0, self.width, self.height)
        self.ewmh.display.flush()

    def fullscreen(self):
        win = self.frame(self.ewmh.getActiveWindow())
        self.ewmh.setWmState(win, self.state_enable, self.vert)
        self.ewmh.setWmState(win, self.state_enable, self.horz)
        self.ewmh.display.flush()


class PoupleWin32(Pouple):
    '''
        Windows support
    '''
    SW_NORMAL = 1
    SW_MAXIMIZE = 3
    OFFSET = 2

    def __init__(self):
        Pouple.__init__(self)

        h_monit = win32api.EnumDisplayMonitors()[0][0].handle
        _, _, self.width, self.height = win32api.GetMonitorInfo(h_monit)['Work']

    def align(self, x, y, width, height, type=''):
        hwnd = win32gui.GetForegroundWindow()
        win32gui.SetWindowPlacement(hwnd, (0, self.SW_NORMAL, (-1, -1), (-1, -1), (x, y, x + width, y + height)))
        win32gui.SetWindowPos(hwnd, 0, x, y, width, height, 0)

    def align_left(self, percent=50):
        self.align(self.OFFSET, self.OFFSET, self.width // 2 + self.OFFSET, self.height)

    def align_right(self, percent=50):
        self.align(self.width // 2 - self.OFFSET, self.OFFSET, self.width // 2, self.height)

    def align_top(self, percent=50):
        self.align(self.OFFSET, self.OFFSET, self.width, self.height // 2)

    def align_bottom(self, percent=50):
        self.align(self.OFFSET, self.height // 2, self.width, self.height // 2)

    def center(self):
        hwnd = win32gui.GetForegroundWindow()
        x, y, x2, y2 = win32gui.GetWindowRect(hwnd)

        width = x2 - x
        height = y2 - y

        x = (self.width - width) // 2
        y = (self.height - height - 30) // 2

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
        from time import sleep
        # while True:
        # app = NSWorkspace.sharedWorkspace().activeApplication()
        self.width, self.height = NSScreen.mainScreen().frame().size
        print(NSWorkspace.sharedWorkspace())
        # sleep(0.5)
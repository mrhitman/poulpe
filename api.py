from sys import platform

if platform.startswith('linux'):
    from ewmh import EWMH
elif platform == 'windows':
    import win32gui
    import win32api
elif platform == 'darwin':
    from AppKit import NSScreen


def get_api():
    if platform.startswith('linux'):
        return Xlib
    elif platform == 'windows':
        return Win32
    elif platform == 'darwin':
        return Darwin


class Api():
    @staticmethod
    def get_top_window():
        raise Exception("Abstract method")

    @staticmethod
    def get_desktop():
        raise Exception("Abstract method")

    @staticmethod
    def get_win_size(hwnd):
        raise Exception("Abstract method")

    @staticmethod
    def set_win_size(hwnd, x, y, width, height):
        raise Exception("Abstract method")

    @staticmethod
    def maximize(hwnd):
        raise Exception("Abstract method")

    @staticmethod
    def unmaximize(hwnd, x, y, width, height):
        raise Exception("Abstract method")

    @staticmethod
    def get_workspace_count():
        raise Exception("Abstract method")


class Xlib(Api):
    @staticmethod
    def get_top_window():
        ewmh = EWMH()
        return ewmh.getActiveWindow()

    @staticmethod
    def get_desktop():
        ewmh = EWMH()
        return ewmh.getDesktopGeometry()

    @staticmethod
    def get_win_size(hwnd):
        return hwnd.get_geometry()

    @staticmethod
    def set_win_size(hwnd, x, y, width, height):
        ewmh = EWMH()
        ewmh.setMoveResizeWindow(hwnd, 0, x, y, width, height)
        ewmh.display.flush()

    @staticmethod
    def maximize(hwnd):
        ewmh = EWMH()
        ewmh.setWmState(hwnd, 1, '_NET_WM_STATE_MAXIMIZED_HORZ')
        ewmh.setWmState(hwnd, 1, '_NET_WM_STATE_MAXIMIZED_VERT')
        ewmh.display.flush()

    @staticmethod
    def unmaximize(hwnd, x, y, width, height):
        ewmh = EWMH()
        ewmh.setWmState(hwnd, 0, '_NET_WM_STATE_MAXIMIZED_HORZ')
        ewmh.setWmState(hwnd, 0, '_NET_WM_STATE_MAXIMIZED_VERT')
        ewmh.display.flush()


class Win32(Api):
    @staticmethod
    def get_top_window():
        return win32gui.GetForegroundWindow()

    @staticmethod
    def get_desktop():
        h_monit = win32api.EnumDisplayMonitors()[0][0].handle
        return win32api.GetMonitorInfo(h_monit)['Work']

    @staticmethod
    def get_win_size(hwnd):
        x, y, x2, y2 = win32gui.GetWindowRect(hwnd)
        width = x2 - x
        height = y2 - y
        return x, y, width, height

    @staticmethod
    def set_win_size(hwnd, x, y, width, height):
        win32gui.SetWindowPos(hwnd, 0, x, y, width, height, 0)

    @staticmethod
    def maximize(hwnd):
        SW_MAXIMIZE = 3
        x, y, x2, y2 = win32gui.GetWindowRect(hwnd)
        win32gui.SetWindowPlacement(hwnd, (2, SW_MAXIMIZE, (-1, -1), (-1, -1), (x, y, x2, y2)))

    @staticmethod
    def unmaximize(hwnd, x, y, width, height):
        import win32gui
        SW_NORMAL = 1
        win32gui.SetWindowPlacement(hwnd, (0, SW_NORMAL, (-1, -1), (-1, -1), (x, y, x + width, y + height)))


class Darwin(Api):
    @staticmethod
    def get_top_window():
        raise Exception("Abstract method")

    @staticmethod
    def get_desktop():
        size = NSScreen.mainScreen().frame().size
        return 0, 0, size.width, size.height

    @staticmethod
    def get_win_size(hwnd):
        raise Exception("Abstract method")

    @staticmethod
    def set_win_size(hwnd, x, y, width, height):
        raise Exception("Abstract method")

    @staticmethod
    def maximize(hwnd):
        raise Exception("Abstract method")

    @staticmethod
    def unmaximize(hwnd, x, y, width, height):
        raise Exception("Abstract method")

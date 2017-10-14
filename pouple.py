from api import get_api


class Pouple:
    def __init__(self):
        self.api = get_api()
        _, _, self.width, self.height = self.api.get_desktop()

    def align(self, x, y, width, height):
        hwnd = self.api.get_top_window()
        self.api.unmaximize(hwnd, x, y, width, height)
        self.api.set_win_size(hwnd, int(x), int(y), int(width), int(height))

    def align_left(self, proportion=0.5):
        self.align(0, 0, self.width * proportion, self.height)

    def align_right(self, proportion=0.5):
        self.align(self.width * proportion, 0, self.width * proportion, self.height)

    def align_top(self, proportion=0.5):
        self.align(0, 0, self.width, self.height * proportion)

    def align_bottom(self, proportion=0.5):
        self.align(0, self.height * proportion, self.width, self.height * proportion)

    def center(self):
        hwnd = self.api.get_top_window()

        x, y, width, height = self.api.get_win_size(hwnd)
        self.api.unmaximize(hwnd, x, y, width, height)
        x = (self.width - width) // 2
        y = (self.height - height) // 2

        x = x if x > 0 else 0
        y = y if y > 0 else 0

        self.api.set_win_size(hwnd, x, y, width, height)

    def screen(self):
        hwnd = self.api.get_top_window()
        self.api.unmaximize(hwnd, 0, 0, self.width, self.height)
        self.api.set_win_size(hwnd, 0, 0, self.width, self.height)

    def fullscreen(self):
        hwnd = self.api.get_top_window()
        self.api.maximize(hwnd)
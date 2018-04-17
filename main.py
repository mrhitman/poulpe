import keyboard
import configparser
from pouple import Pouple
from history import History
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QAction, QStyle, qApp, QWidget


class MainWindow(QMainWindow):
    tray_icon = None

    def __init__(self):
        QMainWindow.__init__(self)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        self.hide()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        self.pouple = Pouple()
        self.history = History()
        self.bind_keys()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.tray_icon.hide()

    def command(self, cmd):
        def execute():
            print(cmd.__name__)
            self.history.add(cmd)
            cmd()

        return execute

    def bind_keys(self):
        cfg = configparser.RawConfigParser()
        cfg.read('settings.cfg')

        hot_keys = {
            'align_left': self.pouple.align_left,
            'align_right': self.pouple.align_right,
            'align_top': self.pouple.align_top,
            'align_bottom': self.pouple.align_bottom,
            'center': self.pouple.center,
            'screen': self.pouple.screen,
            'fullscreen': self.pouple.fullscreen,
            'undo': self.history.undo,
            'redo': self.history.redo,
        }
        for name in hot_keys:
            keyboard.add_hotkey(cfg.get('keys', name), self.command(hot_keys[name]))


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())

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

    def command(self, cmd):
        def execute():
            print(cmd.__name__)
            self.history.add(cmd)
            cmd()

        return execute

    def bind_keys(self):
        cfg = configparser.RawConfigParser()
        cfg.read('settings.cfg')

        keyboard.add_hotkey(cfg.get('keys', 'align_left'), self.command(self.pouple.align_left))
        keyboard.add_hotkey(cfg.get('keys', 'align_right'), self.command(self.pouple.align_right))
        keyboard.add_hotkey(cfg.get('keys', 'align_top'), self.command(self.pouple.align_top))
        keyboard.add_hotkey(cfg.get('keys', 'align_bottom'), self.command(self.pouple.align_bottom))

        keyboard.add_hotkey(cfg.get('keys', 'center'), self.command(self.pouple.center))
        keyboard.add_hotkey(cfg.get('keys', 'screen'), self.command(self.pouple.screen))
        keyboard.add_hotkey(cfg.get('keys', 'fullscreen'), self.command(self.pouple.fullscreen))


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    mw = MainWindow()

    sys.exit(app.exec_())

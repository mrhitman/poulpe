from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QAction, QStyle, qApp, QWidget


def command(cmd, history):
    history.add(cmd)
    cmd()

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


if __name__ == "__main__":
    import sys
    from history import History
    # import keyboard
    import configparser
    from pouple import Pouple

    pouple = Pouple.create()

    cfg = configparser.RawConfigParser()
    cfg.read('settings.cfg')

    history = History()

    # keyboard.add_hotkey(cfg.get('keys', 'align_left'), lambda: command(pouple.align_left, history))
    # keyboard.add_hotkey(cfg.get('keys', 'align_right'), pouple.align_right)
    # keyboard.add_hotkey(cfg.get('keys', 'align_top'), pouple.align_top)
    # keyboard.add_hotkey(cfg.get('keys', 'align_bottom'), pouple.align_bottom)
    #
    # keyboard.add_hotkey(cfg.get('keys', 'center'), pouple.center)
    # keyboard.add_hotkey(cfg.get('keys', 'screen'), pouple.screen)

    app = QApplication(sys.argv)
    mw = MainWindow()

    sys.exit(app.exec_())
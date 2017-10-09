import time
import keyboard
import configparser
from pouple import Pouple
from history import History


def command(cmd, history):
    history.add(cmd)
    cmd()


if __name__ == '__main__':
    pouple = Pouple.create()

    cfg = configparser.RawConfigParser()
    cfg.read('settings.cfg')

    history = History()

    keyboard.add_hotkey(cfg.get('keys', 'align_left'), lambda: command(pouple.align_left, history))
    keyboard.add_hotkey(cfg.get('keys', 'align_right'), pouple.align_right)
    keyboard.add_hotkey(cfg.get('keys', 'align_top'), pouple.align_top)
    keyboard.add_hotkey(cfg.get('keys', 'align_bottom'), pouple.align_bottom)

    keyboard.add_hotkey(cfg.get('keys', 'center'), pouple.center)
    keyboard.add_hotkey(cfg.get('keys', 'screen'), pouple.screen)

    keyboard.add_hotkey('ctrl+q', pouple.test)

    while True:
        print(len(history.items))
        time.sleep(0.2)

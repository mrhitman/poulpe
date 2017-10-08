import time
import keyboard
import configparser
from pouple import Pouple


if __name__ == '__main__':
    pouple = Pouple.create()
    
    cfg = configparser.RawConfigParser()
    cfg.read('settings.cfg')

    keyboard.add_hotkey(cfg.get('keys', 'align_left'), pouple.alignLeft)
    keyboard.add_hotkey(cfg.get('keys', 'align_right'), pouple.alignRight)
    keyboard.add_hotkey(cfg.get('keys', 'align_top'), pouple.alignTop)
    keyboard.add_hotkey(cfg.get('keys', 'align_bottom'), pouple.alignBottom)

    keyboard.add_hotkey(cfg.get('keys', 'center'), pouple.center)
    keyboard.add_hotkey(cfg.get('keys', 'screen'), pouple.screen)

    keyboard.add_hotkey('ctrl+q', pouple.test)

    while True:
        time.sleep(0.2)

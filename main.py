import time
import keyboard
from pouple import Pouple


if __name__ == '__main__':
    pouple = Pouple.create()

    keyboard.add_hotkey('ctrl+left arrow', pouple.alignLeft)
    keyboard.add_hotkey('ctrl+right arrow', pouple.alignRight)
    keyboard.add_hotkey('ctrl+up arrow', pouple.alignTop)
    keyboard.add_hotkey('ctrl+down arrow', pouple.alignBottom)

    keyboard.add_hotkey('ctrl+alt+f', pouple.center)

    while True:
        time.sleep(0.2)


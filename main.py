import time
import keyboard
import configparser
import pystray
from pouple import Pouple
from history import History
from PIL import Image, ImageDraw

width = height = 64
color1 = 0xffffff
color2 = 0xfcfcfc

image = Image.new('RGB', (width, height), color1)
dc = ImageDraw.Draw(image)
dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
dc.rectangle((0, height // 2, width // 2, height), fill=color2)

icon = pystray.Icon('test name')
icon.image = image

# def setup(icon):
#     icon.visible = True

# icon.run(setup)

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
        time.sleep(0.2)

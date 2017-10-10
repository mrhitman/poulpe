from setuptools import setup

APP = ['poupleapp.py']
DATA_FILES = ['settings.cfg']
OPTIONS = {'argv_emulation': True}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

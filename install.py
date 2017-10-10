import pip

__all__ = [
    "keyboard",
    "configparser",
    "PyQt5"
]

windows = ["pypiwin32"]

linux = ["ewmh"]

darwin = []


def install(packages):
    for package in packages:
        pip.main(['install', package])


if __name__ == '__main__':
    from sys import platform

    install(__all__)
    if platform == 'windows':
        install(windows)
    elif platform.startswith('linux'):
        install(linux)
    elif platform == 'darwin':
        install(darwin)
    else:
        raise Exception("Invalid platform")

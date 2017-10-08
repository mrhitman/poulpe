class History:
    def __init__(self):
        self.items = [];

    def add(self, item):
        self.items.push(item)

    def undo(self):
        pass

    def redo(self):
        pass
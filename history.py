class History:
    MAX_HISTORY = 20

    def __init__(self):
        self.commands = []
        self.undo_commands = []

    def add(self, command):
        if len(self.commands) > History.MAX_HISTORY:
            self.commands.pop(0)
        self.commands.append(command)

    def undo(self):
        if self.commands:
            command = self.commands.pop()
            command()
            self.undo_commands.append(command)

    def redo(self):
        if self.undo_commands:
            command = self.undo_commands.pop()
            command()
            self.commands.append(command)

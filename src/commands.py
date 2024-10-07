class Command:
    def execute(self):
        pass

    def undo(self):
        pass


class MoveImageCommand(Command):
    def __init__(self, image_manager, src, dst):
        self.image_manager = image_manager
        self.src = src
        self.dst = dst

    def execute(self):
        self.image_manager.move_image(self.src, self.dst)

    def undo(self):
        self.image_manager.move_image(self.dst, self.src)


# In ImageSorter class
self.command_history = []


def execute_command(self, command):
    command.execute()
    self.command_history.append(command)


def undo_last_command(self):
    if self.command_history:
        command = self.command_history.pop()
        command.undo()

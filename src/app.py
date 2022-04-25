"""Module for handling....handlers....probably...not sure yet. Definitely main entry point though"""

import os

import base_classes
import CLI
import core


# Remember: Receiver -> Command -> Invoker -> Client
# This could easily be a 'main' function. A class allows for namespacing, holding state(settings), and the coupling
# of logic to the aforementioned state. Consider if this is the best solution later. Right now main is acting as app.
class App:
    """I'll move this to app.py at some point. Easier to work on all my new classes in once place for now."""
    cmd_handler: base_classes.CommandSetHandler
    interface_handler: base_classes.InterfaceHandler

    # I could set default handler state here?
    def __init__(self, command_handler, interface_handler):
        self.command_handler = command_handler
        self.interface_handler = interface_handler

    @staticmethod
    def clean_up() -> None:
        files_in_directory = os.listdir('.')
        csv_files = [file for file in files_in_directory if file.endswith('csv')]
        for file in csv_files:
            os.remove(file)

    def run(self) -> None:
        self.interface_handler.run()


if __name__ == '__main__':
    core = core.CoreEngine()
    cmd_handler = base_classes.CommandSetHandler(CLI.CommandSet(core))
    _interface_handler = base_classes.InterfaceHandler(CLI.Interface(cmd_handler))

    app = App(interface_handler=_interface_handler, command_handler=cmd_handler)
    app.run()
    # Initialize Handlers w/ chosen interface and command set
    # run via app -> interface handler -> interface
    # Command set is responsible for handling commands.
    # I can change command sets on the fly via handler

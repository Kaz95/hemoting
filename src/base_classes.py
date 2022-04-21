"""Module for holding ABCs until I clean up core module"""
import pprint
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
import os


@dataclass
class Command:
    receiver: Callable
    args: list = field(default_factory=list)

    def execute(self):
        if self.args:
            self.receiver(self.args)
        else:
            self.receiver()


@dataclass
class CommandInfo:
    receiver: Callable
    description: str
    aliases: list[str]


class CommandSet(ABC):
    def __init__(self):
        self.command_info_registry = {}
        self._register_commands()

    @abstractmethod
    def get_receiver_info(self, cmd):
        pass

    @abstractmethod
    def register_command(self, receiver: Callable, description: str, aliases: list[str]):
        pass

    @abstractmethod
    def _register_commands(self):
        pass

    @abstractmethod
    def list_commands(self):
        pass


class CommandSetHandler:
    def __init__(self, command_set: CommandSet):
        self.command_set = command_set
        https: // w2.gomovies.fan / watch - series / watch - archer - season - 4 - full - episodes - online - free / gomovies - 5l
        rp4pq - y65xako75z?watching = 2
        # This will not map to a GUI well. I WILL want an 'ls' command of some sort that returns the command registry
        # for the purposes of displaying some sort of key binds list in the GUI...Interface...I just realized I'm saying
        # ATM Machine.....fuck.
        # Wait.....actually....
        # If I implement the underlying CommandSet.print_all method correctly for the GUI.CommandSet class, I can leave
        # this as is.
        #   - I'll still want to use the handler to trigger the concrete implementation of the method.
        #   - I'll still want a description of what the command is doing.
        #   - I'll still want a list of aliases(KeyEvents and what not in GUI case) so I can build the commands registry
        # So pretty much everything can be used in place. The handler don't give two shits. I'll need some way of what
        # aliases to pass in. I could pass them all in all the time(CLI & GUI) or I need to move this somewhere else...
        # maybe...probably...
        self.command_set.register_command(self.ls, "Lists all current commands in the current command set.",
                                          ['ls', 'list'])

    def _split_input(self, user_input):
        split_input = user_input.split()
        match split_input:
            case [user_cmd, *args]:
                receiver_info = self.command_set.get_receiver_info(user_cmd)
                receiver = receiver_info.receiver
                command = Command(receiver, args)
                return command
            case [user_cmd]:
                receiver_info = self.command_set.get_receiver_info(user_cmd)
                receiver = receiver_info.receiver
                command = Command(receiver)
                return command
            case _:
                print('invalid input')

    # This feels like the invoker. To, more closely, follow the command pattern, I should split this method into two
    # parts: 'create_command_from_user_input' and 'invoke'
    def handle_command(self, user_input):
        command = self._split_input(user_input)
        command.execute()

    def ls(self, option=None):
        if option:
            option = option[0]
            self.ls_option(option)
        else:
            self.command_set.list_commands()

    def ls_option(self, option):
        cmd = self.command_set.command_info_registry[option]
        print(f'Command: {option}')
        print(f'Description: {cmd.description}')
        print(f'Aliases: {cmd.aliases}')


class Interface(ABC):
    command_handler: CommandSetHandler

    def __init__(self, command_handler):
        self.command_handler = command_handler

    @abstractmethod
    def run(self):
        pass


class InterfaceHandler:
    interface: Interface

    def __init__(self, interface):
        self.interface = interface

    def run(self):
        self.interface.run()


# This could easily be a 'main' function. A class allows for namespacing, holding state(settings), and the coupling
# of logic to the aforementioned state. Consider if this is the best solution later. Right now main is acting as app.
class App:
    cmd_handler: CommandSetHandler
    interface_handler: InterfaceHandler

    # I could set default handler state here?
    def __init__(self, cmd_handler, interface_handler):
        self.cmd_handler = cmd_handler
        self.interface_handler = interface_handler

    @staticmethod
    def clean_up():
        files_in_directory = os.listdir('.')
        csv_files = [file for file in files_in_directory if file.endswith('csv')]
        for file in csv_files:
            os.remove(file)

    def run(self):
        self.interface_handler.run()


if __name__ == '__main__':
    App.clean_up()

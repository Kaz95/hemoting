"""Classes used to create command sets and user interfaces.

The classes defined in this module are used to build unique command sets and user interfaces bound to those commands.
A module implementing a front-end(GUI, CLI, ect) must include

This module will make more sense when core functionality is decoupled from front-end implementations. This module will
essentially be the core of the program 'Hemoting Desktop', which will be built using 'Hemoting Core' the package.

Example:
    A module implementing a user interface must include:
        * At least one Receiver class that inherits from the Receiver ABC defined in this module.
        * At least one CommandSet class that inherits from the CommandSet ABC defined in this module.
        * At least one Interface class that inherits from the Interface ABC defined in this module.

    CommandSetHandler and InterfaceHandler are used to handle concrete implementations of the base classes defined in
    this module.

TODO:
    * Finish adding docstrings.
    * Look for more things to do.
"""

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field

from src import core


@dataclass
class Command:
    receiver: Callable
    args: list = field(default_factory=list)

    def execute(self) -> None:
        if self.args:
            self.receiver(self.args)
        else:
            self.receiver()


@dataclass
class CommandInfo:
    receiver: Callable
    description: str
    aliases: list[str]


# This classes only purpose is to provide a namespace and to define a set of commands any interface or command set
# should include.
class Receivers(ABC):
    core_engine: core.CoreEngine

    def __init__(self, core_engine):
        self.core_engine = core_engine

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def update_setting(self):
        pass

    @abstractmethod
    def reset_settings(self):
        pass

    @abstractmethod
    def add_bepisode(self):
        pass

    @abstractmethod
    def remove_bepisode(self):
        pass


class CommandSet(ABC):
    core: core.CoreEngine
    receivers: Receivers

    def __init__(self, core_engine):
        self.core_engine = core_engine
        self.receivers = self._bind_core_to_receivers()
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

    @abstractmethod
    def _bind_core_to_receivers(self):
        pass


class CommandSetHandler:
    command_set: CommandSet

    def __init__(self, command_set):
        self.command_set = command_set
        self.command_set.register_command(self._ls, "Lists all commands in the current command set.",
                                          ['ls', 'list'])

    def _split_input(self, user_input) -> Command:
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
    # parts: 'create_command_from_user_input' and 'invoke'. Which actually makes no sense when you aren't forced into
    # object orientation every step of the way.
    def handle_command(self, user_input) -> None:
        command = self._split_input(user_input)
        command.execute()

    def _ls(self, args=None) -> None:
        match args:
            case [user_cmd_argument]:
                self._ls_command_info(user_cmd_argument)
            case None:
                self.command_set.list_commands()
            case _:
                print(f"Invalid Command. Expected 1 argument, got {len(args)} instead")

    def _ls_command_info(self, cmd) -> None:
        cmd_info = self.command_set.command_info_registry[cmd]
        print(f'Command: {cmd}')
        print(f'Description: {cmd_info.description}')
        print(f'Aliases: {cmd_info.aliases}')


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

"""Module for encapsulating command creation, registration, and invocation"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from collections.abc import Callable


@dataclass
class Command:
    receiver: Callable
    description: str
    aliases: list[str]


class CommandSet(ABC):

    def __init__(self):
        self.commands = {}
        self._register_base_commands()

    @abstractmethod
    def get_receiver(self, cmd):
        pass

    @abstractmethod
    def register_command(self, func: Callable, description: str, aliases: list[str]):
        pass

    @abstractmethod
    def _register_base_commands(self):
        pass

    @abstractmethod
    def list_commands(self):
        pass


class CLI(CommandSet):
    def get_receiver(self, cmd):
        pass

    def register_command(self, func: Callable, description: str, aliases: list[str]):
        pass

    def _register_base_commands(self):
        pass

    def list_commands(self):
        pass


class GUI(CommandSet):
    def get_receiver(self, cmd):
        pass

    def register_command(self, func: Callable, description: str, aliases: list[str]):
        pass

    def _register_base_commands(self):
        pass

    def list_commands(self):
        pass


class CommandHandler:
    def __init__(self, command_set: CommandSet):
        self.command_set = command_set

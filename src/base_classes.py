"""Module for holding ABCs until I clean up core module"""

from abc import ABC, abstractmethod
from collections.abc import Callable


class CommandSet(ABC):
    def __init__(self):
        self.commands = {}
        self._register_commands()

    @abstractmethod
    def get_receiver(self, cmd):
        pass

    @abstractmethod
    def register_command(self, func: Callable, description: str, aliases: list[str]):
        pass

    @abstractmethod
    def _register_commands(self):
        pass

    @abstractmethod
    def list_commands(self):
        pass


class Interface(ABC):

    @abstractmethod
    def run(self):
        pass

"""Module for holding ABCs until I clean up core module"""
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Optional


@dataclass
class Command:
    receiver: Callable
    args: list = field(default_factory=list)


@dataclass
class CommandInfo:
    receiver: Callable
    number_of_args: int
    description: str
    aliases: list[str]

    def __str__(self):
        return f'{self.description}\n{self.aliases}'


class CommandSet(ABC):
    def __init__(self):
        self.command_info_registry = {}
        self._register_commands()

    @abstractmethod
    def get_receiver_info(self, cmd):
        pass

    @abstractmethod
    def register_command(self, receiver: Callable, number_of_args: int, description: str, aliases: list[str]):
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

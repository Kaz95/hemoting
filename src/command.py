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
    pass


class CLI(CommandSet):
    pass


class GUI(CommandSet):
    pass


class CommandHandler:
    pass

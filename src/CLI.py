"""Module for implementing all things CLI"""
import base_classes
from collections.abc import Callable


class Interface(base_classes.Interface):
    def run(self):
        pass


class CommandSet(base_classes.CommandSet):
    def get_receiver(self, cmd):
        pass

    def register_command(self, func: Callable, description: str, aliases: list[str]):
        pass

    def _register_commands(self):
        pass

    def list_commands(self):
        pass

"""Module for implementing all things GUI"""
import base_classes
from collections.abc import Callable


class Interface(base_classes.Interface):
    def run(self):
        raise NotImplementedError('Soon™')


class CommandSet(base_classes.CommandSet):
    def get_receiver_info(self, cmd):
        raise NotImplementedError('Soon™')

    def register_command(self, receiver: Callable, description: str, aliases: list[str]):
        raise NotImplementedError('Soon™')

    def _register_commands(self):
        raise NotImplementedError('Soon™')

    def list_commands(self):
        raise NotImplementedError('Soon™')

    def bind_core_to_receivers(self):
        raise NotImplementedError('Soon™')

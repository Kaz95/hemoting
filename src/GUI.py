"""Module for implementing all things GUI"""

import base_classes
from collections.abc import Callable


class Interface(base_classes.Interface):
    def run(self):
        raise NotImplementedError('Soon™')


class CommandSet(base_classes.CommandSet):
    def get_receiver_info(self, cmd):
        pass

    def register_command(self, receiver: Callable, description: str, aliases: list[str]):
        pass

    def _register_commands(self):
        pass

    def list_commands(self):
        pass

    def _bind_core_to_receivers(self):
        pass

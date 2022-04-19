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


# import pprint
# from abc import ABC, abstractmethod
# from dataclasses import dataclass
# from collections.abc import Callable
#
#
# def run(args):
#     print(f'I ran with args: {args}')
#
#
# def reset(args):
#     print(f'I reset with args: {args}')
#
#
# def update(args):
#     print(f'I updated with args: {args}')
#
#
# @dataclass
# class Command:
#     receiver: Callable
#     description: str
#     aliases: list[str]
#
#
# class CommandSet(ABC):
#
#     def __init__(self):
#         self.commands = {}
#         self._register_commands()
#
#     @abstractmethod
#     def get_receiver(self, cmd):
#         pass
#
#     @abstractmethod
#     def register_command(self, func: Callable, description: str, aliases: list[str]):
#         pass
#
#     @abstractmethod
#     def _register_commands(self):
#         pass
#
#     @abstractmethod
#     def list_commands(self):
#         pass
#
#
# class CLICommands(CommandSet):
#
#     def get_receiver(self, cmd):
#         return self.commands[cmd].receiver
#
#     def register_command(self, func: Callable, description: str, aliases: list[str]):
#         cmd = Command(func, description, aliases)
#         for alias in cmd.aliases:
#             self.commands[alias] = cmd
#
#     def _register_commands(self):
#         self.register_command(run, "Runs program", ['run', 'go', 'execute'])
#         self.register_command(reset, "Resets program", ['reset', 'defaults'])
#         self.register_command(update, "Updates program", ['update'])
#
#     def list_commands(self):
#         pprint.pprint(self.commands)
#
#
# class GUICommands(CommandSet):
#
#     def get_receiver(self, cmd):
#         pass
#
#     def register_command(self, func: Callable, description: str, aliases: list[str]):
#         pass
#
#     def _register_commands(self):
#         pass
#
#     def list_commands(self):
#         pass
#
#
# class CommandHandler:
#
#     def __init__(self, command_set: CommandSet):
#         self.command_set = command_set
#         self.command_set.register_command(self.ls, "Lists all current commands in the current command set.",
#                                           ['ls', 'list'])
#
#     @staticmethod
#     def _split_input(user_input):
#         split_input = user_input.split()
#         match split_input:
#             case [cmd, *args]:
#                 return [cmd, args]
#             case _:
#                 print('invalid input')
#
#     def handle_command(self, user_input):
#         cmd, args = CommandHandler._split_input(user_input)
#         receiver = self.command_set.get_receiver(cmd)
#         receiver(args)
#
#     def ls(self, option=None):
#         if option:
#             option = option[0]
#             self.ls_option(option)
#         else:
#             self.command_set.list_commands()
#
#     def ls_option(self, option):
#         cmd = self.command_set.commands[option]
#         print(f'Command: {option}')
#         print(f'Description: {cmd.description}')
#         print(f'Aliases: {cmd.aliases}')
#
#
# if __name__ == '__main__':
#     cmd_set = CLICommands()
#     cmd_handler = CommandHandler(cmd_set)
#     u_input = 'ls go'
#     cmd_handler.handle_command(u_input)
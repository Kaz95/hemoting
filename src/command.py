"""Module for encapsulating command creation, registration, and invocation"""
import core
import pprint
import settings

from interface import DEFAULT_DATE
from abc import ABC, abstractmethod
from dataclasses import dataclass
from collections.abc import Callable


# Some core functions, that will be refactored and moved at some point. They were created to encapsulate all of the code
# needed to perform a user inputted command.
def run(args, **kwargs):
    log = core.generate_log(settings_handler=kwargs['setting_handler'], starting_date=args[0], manual_bepisodes=[])
    core.print_log(log)
    core.output_log_to_csv(log)


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
        return self.commands[cmd].receiver

    def register_command(self, func: Callable, description: str, aliases: list[str]):
        cmd = Command(func, description, aliases)
        for alias in cmd.aliases:
            self.commands[alias] = cmd

    def _register_base_commands(self):
        self.register_command(run, 'Runs main program with defaults', ['run', 'go', 'execute'])

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

    @staticmethod
    def _split_input(user_input):
        split_input = user_input.split()
        match split_input:
            case [cmd, *args]:
                return [cmd, args]
            case _:
                print('invalid input')

    def handle_command(self, user_input, settings_handler):
        cmd, args = CommandHandler._split_input(user_input)
        receiver = self.command_set.get_receiver(cmd)
        receiver(args)

    def ls(self, option=None):
        if option:
            option = option[0]
            self.ls_option(option)
        else:
            self.command_set.list_commands()

    def ls_option(self, option):
        cmd = self.command_set.commands[option]
        print(f'Command: {option}')
        print(f'Description: {cmd.description}')
        print(f'Aliases: {cmd.aliases}')


def run_cli(settings_handler):
    cmd_set = CLI()
    cmd_handler = CommandHandler(cmd_set)
    while True:
        user_input = input('$ ')
        cmd_handler.handle_command(user_input, settings_handler)


def argu(arg: list[str], **kwargs):
    return f'Arg: {arg} and {kwargs}'


if __name__ == '__main__':
    # settings_h = settings.initialize_settings()
    # run_cli(settings_h)
    print(argu(['1', 2, 3], some_shit='ok', some_other_shit='bud'))

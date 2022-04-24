"""Module for holding ABCs until I clean up core module"""
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
import os

from src import core


@dataclass
class Command:
    receiver: Callable
    args: list = field(default_factory=list)

    def execute(self):
        if self.args:
            self.receiver(self.args)
        else:
            self.receiver()


@dataclass
class CommandInfo:
    receiver: Callable
    description: str
    aliases: list[str]


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
        # This will not map to a GUI well. I WILL want an 'ls' command of some sort that returns the command registry
        # for the purposes of displaying some sort of key binds list in the GUI...Interface...I just realized I'm saying
        # ATM Machine.....fuck.
        # Wait.....actually....
        # If I implement the underlying CommandSet.print_all method correctly for the GUI.CommandSet class, I can leave
        # this as is.
        #   - I'll still want to use the handler to trigger the concrete implementation of the method.
        #   - I'll still want a description of what the command is doing.
        #   - I'll still want a list of aliases(KeyEvents and what not in GUI case) so I can build the commands registry
        # So pretty much everything can be used in place. The handler don't give two shits. I'll need some way of what
        # aliases to pass in. I could pass them all in all the time(CLI & GUI) or I need to move this somewhere else...
        # maybe...probably...
        self.command_set.register_command(self.ls, "Lists all commands in the current command set.",
                                          ['ls', 'list'])

    def _split_input(self, user_input):
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
    def handle_command(self, user_input):
        command = self._split_input(user_input)
        command.execute()

    def ls(self, args=None):
        match args:
            case [user_cmd_argument]:
                self._ls_command_info(user_cmd_argument)
            case None:
                self.command_set.list_commands()
            case _:
                print(f"Invalid Command. Expected 1 argument, got {len(args)} instead")
        # if args:
        #     option = args[0]
        #     self.ls_command_info(option)
        # else:
        #     self.command_set.list_commands()

    def _ls_command_info(self, cmd):
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

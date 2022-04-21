"""Module for implementing all things CLI"""
import pprint
from collections.abc import Callable

import base_classes
import core
import settings


# A few test receiver functions. Receivers being a function that encapsulates all the logic needed to carry out
# a command requested by the user.

def _serialize_date_input(u_input: str):
    match u_input.split('-'):
        case [year, month, day]:
            year = int(year)
            month = int(month)
            day = int(day)
            starting_date = core.Date(year, month, day)
            return starting_date


def run(args=None):
    match args:
        case [user_date_input]:
            starting_date = _serialize_date_input(user_date_input)
        case _:
            starting_date = core.Date(2022, 2, 2)

    # if args:
    #     starting_date = _serialize_date_input(args[0])
    # else:
    #     starting_date = core.Date(2022, 2, 2)

    setting_handler = settings.initialize_settings()
    manual_bepisodes = []
    log = core.generate_log(setting_handler, starting_date, manual_bepisodes)
    core.print_log(log)
    core.output_log_to_csv(log)


class CommandSet(base_classes.CommandSet):

    def register_command(self, receiver: Callable, description: str, aliases: list[str]):
        cmd_info = base_classes.CommandInfo(receiver, description, aliases)
        for alias in cmd_info.aliases:
            self.command_info_registry[alias] = cmd_info

    def _register_commands(self):
        self.register_command(run, "runs program, vrooooooom", ['run', 'go', 'execute'])
        self.register_command(base_classes.App.clean_up, 'Deletes all csv files in current directory(src)',
                              ['d', 'D', 'delete', 'cleanup'])

    def get_receiver_info(self, cmd):
        return self.command_info_registry[cmd]

    def list_commands(self):
        pprint.pprint(self.command_info_registry)


class Interface(base_classes.Interface):

    def run(self):
        while True:
            user_input = input('$ ')
            match user_input:
                case 'q' | 'Q':
                    print('Quitting...')
                    break
                case _:
                    self.command_handler.handle_command(user_input)

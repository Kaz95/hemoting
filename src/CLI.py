"""Module for implementing all things CLI"""
import pprint
from collections.abc import Callable

import base_classes
import core
import settings


# A few test receiver functions. Receivers being a function that encapsulates all the logic needed to carry out
# a command requested by the user.

def _serialize_date_input(u_input: list):
    dates = []
    for arg in u_input:
        match arg.split('-'):
            case [year, month, day]:
                year = int(year)
                month = int(month)
                day = int(day)
                starting_date = core.Date(year, month, day)
                dates.append(starting_date)
    return dates


def run(starting_date: core.Date | list = core.Date(2022, 2, 2)):
    # There has to be a better way to decide how the function was called. I'm using input type to allow this function
    # to run with a default value when no arg is passed, and to operate on the argument, if there is one. Maybe I should
    # accept only args, and if args, overload the default values with args?
    if isinstance(starting_date, list):
        dates = _serialize_date_input(starting_date)
        starting_date = dates[0]

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
            self.command_handler.handle_command(user_input)

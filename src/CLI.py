"""Module for implementing all things CLI"""
import pprint
from collections.abc import Callable

import base_classes
import core
import settings


# A few test receiver functions. Receivers being a function that encapsulates all the logic needed to carry out
# a command requested by the user.

def serialize_date_input(u_input: list):
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
    if isinstance(starting_date, list):
        dates = serialize_date_input(starting_date)
        starting_date = dates[0]

    setting_handler = settings.initialize_settings()
    manual_bepisodes = []
    log = core.generate_log(setting_handler, starting_date, manual_bepisodes)
    core.print_log(log)
    core.output_log_to_csv(log)


class Interface(base_classes.Interface):
    def run(self):
        while True:
            user_input = input('$ ')
            return user_input  # TODO: handler user input here instead of printing


class CommandSet(base_classes.CommandSet):

    def register_command(self, receiver: Callable, number_of_args: int, description: str, aliases: list[str]):
        cmd_info = base_classes.CommandInfo(receiver, number_of_args, description, aliases)
        for alias in cmd_info.aliases:
            self.command_info_registry[alias] = cmd_info

    def _register_commands(self):
        self.register_command(run, 1, "runs program, vrooooooom", ['run', 'go', 'execute'])

    def get_receiver_info(self, cmd):
        return self.command_info_registry[cmd]

    def list_commands(self):
        pprint.pprint(self.command_info_registry)

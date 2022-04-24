"""Module for implementing all things CLI"""
import pprint
from collections.abc import Callable

import base_classes
import core


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


def _print_log(log: list[core.Date]) -> None:
    for date in log:
        if date.bleeds_list:
            print(f'{date} - {date.infused} - {date.bleeds_list}')
        else:
            print(f'{date} - {date.infused} - Prophey')


class Receivers(base_classes.Receivers):

    def run(self, args=None):
        match args:
            case [user_date_input]:
                starting_date = _serialize_date_input(user_date_input)
            case _:
                starting_date = core.Date(2022, 2, 2)

        self.core_engine.logger.starting_date = starting_date
        self.core_engine.logger.generate_log()

        _print_log(self.core_engine.logger.log)
        # self.core_engine.logger.print_log()
        self.core_engine.logger.output_log_to_csv()

    def update_setting(self):
        raise NotImplementedError('Soon™')

    def reset_settings(self):
        raise NotImplementedError('Soon™')

    def add_bepisode(self):
        raise NotImplementedError('Soon™')

    def remove_bepisode(self):
        raise NotImplementedError('Soon™')


class CommandSet(base_classes.CommandSet):

    def register_command(self, receiver: Callable, description: str, aliases: list[str]):
        cmd_info = base_classes.CommandInfo(receiver, description, aliases)
        for alias in cmd_info.aliases:
            self.command_info_registry[alias] = cmd_info

    def _register_commands(self):
        self.register_command(self.receivers.run, "runs program, vrooooooom", ['run', 'go', 'execute'])
        self.register_command(base_classes.App.clean_up, 'Deletes all csv files in current directory(src)',
                              ['d', 'D', 'delete', 'cleanup'])

    def get_receiver_info(self, cmd):
        return self.command_info_registry[cmd]

    def list_commands(self):
        pprint.pprint(self.command_info_registry)

    def _bind_core_to_receivers(self):
        return Receivers(self.core)


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



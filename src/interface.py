"""Module for implementing CLI and GUI"""
import pprint

import core
import settings

DEFAULT_DATE = core.Date(2022, 2, 2)
""" 
    Some thoughts on how the CLI will be implemented. First, the following structure will be used for commands:
    
    COMMAND <arguments>
    
    This will be the structure going forward. I may choose to add options or 'modes' later on. Command will correspond
    to a string value in 'commands' dictionary. All available commands will be 'registered' in this dictionary. 
    
    commands = {}
    
    At the moment I plan to add the following values in a 'command details' object...maybe a dataclass or something.
    
    - Receiver, or function that encapsulates all of the logic needed to carry out a given user command
    - Command aliases, Ex: 'run' | 'go' | 'do the thing'
    - Command description
    
    I will also need an 'invoker' function that will look something like:

    def invoker(receiver, args):
        receiver(*args)
    
    I will bind the original user input via match case like:
    
    match user_input.split():
        case [cmd, *params] if cmd in commands_and_aliases:  # Where commands_and_aliases is a list...of what it says.
            # Do a bunch of work here
        case _:
            print('Invalid command brother!)   
    
    Then I guess I'd use a helper function to decide to correct function to use. Maybe like:
    
    def get_receiver(cmd)
        return commands[cmd]
        
    Then, I need a client to tie it all together:
    
    def client(cmd, args, invoker):
        receiver = get_receiver(cmd)
        invoker(receiver, *(?)args)
        
    Hokay, so the flow of the execution will look something like:
    
    0.) Commands objects must be initialized and registered into 'commands' dictionary. I could har code them, but I
        feel this approach is better. It allows be encapsulate a default set of commands, without hard coding multiple
        dictionaries. Instead I create some factory(?) functions that build a known set of commands at runtime.
    1.) User inputs command. This will hereby be referred to as: user_input
    2.) user_input is validated and bound to variables by a split() call and a match case. 
            a.) If command is expected format, variables now available: cmd: str, params: list 
            b.) If command is invalid format, continue back to start of loop to get new user_input.
    3.) Pass cmd and args into client function to perform the actual command. Optionally I can provide an invoker 
        argument that can decide behavior surrounding a function call. Things like book keeping and modes.
    4.) Something like that.
    """


def parse_setting_command(setting: str, settings_handler: settings.SettingsHandler, value: str):
    match setting:
        case 'number_of_bleeds':
            settings_handler.number_of_bleeds = int(value)
        case 'time_stamp_range':
            # TODO: I might need to handle range validation here. Not sure atm.
            match value.split('-'):
                case [start, stop]:
                    settings_handler.time_stamp_range['min'] = int(start)
                    settings_handler.time_stamp_range['max'] = int(stop)
                case _:
                    print(f"Value: {value!r} is not the correct format. Expected 2 digits separated by a '-'")

        case 'schedules':
            match value.split('-'):
                case [main, alternate]:
                    main = [int(x) for x in main if x.isdigit()]
                    alternate = [int(x) for x in alternate if x.isdigit()]
                    settings_handler.schedules['normal'] = main
                    settings_handler.schedules['alternate'] = alternate
                case _:
                    print(f"Value: {value!r} is not the correct format. Expected 2 sets of 3 digits separated by a '-'")

        case 'bleed_duration_range':
            match value.split('-'):
                case [start, stop]:
                    settings_handler.bleed_duration_range['min'] = int(start)
                    settings_handler.bleed_duration_range['max'] = int(stop)
                case _:
                    print(f"Value: {value!r} is not the correct format. Expected 2 digits separated by a '-'")

        case _:
            print(f'Setting: {setting!r} not recognized')


def parse_list_command(value: str, bepisodes: list, settings_handler: settings.SettingsHandler):
    match value:
        case "bepisodes":
            for index, bepisode in enumerate(bepisodes):
                print(f'{index + 1}.) {bepisode}')
        case "settings":
            pprint.pprint(settings_handler.__dict__)


def run_cli(settings_handler: settings.SettingsHandler):
    manual_bepisodes = []
    while True:
        command = input('$ ')
        match command.split():
            case ['quit' | 'q' | 'Q']:  # Brackets are needed to specify sequence, could also be () or a single ,
                print('quitting...')
                break

            case ['run' | 'go']:
                starting_date = DEFAULT_DATE
                log = core.generate_log(settings_handler, starting_date, manual_bepisodes)
                core.print_log(log)
                core.output_log_to_csv(log)

            case ['reset']:
                settings.reset_settings(settings_handler)

            case ['update', setting, value]:
                parse_setting_command(setting, settings_handler, value)

            case ['add']:
                manual_bepisodes += core.get_manual_bleeds()

            case ['remove', bepisode]:
                """Case for removing a manual bepisode"""
                # TODO: This will need some way of viewing current manual bepisodes
                #  and then some way of uniquely identifying them so one can be chosen for deletion.
                #  That can be done here or in its own case.

            case ['list', option]:
                parse_list_command(option, manual_bepisodes, settings_handler)
                pass

            case ['list']:
                """Case for listing all commands"""
                pass

            case _:
                print(f'Command {command!r} not found')  # !r flag is used to give output quotes around command.

"""Module for implementing CLI and GUI"""
import core
import settings

DEFAULT_DATE = core.Date(2022, 2, 2)


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
                pass
            case ['add', bepisode]:
                """Case for adding manual bepisode"""
                pass
            case ['remove', bepisode]:
                """Case for removing a manual bepisode"""
                # TODO: This will need some way of viewing current manual bepisodes
                #  and then some way of uniquely identifying them so one can be chosen for deletion.
                #  That can be done here or in its own case.
            case ['list', option]:
                """
                   ~ Case for listing specific information. This could include, but is not limited to:
                   - Current bepisodes
                   - All current settings
                   - A specific settings current value
                   - ect.....
                """
                pass
            case ['list']:
                """Case for listing all commands"""
                pass
            case _:
                print(f'Command {command!r} not found')  # !r flag is used to give output quotes around command.

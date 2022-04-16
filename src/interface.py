"""Module for implementing CLI and GUI"""
import core
import settings

DEFAULT_DATE = core.Date(2022, 2, 2)


def parse_setting_command(setting: str, setting_handler: settings.SettingsHandler, value: str):
    match setting:
        case 'number_of_bleeds':
            setting_handler.number_of_bleeds = value
        case 'time_stamp_range':
            # TODO: I might need to handle range validation here. Not sure atm.
            """Split -> turn to tuple -> set value """
        case 'schedules':
            """Split -> turn to two tuples? -> set values"""
            pass
        case 'bleed_duration_range':
            """Split -> turn to dict -> set values"""
            pass
        case 'bleed_locations':
            """Split -> turn to tuple -> set value"""
            pass
        case _:
            print(f'Setting: {setting!r} not recognized')


def run_cli(setting_handler: settings.SettingsHandler):
    while True:
        command = input('$ ')
        match command.split():
            case ['quit' | 'q' | 'Q']:  # Brackets are needed to specify sequence, could also be () or a single ,
                print('quitting...')
                break
            case ['run' | 'go']:
                starting_date, manual_bepisodes = DEFAULT_DATE, []
                log = core.generate_log(setting_handler, starting_date, manual_bepisodes)
                core.print_log(log)
                core.output_log_to_csv(log)
            case ['reset']:
                """Case for resetting settings to defaults"""
                settings.reset_settings()
            case ['update', setting, value]:
                """Case for updating a given setting"""
                parse_setting_command(setting, setting_handler, value)
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

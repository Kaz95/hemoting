"""Module for implementing CLI and GUI"""
import core
import settings

DEFAULT_DATE = core.Date(2022, 2, 2)


def run_cli(setting_handler: core.ScheduleHandler):
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
                pass
            case ['add', bepisode]:
                """Case for adding manual bepisode"""
                pass
            case ['remove', bepisode]:
                """Case for removing a manual bepisode"""
                # TODO: This will need some way of viewing current manual bepisodes
                #  and then some way of uniquely identifying them so one can be chosen for deletion.
                #  That can be done here or in its own case.
            case ['list']:
                """Case for listing all commands"""
                pass
            case _:
                print(f'Command {command!r} not found')  # !r flag is used to give output quotes around command.

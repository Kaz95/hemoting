"""Module for implementing CLI and GUI"""
import core
import settings

DEFAULT_DATE = core.Date(2022, 2, 2)


def run_cli():
    setting_handler = settings.initialize_settings()
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
            case _:
                print(f'Command {command!r} not found')  # !r flag is used to give output quotes around command.

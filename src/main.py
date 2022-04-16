import interface
import settings

if __name__ == '__main__':
    setting_handler = settings.initialize_settings()
    interface.run_cli(setting_handler)
    settings.save_settings(setting_handler)  # TODO: Settings will not be saved correctly if program exits early.

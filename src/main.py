import interface
import settings

if __name__ == '__main__':
    setting_handler = settings.initialize_settings()
    interface.run_cli(setting_handler)

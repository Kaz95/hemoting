import json
from dataclasses import dataclass

# TODO: Remember JSON doesn't know or care w/e a tuple is. That's on me.


@dataclass
class Settings:
    number_of_bleeds: int
    time_stamp_range: dict
    schedules: dict


normal_prophey_schedule = (0, 2, 4)
alternate_prophey_schedule = (1, 3, 5)

settings_schema = {'number_of_bleeds': 3,
                   'time_stamp_range': {'min': 7, 'max': 10},
                   'schedules':
                       {'normal': normal_prophey_schedule,
                        'alternate': alternate_prophey_schedule,
                        'current': normal_prophey_schedule
                        }
                   }


def create_settings_json():
    try:
        open("settings.json", 'x')
    except FileExistsError:
        print('Settings already exists!')
    else:
        with open("settings.json", 'w') as json_file:
            json.dump(settings_schema, json_file)


def load_settings():
    try:
        with open("settings.json", 'r') as json_file:
            settings_dictionary = json.load(json_file)
            return settings_dictionary
    except FileNotFoundError:
        print('There\'s no settings yet bud...')
        raise


def save_settings(updated_settings: Settings) -> None:
    settings_dict = updated_settings.__dict__
    with open("settings.json", 'w') as json_file:
        json.dump(settings_dict, json_file)


def make_settings_object(settings_dict):
    settings_obj = Settings(**settings_dict)
    return settings_obj


def initialize_settings():
    try:
        settings_dict = load_settings()
    except FileNotFoundError:
        print('creating default JSON')
        create_settings_json()
        settings_dict = load_settings()

    settings_obj = make_settings_object(settings_dict)
    return settings_obj



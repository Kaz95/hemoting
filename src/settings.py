import json
from collections.abc import Sequence
from dataclasses import dataclass


# TODO: Remember JSON doesn't know or care w/e a tuple is. That's on me.


class __SettingsHandler:
    number_of_bleeds: int
    time_stamp_range: dict
    schedules: dict
    bleed_duration_range: dict
    bleed_locations: Sequence

    def __init__(self, number_of_bleeds, time_stamp_range, schedules, bleed_duration_range, bleed_locations):
        self.number_of_bleeds = number_of_bleeds
        self.time_stamp_range = time_stamp_range
        self.schedules = schedules
        self.bleed_duration_range = bleed_duration_range
        self.bleed_locations = bleed_locations

    # Used to randomize bleed location. Nothing else.
    bleed_locations = ('Elbow', 'Knee', 'Ankle', 'Hip', 'Shoulder', 'Wrist', 'Quadriceps', 'Calf', 'Biceps', 'Triceps')

    normal_prophey_schedule = (0, 2, 4)
    alternate_prophey_schedule = (1, 3, 5)

    default_settings = {'number_of_bleeds': 3,
                        'time_stamp_range': {'min': 7, 'max': 10},
                        'schedules': {'normal': normal_prophey_schedule, 'alternate': alternate_prophey_schedule},
                        'bleed_duration_range': {'min': 1, 'max': 4},
                        'bleed_locations': bleed_locations}

    @classmethod
    def create_settings_json(cls):
        try:
            open("settings.json", 'x')
        except FileExistsError:
            print('Settings already exists!')
        else:
            with open("settings.json", 'w') as json_file:
                json.dump(cls.default_settings, json_file)

    @staticmethod
    def load_settings():
        try:
            with open("settings.json", 'r') as json_file:
                settings_dictionary = json.load(json_file)
                return settings_dictionary
        except FileNotFoundError:
            print('There\'s no settings yet bud...')
            raise

    def save_settings(self) -> None:
        settings_dict = self.__dict__
        with open("settings.json", 'w') as json_file:
            json.dump(settings_dict, json_file)

    def reset_settings(self):
        self.__dict__ = self.default_settings

    @classmethod
    def initialize_settings(cls):
        try:
            settings_dict = cls.load_settings()
        except FileNotFoundError:
            print('creating default JSON')
            cls.create_settings_json()
            settings_dict = cls.load_settings()

        settings_obj = cls(**settings_dict)
        return settings_obj


if __name__ == '__main__':
    settings = __SettingsHandler(2, 3, 4, 5, 6)
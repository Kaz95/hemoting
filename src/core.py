"""This module will be a refactored version of core. This version will be more generalized, and will encapsulate
    all the state and functionality that makes of the core 'engine'.
"""
import csv
import datetime
import functools
import json
import random
from dataclasses import dataclass, field
from typing import Final, Sequence

# Some constants to help write days for Date class in a more readable form


MONDAY: Final = 0
TUESDAY: Final = 1
WEDNESDAY: Final = 2
THURSDAY: Final = 3
FRIDAY: Final = 4
SATURDAY: Final = 5
SUNDAY: Final = 6


# TODO: Remember JSON doesn't know or care w/e a tuple is. That's on me.


class Settings:
    number_of_bleeds: int
    time_stamp_range: dict
    schedules: dict
    bleed_duration_range: dict
    bleed_locations: Sequence

    def __init__(self):
        self.load_settings()

    # Used to randomize bleed location. Nothing else.
    bleed_locations = ('Elbow', 'Knee', 'Ankle', 'Hip', 'Shoulder', 'Wrist', 'Quadriceps', 'Calf', 'Biceps', 'Triceps')

    normal_prophey_schedule = (0, 2, 4)
    alternate_prophey_schedule = (1, 3, 5)

    default_settings = {'number_of_bleeds': 3,
                        'time_stamp_range': {'min': 7, 'max': 10},
                        'schedules': {'normal': normal_prophey_schedule, 'alternate': alternate_prophey_schedule},
                        'bleed_duration_range': {'min': 1, 'max': 4},
                        'bleed_locations': bleed_locations}

    def _create_settings_json(self):
        try:
            open("settings.json", 'x')
        except FileExistsError:
            print('Settings already exists!')
        else:
            with open("settings.json", 'w') as json_file:
                json.dump(self.default_settings, json_file)

    @staticmethod
    def _get_settings_from_json():
        try:
            with open("settings.json", 'r') as json_file:
                settings_dictionary = json.load(json_file)
                return settings_dictionary
        except FileNotFoundError:
            print('There\'s no settings yet bud...')
            raise

    def load_settings(self):
        try:
            settings_dict = self._get_settings_from_json()
        except FileNotFoundError:
            print('creating default JSON')
            self._create_settings_json()
            settings_dict = self._get_settings_from_json()

        self.__dict__ = settings_dict

    def save_settings(self) -> None:
        with open("settings.json", 'w') as json_file:
            json.dump(self.__dict__, json_file)

    def reset_settings(self):
        self.__dict__ = self.default_settings


# Extended date object. Allows me to couple bleeds, infusions, and infusion timestamps to a given date.
class Date(datetime.date):
    bleeds_list: list[str]
    infused: bool
    time_stamp: datetime.time | None

    def __new__(cls, year, month, day):
        return super().__new__(cls, year, month, day)

    def __init__(self, year, month, day):
        self.bleeds_list = []  # Holds strings representing an active bleeding episode
        self.infused = False
        self.time_stamp = None

    # Hours -> 1-24, Where 1 = 1 AM and 24 = Midnight
    def randomize_time_stamp(self, starting_hour: int, ending_hour: int) -> None:
        if 1 <= (starting_hour and ending_hour) <= 24:
            randomized_hour = random.randrange(starting_hour, (ending_hour + 1))
            randomized_minute = random.randrange(1, 60)
            self.time_stamp = datetime.time(hour=randomized_hour, minute=randomized_minute)
        else:
            raise ValueError('Hour should be 1->24')


# A general interface for handling schedule state. Subclass this to extend schedule handling functionality.
class ScheduleHandler:
    # schedule = Iterable[int, int, int]
    #
    # normal_prophey_schedule: schedule
    # alternative_prophey_schedule: schedule
    # current_schedule: schedule

    def __init__(self, settings):
        self.settings = settings
        self.normal_schedule = self.settings.schedules['normal']
        self.alternate_schedule = self.settings.schedules['alternate']
        self.current_schedule = self.normal_schedule

    def toggle(self) -> None:
        if self.current_schedule == self.normal_schedule:
            self.current_schedule = self.alternate_schedule
        else:
            self.current_schedule = self.normal_schedule

    def reset(self) -> None:
        self.current_schedule = self.normal_schedule


# Returns max days possible, given normal prophey schedule, based on a starting wkday as input.
# 21 days is always possible at the least, then depending on starting wkday max length is extended.
# TODO: Figured out by hand, consider how I could have done this using math.
# TODO: Use of magic #s are hindering testing. Only way to test current implementation is...more magic #s.
# TODO: I'd only be testing that I haven't changed them, which is to say they don't test anything.
# TODO: Nothing relies on this number being accurate. The log will just be created within a smaller window.
# TODO: Bepisodes would continue to be created within this new smaller window as well.
# TODO: Also, what happens when I pass a decimal into this? Pretty sure it will raise a value error no matter what.
def get_max_days(starting_weekday: int) -> int:
    """Used by beps and for log generation"""
    maximum_possible_days = 21
    # Mon or Wed
    if starting_weekday in [MONDAY, WEDNESDAY]:
        maximum_possible_days += 2
    # Sun, Tue, or Fri
    elif starting_weekday in [SUNDAY, TUESDAY, FRIDAY]:
        maximum_possible_days += 3
    # Sat or Thr
    elif starting_weekday in [THURSDAY, SATURDAY]:
        maximum_possible_days += 4
    else:
        raise ValueError('Weekday was out of range while calculating max possible days.')
    return maximum_possible_days


"""
    ====================
    Bepisode shits
    ====================
"""


@dataclass
class Bepisode:
    start_date: Date
    location: str
    duration: int
    dates_active: list[Date] = field(default_factory=list)

    def project_dates(self):
        self.dates_active = generate_dates(self.start_date, self.duration)


class BepisodeHandler:
    bepisodes: list[Bepisode]
    settings: Settings

    def __init__(self, settings):
        self.bepisodes = []
        self.settings = settings

    # Randomizes a Date object within a given range of dates.
    @staticmethod
    def _randomize_bleed_episode_start(starting_date: Date, maximum_days_added: int) -> Date:
        days_added = random.randrange(1, maximum_days_added)
        bleed_start_date = starting_date + datetime.timedelta(days_added)
        return bleed_start_date

    # Chooses and returns a random string from bleed locations list
    def _randomize_bleed_location(self) -> str:
        return random.choice(self.settings.bleed_locations)

    def _randomize_bleed_duration(self) -> int:
        return random.randint(self.settings.bleed_duration_range['min'],
                              self.settings.bleed_duration_range['max'])

    def randomize_bleed_episode(self, starting_date: Date, maximum_possible_days: int) -> None:
        bleed_start_date = self._randomize_bleed_episode_start(starting_date, maximum_possible_days)
        location = self._randomize_bleed_location()
        duration = self._randomize_bleed_duration()
        randomized_bepisode = Bepisode(bleed_start_date, location, duration)
        self.bepisodes.append(randomized_bepisode)

    # Accepts an amount of bleeds, and will randomize and add bleeds until the list is 'filled' to that amount.
    # The list may or may not be empty when passed in. This allows program to back-fill any non-manual bleeds.
    # TODO: Consider using a closure on randomize_bleed_episode to avoid passing so many args.
    #  2 of 3 args arent used by parent func. Also this function ALWAYS expects a bep list.
    #  Maybe it should create an empty one if no list is passed?
    #  Also this modifies the original list not sure if matters.
    def fill_bepisode_list(self, starting_date: Date, maximum_possible_days_added: int) -> None:
        while len(self.bepisodes) < self.settings.number_of_bleeds:
            self.randomize_bleed_episode(starting_date, maximum_possible_days_added)

        for bepisode in self.bepisodes:
            print(f'{bepisode.duration} - {bepisode.location}')  # Used to display bleeds that were active. Remove later
            bepisode.project_dates()

    # TODO: This should be tied to CLI not core.
    # # Resulting list will be fed into randomize_all_bleed_episodes function at some point. Keep them compatible.
    # def get_manual_bleeds(self) -> None:
    #     while True:
    #         answer = input('Add Manual Bepisode? ')
    #         if answer.capitalize() == 'Y':
    #             year, month, day = get_date_input()
    #             starting_date = Date(year, month, day)
    #             location = input('Enter Bleed location ')
    #             duration = int(input('Enter Numerical Duration '))
    #             bepisode = Bepisode(starting_date, location, duration)
    #             self.manual_bleeds.append(bepisode)
    #         else:
    #             break


"""
    ==========================
    logger shits
    ==========================
"""


# Creates and returns a list of Date objects within a range based on input.
def generate_dates(starting_date: Date, days_added: int) -> list:
    blank_log = [starting_date + datetime.timedelta(_) for _ in range(days_added)]
    return blank_log


class Logger:
    log: list[Date] | None
    schedule_handler: ScheduleHandler
    settings: Settings
    bepisodes_handler: BepisodeHandler
    bepisodes: list[Bepisode]
    starting_date: Date
    max_possible_days: int

    def __init__(self, settings, bepisode_handler, schedule_handler):
        self.schedule_handler = schedule_handler
        self.settings = settings
        self.bepisodes_handler = bepisode_handler
        self.bepisodes = self.bepisodes_handler.bepisodes

        self.starting_date = Date(2022, 2, 2)
        self.max_possible_days = get_max_days(self.starting_date.weekday())

        self.log = None

    def update_starting_date(self, new_date: Date) -> None:
        self.starting_date = new_date
        self.max_possible_days = get_max_days(self.starting_date.weekday())

    def create_blank_log(self) -> None:
        blank_log = generate_dates(self.starting_date, self.max_possible_days)
        self.log = blank_log

    # TODO: This is on the list for a refactor. Test later.
    # Checks each date that bleeding occurred in each bepisode and tries to find a corresponding Date object in given list.
    # If one is found, the Date object will have its bleed list updated with a string.
    # The string represents the location of the aforementioned bleed.
    def couple_bleeds_to_dates(self) -> None:
        for bepisode in self.bepisodes:
            for date in bepisode.dates_active:
                try:
                    date_to_tag_index = self.log.index(date)
                    date_to_tag = self.log[date_to_tag_index]
                    date_to_tag.bleeds_list.append(bepisode.location)
                except ValueError:
                    print('Bleed projected passed end of window, probably.')

    # TODO: Magic #
    # Meat and potatoes function. Handles most of the logic to create an infusion log. Accepts an 'empty log' as input.
    # Infusions will be programmatically applied to Date objects based on a pre defined algorithm, until doses are exhausted.
    # A new list will be created with Date objects that meet certain criteria.
    # Criterion includes: Was infused, had corresponding Bepisode, or both.
    def add_infusions_to_log(self) -> None:
        doses_on_hand = 12
        infusion_log = []
        scheduler = self.schedule_handler

        # Helper function to apply infusion and time-stamp to Date object, increment doses, and handle schedule state.
        def infuse(toggle: bool = False) -> int:
            nonlocal doses_on_hand
            date.infused = True
            doses_on_hand -= 1
            date.randomize_time_stamp(self.settings.time_stamp_range['min'],
                                      self.settings.time_stamp_range['max'])
            if toggle:
                scheduler.toggle()
            return doses_on_hand

        for date in self.log:
            if doses_on_hand > 1:
                if date.bleeds_list:
                    infusion_log.append(date)
                    yesterday_index = self.log.index(date) - 1
                    day_before_yesterday_index = self.log.index(date) - 2
                    if yesterday_index >= 0 and day_before_yesterday_index >= 0:
                        if self.log[yesterday_index].infused and self.log[day_before_yesterday_index].infused:
                            if date.weekday() == 6:
                                scheduler.toggle()
                            continue
                        if date.weekday() not in scheduler.current_schedule:
                            doses_on_hand = infuse(toggle=True)
                        else:
                            doses_on_hand = infuse()
                    else:
                        if date.weekday() not in scheduler.current_schedule:
                            doses_on_hand = infuse(toggle=True)
                        else:
                            doses_on_hand = infuse()
                elif date.weekday() in scheduler.current_schedule:
                    infusion_log.append(date)
                    doses_on_hand = infuse()
                else:
                    if date.weekday() == 6:
                        scheduler.reset()
            else:
                break

        self.log = infusion_log

    # Used to visualize final log output, without having to check csv(or later DB)
    def print_log(self) -> None:
        for date in self.log:
            if date.bleeds_list:
                print(f'{date} - {date.infused} - {date.bleeds_list}')
            else:
                print(f'{date} - {date.infused} - Prophey')

    # TODO: This will blow right the fuck up if list passed doesn't have specific members.  Not date and its fukt.
    # Creates a string title for csv files based on first and last item in a list of Date objects.
    def make_csv_title(self) -> str:
        starting_date, ending_date = self.log[0].strftime('%m-%d-%Y'), self.log[-1].strftime('%m-%d-%Y')
        csv_title = f'{starting_date} - {ending_date}'
        return csv_title

    # Used to output log to csv
    def output_log_to_csv(self) -> None:
        csv_title = self.make_csv_title()
        with open(f'{csv_title}.csv', 'x', newline='') as csv_log:
            log_writer = csv.writer(csv_log)
            log_writer.writerow(['Date', 'Infused', 'time-stamp', 'Reason'])
            for date in self.log:
                if date.bleeds_list:
                    if date.infused:
                        log_writer.writerow([date, 'Yes', date.time_stamp, date.bleeds_list])
                    else:
                        log_writer.writerow([date, 'No', 'N/A', date.bleeds_list])
                else:
                    log_writer.writerow([date, 'Yes', date.time_stamp, 'Prophylaxis'])

    # Creates a blank log based on user inputted start date/last shipment.
    # Fills that log with occurrences of bleeding and infusions based on user inputted manual bleeds.
    # Returns a list of Date objects that is ready for sifting.
    # Pretty much everything outside of creating a csv.
    def generate_log(self) -> None:
        self.bepisodes_handler.fill_bepisode_list(self.starting_date, self.max_possible_days)
        self.create_blank_log()
        self.couple_bleeds_to_dates()
        self.add_infusions_to_log()


"""
    ==========================
    Input shits
    ==========================
"""


def _get_valid_date_input(minimum, maximum, unit):
    while True:
        answer = input(f'Enter {unit}: ')

        if answer.isdecimal():
            answer = int(answer)
        else:
            print('That is not a number!')
            continue

        if answer in range(minimum, maximum + 1):
            return answer
        else:
            print(f'{unit} out of range! Enter an integer in range {minimum} - {maximum}')
            continue


get_valid_day_input = functools.partial(_get_valid_date_input, minimum=datetime.date.min.day,
                                        maximum=datetime.date.max.day, unit='Day')
get_valid_month_input = functools.partial(_get_valid_date_input, minimum=datetime.date.min.month,
                                          maximum=datetime.date.max.month, unit='Month')
get_valid_year_input = functools.partial(_get_valid_date_input, minimum=datetime.date.min.year,
                                         maximum=datetime.date.max.year, unit='Year')


def get_date_input():
    year = get_valid_year_input()
    month = get_valid_month_input()
    day = get_valid_day_input()
    return year, month, day
    # return Date(year, month, day)


class CoreEngine:
    settings: Settings
    bepiode_handler: BepisodeHandler
    schedule_handler: ScheduleHandler
    logger: Logger

    def __init__(self):
        self.settings = Settings()
        self.bepiode_handler = BepisodeHandler(self.settings)
        self.schedule_handler = ScheduleHandler(self.settings)
        self.logger = Logger(self.settings, self.bepiode_handler, self.schedule_handler)


if __name__ == '__main__':
    ...
    core = CoreEngine()
    core.logger.generate_log()
    core.logger.print_log()
    core.logger.output_log_to_csv()

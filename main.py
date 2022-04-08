import datetime
import functools
import random
import csv
from typing import Final
from dataclasses import dataclass, field
import settings
from collections.abc import Iterable

# Some constants to help write days for Date class in a more readable form
MONDAY: Final = 0
TUESDAY: Final = 1
WEDNESDAY: Final = 2
THURSDAY: Final = 3
FRIDAY: Final = 4
SATURDAY: Final = 5
SUNDAY: Final = 6

# Used to randomize bleed location. Nothing else.
bleed_locations = ('Elbow', 'Knee', 'Ankle', 'Hip', 'Shoulder', 'Wrist', 'Quadriceps', 'Calf', 'Biceps', 'Triceps')


# Tuple of days of the week as used by the datetime class. Mon, Wed, Fri. Used as a schedule representation.
# normal_prophey_schedule = (MONDAY, WEDNESDAY, FRIDAY)
# Tuple of days of the week as referenced by the datetime class. Tue, Thur, Sat. Used as a schedule representation.
# alternative_prophey_schedule = (TUESDAY, THURSDAY, SATURDAY)

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
    schedule = Iterable[int, int, int]

    normal_prophey_schedule: schedule
    alternative_prophey_schedule: schedule
    current_schedule: schedule

    def __init__(self, normal_schedule, alternate_schedule):
        self.normal_schedule = normal_schedule
        self.alternate_schedule = alternate_schedule
        self.current_schedule = normal_schedule

    # TODO: This will toggle ANYTHING that isn't the normal schedule back to normal schedule.
    # TODO: There is an implicit reset. I'm not sure how I feel about that.
    def toggle(self) -> None:
        if self.current_schedule == self.normal_schedule:
            self.current_schedule = self.alternate_schedule
        else:
            self.current_schedule = self.normal_schedule

    def reset(self) -> None:
        self.current_schedule = self.normal_schedule


# TODO: Make dates active a class var, append all projected dates to that and you can avoid a double loop later on.
# TODO: Something, something, O(n**2) vs O(n). Use this as a real example to solidify your knowledge of BIG O notation
@dataclass
class Bepisode:
    start_date: Date
    location: str
    duration: int
    dates_active: list[Date] = field(default_factory=list)

    def project_dates(self):
        self.dates_active = generate_dates(self.start_date, self.duration)


# TODO: Don't think i can....Test...easily...
# TODO: OK what if I mock input method w/ side effects? I can verify the length of the fake input list to be sure the -
# TODO: func did not return on given inputs, but did continue accepting them. I could even verify stdout stream I spose.
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


# TODO: Test..I guess I can verify the func and params via Partial attributes...That's actually super fucking useful.
# TODO: 100% better option then simple closure for testing purposes alone. Not to mention saving a crap ton of boiler plate.
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


# Returns max days possible, given normal prophey schedule, based on a starting wkday as input.
# 21 days is always possible at the least, then depending on starting wkday max length is extended.
# TODO: Figured out by hand, consider how I could have done this using math.
# TODO: Use of magic #s are hindering testing. Only way to test current implementation is...more magic #s.
# TODO: I'd only be testing that I haven't changed them, which is to say they don't test anything.
# TODO: Nothing relies on this number being accurate. The log will just be created within a smaller window.
# TODO: Bepisodes would continue to be created within this new smaller window as well.
# TODO: Also, what happens when I pass a decimal into this? Pretty sure it will raise a value error no matter what.
def get_max_days(starting_weekday: int) -> int:
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


# Creates and returns a list of Date objects within a range based on input.
def generate_dates(starting_date: Date, days_added: int) -> list:
    blank_log = [starting_date + datetime.timedelta(_) for _ in range(days_added)]
    return blank_log


# Randomizes a Date object within a given range of dates.
def randomize_bleed_episode_start(starting_date: Date, maximum_days_added: int) -> Date:
    days_added = random.randrange(1, maximum_days_added)
    bleed_start_date = starting_date + datetime.timedelta(days_added)
    return bleed_start_date


# TODO: Relies on global list. Change to receive list as arg.
# Chooses and returns a random string from bleed locations list
def randomize_bleed_location() -> str:
    bleed_location_index = random.randrange(len(bleed_locations))
    bleed_location = bleed_locations[bleed_location_index]
    return bleed_location


# TODO: Change this to a setting that gets loaded and injected.
# TODO: Magic #
def randomize_bleed_duration() -> int:
    return random.randrange(1, 5)


def randomize_bleed_episode(starting_date: Date, maximum_possible_days: int) -> Bepisode:
    bleed_start_date = randomize_bleed_episode_start(starting_date, maximum_possible_days)
    location = randomize_bleed_location()
    duration = randomize_bleed_duration()
    return Bepisode(bleed_start_date, location, duration)


# TODO: This is on the list for a refactor. Test later.
# Checks each date that bleeding occurred in each bepisode and tries to find a corresponding Date object in given list.
# If one is found, the Date object will have its bleed list updated with a string.
# The string represents the location of the aforementioned bleed.
def couple_bleeds_to_dates(bepisodes_list: list, log: list) -> list:
    for bepisode in bepisodes_list:
        for date in bepisode.dates_active:
            try:
                date_to_tag_index = log.index(date)
                date_to_tag = log[date_to_tag_index]
                date_to_tag.bleeds_list.append(bepisode.location)
            except ValueError:
                print('Bleed projected passed end of window, probably.')
    return log


# Accepts an amount of bleeds, and will randomize and add bleeds until the list is 'filled' to that amount.
# The list may or may not be empty when passed in. This allows program to back-fill any non-manual bleeds.
# TODO: Consider using a closure on randomize_bleed_episode to avoid passing so many args.
#  2 of 3 args arent used by parent func. Also this function ALWAYS expects a bep list.
#  Maybe it should create an empty one if no list is passed? Also this modifies the original list...not sure if matters.
def fill_bepisode_list(number_of_bleeds_set: int, starting_date: Date, maximum_possible_days_added: int,
                       bepisode_list: list) -> list:
    while len(bepisode_list) < number_of_bleeds_set:
        bepisode = randomize_bleed_episode(starting_date, maximum_possible_days_added)
        bepisode_list.append(bepisode)

    for bepisode in bepisode_list:
        print(f'{bepisode.duration} - {bepisode.location}')  # Used to display bleeds that were active. Remove later
        bepisode.project_dates()
        # bepisode.dates_active = generate_dates(bepisode.start_date, bepisode.duration)

    return bepisode_list


# TODO: Magic #
# Meat and potatoes function. Handles most of the logic to create an infusion log. Accepts an 'empty log' as input.
# Infusions will be programmatically applied to Date objects based on a pre defined algorithm, until doses are exhausted.
# A new list will be created with Date objects that meet certain criteria.
# Criterion includes: Was infused, had corresponding Bepisode, or both.
def add_infusions_to_log(blank_log: list, settings_handler: settings.SettingsHandler) -> list:
    doses_on_hand = 12
    infusion_log = []
    normal_prophey_schedule = settings_handler.schedules['normal']
    alternative_prophey_schedule = settings_handler.schedules['alternate']
    scheduler = ScheduleHandler(normal_prophey_schedule, alternative_prophey_schedule)

    # Helper function to apply infusion and time-stamp to Date object, increment doses, and handle schedule state.
    def infuse(toggle: bool = False) -> int:
        nonlocal doses_on_hand
        date.infused = True
        doses_on_hand -= 1
        date.randomize_time_stamp(settings_handler.time_stamp_range['min'], settings_handler.time_stamp_range['max'])
        if toggle:
            scheduler.toggle()
        return doses_on_hand

    for date in blank_log:
        if doses_on_hand > 1:
            if date.bleeds_list:
                infusion_log.append(date)
                yesterday_index = blank_log.index(date) - 1
                day_before_yesterday_index = blank_log.index(date) - 2
                if yesterday_index >= 0 and day_before_yesterday_index >= 0:
                    if blank_log[yesterday_index].infused and blank_log[day_before_yesterday_index].infused:
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

    return infusion_log


# Resulting list will be fed into randomize_all_bleed_episodes function at some point. Keep them compatible.
def get_manual_bleeds() -> list:
    manual_bepisodes = []
    while True:
        answer = input('Add Manual Bepisode? ')
        if answer.capitalize() == 'Y':
            year, month, day = get_date_input()
            starting_date = Date(year, month, day)
            location = input('Enter Bleed location ')
            duration = int(input('Enter Numerical Duration '))
            bepisode = Bepisode(starting_date, location, duration)
            manual_bepisodes.append(bepisode)
        else:
            break
    return manual_bepisodes


# TODO: Add real comment/decide if I actually want to use this.
def get_all_inputs() -> tuple[Date, list]:
    year, month, day = get_date_input()
    starting_date = Date(year, month, day)
    manual_bepisodes = get_manual_bleeds()
    return starting_date, manual_bepisodes


# Creates a blank log based on user inputted start date/last shipment.
# Fills that log with occurrences of bleeding and infusions based on user inputted manual bleeds.
# Returns a list of Date objects that is ready for sifting.
# Pretty much everything outside of creating a csv.
def generate_log(settings_handler) -> list:
    starting_date, manual_bepisodes = get_all_inputs()
    max_possible_days = get_max_days(starting_date.weekday())

    bepisode_list = fill_bepisode_list(settings_handler.number_of_bleeds, starting_date, max_possible_days,
                                       manual_bepisodes)
    blank_log = generate_dates(starting_date, max_possible_days)

    log_with_bleeds = couple_bleeds_to_dates(bepisode_list, blank_log)
    full_log = add_infusions_to_log(log_with_bleeds, settings_handler)

    return full_log


# Used to visualize final log output, without having to check csv(or later DB)
def print_log(log: list) -> None:
    for date in log:
        if date.bleeds_list:
            print(f'{date} - {date.infused} - {date.bleeds_list}')
        else:
            print(f'{date} - {date.infused} - Prophey')


# Creates a string title for csv files based on first and last item in a list of Date objects.
def make_csv_title(log: list) -> str:
    starting_date = log[0]
    start_date_string = starting_date.strftime('%m-%d-%Y')
    ending_date = log[-1]
    end_date_string = ending_date.strftime('%m-%d-%Y')
    csv_title = f'{start_date_string} - {end_date_string}'
    return csv_title


# Used to output log to csv
def output_log_to_csv(log: list) -> None:
    csv_title = make_csv_title(log)
    with open(f'{csv_title}.csv', 'x', newline='') as csv_log:
        log_writer = csv.writer(csv_log)
        log_writer.writerow(['Date', 'Infused', 'time-stamp', 'Reason'])
        for date in log:
            if date.bleeds_list:
                if date.infused:
                    log_writer.writerow([date, 'Yes', date.time_stamp, date.bleeds_list])
                else:
                    log_writer.writerow([date, 'No', 'N/A', date.bleeds_list])
            else:
                log_writer.writerow([date, 'Yes', date.time_stamp, 'Prophylaxis'])


# TODO: Magic #
# Helper function to print out a CLI menu
def print_menu_border() -> None:
    for i in range(54):
        print('-', end="")


# Prints temporary CLI menu
def print_menu_header() -> None:
    print_menu_border()
    print('')
    print('                        Menu                          ')
    print_menu_border()


def print_menu_options() -> None:
    print()
    print('1.) New Shipment Date')
    print('2.) Update Bepisodes')
    print('3.) Update Settings')
    print('4.) Exit')
    print_menu_border()
    print()


# TODO: Clean this up. Man....actually....this makes me feel bad to look at....fix it.
#  Maybe new shiny pattern matching!
def main() -> None:
    setting_handler = settings.initialize_settings()
    while True:
        print_menu_header()
        print_menu_options()
        selection = input('What do?: ')
        if selection == '1':
            log = generate_log(setting_handler)
            print_log(log)
            output_log_to_csv(log)
        elif selection == '3':
            print()
            print('1.) Update # of Bleeds.')
            print('2.) Update Time Stamp Range')
            print('3.) Update Schedules')
            print('4.) <--')
            print_menu_border()
            print()
            selection = input('What do?: ')
            if selection == '4':
                continue
            elif selection == '1':
                new_setting = int(input('Enter new number of bleeds: '))
                setting_handler.number_of_bleeds = new_setting
                settings.save_settings(setting_handler)
                print(f'# of Bleeds updated to: {setting_handler.number_of_bleeds}!')
                continue
            elif selection == '2':
                lower = int(input('Enter lower end of timestamp range: '))
                upper = int(input('Enter upper end of timestamp range: '))
                setting_handler.time_stamp_range['min'] = lower
                setting_handler.time_stamp_range['max'] = upper
                settings.save_settings(setting_handler)
                print(f'Time Stamp range updated to: {setting_handler.time_stamp_range}!')
            elif selection == '3':
                normal_sched = input('Enter new normal schedule as tuple: ')
                alt_sched = input('Enter new alternate schedule as tuple: ')
                normal_sched = [int(x) for x in normal_sched if x.isdecimal()]
                alt_sched = [int(x) for x in alt_sched if x.isdecimal()]
                setting_handler.schedules['normal'] = normal_sched
                setting_handler.schedules['alternate'] = alt_sched
                settings.save_settings(setting_handler)
                print(f'Schedules updated to: {setting_handler.schedules}!')
        elif selection == '4':
            break
        else:
            print('Not yet implemented.\n\n\n')


# TODO: Consider adding custom types that more closely adhere to the public contract.
#  A schedule is a tuple of three integers, but I'm not currently enforcing the range of those integers.
# TODO: Consider freezing dataclasses, and generally leveraging them more in the program. They have unique features.
if __name__ == '__main__':
    main()
    # da = Date(2022, 2, 2)
    # da.randomize_time_stamp(0, 10)

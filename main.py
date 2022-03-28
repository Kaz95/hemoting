import datetime
import random
import csv

# Used to randomize bleed location. Nothing else.
bleed_locations = ('Elbow', 'Knee', 'Ankle', 'Hip', 'Shoulder', 'Wrist', 'Quadriceps', 'Calf', 'Biceps', 'Triceps')

# Tuple of days of the week as used by the datetime class. Mon, Wed, Fri. Used as a schedule representation.
normal_prophey_schedule = (0, 2, 4)
# Tuple of days of the week as referenced by the datetime class. Tue, Thur, Sat. Used as a schedule representation.
alternative_prophey_schedule = (1, 3, 5)


# Extended date object. Allows me to couple bleeds, infusions, and infusion timestamps to a given date.
class Date(datetime.date):

    def __new__(cls, *arg, **kwargs):
        return super().__new__(cls, *arg, **kwargs)

    def __init__(self, *arg, **kwargs):
        super().__init__()
        self.bleeds_list = []   # Holds strings representing an active bleeding episode
        self.infused = False
        self.time_stamp = None


# A general interface for handling schedule state. Subclass this to extend schedule handling functionality.
class ScheduleHandler:
    def __init__(self, normal_schedule, alternate_schedule):
        self.normal_schedule = normal_schedule
        self.alternate_schedule = alternate_schedule
        self.current_schedule = normal_schedule

    def toggle(self) -> None:
        if self.current_schedule == self.normal_schedule:
            self.current_schedule = self.alternate_schedule
        else:
            self.current_schedule = self.normal_schedule

    def reset(self) -> None:
        self.current_schedule = self.normal_schedule


# TODO: Make dates active a class var, append all projected dates to that and you can avoid a double loop later on.
# TODO: Something, something, O(n**2) vs O(n). Use this as a real example to solidify your knowledge of BIG O notation
# Class to encapsulate the data pertaining to a given bleeding episode.
class Bepisode:
    def __init__(self, start_date, location, duration):
        self.start_date = start_date
        self.location = location
        self.duration = duration
        self.dates_active = []

    # Method that projects days bled, based on duration and start date.
    def project_dates(self) -> None:
        for _ in range(self.duration):
            projected_date = self.start_date + datetime.timedelta(_)
            self.dates_active.append(projected_date)


# TODO: Pretty sure if I have Date inherit from date, instead of datetime, I could avoid all the random ass defaults.
# TODO: I could probably also set default values in class init or definition to achieve the same effect.
# Gets user input and creates a Date object.
def get_date() -> Date:
    year = int(input('Input Year XXXX: '))
    month = int(input('Input Month X(X): '))
    day = int(input('Input Day X(X): '))
    date = Date(year, month, day)
    return date


# Returns max days possible, given normal prophey schedule, based on a starting wkday as input.
# 21 days is always possible at the least, then depending on starting wkday max length is extended.
# Figured out by hand, consider how I could have done this using math.
def get_max_days(starting_weekday: int) -> int:
    maximum_possible_days = 21
    # Mon or Wed
    if starting_weekday in [0, 2]:
        maximum_possible_days += 2
    # Sun, Tue, or Fri
    elif starting_weekday in [6, 1, 4]:
        maximum_possible_days += 3
    # Sat or Thr
    elif starting_weekday in [3, 5]:
        maximum_possible_days += 4
    else:
        raise Exception('Weekday was somehow out of range?')
    return maximum_possible_days


# Creates and returns a list of Date objects within a range based on input.
def make_blank_log(starting_date: Date, maximum_possible_days: int) -> list:
    blank_log = [starting_date + datetime.timedelta(_) for _ in range(maximum_possible_days)]
    return blank_log


# Randomizes a Date object within a given range of dates.
def randomize_bleed_episode_start(starting_date: Date, maximum_days_added: int) -> Date:
    days_added = random.randrange(1, maximum_days_added)
    bleed_start_date = starting_date + datetime.timedelta(days_added)
    return bleed_start_date


# Chooses and returns a random string from bleed locations list
def randomize_bleed_location() -> str:
    bleed_location_index = random.randrange(len(bleed_locations))
    bleed_location = bleed_locations[bleed_location_index]
    return bleed_location


def randomize_bleed_duration() -> int:
    return random.randrange(1, 5)


def randomize_bleed_episode(starting_date: Date, maximum_possible_days: int) -> Bepisode:
    bleed_start_date = randomize_bleed_episode_start(starting_date, maximum_possible_days)
    location = randomize_bleed_location()
    duration = randomize_bleed_duration()
    return Bepisode(bleed_start_date, location, duration)


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
def fill_bepisode_list(number_of_bleeds_set: int, starting_date: Date, maximum_possible_days: int, bepisode_list: list) -> list:
    while len(bepisode_list) < number_of_bleeds_set:
        bepisode = randomize_bleed_episode(starting_date, maximum_possible_days)
        bepisode_list.append(bepisode)

    for bepisode in bepisode_list:
        print(f'{bepisode.duration} - {bepisode.location}')     # Used to display bleeds that were active. Remove later
        bepisode.project_dates()

    return bepisode_list


# Hours -> 1-24, Where 1 = 1 AM and 24 = Midnight
def randomize_time_stamp(starting_hour: int, ending_hour: int) -> datetime.time:
    randomized_hour = random.randrange(starting_hour, (ending_hour + 1))
    randomized_minute = random.randrange(1, 60)
    return datetime.time(hour=randomized_hour, minute=randomized_minute)


# Helper function to apply infusion and time-stamp to Date object, increment doses, and handle schedule state.
# TODO: Could this be defined inside add_infusions_to_log()???
def infuse(date: Date, doses_on_hand: int, schedule_handler: ScheduleHandler, toggle: bool = False) -> int:
    date.infused = True
    doses_on_hand -= 1
    date.timestamp = randomize_time_stamp(7, 10)
    if toggle:
        schedule_handler.toggle()
    return doses_on_hand


# Meat and potatoes function. Handles most of the logic to create an infusion log. Accepts an 'empty log' as input.
# Infusions will be programmatically applied to Date objects based on a pre defined algorithm, until doses are exhausted.
# A new list will be created with Date objects that meet certain criteria.
# Criterion includes: Was infused, had corresponding Bepisode, or both.
def add_infusions_to_log(blank_log: list) -> list:
    doses_on_hand = 12
    infusion_log = []
    scheduler = ScheduleHandler(normal_prophey_schedule, alternative_prophey_schedule)
    for date in blank_log:
        if doses_on_hand > 1:
            if date.bleeds_list:
                infusion_log.append(date)
                yesterday_index = blank_log.index(date) - 1
                day_before_yesterday_index = blank_log.index(date) - 2
                if yesterday_index and day_before_yesterday_index >= 0:
                    try:
                        if blank_log[yesterday_index].infused and blank_log[day_before_yesterday_index].infused:
                            if date.weekday() == 6:
                                scheduler.toggle()
                            continue
                    # TODO: Verify wtf is actually happening here.
                    except ValueError:
                        print('index was out of range when checking prev two days, but was handled')

                    if date.weekday() not in scheduler.current_schedule:
                        doses_on_hand = infuse(date, doses_on_hand, scheduler, toggle=True)
                    else:
                        doses_on_hand = infuse(date, doses_on_hand, scheduler)

                else:
                    if date.weekday() not in scheduler.current_schedule:
                        doses_on_hand = infuse(date, doses_on_hand, scheduler, toggle=True)
                    else:
                        doses_on_hand = infuse(date, doses_on_hand, scheduler)

            elif date.weekday() in scheduler.current_schedule:
                infusion_log.append(date)
                doses_on_hand = infuse(date, doses_on_hand, scheduler)

            else:
                if date.weekday() == 6:
                    scheduler.reset()

        # TODO is this else case even needed?
        else:
            pass

    return infusion_log


# Resulting list will be fed into randomize_all_bleed_episodes function at some point. Keep them compatible.
def get_manual_bleeds() -> list:
    manual_bepisodes = []
    while True:
        answer = input('Add Manual Bepisode? ')
        if answer.capitalize() == 'Y':
            starting_date = get_date()
            location = input('Enter Bleed location ')
            duration = int(input('Enter Numerical Duration '))
            bepisode = Bepisode(starting_date, location, duration)
            manual_bepisodes.append(bepisode)
        else:
            break
    return manual_bepisodes


# TODO: Add real comment/decide if I actually want to use this.
def get_all_inputs() -> tuple[Date, list]:
    starting_date = get_date()
    manual_bepisodes = get_manual_bleeds()
    return starting_date, manual_bepisodes


# Creates a blank log based on user inputted start date/last shipment.
# Fills that log with occurrences of bleeding and infusions based on user inputted manual bleeds.
# Returns a list of Date objects that is ready for sifting.
# Pretty much everything outside of creating a csv.
# TODO: I need to break this down a bit. Inputs should be separate from log generation at the least.
def generate_log() -> list:
    starting_date, manual_bepisodes = get_all_inputs()
    max_possible_days = get_max_days(starting_date.weekday())

    bepisode_list = fill_bepisode_list(3, starting_date, max_possible_days, manual_bepisodes)
    blank_log = make_blank_log(starting_date, max_possible_days)

    log_with_bleeds = couple_bleeds_to_dates(bepisode_list, blank_log)
    full_log = add_infusions_to_log(log_with_bleeds)

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


# TODO: I'm pretty sure I pass in a list of ONLY relevant dates already due to previous changes. Look into it.
# Used to output a sifted log to csv
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


def main() -> None:
    while True:
        print_menu_header()
        print_menu_options()
        selection = input('What do?: ')
        if selection == '1':
            log = generate_log()
            print_log(log)
            output_log_to_csv(log)
        elif selection == '4':
            break
        else:
            print('Not yet implemented.\n\n\n')


# TODO: Add Type hints.....I think that's what they are called. Read up on it again.
# TODO: Need Testing, program is growing. Should have done from start. Look into test driven development again.
# TODO: Times I've thought: "Damn,I should write some tests", but did not --> 22
if __name__ == '__main__':
    main()
    
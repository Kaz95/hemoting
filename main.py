import datetime
import random
import csv

# Used to randomize bleed location. Nothing else.
bleed_locations_list = ('Elbow', 'Knee', 'Ankle', 'Hip', 'Shoulder', 'Wrist', 'Quadriceps', 'Calf', 'Biceps', 'Triceps')

# Tuple of days of the week as used by the datetime class. Mon, Wed, Fri. Used as a schedule representation.
normal_prophey_schedule = (0, 2, 4)
# Tuple of days of the week as referenced by the datetime class. Tue, Thur, Sat. Used as a schedule representation.
alt_prophey_schedule = (1, 3, 5)


# Extended datetime object. Always me to couple bleeds, infusions, and infusion timestamps to a given date.
class Date(datetime.datetime):

    def __new__(cls, year, month, day, hour, minute, second, microsecond, tzinfo, infusion=None):
        return super().__new__(cls, year=year, month=month, day=day, hour=hour, minute=minute, second=second, microsecond=microsecond, tzinfo=tzinfo)

    def __init__(self, year, month, day, hour, minute, second, microsecond, tzinfo, infused=False):
        super().__init__()
        self.bleeds_list = []
        self.infused = infused
        self.time_stamp = None


# A general interface for handling schedule state. Subclass this to extend schedule handling functionality.
class ScheduleHandler:
    def __init__(self, norm, alt):
        self.norm = norm
        self.alt = alt
        self.current_schedule = norm

    def toggle(self) -> None:
        if self.current_schedule == self.norm:
            self.current_schedule = self.alt
        else:
            self.current_schedule = self.norm

    def reset(self) -> None:
        self.current_schedule = self.norm


# Class to encapsulate the data pertaining to a given bleeding episode.
class Bepisode:
    def __init__(self, start_date, location, duration):
        self.start_date = start_date
        self.location = location
        self.duration = duration
        self.dates_list = []

    # Method that projects days bled, based on duration and start date.
    def project_dates(self) -> None:
        for _ in range(self.duration):
            projected_date = self.start_date + datetime.timedelta(_)
            self.dates_list.append(projected_date)


# Gets user input and creates a Date object.
def get_date() -> Date:
    year = int(input('Input Year XXXX: '))
    month = int(input('Input Month X(X): '))
    day = int(input('Input Day X(X): '))
    date = Date(year, month, day, 0, 0, 0, 0, None)
    return date


# Returns max days possible, given normal prophey schedule, based on a starting wkday as input.
# 21 days is always possible at the least, then depending on starting wkday max length is extended.
# Figured out by hand, consider how I could have done this using math.
def get_max_days(start_wkday: int) -> int:
    maximum_days = 21
    # Mon or Wed
    if start_wkday in [0, 2]:
        maximum_days += 2
    # Sun, Tue, or Fri
    elif start_wkday in [6, 1, 4]:
        maximum_days += 3
    # Sat or Thr
    elif start_wkday in [3, 5]:
        maximum_days += 4
    else:
        raise Exception('Weekday was somehow out of range?')
    return maximum_days


# Creates and returns a list of Date objects within a range based on input.
def make_blank_log(start_date: Date, maximum_days: int) -> list:
    blank_log = [start_date + datetime.timedelta(_) for _ in range(maximum_days)]
    return blank_log


# Randomizes a Date object within a given range of dates.
def randomize_bleed_episode_start(start_date: Date, maximum_days_added: int) -> Date:
    days_added = random.randrange(1, maximum_days_added)
    bleed_start_date = start_date + datetime.timedelta(days_added)
    return bleed_start_date


# Chooses and returns a random string from bleed locations list
def randomize_bleed_location() -> str:
    bleed_location_index = random.randrange(len(bleed_locations_list))
    bleed_location_string = bleed_locations_list[bleed_location_index]
    return bleed_location_string


def randomize_bleed_duration() -> int:
    return random.randrange(1, 5)


def randomize_bleed_episode(start_date: Date, maximum_days: int) -> Bepisode:
    bleed_start_date = randomize_bleed_episode_start(start_date, maximum_days)
    location = randomize_bleed_location()
    duration = randomize_bleed_duration()
    return Bepisode(bleed_start_date, location, duration)


# Checks each date that bleeding occurred in each bepisode and tries to find a corresponding Date object in given list.
# If one is found, the Date object will have its bleed list updated with a string.
# The string represents the location of the aforementioned bleed.
def couple_bleeds_to_dates(bepisodes_list: list, some_log: list) -> list:
    for bepisode in bepisodes_list:
        for day in bepisode.dates_list:
            try:
                date_to_tag_index = some_log.index(day)
                date_to_tag = some_log[date_to_tag_index]
                date_to_tag.bleeds_list.append(bepisode.location)
            except ValueError:
                print('Bleed projected passed end of window, probably.')
    return some_log


# Accepts an amount of bleeds, and will randomize and add bleeds until the list is 'filled' to that amount.
# The list may or may not be empty when passed in. This allows program to back-fill any non-manual bleeds.
def randomize_bleed_episodes(amount_of_bleeds: int, start_date: Date, maximum_days: int, bepisode_list: list) -> list:
    while len(bepisode_list) < amount_of_bleeds:
        bepisode = randomize_bleed_episode(start_date, maximum_days)
        bepisode_list.append(bepisode)
    for bepisode in bepisode_list:
        print(f'{bepisode.duration} - {bepisode.location}')
        bepisode.project_dates()
    return bepisode_list


# Hours -> 1-24, Where 1 = 1 AM and 24 = Midnight
def randomize_time_stamp(start_hr: int, end_hr: int) -> datetime.time:
    rand_hr = random.randrange(start_hr, (end_hr + 1))
    rand_minute = random.randrange(1, 60)
    return datetime.time(hour=rand_hr, minute=rand_minute)


# Helper function to apply infusion and time-stamp to Date object, increment doses, and handle schedule state.
# TODO: Could this be defined inside add_infusions_to_log()???
def infuse(some_day: Date, doses: int, schedule_handler: ScheduleHandler, tog: bool = False) -> int:
    some_day.infused = True
    doses -= 1
    some_day.timestamp = randomize_time_stamp(7, 10)
    if tog:
        schedule_handler.toggle()
    return doses


# Meat and potatoes function. Handles most of the logic to create an infusion log. Accepts an 'empty log' as input.
# Infusions will be programmatically applied to Date objects based on a pre defined algorithm, until doses are exhausted.
# A new list will be created with Date objects that meet certain criteria.
# Criteria includes: Was infused, had corresponding Bepisode, or both.
def add_infusions_to_log(some_log: list) -> list:
    doses = 12
    infusion_log = []
    scheduler = ScheduleHandler(normal_prophey_schedule, alt_prophey_schedule)
    for day in some_log:
        if doses > 1:
            if day.bleeds_list:
                infusion_log.append(day)
                yesterday_index = some_log.index(day) - 1
                day_before_yesterday_index = some_log.index(day) - 2
                if yesterday_index and day_before_yesterday_index >= 0:
                    try:
                        if some_log[yesterday_index].infused and some_log[day_before_yesterday_index].infused:
                            if day.weekday() == 6:
                                scheduler.toggle()
                            continue
                    except ValueError:
                        print('index was out of range when checking prev two days, but was handled')

                    if day.weekday() not in scheduler.current_schedule:
                        doses = infuse(day, doses, scheduler, tog=True)
                    else:
                        doses = infuse(day, doses, scheduler)

                else:
                    if day.weekday() not in scheduler.current_schedule:
                        doses = infuse(day, doses, scheduler, tog=True)
                    else:
                        doses = infuse(day, doses, scheduler)

            elif day.weekday() in scheduler.current_schedule:
                infusion_log.append(day)
                doses = infuse(day, doses, scheduler)

            else:
                if day.weekday() == 6:
                    scheduler.toggle()

        # TODO is this else case even needed?
        else:
            pass

    return infusion_log


# Resulting list will be fed into randomize_all_bleed_episodes function at some point. Keep them compatible.
def get_manual_bleeds() -> list:
    bepisode_list = []
    while True:
        answer = input('Add Manual Bepisode? ')
        if answer.capitalize() == 'Y':
            start_date = get_date()
            location = input('Enter Bleed location ')
            duration = int(input('Enter Numerical Duration '))
            bepisode = Bepisode(start_date, location, duration)
            bepisode_list.append(bepisode)
        else:
            break
    return bepisode_list


# Creates a blank log based on user inputted start date/last shipment.
# Fills that log with occurrences of bleeding and infusions based on user inputted manual bleeds.
# Returns a list of Date objects that is ready for sifting.
# Pretty much everything outside of creating a csv.
# TODO: I need to break this down a bit. Inputs should be separate from log generation at the least.
def generate_log() -> list:
    start_date = get_date()

    max_days = get_max_days(start_date.weekday())
    blank_log = make_blank_log(start_date, max_days)
    bepisode_list = get_manual_bleeds()
    bepisode_list = randomize_bleed_episodes(3, start_date, max_days, bepisode_list)

    log_with_bleeds = couple_bleeds_to_dates(bepisode_list, blank_log)

    full_log = add_infusions_to_log(log_with_bleeds)
    return full_log


# Used to visualize final log output, without having to check csv(or later DB)
def print_log(some_log: list) -> None:
    for day in some_log:
        if day.bleeds_list:
            print(f'{day} - {day.infused} - {day.bleeds_list}')
        else:
            print(f'{day} - {day.infused} - Prophey')


# Creates a string title for csv files based on first and last item in a list of Date objects.
def make_csv_title(some_log: list) -> str:
    start_date = some_log[0]
    start_date_string = start_date.strftime('%m-%d-%Y')
    end_date = some_log[-1]
    end_date_string = end_date.strftime('%m-%d-%Y')
    csv_title = f'{start_date_string} - {end_date_string}'
    return csv_title


# Used to output a sifted log to csv
def output_to_csv(some_log: list) -> None:
    csv_title = make_csv_title(some_log)
    with open(f'{csv_title}.csv', 'x', newline='') as csv_log:
        log_writer = csv.writer(csv_log)
        log_writer.writerow(['Date', 'Infused', 'time-stamp', 'Reason'])
        for day in some_log:
            if day.bleeds_list:
                if day.infused:
                    log_writer.writerow([day, 'Yes', day.time_stamp, day.bleeds_list])
                else:
                    log_writer.writerow([day, 'No', 'N/A', day.bleeds_list])
            else:
                log_writer.writerow([day, 'Yes', day.time_stamp, 'Prophylaxis'])


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


# TODO: Add Type hints.....I think that's what they are called. Read up on it again.
# TODO: Need Testing, program is growing. Should have done from start. Look into test driven development again.
# TODO: Times I've thought: "Damn,I should write some tests", but did not --> 16
if __name__ == '__main__':
    while True:
        print_menu_header()
        print_menu_options()
        selection = input('What do?: ')
        if selection == '1':
            log = generate_log()
            print_log(log)
            output_to_csv(log)
        elif selection == '4':
            break
        else:
            print('Not yet implemented.\n\n\n')

    
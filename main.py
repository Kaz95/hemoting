import datetime
import random
import csv

# Used to randomize bleed location. Nothing else.
bleed_locations_list = ['Elbow', 'Knee', 'Ankle', 'Hip', 'Shoulder', 'Wrist', 'Quadriceps', 'Calf', 'Biceps', 'Triceps']
# List of days of the week as used by the datetime class. Mon, Wed, Fri.
normal_prophey_schedule = (0, 2, 4)
# List of days of the week as referenced by the datetime class. Tue, Thur, Sat.
alt_prophey_schedule = (1, 3, 5)


# Toggles between Normal and alternative prophey schedules.
# Will always output the schedule tht is not currently selected
def toggle_schedule(schedule):
    if schedule == normal_prophey_schedule:
        schedule = alt_prophey_schedule
    else:
        schedule = normal_prophey_schedule
    return schedule


# TODO: Consider using date object instead of datetime
# TODO: Haven't changed it yet because not sure if sqlite requires a full date time object or just a date will do.
# Extended datetime object. Always me to couple bleeds, infusions, and infusion timestamps to a given date.
class Date(datetime.datetime):

    def __new__(cls, year, month, day, hour, minute, second, microsecond, tzinfo, infusion=None):
        return super().__new__(cls, year=year, month=month, day=day, hour=hour, minute=minute, second=second, microsecond=microsecond, tzinfo=tzinfo)

    def __init__(self, year, month, day, hour, minute, second, microsecond, tzinfo, infused=False):
        super().__init__()
        self.bleeds_list = []
        self.infused = infused
        self.time_stamp = None


# Gets user input for year, date, and month. Coverts to integers and creates a Date object.
def get_date():
    year = int(input('Input Year XXXX: '))
    month = int(input('Input Month X(X): '))
    day = int(input('Input Day X(X): '))
    date = Date(year, month, day, 0, 0, 0, 0, None)
    return date


# Returns max days possible, given normal prophey schedule, based on a starting wkday as input.
# 21 days is always possible at the least, then depending on starting wkday max length is extended.
# Figured out by hand, consider how I could have done this using math.
def get_max_days(start_wkday):
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


# Class to encapsulate the data pertaining to a given bleeding episode.
class Bepisode:
    def __init__(self, start_date, location, duration):
        self.start_date = start_date
        self.location = location
        self.duration = duration
        self.dates_list = []

    # Method that projects days bled, based on duration and start date.
    def project_dates(self):
        for _ in range(self.duration):
            projected_date = self.start_date + datetime.timedelta(_)
            self.dates_list.append(projected_date)


# Creates and returns a list of Date objects within a range based on input.
def make_blank_log(start_date, maximum_days):
    blank_log = [start_date]
    temp_date = start_date
    for _ in range(maximum_days):
        temp_date = temp_date + datetime.timedelta(1)
        blank_log.append(temp_date)
        # start_date = start_date + datetime.timedelta(1)
        # blank_log.append(start_date)
    return blank_log


def randomize_bleed_episode_start(start_date, maximum_days_added):
    days_added = random.randrange(1, maximum_days_added)
    bleed_start_date = start_date + datetime.timedelta(days_added)
    return bleed_start_date


# Chooses and returns a random string from bleed locations list
def randomize_bleed_location():
    bleed_location_index = random.randrange(len(bleed_locations_list))
    bleed_location_string = bleed_locations_list[bleed_location_index]
    return bleed_location_string


def randomize_bleed_duration():
    return random.randrange(1, 5)


def randomize_bleed_episode(start_date, maximum_days):
    bleed_start_date = randomize_bleed_episode_start(start_date, maximum_days)
    location = randomize_bleed_location()
    duration = randomize_bleed_duration()
    return Bepisode(bleed_start_date, location, duration)


# Checks each date that bleeding occurred in each bepisode and tries to find a corresponding date object in given list.
# If one is found, the date object will have its bleed list updated with a string
# The string represents the location of the aforementioned bleed
def couple_bleeds_to_dates(bepisodes_list, some_log):
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
# The list may or may not be empty when passed in. This allows program to back fill any non manual bleeds.
def random_all_bleed_episodes(amount_of_bleeds, start_date, maximum_days, bepisode_list):
    while len(bepisode_list) < amount_of_bleeds:
        bepisode = randomize_bleed_episode(start_date, maximum_days)
        bepisode_list.append(bepisode)
    for bepisode in bepisode_list:
        print(f'{bepisode.duration} - {bepisode.location}')
        bepisode.project_dates()
    return bepisode_list


# Hours -> 1-24, Where 1 = 1 AM and 24 = Midnight
def randomize_time_stamp(start_hr, end_hr):
    rand_hr = random.randrange(start_hr, (end_hr + 1))
    rand_minute = random.randrange(1, 60)
    return datetime.time(hour=rand_hr, minute=rand_minute)


# Meat and potatoes algorithm. Decides if a given date in a list of dates will trigger an infusion.
# Increments dates in list and adds them to a new list if they are relevant to final log.
# Subtracts a dose for every infusion. Finishes after 11 infusions and returns the new list.
def add_infusions_to_log(some_log):
    current_prophey_schedule = normal_prophey_schedule
    doses = 12
    infusion_log = []
    for day in some_log:
        if doses > 1:
            if day.bleeds_list:
                infusion_log.append(day)
                yesterday_index = some_log.index(day) - 1
                day_before_yesterday_index = some_log.index(day) - 2
                if yesterday_index and day_before_yesterday_index >= 0:
                    try:
                        if some_log[yesterday_index].infused and some_log[day_before_yesterday_index].infused:
                            continue
                    except ValueError:
                        print('index was out of range when checking prev two days, but was handled')
                    # TODO: This needs to be refactored into a function
                    if day.weekday() not in current_prophey_schedule:
                        day.infused = True
                        day.time_stamp = randomize_time_stamp(7, 10)
                        doses -= 1
                        current_prophey_schedule = toggle_schedule(current_prophey_schedule)
                    # TODO: This needs to be refactored into a function
                    else:
                        doses -= 1
                        day.infused = True
                        day.time_stamp = randomize_time_stamp(7, 10)
                # TODO: This needs to be refactored into a function
                else:
                    if day.weekday() not in current_prophey_schedule:
                        day.infused = True
                        day.time_stamp = randomize_time_stamp(7, 10)
                        doses -= 1
                        current_prophey_schedule = toggle_schedule(current_prophey_schedule)

                    else:
                        doses -= 1
                        day.infused = True
                        day.time_stamp = randomize_time_stamp(7, 10)
            # TODO: This needs to be refactored into a function
            elif day.weekday() in current_prophey_schedule:
                infusion_log.append(day)
                day.infused = True
                doses -= 1
                day.time_stamp = randomize_time_stamp(7, 10)
            else:
                if day.weekday() == 6:
                    current_prophey_schedule = normal_prophey_schedule
        # TODO is this else case even needed?
        else:
            pass

    return infusion_log


# Resulting list will be fed into randomize all bleed episodes function at some point. Keep them compatible.
def get_manual_bleeds():
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


# TODO: Amount of bleeds should probably be input.
# Creates a blank log based on user inputted start date/last shipment.
# Fills that log with occurrences of bleeding and infusions based on user inputted manual bleeds.
# Returns a list of Date objects that is ready for sifting.
def fill_log():
    start_date = get_date()
    formatted_date = start_date.strftime('%A - %m/%d/%Y')\

    print(formatted_date)
    max_days = get_max_days(start_date.weekday())
    blank_log = make_blank_log(start_date, max_days)
    bepisode_list = get_manual_bleeds()
    bepisode_list = random_all_bleed_episodes(3, start_date, max_days, bepisode_list)

    log_with_bleeds = couple_bleeds_to_dates(bepisode_list, blank_log)

    full_log = add_infusions_to_log(log_with_bleeds)
    return full_log


# Sifts a list of Date objects for bleeds and infusions. Returns them in a new list.
# def sift_log(some_log):
#     sifted_log = []
#     for day in some_log:
#         if day.bleeds_list or day.infused:
#             sifted_log.append(day)
#     for day in sifted_log:
#         if day.bleeds_list:
#             print(f'{day} - {day.infused} - {day.bleeds_list}')
#         else:
#             print(f'{day} - {day.infused} - Prophey')
#     return sifted_log


def test_print_thingo(some_log):
    for day in some_log:
        if day.bleeds_list:
            print(f'{day} - {day.infused} - {day.bleeds_list}')
        else:
            print(f'{day} - {day.infused} - Prophey')


# Creates a string title for csv files based on first and last item in a list of Date objects.
# TODO: I should probably just format the string here to avoid having to return a tuple.
def make_csv_title(some_log):
    start_date = some_log[0]
    start_date_string = start_date.strftime('%m-%d-%Y')
    end_date = some_log[-1]
    end_date_string = end_date.strftime('%m-%d-%Y')
    return start_date_string, end_date_string


# Used to output a sifted log to csv
def output_to_csv(some_log):
    csv_title = make_csv_title(some_log)
    with open(f'{csv_title[0]} - {csv_title[1]}.csv', 'x', newline='') as csv_log:
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


# TODO: Need Testing, program is growing. Should have done from start. Look into test driven development again.
# TODO: Times I've thought: "Damn,I should write some tests", but did not --> 1
if __name__ == '__main__':
    log = fill_log()
    # end_log = sift_log(log)
    test_print_thingo(log)
    output_to_csv(log)

    
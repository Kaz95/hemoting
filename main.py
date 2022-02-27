import datetime
import random
import csv

bleed_locations = ['Elbow', 'Knee', 'Ankle']
normal_prophey_schedule = [0, 2, 4]
alt_prophey_schedule = [1, 3, 5]
cur_prophey_schedule = normal_prophey_schedule


def toggle_schedule(schedule):
    if schedule == normal_prophey_schedule:
        schedule = alt_prophey_schedule
        print('Schedule: Alt')
    else:
        schedule = normal_prophey_schedule
        print('Schedule: Main')
    return schedule


class Date(datetime.date):

    def __new__(cls, year, month, day, infusion=None):
        return super().__new__(cls, year=year, month=month, day=day)

    def __init__(self, year, month, day, infused=False):
        super().__init__()
        self.bleeds = []
        self.infused = infused


def get_start_date():
    y = int(input('Input Year XXXX: '))
    m = int(input('Input Month X(X): '))
    d = int(input('Input Day X(X): '))
    start = Date(y, m, d)
    return start


# Returns max days possible, given normal prophey schedule, based on a starting wkday as input.
# 21 days is always possible at the least, then depending on starting wkday max length is extended.
# Figured out by hand, consider how I could have done this using math.
def get_max_days(start_wkday):
    max_days = 21
    # Mon or Wed
    if start_wkday in [0, 2]:
        max_days += 2
    # Sun, Tue, or Fri
    elif start_wkday in [6, 1, 4]:
        max_days += 3
    # Sat or Thr
    elif start_wkday in [3, 5]:
        max_days += 4
    else:
        raise Exception('Weekday was somehow out of range?')

    return max_days


class Bepisode:
    def __init__(self, start, location, duration):
        self.start = start
        self.location = location
        self.duration = duration
        self.dates = []

    def project_dates(self):
        for _ in range(self.duration):
            # print(_)
            d = self.start + datetime.timedelta(_)
            self.dates.append(d)


def make_blank_log(start, max_days):
    days = [start]
    for _ in range(max_days):
        start = start + datetime.timedelta(1)
        days.append(start)
    return days


def randomize_bleed_episode_start(start, max_days):
    days_added = random.randrange(1, max_days)
    bleed_start = start + datetime.timedelta(days_added)
    return bleed_start


def randomize_bleed_location():
    bleed_location_index = random.randrange(len(bleed_locations))
    bleed_location = bleed_locations[bleed_location_index]
    return bleed_location


def randomize_bleed_duration():
    return random.randrange(1, 5)


def randomize_bleed_episode(start, max_days):
    bleed_start = randomize_bleed_episode_start(start, max_days)
    location = randomize_bleed_location()
    duration = randomize_bleed_duration()
    return Bepisode(bleed_start, location, duration)


def couple_bleeds_to_dates(bepisodes_list):
    for bepisode in bepisodes_list:
        for day in bepisode.dates:
            try:
                date_to_tag_index = log.index(day)
                date_to_tag = log[date_to_tag_index]
                date_to_tag.bleeds.append(bepisode.location)
            except ValueError:
                print('Bleed projected passed end of window, probably.')


def random_all_bleed_episodes(amount, start, max_days):
    bep_list = []
    for i in range(amount):
        _ = randomize_bleed_episode(start, max_days)
        bep_list.append(_)
    for _ in bep_list:
        print(f'{_.duration} - {_.location}')
        _.project_dates()
    return bep_list


def add_infusions_to_log(log, cur_proph_schedule):
    doses = 12
    for _ in log:
        print(f'{doses} left')
        if doses > 1:
            if _.bleeds:
                cur_min_one = log.index(_) - 1
                cur_min_two = log.index(_) - 2
                # print(f'{_} - {_.bleeds}')
                if cur_min_one and cur_min_two >= 0:
                    try:
                        if log[cur_min_one].infused and log[cur_min_two].infused:
                            continue
                    except ValueError:
                        print('index was out of range when checking prev two days, but was handled')
                    if _.weekday() not in cur_proph_schedule:
                        _.infused = True
                        doses -= 1
                        cur_proph_schedule = toggle_schedule(cur_proph_schedule)

                    else:
                        doses -= 1
                        _.infused = True
                # else:
                #     if _.weekday() not in cur_proph_schedule:
                #         _.infused = True
                #         toggle_schedule(cur_proph_schedule)
                #     else:
                #         _.infused = True
            elif _.weekday() in cur_proph_schedule:
                _.infused = True
                doses -= 1
            else:
                if _.weekday() == 6:
                    cur_proph_schedule = normal_prophey_schedule
                    print('Schedule: Main')
        else:
            log.remove(_)


if __name__ == '__main__':
    start_date = get_start_date()
    fdate = start_date.strftime('%A - %m/%d/%Y')\

    print(fdate)
    max_days = get_max_days(start_date.weekday())
    log = make_blank_log(start_date, max_days)
    #
    bep_list = random_all_bleed_episodes(3, start_date, max_days)

    couple_bleeds_to_dates(bep_list)

    add_infusions_to_log(log, cur_prophey_schedule)
    end_log = []
    for _ in log:
        if _.bleeds or _.infused:
            end_log.append(_)
    for _ in end_log:
        if _.bleeds:
            print(f'{_} - {_.infused} - {_.bleeds}')
        else:
            print(f'{_} - {_.infused} - Prophey')
    # with open('log.csv', 'x', newline='') as log:
    #     log_writer = csv.writer(log)
    #     log_writer.writerow(['Date', 'Infused', 'Reason'])
    #     log_writer.writerow(['2022-02-02', 'Yes', 'Prophey'])
    #     log_writer.writerow(['2022-02-04', 'Yes', 'Knee'])
    end_log_start = end_log[0]
    end_log_end = end_log[-1]
    with open(f'{end_log_start} - {end_log_end}.csv', 'x', newline='') as csv_log:
        log_writer = csv.writer(csv_log)
        log_writer.writerow(['Date', 'Infused', 'Reason'])
        for _ in end_log:
            if _.bleeds:
                if _.infused:
                    log_writer.writerow([_, 'Yes', _.bleeds])
                else:
                    log_writer.writerow([_, 'No', _.bleeds])
            else:
                log_writer.writerow([_, 'Yes', 'Prophylaxis'])

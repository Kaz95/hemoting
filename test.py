import datetime
import unittest
import main
import settings


class TestDate(unittest.TestCase):
    def setUp(self):
        self.date = main.Date(2022, 2, 2)

    def tearDown(self):
        del self.date

    def test_randomize_time_stamp_timestamp_is_applied(self):
        self.date.randomize_time_stamp(7, 10)
        self.assertIsNotNone(self.date.time_stamp)

    def test_randomize_time_stamp_validates_inputs(self):
        self.assertRaises(ValueError, self.date.randomize_time_stamp, starting_hour=0, ending_hour=6)
        self.assertRaises(ValueError, self.date.randomize_time_stamp, starting_hour=6, ending_hour=0)

    def test_randomize_time_stamp_range_works(self):
        lower_range = 7
        upper_range = 10

        # Test timestamp was applied within the correct range.
        self.date.randomize_time_stamp(lower_range, upper_range)
        self.assertTrue(lower_range <= self.date.time_stamp.hour <= upper_range)

        # Test to make sure this test is actually doing anything....lol. Can probably remove.
        # Good example though. Shows a test can be written for the sole purpose of checking what your actual test -
        # is doing. I now know the above test is checking for the hour attribute of a datetime.time object.
        self.date.time_stamp = datetime.time(hour=11)
        self.assertFalse(lower_range <= self.date.time_stamp.hour <= upper_range)


class TestScheduleHandler(unittest.TestCase):
    def setUp(self):
        self.handler = main.ScheduleHandler(settings.normal_prophey_schedule, settings.alternate_prophey_schedule)

    def tearDown(self):
        del self.handler

    def test_default_current_schedule(self):
        pass

    def test_toggle(self):
        pass

    def test_reset(self):
        pass


class TestBepisode(unittest.TestCase):
    def test_project_dates(self):
        pass


class TestPartialFunctionCreation(unittest.TestCase):
    def test_get_valid_day_input_creation(self):
        pass

    def test_get_valid_month_input_creation(self):
        pass

    def test_get_valid_year_input_creation(self):
        pass


class TestPureFunctions(unittest.TestCase):
    def test_validate_date_inputs(self):
        pass

    def test_get_valid_date_inputs(self):
        pass

    def test_make_date(self):
        pass

    def test_get_max_days(self):
        pass

    def test_generate_dates(self):
        pass

    def test_randomize_bleed_episode_start(self):
        pass

    def test_randomize_bleed_location(self):
        pass

    def test_randomize_bleed_duration(self):
        pass

    def test_randomize_bleed_episode(self):
        pass

    def test_couple_bleeds_to_dates(self):
        pass

    def test_fill_bepisode_list(self):
        pass

    def test_infuse(self):
        pass

    def test_add_infusions_to_log(self):
        pass

    def test_get_manual_bleeds(self):
        pass

    def test_get_all_inputs(self):
        pass

    def test_generate_log(self):
        pass

    def test_make_csv_title(self):
        pass

    def test_output_log_to_csv(self):
        pass

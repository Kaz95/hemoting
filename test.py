import datetime
import unittest
import main
import settings
from unittest.mock import patch


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
    # Create handler with program defaults.
    def setUp(self):
        self.handler = main.ScheduleHandler(settings.normal_prophey_schedule, settings.alternate_prophey_schedule)

    def tearDown(self):
        del self.handler

    def test_default_current_schedule(self):
        self.assertEqual(self.handler.current_schedule, self.handler.normal_schedule)

    def test_toggle(self):
        # Confirm expected state.
        assert self.handler.current_schedule == self.handler.normal_schedule

        self.handler.toggle()
        self.assertEqual(self.handler.current_schedule, self.handler.alternate_schedule)
        self.handler.toggle()
        self.assertEqual(self.handler.current_schedule, self.handler.normal_schedule)

    def test_reset(self):
        # Confirm expected state
        assert self.handler.normal_schedule != self.handler.alternate_schedule

        # Then test toggle functionality now that you can be sure something is actually being done when you toggle.
        self.handler.current_schedule = self.handler.alternate_schedule
        self.handler.reset()
        self.assertEqual(self.handler.current_schedule, self.handler.normal_schedule)


class TestBepisode(unittest.TestCase):
    # TODO: I'm not sure how long this method will exist. I'm not testing it now.
    def test_project_dates(self):
        pass


class TestPartialFunctionCreation(unittest.TestCase):
    def test_get_valid_day_input_creation(self):
        self.assertEqual(main.get_valid_day_input.func, main._get_valid_date_input)
        self.assertEqual(main.get_valid_day_input.keywords,
                         {'minimum': datetime.date.min.day, 'maximum': datetime.date.max.day,
                          'unit': 'Day'})

    def test_get_valid_month_input_creation(self):
        self.assertEqual(main.get_valid_month_input.func, main._get_valid_date_input)
        self.assertEqual(main.get_valid_month_input.keywords,
                         {'minimum': datetime.date.min.month, 'maximum': datetime.date.max.month, 'unit': 'Month'})

    def test_get_valid_year_input_creation(self):
        self.assertEqual(main.get_valid_year_input.func, main._get_valid_date_input)
        self.assertEqual(main.get_valid_year_input.keywords,
                         {'minimum': datetime.date.min.year, 'maximum': datetime.date.max.year, 'unit': 'Year'})


class TestPureFunctions(unittest.TestCase):
    # TODO: This test will take a little finagling. Write it...not now...sorry future self.
    def test_get_valid_date_inputs(self):
        pass

    # TODO: Im not even sure this is worth testing...
    # Spoiler, I tested it anyway. Tried to mock the entire main module, but didn't work. Try again later.
    @patch('main.get_valid_day_input')
    @patch('main.get_valid_month_input')
    @patch('main.get_valid_year_input')
    def test_get_date_input(self, mock_get_valid_year_input, mock_get_valid_month_input, mock_get_valid_day_input):
        mock_get_valid_year_input.return_value = 2022
        mock_get_valid_month_input.return_value = 2
        mock_get_valid_day_input.return_value = 2

        self.assertEqual(main.get_date_input(), (2022, 2, 2))

    def test_get_max_days_validates_inputs(self):
        # Make sure there is some range that doesn't raise ValueError
        for _ in range(7):
            with self.subTest(_=_):
                self.assertIsNotNone(main.get_max_days(_))

        # Make sure values outside that range, do raise ValueError
        self.assertRaises(ValueError, main.get_max_days, -1)
        self.assertRaises(ValueError, main.get_max_days, 7)

    def test_generate_dates(self):
        start_date = main.Date(2022, 2, 2)
        list_of_dates = main.generate_dates(start_date, 3)
        # Test right amount of Date objects were created.
        self.assertEqual(len(list_of_dates), 3)

        # Test correct objects were created with correct parameters.
        for date in list_of_dates:
            index = list_of_dates.index(date)
            with self.subTest(date=date, index=index):
                self.assertIsInstance(date, main.Bepisode)
                self.assertEqual(date, start_date + datetime.timedelta(index))

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

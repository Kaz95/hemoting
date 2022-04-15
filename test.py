import datetime
import unittest
from src import settings, core
from unittest.mock import patch


class TestDate(unittest.TestCase):
    def setUp(self):
        self.date = core.Date(2022, 2, 2)

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
        self.handler = core.ScheduleHandler(settings.normal_prophey_schedule, settings.alternate_prophey_schedule)

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
        self.assertEqual(core.get_valid_day_input.func, core._get_valid_date_input)
        self.assertEqual(core.get_valid_day_input.keywords,
                         {'minimum': datetime.date.min.day, 'maximum': datetime.date.max.day,
                          'unit': 'Day'})

    def test_get_valid_month_input_creation(self):
        self.assertEqual(core.get_valid_month_input.func, core._get_valid_date_input)
        self.assertEqual(core.get_valid_month_input.keywords,
                         {'minimum': datetime.date.min.month, 'maximum': datetime.date.max.month, 'unit': 'Month'})

    def test_get_valid_year_input_creation(self):
        self.assertEqual(core.get_valid_year_input.func, core._get_valid_date_input)
        self.assertEqual(core.get_valid_year_input.keywords,
                         {'minimum': datetime.date.min.year, 'maximum': datetime.date.max.year, 'unit': 'Year'})


class TestPureFunctions(unittest.TestCase):
    # TODO: This test will take a little finagling. Write it...not now...sorry future self.
    def test_get_valid_date_inputs(self):
        pass

    # TODO: Im not even sure this is worth testing...
    # Spoiler, I tested it anyway. Tried to mock the entire main module, but didn't work. Try again later.
    @patch('src.core.get_valid_day_input')
    @patch('src.core.get_valid_month_input')
    @patch('src.core.get_valid_year_input')
    def test_get_date_input(self, mock_get_valid_year_input, mock_get_valid_month_input, mock_get_valid_day_input):
        mock_get_valid_year_input.return_value = 2022
        mock_get_valid_month_input.return_value = 2
        mock_get_valid_day_input.return_value = 2

        self.assertEqual(core.get_date_input(), (2022, 2, 2))

    def test_get_max_days_validates_inputs(self):
        # Make sure there is some range that doesn't raise ValueError
        for _ in range(7):
            with self.subTest(_=_):
                self.assertIsNotNone(core.get_max_days(_))

        # Make sure values outside that range, do raise ValueError
        self.assertRaises(ValueError, core.get_max_days, -1)
        self.assertRaises(ValueError, core.get_max_days, 7)

    def test_generate_dates(self):
        start_date = core.Date(2022, 2, 2)
        list_of_dates = core.generate_dates(start_date, 3)
        # Test right amount of Date objects were created.
        self.assertEqual(len(list_of_dates), 3)

        # Test correct objects were created with correct parameters.
        for date in list_of_dates:
            index = list_of_dates.index(date)
            with self.subTest(date=date, index=index):
                self.assertIsInstance(date, core.Date)
                self.assertEqual(date, start_date + datetime.timedelta(index))

    @patch('random.randrange')
    def test_randomize_bleed_episode_start(self, mock_randrange):
        starting_date = core.Date(2022, 2, 2)
        expected_date = core.Date(2022, 2, 4)
        mock_randrange.return_value = 2
        known_delta = datetime.timedelta(2)
        with patch('datetime.timedelta') as mock_timedelta:
            mock_timedelta.return_value = known_delta
            bep_start = core.randomize_bleed_episode_start(starting_date, 10)

            mock_randrange.assert_called_once_with(1, 10)
            mock_timedelta.assert_called_once_with(2)
            self.assertEqual(bep_start, expected_date)
            self.assertIsInstance(bep_start, core.Date)

    # TODO: Test once you clean TODO comment in core.py
    def test_randomize_bleed_location(self):
        pass

    # TODO: Test once you clean TODO comment in core.py
    def test_randomize_bleed_duration(self):
        pass

    @patch('src.core.randomize_bleed_duration')
    @patch('src.core.randomize_bleed_location')
    @patch('src.core.randomize_bleed_episode_start')
    def test_randomize_bleed_episode(self, mock_start, mock_location, mock_duration):
        de = core.Date(2022, 2, 2)
        mock_start.return_value = de
        mock_location.return_value = 'Some Location'
        mock_duration.return_value = 3

        test_bepisode = core.randomize_bleed_episode(de, 2, 1, 3, ['a sequence'])

        self.assertIsInstance(test_bepisode, core.Bepisode)
        self.assertEqual(test_bepisode.start_date, de)
        self.assertEqual(test_bepisode.location, 'Some Location')
        self.assertEqual(test_bepisode.duration, 3)

        mock_start.assert_called_once_with(de, 2)
        mock_location.assert_called_once()
        mock_duration.assert_called_once()

    # TODO: Test once you clean TODO comment in core.py
    def test_couple_bleeds_to_dates(self):
        pass

    @patch('src.core.randomize_bleed_episode')
    @patch('src.core.Bepisode.project_dates')
    @patch('src.core.print')  # Decided to patch out print to avoid messy terminal during testing
    def test_fill_bepisode_list(self, mock_print, mock_project_dates, mock_randomize_bleed_episode):
        test_date = core.Date(2022, 2, 2)
        test_bepisode = core.Bepisode(test_date, 'location', 2)
        number_of_bleeds_set = 3
        duration = 2
        test_bep_list = [test_bepisode]
        mock_randomize_bleed_episode.return_value = test_bepisode

        # Test empty list route
        bep_list = core.fill_bepisode_list(number_of_bleeds_set, test_date, duration, [], 1, 3, ['a sequence'])
        self.assertEqual(len(bep_list), number_of_bleeds_set)
        self.assertEqual(mock_project_dates.call_count, len(bep_list))
        self.assertEqual(mock_randomize_bleed_episode.call_count, number_of_bleeds_set)

        # Test partially filled list route
        mock_randomize_bleed_episode.reset_mock()
        mock_project_dates.reset_mock()

        bep_list = core.fill_bepisode_list(number_of_bleeds_set, test_date, duration, test_bep_list, 1, 3, ['a sequence'])

        self.assertEqual(len(bep_list), number_of_bleeds_set)
        self.assertEqual(mock_project_dates.call_count, len(bep_list))
        self.assertEqual(mock_randomize_bleed_episode.call_count, 2)

    # TODO: I'm not even sure how to go about testing a nested func atm.
    def test_infuse(self):
        pass

    # TODO: This is a donger of a fookin test m8. Do it later.
    def test_add_infusions_to_log(self):
        pass

    # TODO: One of those crappy while loop situations. Mock out input? With side effects probably...?
    def test_get_manual_bleeds(self):
        pass

    @patch('src.core.get_manual_bleeds')
    @patch('src.core.get_date_input')
    def test_get_all_inputs(self, mock_get_date_input, mock_get_manual_bleeds):
        year, month, day = mock_get_date_input.return_value = (2022, 2, 2)
        # didn't use actual bepisode in list to reinforce that this func doesn't about that.
        mock_get_manual_bleeds.return_value = ['yup']

        starting_date, manual_bepisodes = inputs = core.get_all_inputs()
        # TODO: Pretty sure the unpacking with fail before len assert...not sure why its here...
        self.assertEqual(len(inputs), 2)
        self.assertIsInstance(starting_date, core.Date)
        self.assertEqual(starting_date.year, year)
        self.assertEqual(starting_date.month, month)
        self.assertEqual(starting_date.day, day)

        mock_get_date_input.assert_called_once()
        mock_get_manual_bleeds.assert_called_once()

    # TODO: Test later. Too many patched funcs. No clear place to break it up. Will test when better UI
    def test_generate_log(self):
        pass

    # TODO: This test kinda sucks...
    @patch('src.core.Date.strftime')
    def test_make_csv_title(self, mock_strftime):
        mock_strftime.return_value = 1
        some_date = core.Date(2022, 2, 2)
        some_other_date = core.Date(2022, 2, 4)
        log = [some_date, some_other_date]

        csv_title = core.make_csv_title(log)
        self.assertEqual(csv_title, '1 - 1')
        self.assertEqual(mock_strftime.call_count, 2)

    def test_output_log_to_csv(self):
        # TODO: ....yup....nope actually
        pass

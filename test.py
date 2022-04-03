import unittest
import main


class TestDateMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.date = main.Date(2022, 2, 2)

    def tearDown(self) -> None:
        del self.date

    def test_infuse(self):
        self.date.infuse()
        self.assertTrue(self.date.infused)

    def test_randomize_time_stamp(self):
        self.date.randomize_time_stamp(7, 10)


class TestScheduleHandlerMethods(unittest.TestCase):
    def test_toggle(self):
        pass

    def test_reset(self):
        pass


class TestBepisodeMethods(unittest.TestCase):
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

import unittest

import pandas as pd
from pandas.testing import assert_frame_equal
from rugby_stats_scraper.constants import DATA_FOLDER
from rugby_stats_scraper.espn import EspnDate, EspnMatch

from tests.data import EXPECTED_MATCH


class TestEspnMatch(unittest.TestCase):
    def test_match_data(self):

        test_match_url = (
            'https://www.espn.co.uk/rugby/match?gameId=594214&league=270559'
        )

        test_match = EspnMatch(test_match_url)
        self.assertEqual(EXPECTED_MATCH, test_match.match_data())


class TestEspnDate(unittest.TestCase):
    def test_data_data(self):
        test_date = EspnDate(
            'https://www.espn.co.uk/rugby/scoreboard?date=20220917'
        )

        expected_data_path = DATA_FOLDER.joinpath('espn_date_test.csv')
        expected_date_data = pd.read_csv(
            expected_data_path, dtype={'year': str}, parse_dates=['match_date']
        )
        assert_frame_equal(
            expected_date_data,
            test_date.date_data(),
            check_dtype=False,
            check_names=False,
        )


if __name__ == '__main__':
    unittest.main()

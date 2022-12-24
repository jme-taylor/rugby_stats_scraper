import json
import unittest

import pandas as pd
from pandas.testing import assert_frame_equal
from rugby_stats_scraper.constants import DATA_FOLDER
from rugby_stats_scraper.espn import Date, Match

from tests.data import EXPECTED_MATCH


class TestEspnMatch(unittest.TestCase):
    def test_match_data(self):

        test_match_json_filepath = DATA_FOLDER.joinpath('espn_match_test.json')
        with open(test_match_json_filepath) as f:
            test_match_json = json.load(f)

        test_match = Match(test_match_json)
        self.assertEqual(EXPECTED_MATCH, test_match.create_match_data_dict())


class TestEspnDate(unittest.TestCase):
    def test_data_data(self):
        test_date = Date('20220917')

        expected_data_path = DATA_FOLDER.joinpath('espn_date_test.csv')
        expected_date_data = pd.read_csv(
            expected_data_path,
            dtype={
                'match_id': str,
                'year': str,
                'team_1_id': str,
                'team_2_id': str,
                'team_1_score': str,
                'team_2_score': str,
            },
        )
        assert_frame_equal(
            expected_date_data,
            test_date.create_date_dataframe(),
            check_dtype=False,
            check_names=False,
        )


if __name__ == '__main__':
    unittest.main()

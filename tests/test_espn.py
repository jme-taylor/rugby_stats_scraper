import json

import pandas as pd
from pandas.testing import assert_frame_equal

from rugby_stats_scraper.constants import DATA_FOLDER
from rugby_stats_scraper.espn import EspnDate, EspnMatch
from tests.data import EXPECTED_MATCH


def test_match_data():
    test_match_json_filepath = DATA_FOLDER.joinpath("espn_match_test.json")
    with open(test_match_json_filepath) as f:
        test_match_json = json.load(f)

    test_match = EspnMatch(test_match_json)
    assert EXPECTED_MATCH == test_match.match_data()


def test_date_data():
    test_date = EspnDate("20220917")

    expected_data_path = DATA_FOLDER.joinpath("espn_date_test.csv")
    expected_date_data = pd.read_csv(
        expected_data_path,
        dtype={
            "match_id": str,
            "year": str,
            "team_1_id": str,
            "team_2_id": str,
            "team_1_score": str,
            "team_2_score": str,
        },
    )

    assert_frame_equal(
        expected_date_data,
        test_date.date_data(),
        check_dtype=False,
        check_names=False,
    )

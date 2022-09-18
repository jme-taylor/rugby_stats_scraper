import unittest

from rugby_stats_scraper.espn import EspnMatch

from tests.data import EXPECTED_MATCH

test_match_url = (
    'https://www.espn.co.uk/rugby/match?gameId=594214&league=270559'
)


class TestEspnMatch(unittest.TestCase):
    def test_competition_data(self):
        test_match = EspnMatch(test_match_url)
        test_match.competition_information()
        self.assertEqual(
            [test_match.competition, test_match.year],
            [EXPECTED_MATCH['competition'], EXPECTED_MATCH['year']],
        )

    def test_score_information(self):
        test_match = EspnMatch(test_match_url)
        test_match.score_information()
        self.assertEqual(
            [test_match.home_score, test_match.away_score],
            [EXPECTED_MATCH['home_score'], EXPECTED_MATCH['away_score']],
        )

    def test_venue_information(self):
        test_match = EspnMatch(test_match_url)
        test_match.venue_information()
        self.assertEqual(test_match.venue, EXPECTED_MATCH['venue'])

    def test_match_data(self):

        test_match = EspnMatch(test_match_url)
        self.assertEqual(EXPECTED_MATCH, test_match.match_data())


if __name__ == '__main__':
    unittest.main()

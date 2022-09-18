import unittest

from rugby_stats_scraper.espn import EspnMatch

from tests.data import EXPECTED_MATCH

test_match_url = (
    'https://www.espn.co.uk/rugby/match?gameId=594214&league=270559'
)


class TestEspnMatch(unittest.TestCase):
    def test_match_data(self):

        test_match = EspnMatch(test_match_url)
        self.assertEqual(EXPECTED_MATCH, test_match.match_data())


if __name__ == '__main__':
    unittest.main()

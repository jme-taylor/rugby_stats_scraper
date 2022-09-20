from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

DATA_FOLDER = PROJECT_ROOT.joinpath('data')

ESPN_HEADERS = {
    'authority': 'site.web.api.espn.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'origin': 'https://www.espn.co.uk',
    'referer': 'https://www.espn.co.uk/',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',  # noqa
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',  # noqa
}
ESPN_BASE_URL = 'https://www.espn.co.uk'
ESPN_SCORES_URL = ESPN_BASE_URL + '/rugby/scoreboard?date='
ESPN_EARLIEST_DATE = datetime(2005, 2, 5)
ESPN_ATTRIBUTES = {
    'competition': 'game-details header',
    'long_name': 'long-name',
    'short_name': 'short-name',
    'abbreviation': 'abbrev',
    'score_home': 'score icon-font-after',
    'score_away': 'score icon-font-before',
    'venue': 'game-details location-details',
}
ESPN_MATCH_DATA_BASE = {
    'match_date': None,
    'url': None,
    'competition': None,
    'year': None,
    'home_score': None,
    'away_score': None,
    'venue': None,
    'home_long_name': None,
    'home_short_name': None,
    'home_abbreviation': None,
    'away_long_name': None,
    'away_short_name': None,
    'away_abbreviation': None,
}
ESPN_STRING_DATA = [
    'url',
    'competition',
    'year',
    'venue',
    'home_long_name',
    'home_short_name',
    'home_abbreviation',
    'away_long_name',
    'away_short_name',
    'away_abbreviation',
]
ESPN_INT_DATA = ['home_score', 'away_score']
ESPN_DATE_DATA = ['match_date']

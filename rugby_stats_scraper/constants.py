from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

DATA_FOLDER = PROJECT_ROOT.joinpath('data')

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

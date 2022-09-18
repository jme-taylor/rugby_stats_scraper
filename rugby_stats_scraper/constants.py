from datetime import datetime
from pathlib import Path

BASE_URL = 'https://www.espn.co.uk'

SCORES_URL = BASE_URL + '/rugby/scoreboard?date='

EARLIEST_DATE = datetime(2005, 2, 5)

PROJECT_ROOT = Path(__file__).parent.parent

DATA_FOLDER = PROJECT_ROOT.joinpath('data')

ESPN_ATTRIBUTES = {
    'competition': 'game-details header',
    'long_name': 'long-name',
    'short_name': 'short-name',
    'abbreviation': 'abbrev',
    'score_home': 'score icon-font-after',
    'score_away': 'score icon-font-before',
    'venue': 'game-details location-details',
}

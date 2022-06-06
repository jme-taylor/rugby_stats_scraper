from datetime import datetime
from pathlib import Path

BASE_URL = 'https://www.espn.co.uk'

SCORES_URL = BASE_URL + '/rugby/scoreboard?date='

EARLIEST_DATE = datetime(2005, 2, 5).date()

PROJECT_ROOT = Path(__file__).parent.parent

DATA_FOLDER = PROJECT_ROOT.joinpath('data')
